# San Francisco Inner Bay Water Quality Monitoring Database

A comprehensive project to build a relational database from EPA Water Quality Portal data, focusing on water quality measurements in a subwatershed of the San Francisco Bay region.

## Table of Contents

- [Project Overview](#project-overview)
- [Technical Stack](#technical-stack)
- [Data Source](#data-source)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Data Pipeline Workflow](#data-pipeline-workflow)
- [Installation & Requirements](#installation--requirements)
- [How to Use](#how-to-use)
- [Analysis & Visualization](#analysis--visualization)
- [Deliverables](#deliverables)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project builds a relational database to analyze water quality measurements within a subwatershed of the San Francisco Bay region (HUC12: 180500021002). The goal is to organize environmental monitoring data into a structured format that enables efficient querying and analysis of water quality patterns.

The database is designed to reflect real-world data collection processes, linking monitoring locations (stations), sampling events (activities), and laboratory measurements (results). Using this structured approach, the project demonstrates the ability to clean real-world environmental data, design a relational database schema, and extract meaningful insights using SQL.

**Key Workflow:** Raw Data → Cleaning → Database Schema → Analysis & Visualization

## Technical Stack

- **Languages**: Python, SQL
- **Database**: DuckDB (in-process SQL OLAP database)
- **Data Processing**: pandas, numpy
- **Notebooks**: Jupyter Notebook
- **Visualization**: matplotlib, seaborn
- **Data Source**: Water Quality Portal (WaterQualityData.us)
- **Geographic Focus**: San Francisco Bay region (HUC12: 180500021002)

## Data Source

The data for this project was obtained from the [Water Quality Portal (WQP)](https://www.waterqualitydata.us/) via WaterQualityData.us, which aggregates data from multiple agencies including the USGS, EPA, and partner organizations.

### Dataset Overview

The raw dataset includes three main data tables:

- **Station**: Metadata about monitoring locations (coordinates, location type, administrative codes)
- **Activity**: Sampling events conducted at each station (date, time, sampling method)
- **Result**: Measured environmental variables (e.g., chemical concentrations, temperature)

The data was filtered using a 12-digit Hydrologic Unit Code (HUC12) corresponding to a subwatershed within the San Francisco Bay region.

### About HUC12 Codes

HUC (Hydrologic Unit Code) codes are standardized geographic areas used by the USGS to classify watersheds and subwatersheds. The 12-digit code (HUC12) represents the most detailed watershed classification level. Learn more at the [USGS Watershed Boundary Dataset](https://www.usgs.gov/national-hydrography/watershed-boundary-dataset).

## Database Schema

The cleaned data is loaded into a DuckDB database with the following relational structure (see `final_project_schema.png` for a visual diagram).

### Data Cleaning Process

The raw dataset contains a large number of columns, many of which are sparsely populated or not relevant to the analysis. The cleaning process focuses on:

- Removing columns with mostly missing values
- Standardizing column names for clarity and consistency
- Selecting only relevant variables for each table (e.g., location, time, measurement values)
- Ensuring consistent data types (e.g., numeric values for measurements, dates for sampling events)
- Filtering the results table to include a subset of water quality variables for analysis

Primary and foreign key relationships are preserved during cleaning to maintain the integrity of the relational structure.

### Table: `station`

Stores metadata about monitoring locations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `station_id` | TEXT | PRIMARY KEY | Unique identifier for monitoring location |
| `station_name` | TEXT | | Human-readable name of the station |
| `station_type` | TEXT | | Type of monitoring location (e.g., Well, Stream) |
| `latitude` | DOUBLE | | Geographic latitude coordinate |
| `longitude` | DOUBLE | | Geographic longitude coordinate |
| `huc8` | TEXT | | 8-digit Hydrologic Unit Code |
| `state_code` | TEXT | | State abbreviation |
| `county_code` | TEXT | | County code |
| `provider_name` | TEXT | | Data provider organization name |

### Table: `activity`

Stores sampling events conducted at each station.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `activity_pk` | INTEGER | PRIMARY KEY | Auto-incrementing primary key |
| `activity_id` | TEXT | NOT NULL, UNIQUE* | Unique activity identifier |
| `station_id` | TEXT | FOREIGN KEY | References station(station_id) |
| `activity_type` | TEXT | | Type of sampling activity |
| `activity_start_date` | DATE | | Date when sampling occurred |
| `activity_start_time` | TIME | | Time when sampling started |
| `activity_media` | TEXT | | Sampling medium (Water, Sediment, etc.) |
| `activity_depth_m` | DOUBLE | | Sampling depth in meters |
| `activity_depth_original_value` | DOUBLE | | Original depth value |
| `activity_depth_original_unit` | TEXT | | Original depth unit |
| `activity_depth_reference_point` | TEXT | | Reference point for depth measurement |
| `activity_depth_flag` | TEXT | | Quality flag for depth data |
| `activity_comment` | TEXT | | Additional comments about the activity |

*Part of composite UNIQUE constraint with station_id, date, time, type, media

### Table: `characteristic`

Stores metadata about measured water quality variables.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `characteristic_id` | INTEGER | PRIMARY KEY | Unique identifier for the variable |
| `characteristic_name` | TEXT | NOT NULL, UNIQUE* | Name of the measured characteristic |
| `usgs_pcode` | TEXT | NOT NULL, UNIQUE* | USGS parameter code |

*Part of composite UNIQUE constraint

### Table: `result`

Stores measured water quality values and detection limits.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `result_pk` | INTEGER | PRIMARY KEY | Auto-incrementing primary key |
| `activity_pk` | INTEGER | FOREIGN KEY | References activity(activity_pk) |
| `characteristic_id` | INTEGER | FOREIGN KEY | References characteristic(characteristic_id) |
| `activity_id_source` | TEXT | | Source activity identifier |
| `station_id_source` | TEXT | | Source station identifier |
| `result_value` | DOUBLE | | Measured value |
| `result_unit` | TEXT | | Unit of measurement |
| `result_detection_condition` | TEXT | | Detection status (Detected, Not Detected, etc.) |
| `result_status` | TEXT | | Validation status of the result |
| `result_sample_fraction` | TEXT | | Fraction analyzed (Dissolved, Total, etc.) |
| `measure_qualifier` | TEXT | | Qualifier flags for the measurement |
| `detection_limit_value` | DOUBLE | | Minimum detectable concentration |
| `detection_limit_unit` | TEXT | | Unit of detection limit |
| `detection_limit_type` | TEXT | | Type of detection limit |
| `analytical_method_id` | TEXT | | Method identifier |
| `analytical_method_context` | TEXT | | Method context/source |
| `analytical_method_name` | TEXT | | Name of analytical method used |
| `result_comment` | TEXT | | Additional result comments |
| `provider_name` | TEXT | | Data provider organization |

### Schema Relationships

The schema supports one-to-many relationships:

```
station (1) ──→ (many) activity
activity (1) ──→ (many) result
characteristic (1) ──→ (many) result
```

This structure ensures referential integrity and prevents orphaned records through foreign key constraints.

## Project Structure

```
WaterQuality-RDBMS/
├── README.md                          # Documentation
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── data_raw/                          # Raw data from Water Quality Portal
│   ├── activity.csv
│   ├── characteristic.csv
│   ├── result.csv
│   └── station.csv
├── data_processed/                    # Cleaned CSV files
│   ├── activity_clean.csv
│   ├── characteristic_clean.csv
│   ├── result_clean.csv
│   └── station_clean.csv
├── database/                          # DuckDB database file
├── data_cleaning.py                   # Data cleaning script
├── create_database.sql                # Main database schema and load
├── test_station.sql                   # Individual table definitions
├── test_activity.sql
├── test_characteristic.sql
├── test_result.sql
├── data_exploration.ipynb             # EDA notebook
├── database_visualization.ipynb       # Query results & visualizations
├── plot_study_area.ipynb              # Geographic analysis
├── final_project_schema.png           # Schema diagram
├── images/                            # Generated visualizations
└── WBD_Shape/                         # Watershed boundary shapefiles
```

## Data Pipeline Workflow

The project follows this sequence:

1. **Data Acquisition** → Download raw data from Water Quality Portal (WQP) into `data_raw/`
2. **Data Cleaning** → Run `data_cleaning.py` to process raw CSVs → outputs to `data_processed/`
3. **Database Creation** → Execute `create_database.sql` to:
   - Define table schemas
   - Load cleaned CSVs into DuckDB
   - Establish relationships and constraints
4. **Analysis & Visualization** → Use Jupyter notebooks to query and visualize results

## Installation & Requirements

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager

### Required Libraries

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install duckdb pandas numpy jupyter matplotlib seaborn
```

Using conda:

```bash
conda install -c conda-forge duckdb pandas numpy jupyter matplotlib seaborn
```

### DuckDB Installation

DuckDB is included in the pip/conda dependencies above. For more information, visit [DuckDB documentation](https://duckdb.org/docs/).

## How to Use

### Clone the Repository

```bash
git clone https://github.com/mmorenorolon/WaterQuality-RDBMS.git
cd WaterQuality-RDBMS
```

### Set Up Your Environment

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup

#### Step 1: Prepare Raw Data

Download data from the [Water Quality Portal](https://www.waterqualitydata.us/) filtered for HUC12: 180500021002.
Alternatively, access the links directly from their API:
- https://www.waterqualitydata.us/data/Station/search?huc=180500021002&mimeType=csv
- https://www.waterqualitydata.us/data/Activity/search?huc=180500021002&mimeType=csv
- https://www.waterqualitydata.us/data/Result/search?huc=180500021002&mimeType=csv
 
 Place the following files in `data_raw/`:
- `activity.csv`
- `result.csv`
- `station.csv`

#### Step 2: Clean Data

Run the data cleaning script to process raw files:

```bash
python data_cleaning.py
```

This generates cleaned CSV files in `data_processed/`:
- `activity_clean.csv`
- `characteristic_clean.csv`
- `result_clean.csv`
- `station_clean.csv`

The script uses pandas to:
- Parse dates in a format compatible with SQL/DuckDB
- Select and rename columns for consistency
- Handle mixed data types and missing values
- Prepare data for relational database import

#### Step 3: Create Database

Execute the main database creation script:

```bash
duckdb < create_database.sql
```

This will:
- Create the four-table relational schema
- Load cleaned CSV files from `data_processed/`
- Establish foreign key relationships and constraints
- Generate the DuckDB database file

**Alternative:** Load individual table schemas:
```bash
duckdb < test_station.sql
duckdb < test_activity.sql
duckdb < test_characteristic.sql
duckdb < test_result.sql
```

## Analysis & Visualization

### Run the Jupyter Notebooks

```bash
jupyter notebook
```

Then navigate to and open the notebooks in order.

### Available Notebooks

#### `data_exploration.ipynb`
Exploratory data analysis of raw and cleaned data. Use this to:
- Understand data distributions and patterns
- Identify missing values and outliers
- Examine relationships between variables
- Generate summary statistics

#### `database_visualization.ipynb`
Query the database and create visualizations of results. Use this to:
- Write SQL queries to answer analytical questions
- Create plots and charts from query results
- Visualize temporal and spatial patterns in water quality
- Generate summary tables and statistics

#### `plot_study_area.ipynb`
Geographic and spatial analysis. Use this to:
- Visualize monitoring station locations on a map
- Overlay watershed boundary shapefiles from `WBD_Shape/`
- Create spatial visualizations of water quality data
- Analyze geographic patterns in the data

### Schema Diagram

A visual representation of the database schema and table relationships is provided in `final_project_schema.png`. This diagram illustrates:
- All four tables and their columns
- Primary and foreign key relationships
- Data types and constraints

## Deliverables

The final project includes:

- ✅ A cleaned and structured DuckDB database with relational schema
- ✅ SQL queries addressing analytical questions related to water quality patterns
- ✅ Visualizations created in Python to support the analysis
- ✅ Comprehensive documentation of the data, schema, and workflow
- ✅ A schema diagram illustrating table relationships
- ✅ Jupyter notebooks for data exploration, analysis, and visualization

### Key Outputs

- **Database file**: DuckDB database containing the relational schema
- **Analysis results**: Statistical insights and trends in water quality data
- **Visualizations**: Charts, graphs, and maps illustrating water quality patterns
- **SQL queries**: Reusable queries for future analysis
- **Documentation**: Complete data dictionary and schema documentation

## Contributing

Contributions are welcome! If you'd like to improve this project, please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

---

**Last Updated**: June 2026
**Repository**: [https://github.com/mmorenorolon/WaterQuality-RDBMS](https://github.com/mmorenorolon/WaterQuality-RDBMS)
