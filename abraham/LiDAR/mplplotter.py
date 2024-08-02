
import matplotlib.pyplot as plt
import act
import numpy as np

#file path for mpl
filename_mpl = '/Users/rubenabraham/AIMLProject/LIDAR/minimpl_202203/202203151800.mpl'

#read the data
ds = act.io.mpl.read_sigma_mplv5(filename_mpl)

print(ds['nrb_copol'].head())

print(ds['time'].head())

# get time, range, signal values
time = ds['time'].values
range_data = ds['range'].values 
signal = ds['nrb_copol'].values 

max_range = 10000
range_mask = range_data <= max_range
range_data = range_data[range_mask]
signal = signal[:, range_mask]


time_float = time.astype('datetime64[s]').astype(np.float64)

#  meshgrid for time and range
time_grid, range_grid = np.meshgrid(
    np.concatenate([time_float, [time_float[-1] + (time_float[-1] - time_float[-2])]]),
    np.concatenate([range_data, [range_data[-1] + (range_data[-1] - range_data[-2])]]),
    indexing='ij'
)

# dimensions match for pcolormesh
if signal.shape == (time_grid.shape[0] - 1, range_grid.shape[1] - 1):
    plt.figure(figsize=(12, 8))
    plt.pcolormesh(time_grid, range_grid, signal, shading='auto', cmap='jet', vmin=0, vmax=1.0)
    plt.colorbar(label='NRB Co-pol')
    plt.ylabel('Range (m)')
    plt.xlabel('Time')
    plt.title('NRB Co-pol Radar Plot')

    time_labels = [np.datetime64(int(ts), 's') for ts in np.linspace(time_float[0], time_float[-1], num=10)]
    time_labels_str = [str(t) for t in time_labels]
    plt.xticks(ticks=np.linspace(time_float[0], time_float[-1], num=10), labels=time_labels_str, rotation=45)

    plt.tight_layout()
    plt.show()
else:
    print("Dimension mismatch detected.")
    print("Field data shape:", signal.shape)
    print("Time grid shape:", time_grid.shape)
    print("Range grid shape:", range_grid.shape)



