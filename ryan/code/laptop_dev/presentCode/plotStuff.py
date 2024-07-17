import json
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# Load JSON data
with open('/home/ryanrearden/Documents/SAGE_fromLaptop/tegdata_florence.json', 'r') as file:
    data = json.load(file)

with open('/home/ryanrearden/Documents/SAGE_fromLaptop/florencedata.json', 'r') as file:
    data2 = json.load(file)

def plotWithAllCPU():
    # Extract timestamps and CPU percentages
    timestamps = []
    cpu_percentages = []

    for entry in data:
        timestamps.append(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S'))
        cpu_percentage = [int(p.split('%')[0]) for p in entry["CPU"].split(',')]
        cpu_percentages.append(cpu_percentage)

    # Plot CPU percentages over time
    plt.figure(figsize=(10, 6))

    for i in range(len(cpu_percentages[0])):  # assuming all entries have the same number of CPU percentages
        cpu_i = [percentages[i] for percentages in cpu_percentages]
        plt.plot(timestamps, cpu_i, label=f'CPU {i+1}')

    plt.xlabel('Time')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()

def plotAvgCPU():
    # Extract timestamps and calculate average CPU percentages
    timestamps = []
    average_cpu_percentages = []

    for entry in data:
        timestamps.append(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S'))
        cpu_percentage = [int(p.split('%')[0]) for p in entry["CPU"].split(',')]
        average_cpu_percentages.append(sum(cpu_percentage) / len(cpu_percentage))

    # Plot average CPU usage over time
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, average_cpu_percentages, label='Average CPU Usage')

    plt.xlabel('Time')
    plt.ylabel('CPU Usage (%)')
    plt.title('Average CPU Usage Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()

def plotRAMandSWAP():
    # Extract timestamps, RAM, and SWAP usage
    timestamps = []
    ram_used = []
    ram_total = []
    swap_used = []
    swap_total = []

    for entry in data:
        timestamps.append(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S'))
        ram_usage = entry["RAM"].split('/')
        swap_usage = entry["SWAP"].split('/')
        ram_used.append(int(ram_usage[0].replace('MB', '')))
        ram_total.append(int(ram_usage[1].replace('MB', '')))
        swap_used.append(int(swap_usage[0].replace('MB', '')))
        swap_total.append(int(swap_usage[1].replace('MB', '')))

    # Plot RAM and SWAP usage over time
    plt.figure(figsize=(12, 6))

    # Plot RAM usage
    plt.subplot(2, 1, 1)
    plt.plot(timestamps, ram_used, label='RAM Used (MB)')
    plt.plot(timestamps, ram_total, label='RAM Total (MB)', linestyle='--')
    plt.xlabel('Time')
    plt.ylabel('RAM (MB)')
    plt.title('RAM Usage Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Plot SWAP usage
    plt.subplot(2, 1, 2)
    plt.plot(timestamps, swap_used, label='SWAP Used (MB)')
    plt.plot(timestamps, swap_total, label='SWAP Total (MB)', linestyle='--')
    plt.xlabel('Time')
    plt.ylabel('SWAP (MB)')
    plt.title('SWAP Usage Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()

def tokensVSTemp():
    timestamps1 = []
    cpu_temps = []

    for entry in data:
        timestamps1.append(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S'))
        cpu_temps.append(float(entry["CPU_TEMP"].replace('C', '')))

    # Extract relevant data from the second dataset
    timestamps2 = []
    tokens_per_second = []

    for entry in data2:
        timestamps2.append(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S'))
        tokens_per_second.append(entry["tokens per second"])

    # Merge data based on timestamps
    merged_timestamps = []
    merged_cpu_temps = []
    merged_tokens_per_second = []

    for t2, tokens in zip(timestamps2, tokens_per_second):
        closest_time = min(timestamps1, key=lambda t1: abs(t1 - t2))
        index = timestamps1.index(closest_time)
        merged_timestamps.append(t2)
        merged_cpu_temps.append(cpu_temps[index])
        merged_tokens_per_second.append(tokens)

    # Plot tokens per second against CPU temperature
    plt.figure(figsize=(10, 6))
    plt.scatter(merged_cpu_temps, merged_tokens_per_second, c='blue', label='Tokens per Second vs. CPU Temperature')
    plt.xlabel('CPU Temperature (°C)')
    plt.ylabel('Tokens per Second')
    plt.title('Tokens per Second vs. CPU Temperature')
    plt.legend()
    plt.tight_layout()

    # Show the plot
    plt.show()

def CPUPowerWithTokens():
    timestamps1 = []
    average_cpu_percentages = []

    for entry in data:
        timestamps1.append([(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') - datetime.strptime(data[0]["timestamp"], '%Y-%m-%d %H:%M:%S')).total_seconds() / 3600.0])
        cpu_percentage = [int(p.split('%')[0]) for p in entry["CPU"].split(',')]
        average_cpu_percentages.append(sum(cpu_percentage) / len(cpu_percentage))

    # Extract relevant data from the second dataset
    timestamps2 = []
    tokens_per_second = []

    for entry in data2:
        timestamps2.append([(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') - datetime.strptime(data[0]["timestamp"], '%Y-%m-%d %H:%M:%S')).total_seconds() / 3600.0])
        tokens_per_second.append(entry["tokens per second"])

    # Create a figure and a single subplot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot average CPU percentage over time on primary y-axis
    ax1.plot(timestamps1, average_cpu_percentages, 'g-', label='Average CPU Percentage')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Average CPU Percentage (%)', color='g')
    ax1.tick_params(axis='y', labelcolor='g')
    ax1.set_title('Average CPU Percentage and Tokens per Second Over Time')
    ax1.grid(True)
    fig.autofmt_xdate(rotation=45)

    # Create a secondary y-axis for tokens per second
    ax2 = ax1.twinx()
    ax2.plot(timestamps2, tokens_per_second, 'b-', label='Tokens per Second')
    ax2.set_ylabel('Tokens per Second', color='b')
    ax2.tick_params(axis='y', labelcolor='b')

    # Add legends
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.9))

    plt.tight_layout()
    plt.show()

def plotTemps():
    # Extract timestamps and temperatures, skipping entries with missing data
    timestamps = []
    ao_temps = []
    gpu_temps = []
    iwifi_temps = []
    pmic_temps = []
    aux_temps = []
    cpu_temps = []

    for entry in data:
        try:
            if entry["IWIFI_TEMP"] == "C" or entry["IWIFI_TEMP"] == "0C":
                continue  # Skip this entry if IWIFI_TEMP is missing

            timestamps.append([(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') - datetime.strptime(data[0]["timestamp"], '%Y-%m-%d %H:%M:%S')).total_seconds() / 3600.0])
            ao_temps.append(float(entry["AO_TEMP"].replace('C', '')))
            gpu_temps.append(float(entry["GPU_TEMP"].replace('C', '')))
            iwifi_temps.append(float(entry["IWIFI_TEMP"].replace('C', '')))
            pmic_temps.append(float(entry["PMIC_TEMP"].replace('C', '')))
            aux_temps.append(float(entry["AUX_TEMP"].replace('C', '')))
            cpu_temps.append(float(entry["CPU_TEMP"].replace('C', '')))
        except KeyError:
            continue  # Skip entry if any temperature data is missing

    # Plot temperatures over time
    plt.figure(figsize=(12, 8))

    plt.plot(timestamps, ao_temps, label='AO Temp')
    plt.plot(timestamps, gpu_temps, label='GPU Temp')
    plt.plot(timestamps, iwifi_temps, label='IWIFI Temp')
    plt.plot(timestamps, pmic_temps, label='PMIC Temp')
    plt.plot(timestamps, aux_temps, label='AUX Temp')
    plt.plot(timestamps, cpu_temps, label='CPU Temp')

    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperatures Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()

def graphCPUwithToken():
    # Extract relevant data from the first dataset, filtering by time range
    timestamps1 = [datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') for entry in data]
    average_cpu_percentages = [sum([int(p.split('%')[0]) for p in entry["CPU"].split(',')]) / len(entry["CPU"].split(',')) for entry in data]

    # Convert timestamps1 to hours relative to the first timestamp
    first_timestamp = timestamps1[0]
    hours_from_start = [(ts - first_timestamp).total_seconds() / 3600.0 for ts in timestamps1]

    # Extract relevant data from the second dataset, filtering by time range
    timestamps2 = [datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') for entry in data2]
    tokens_generated = [50 if entry["tokens per second"] else None for entry in data2]

    # Plot average CPU percentage over time
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Plot average CPU percentage over time
    ax1.plot(hours_from_start, average_cpu_percentages, 'deepskyblue', label='Average CPU Utilization', zorder=2)
    ax1.set_xlabel('Time (hours)')
    ax1.set_ylabel('Average Overall CPU Utilization (%)')
    ax1.tick_params(axis='y')
    ax1.set_title('Florence-2-base on Edge: Average Overall CPU Utilization with Image Description Generation Over Time')
    ax1.grid(True)

    # Synchronize tokens generated with CPU data timestamps
    for ts, token in zip(timestamps2, tokens_generated):
        if token is not None:
            # Find the index of the closest timestamp in timestamps1 to ts
            closest_index = min(range(len(timestamps1)), key=lambda i: abs(timestamps1[i] - ts))
            closest_cpu_percentage = average_cpu_percentages[closest_index]
            # Plot the red dot at the corresponding CPU percentage value
            ax1.scatter([hours_from_start[closest_index]], [closest_cpu_percentage], color='darkmagenta', marker='o', zorder=3)



    plt.xlim(0, 10)

    # Add legend for 'Token Generated' once
    plt.legend(['Average CPU Utilization', 'Image Description Generation'], loc='lower left')
    plt.tight_layout()
    plt.show()

# Extract "Total Time" values from each entry
total_times = [entry["Total Time"] for entry in data2]

# Calculate the average of "Total Time"
if total_times:
    average_total_time = sum(total_times) / len(total_times)
    print(f"Average Total Time: {average_total_time} seconds")
else:
    print("No data available")
