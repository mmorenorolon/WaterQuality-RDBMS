# %%
from pathlib import Path
import pandas as pd

# %%

# ------------------------------------------------------------
#           CLEAN ACTIVITY DATA
# ------------------------------------------------------------

# Read in activity data
# Import the data and parse the dates in a format digestible in SQL
activity_csv = pd.read_csv(
    'data_raw/activity.csv', parse_dates=['ActivityStartDate'], date_format='%m/%d/%Y'
)

# Column 25 and 26 have mixed types, but we will not be using these columns


# %%
# Display all columns for better accesibility during data cleaning process
pd.set_option('display.max_columns', None)


print(activity_csv.head())

# %%
# Select the columns of interest for the database
activity = activity_csv.loc[
    :,
    [
        'MonitoringLocationIdentifier',
        'ActivityIdentifier',
        'ActivityTypeCode',
        'ActivityMediaName',
        'ActivityStartDate',
        'ActivityStartTime/Time',
        'ActivityStartTime/TimeZoneCode',
        'ActivityRelativeDepthName',
        'ActivityDepthHeightMeasure/MeasureValue',
        'ActivityDepthHeightMeasure/MeasureUnitCode',
        'ActivityCommentText',
    ],
].copy()

# %%
activity.columns.to_list()

# %%
# Rename Columns
activity.columns = [
    'station_id',
    'activity_id',
    'activity_type',
    'activity_media',
    'activity_start_date',
    'activity_start_time',
    'activity_time_zone',
    'activity_depth_name',
    'activity_depth',
    'activity_depth_unit',
    'activity_comment',
]

# %%
activity.info()

# %%
# Convert all columns to string first
# activity = activity.astype('string')

# %%
# Convert start time to datetime format
activity['activity_start_time'] = pd.to_datetime(
    activity['activity_start_time'], format='%H:%M:%S'
)
# %%                                                 errors = 'coerce')
# preserve only time (will be saved as an object dtype)
activity['activity_start_time'] = activity['activity_start_time'].dt.time

# %%
# Save all other columns as strings
object_cols = [
    'station_id',
    "activity_id",
    'activity_type',
    'activity_media',
    'activity_time_zone',
    'activity_depth_name',
    'activity_depth_unit',
    'activity_comment',
]

# Save object columns as strings
activity[object_cols] = activity[object_cols].astype('string')

# %%
(activity.info())

# %%
# Check for fake NA values
print(
    activity.apply(
        lambda col: col.isin([".", "-", "n/a", "NA", "Not determined", ""]).any()
    )
)

# %%
activity.activity_depth_unit.unique()

# Some measurements are in meters and feet.
# %%

# Normalize the unit column
# Normalize unit column
activity['activity_depth_unit'] = (
    activity['activity_depth_unit']
    .str.strip()
    .str.lower()
    .replace(
        {
            'ft': 'feet',
            'feet ': 'feet',
            'm': 'meters',
            'meter': 'meters',
            'meters ': 'meters',
            'nan': pd.NA,
        }
    )
)

# %%
activity['activity_depth_unit'].unique()

# %%
# Convert depth column to numeric
activity['activity_depth'] = pd.to_numeric(activity['activity_depth'], errors='coerce')

# %%
# Count negative values
(activity['activity_depth'] < 0).sum()

# %%
# Replace negative values in depth column with NA
activity.loc[activity['activity_depth'] < 0, 'activity_depth'] = pd.NA

# %%

# Identify rows in feet
feet_mask = activity['activity_depth_unit'] == 'feet'

# Convert from feet to meters
activity.loc[feet_mask, 'activity_depth'] = (
    activity.loc[feet_mask, 'activity_depth'] * 0.3048
)

# %%
activity['activity_depth'].describe()

# %%

# Set abnormally large depth value to NA
activity[activity['activity_depth'] == 1015999.8984000001] = pd.NA

# %%
activity['activity_depth'].max()

# %%
# Save cleaned activity data as csv

filepath = Path("data_processed/activity_clean.csv")
filepath.parent.mkdir(parents=True, exist_ok=True)
activity.to_csv(filepath)

# %%

# Read in cleaned activity csv to compare to raw data
activity_clean = pd.read_csv('data_processed/activity_clean.csv')
activity_clean.head(2)

# %%

# Compare raw data to cleaned activity data

print(activity.info())

print(activity_clean.info())
# %%


# ------------------------------------------------------------
#           CLEAN STATIONS DATA
# ------------------------------------------------------------

