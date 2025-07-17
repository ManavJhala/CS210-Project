#Air Quality Forecasting

#Step 1: Get PM2.5 data from OpenAQ
import requests
import pandas as pd

# Pulling PM2.5 data for Los Angeles using OpenAQ API
url = 'https://api.openaq.org/v2/measurements'
params = {
    'city': 'Los Angeles',
    'parameter': 'pm25',
    'limit': 1000,
    'sort': 'desc'
}
response = requests.get(url, params=params)
data = response.json()['results']
pm25_df = pd.DataFrame(data)

#Get weather data from Meteostat
from meteostat import Hourly, Point
from datetime import datetime

# Define location and time range for weather data
location = Point(34.0522, -118.2437) 
start = datetime(2024, 5, 1)
end = datetime(2024, 5, 31)


weather_data = Hourly(location, start, end)
weather_df = weather_data.fetch()

# Clean and prepare both datasets

# Convert OpenAQ datetime to pandas datetime
pm25_df['date'] = pd.to_datetime(pm25_df['date'].apply(lambda x: x['utc']))


pm25_df = pm25_df.rename(columns={'value': 'pm25'})


pm25_df = pm25_df[['date', 'pm25']].groupby('date').mean().reset_index()

# Make sure weather datetime column is labeled the same
weather_df = weather_df.reset_index().rename(columns={'time': 'date'})

# Merge both datasets on timestamp
merged_df = pd.merge(pm25_df, weather_df, on='date', how='inner')


merged_df.interpolate(method='time', inplace=True)


Q1 = merged_df['pm25'].quantile(0.25)
Q3 = merged_df['pm25'].quantile(0.75)
IQR = Q3 - Q1
merged_df = merged_df[~((merged_df['pm25'] < (Q1 - 1.5 * IQR)) | (merged_df['pm25'] > (Q3 + 1.5 * IQR)))]

# Feature engineering: lag and rolling average
merged_df['pm25_lag1'] = merged_df['pm25'].shift(1)
merged_df['pm25_rolling3'] = merged_df['pm25'].rolling(window=3).mean()

merged_df.dropna(inplace=True)

# Generate some basic visualizations
import matplotlib.pyplot as plt
import seaborn as sns



# Create a heatmap to show correlations
plt.figure(figsize=(8, 6))
sns.heatmap(merged_df[['pm25', 'temperature', 'humidity', 'wspd']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('correlation_heatmap_dark.png')

# Plot PM2.5 levels over time
plt.figure(figsize=(10, 5))
plt.plot(merged_df['date'], merged_df['pm25'], label='PM2.5', color='cyan')
plt.xlabel('Time')
plt.ylabel('PM2.5 Level')
plt.title('PM2.5 Levels Over Time')
plt.legend()
plt.tight_layout()
plt.savefig('pm25_timeseries.png')
