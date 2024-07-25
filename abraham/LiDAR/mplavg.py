import act
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename_mpl = '/Users/rubenabraham/AIMLProject/LIDAR/minimpl_202203/202203111800.mpl'  


ds = act.io.mpl.read_sigma_mplv5(filename_mpl)

df = ds.to_dataframe()

df = df.reset_index()

#'time' to datetime
df['time_utc'] = pd.to_datetime(df['time_utc'])

df.set_index('time_utc', inplace=True)

#only up to 10000 range
limit = 10000
df = df[df['range'] < limit]

# resample for 5-minute intervals and calculate the average NRB Co-pol values for each range
df_resampled = df.groupby('range').resample('5min').mean().unstack(level=0)['nrb_copol']


first_interval = df_resampled.iloc[0]


plt.figure(figsize=(10, 8))
plt.plot(first_interval.values, first_interval.index, marker=',', linestyle='-', color='b')

# print(df['nrb_copol'].mean(), df['nrb_copol'].max())
# print(first_interval.describe())

plt.title('NRB Co-pol by Range 0-5 Minute Interval')
plt.xlabel('Average NRB Co-pol')
plt.ylabel('Range (m)')
# plt.legend()
plt.grid(True)
plt.show()

plt.savefig('/Users/rubenabraham/AIMLProject/LIDAR/thick overcast/to0-5')