# Read in stations data
station_csv = pd.read_csv('data_raw/station.csv')

# %%
# Display all columns
pd.set_option('display.max_columns', None)
print(station_csv.head())

# %%

print(station_csv.columns.tolist())

# %%

station_csv.info()
# %%
# Select the columns of interest for the database
station = station_csv.loc[
    :,
    [
        'MonitoringLocationIdentifier',
        'MonitoringLocationName',
        'MonitoringLocationTypeName',
        'LatitudeMeasure',
        'LongitudeMeasure',
        'HUCEightDigitCode',
        'StateCode',
        'CountyCode',
        'ProviderName',
    ],
].copy()

# %%
station.columns.to_list()

# %%
# Rename Columns
station.columns = [
    'station_id',
    'station_name',
    'station_type',
    'latitude',
    'longitude',
    'huc8',
    'state_code',
    'county_code',
    'provider_name',
]

# %%
station.info()

# %%
# Save all other columns as strings
station_object_dtype = ['station_id', 'station_name', 'station_type', 'provider_name']

# Save object columns as strings
station[station_object_dtype] = station[station_object_dtype].astype('string')

# %%
station.info()

# %%
# Check for fake NA values
print(
    station.apply(
        lambda col: col.isin([".", "-", "n/a", "NA", "Not determined", ""]).any()
    )
)

# %%
print(station.latitude.min())
print(station.latitude.max())

print(station.longitude.min())
print(station.longitude.max())


# %%
# Save cleaned station data as csv

filepath = Path("data_processed/station_clean.csv")
filepath.parent.mkdir(parents=True, exist_ok=True)
station.to_csv(filepath)

# %%

# Read in cleaned activity csv to compare to raw data
station_clean = pd.read_csv('data_processed/station_clean.csv')
station_clean.head(2)

# %%

# Compare raw data to cleaned activity data

print(station.info())

print(station_clean.info())

# %%
# ------------------------------------------------------------
#           CLEAN RESULTS DATA
# ------------------------------------------------------------

# Multiple columns have mixed types
# Thus, all will be read as strings, then converted to their appropriate data types

result_csv = pd.read_csv('data_raw/result.csv', dtype='string')
# %%

# Display all columns
pd.set_option('display.max_columns', None)
print(result_csv.head())

# %%

print(result_csv.columns.tolist())

# %%

result_csv.info()

# %%
# Select the columns of interest for the database
result = result_csv.loc[
    :,
    [
        'ActivityIdentifier',
        'ProjectIdentifier',
        'ResultDetectionConditionText',
        'CharacteristicName',
        'ResultMeasureValue',
        'ResultMeasure/MeasureUnitCode',
        'ResultStatusIdentifier',
        'ResultValueTypeName',
        'ResultAnalyticalMethod/MethodIdentifier',
        'ResultAnalyticalMethod/MethodName',
        'LaboratoryName',
        'DetectionQuantitationLimitTypeName',
        'DetectionQuantitationLimitMeasure/MeasureValue',
        'DetectionQuantitationLimitMeasure/MeasureUnitCode',
    ],
].copy()

# %%
result.columns.to_list()

# %%
# Rename Columns
result.columns = [
    'activity_id',
    'project_id',
    'result_condition',
    'characteristic_name',
    'result_value',
    'result_unit',
    'result_status',
    'result_type',
    'analytical_method_id',
    'analytical_method',
    'lab_name',
    'detection_limit_type',
    'detection_limit_value',
    'detection_limit_unit',
]

# %%
result.info()

# %%
result['detection_limit-value']

# %%
# Save all other columns as strings
result_float_dtype = [
    'result_value',
    'detection_limit_value',
    'station_type',
    'provider_name',
]

# Save object columns as strings
station[station_object_dtype] = station[station_object_dtype].astype('string')

# %%
station.info()

# %%
# Check for fake NA values
print(
    station.apply(
        lambda col: col.isin([".", "-", "n/a", "NA", "Not determined", ""]).any()
    )
)

# %%
print(station.latitude.min())
print(station.latitude.max())

print(station.longitude.min())
print(station.longitude.max())


# %%
# Save cleaned station data as csv

filepath = Path("data_processed/station_clean.csv")
filepath.parent.mkdir(parents=True, exist_ok=True)
station.to_csv(filepath)

# %%

# Read in cleaned activity csv to compare to raw data
station_clean = pd.read_csv('data_processed/station_clean.csv')
station_clean.head(2)

# %%

# Compare characteristics of raw data to cleaned activity data

print(station.info())

print(station_clean.info())
