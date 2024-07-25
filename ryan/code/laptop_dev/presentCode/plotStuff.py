import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

# Load JSON data
with open('/home/ryanrearden/Documents/SAGE_fromLaptop/tegdata_florence.json', 'r') as file:
    data = json.load(file)

with open('/home/ryanrearden/Documents/SAGE_fromLaptop/florencedata.json', 'r') as file:
    data2 = json.load(file)

# Load JSON data
with open('/home/ryanrearden/Documents/SAGE_fromLaptop/tegdata_llava.json', 'r') as file:
    data3 = json.load(file)

with open('/home/ryanrearden/Documents/SAGE_fromLaptop/llavadata.json', 'r') as file:
    data4 = json.load(file)


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
    ax1.set_title('LLaVA on Edge: Average Overall CPU Utilization with Image Description Generation Over Time')
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

def getAvgTime():
    # Extract "Total Time" values from each entry
    total_times = [entry["Total Time"] for entry in data2]

    # Calculate the average of "Total Time"
    if total_times:
        average_total_time = sum(total_times) / len(total_times)
        print(f"Average Total Time: {average_total_time} seconds")
    else:
        print("No data available")

def plotComparison():
    # Function to filter entries within the first 10 hours
    def filter_data_within_9_hours(data, start_time):
        return [entry for entry in data if datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') - start_time <= timedelta(hours=9)]

    # Function to calculate average total time
    def calculate_average_total_time(data):
        total_times = [entry["Total Time"] for entry in data if "Total Time" in entry]
        if total_times:
            return sum(total_times) / len(total_times)
        return 0

    # Function to calculate average CPU usage
    def calculate_average_cpu_usage(data):
        cpu_usages = [
            sum([int(p.split('%')[0]) for p in entry["CPU"].split(',')]) / len(entry["CPU"].split(','))
            for entry in data if "CPU" in entry
        ]
        if cpu_usages:
            return sum(cpu_usages) / len(cpu_usages)
        return 0

    # Determine the start time from the first dataset
    start_time = datetime.strptime(data[0]["timestamp"], '%Y-%m-%d %H:%M:%S')

    # Filter data within the first 10 hours
    filtered_data = filter_data_within_9_hours(data, start_time)
    filtered_data2 = filter_data_within_9_hours(data2, start_time)
    filtered_data3 = filter_data_within_9_hours(data3, start_time)
    filtered_data4 = filter_data_within_9_hours(data4, start_time)

    # Calculate averages for filtered data
    avg_total_time_florence = calculate_average_total_time(filtered_data2)
    avg_total_time_llava = calculate_average_total_time(filtered_data4)

    avg_cpu_usage_florence = calculate_average_cpu_usage(filtered_data)
    avg_cpu_usage_llava = calculate_average_cpu_usage(filtered_data3)


    # Prepare data for plotting
    labels = ['Florence-2', 'LLaVA']
    avg_total_times = [avg_total_time_florence, avg_total_time_llava]
    avg_cpu_usages = [avg_cpu_usage_florence, avg_cpu_usage_llava]

    x = range(len(labels))  # the label locations

    # Create a bar graph
    fig, ax1 = plt.subplots(figsize=(14, 8))

    bar_width = 0.35
    opacity = 0.8

    # Bar for average total time
    bars1 = ax1.bar(x, avg_total_times, bar_width, alpha=opacity, color='dimgrey', label='Average Total Time (s)')

    # Create another y-axis for CPU usage
    ax2 = ax1.twinx()
    bars2 = ax2.bar([p + bar_width for p in x], avg_cpu_usages, bar_width, alpha=opacity, color='slateblue', label='Average CPU Usage (%)')

    # Set labels and titles
    ax1.set_xlabel('Models')
    ax1.set_ylabel('Average Total Time (s)', color='dimgrey')
    ax2.set_ylabel('Average CPU Usage (%)', color='slateblue')
    ax1.set_title('Average Total Time and CPU Usage for Florence-2 and LLaVA')
    ax1.set_xticks([p + bar_width / 2 for p in x])
    ax1.set_xticklabels(labels)

    # Add legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Display the plot
    plt.tight_layout()
    plt.show()

def betterplotComparison():
    # Function to filter entries within the first 9 hours
    def filter_data_within_9_hours(data, start_time):
        return [entry for entry in data if datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') - start_time <= timedelta(hours=9)]

    # Function to calculate average total time
    def calculate_average_total_time(data):
        total_times = [entry["Total Time"] for entry in data if "Total Time" in entry]
        if total_times:
            return sum(total_times) / len(total_times)
        return 0

    # Function to calculate average CPU usage
    def calculate_average_cpu_usage(data):
        cpu_usages = [
            sum([int(p.split('%')[0]) for p in entry["CPU"].split(',')]) / len(entry["CPU"].split(','))
            for entry in data if "CPU" in entry
        ]
        if cpu_usages:
            return sum(cpu_usages) / len(cpu_usages)
        return 0

    # Determine the start time from the first dataset
    start_time = datetime.strptime(data[0]["timestamp"], '%Y-%m-%d %H:%M:%S')

    # Filter data within the first 9 hours
    filtered_data = filter_data_within_9_hours(data, start_time)
    filtered_data2 = filter_data_within_9_hours(data2, start_time)
    filtered_data3 = filter_data_within_9_hours(data3, start_time)
    filtered_data4 = filter_data_within_9_hours(data4, start_time)

    # Calculate averages for filtered data
    avg_total_time_florence = calculate_average_total_time(filtered_data2)
    avg_total_time_llava = calculate_average_total_time(filtered_data4)

    avg_cpu_usage_florence = calculate_average_cpu_usage(filtered_data)
    avg_cpu_usage_llava = calculate_average_cpu_usage(filtered_data3)

    # Prepare data for plotting
    labels = ['Florence-2']
    avg_total_times_florence = [avg_total_time_florence]
    avg_cpu_usages_florence = [avg_cpu_usage_florence]

    # Create the first bar graph for Average Total Time
    fig1, ax1 = plt.subplots(figsize=(6, 8))

    bar_width = 0.35
    opacity = 0.8

    # Bar for average total time for Florence-2
    bars1 = ax1.bar(labels, avg_total_times_florence, bar_width, alpha=opacity, color='dimgrey', label='Florence-2 Total Time (s)')

    # Plot dashed lines for LLaVA average total time
    ax1.axhline(y=avg_total_time_llava, color='red', linestyle='--', label='LLaVA Total Time (s)')

    # Set labels and titles
    ax1.set_xlabel('', fontsize=18)
    ax1.set_ylabel('Average Total Runtime Per Image (s)', color='black', fontsize=18)
    ax1.set_title(f'Average Total Runtime Per Image \n for Florence-2 and LLaVA', fontsize=18)
    ax1.set_xticks([p for p in range(len(labels))])
    ax1.set_xticklabels(labels, fontsize=18)
    ax1.tick_params(axis='y', labelsize=16)
    ax1.tick_params(axis='x', labelsize=16)

    # Add legend
    ax1.legend(loc='lower center', fontsize=16)

    # Display the plot
    plt.tight_layout()
    plt.show()

    # Create the second bar graph for Average CPU Usage
    fig2, ax2 = plt.subplots(figsize=(6, 8))

    # Bar for average CPU usage for Florence-2
    bars2 = ax2.bar(labels, avg_cpu_usages_florence, bar_width, alpha=opacity, color='slateblue', label='Florence-2 CPU Usage (%)')

    # Plot dashed lines for LLaVA average CPU usage
    ax2.axhline(y=avg_cpu_usage_llava, color='blue', linestyle='--', label='LLaVA CPU Usage (%)')

    # Set labels and titles
    ax2.set_xlabel('', fontsize=18)
    ax2.set_ylabel('Average CPU Usage (%)', color='black', fontsize=18)
    ax2.set_title('Average CPU Usage for Florence-2 and LLaVA', fontsize=18)
    ax2.set_xticks([p for p in range(len(labels))])
    ax2.set_xticklabels(labels, fontsize=18)
    ax1.tick_params(axis='y', labelsize=16)
    ax1.tick_params(axis='x', labelsize=16)


    # Add legend
    ax2.legend(loc='lower center', fontsize=16)

    # Display the plot
    plt.tight_layout()
    plt.show()

def graphCPUwithToken2():
    # Extract relevant data from the first dataset (Florence-2), filtering by time range
    timestamps1 = [datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') for entry in data]
    average_cpu_percentages1 = [sum([int(p.split('%')[0]) for p in entry["CPU"].split(',')]) / len(entry["CPU"].split(',')) for entry in data]

    # Convert timestamps1 to hours relative to the first timestamp
    first_timestamp = timestamps1[0]
    hours_from_start1 = [(ts - first_timestamp).total_seconds() / 3600.0 for ts in timestamps1]

    # Extract relevant data from the second dataset (Florence-2), filtering by time range
    timestamps2 = [datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') for entry in data2]
    tokens_generated1 = [50 if entry["tokens per second"] else None for entry in data2]

    # Extract relevant data from the third dataset (LLaVA), filtering by time range
    timestamps3 = [datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') for entry in data3]
    average_cpu_percentages2 = [sum([int(p.split('%')[0]) for p in entry["CPU"].split(',')]) / len(entry["CPU"].split(',')) for entry in data3]

    # Convert timestamps3 to hours relative to the first timestamp
    first_timestamp3 = timestamps3[0]
    hours_from_start3 = [(ts - first_timestamp3).total_seconds() / 3600.0 for ts in timestamps3]

    # Extract relevant data from the fourth dataset (LLaVA), filtering by time range
    timestamps4 = [datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') for entry in data4]
    tokens_generated2 = [50 if entry["tokens per second"] else None for entry in data4]

    # Plot average CPU percentage over time for both Florence-2 and LLaVA
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Plot Florence-2 average CPU percentage over time
    ax1.plot(hours_from_start1, average_cpu_percentages1, 'deepskyblue', label='Florence-2 Average CPU Utilization', zorder=2)

    # Plot LLaVA average CPU percentage over time
    ax1.plot(hours_from_start3, average_cpu_percentages2, 'orange', label='LLaVA Average CPU Utilization', zorder=2)

    ax1.set_xlabel('Time (hours)')
    ax1.set_ylabel('Average Overall CPU Utilization (%)')
    ax1.tick_params(axis='y')
    ax1.set_title('Comparison of Average Overall CPU Utilization with Image Description Generation Over Time')
    ax1.grid(True)

    # Synchronize tokens generated with CPU data timestamps for Florence-2
    for ts, token in zip(timestamps2, tokens_generated1):
        if token is not None:
            # Find the index of the closest timestamp in timestamps1 to ts
            closest_index = min(range(len(timestamps1)), key=lambda i: abs(timestamps1[i] - ts))
            closest_cpu_percentage = average_cpu_percentages1[closest_index]
            # Plot the red dot at the corresponding CPU percentage value
            ax1.scatter([hours_from_start1[closest_index]], [closest_cpu_percentage], color='darkmagenta', marker='o', zorder=3)

    # Synchronize tokens generated with CPU data timestamps for LLaVA
    for ts, token in zip(timestamps4, tokens_generated2):
        if token is not None:
            # Find the index of the closest timestamp in timestamps3 to ts
            closest_index = min(range(len(timestamps3)), key=lambda i: abs(timestamps3[i] - ts))
            closest_cpu_percentage = average_cpu_percentages2[closest_index]
            # Plot the red dot at the corresponding CPU percentage value
            ax1.scatter([hours_from_start3[closest_index]], [closest_cpu_percentage], color='red', marker='x', zorder=3)

    plt.xlim(0, 10)

    # Add legend for both Florence-2 and LLaVA
    plt.legend(loc='lower left')
    plt.tight_layout()
    plt.show()


def graphCPUwithToken3():
    # Extract relevant data from the first dataset (Florence-2), filtering by time range
    timestamps1 = [datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') for entry in data]
    average_cpu_percentages1 = [sum([int(p.split('%')[0]) for p in entry["CPU"].split(',')]) / len(entry["CPU"].split(',')) for entry in data]

    # Convert timestamps1 to hours relative to the first timestamp
    first_timestamp = timestamps1[0]
    hours_from_start1 = [(ts - first_timestamp).total_seconds() / 3600.0 for ts in timestamps1]

    # Extract relevant data from the second dataset (Florence-2), filtering by time range
    timestamps2 = [datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') for entry in data2]
    tokens_generated1 = [50 if entry["tokens per second"] else None for entry in data2]

    # Extract relevant data from the third dataset (LLaVA), filtering by time range
    timestamps3 = [datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') for entry in data3]
    average_cpu_percentages2 = [sum([int(p.split('%')[0]) for p in entry["CPU"].split(',')]) / len(entry["CPU"].split(',')) for entry in data3]

    # Convert timestamps3 to hours relative to the first timestamp
    first_timestamp3 = timestamps3[0]
    hours_from_start3 = [(ts - first_timestamp3).total_seconds() / 3600.0 for ts in timestamps3]

    # Extract relevant data from the fourth dataset (LLaVA), filtering by time range
    timestamps4 = [datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S') for entry in data4]
    tokens_generated2 = [50 if entry["tokens per second"] else None for entry in data4]

    # Plot average CPU percentage over time for both Florence-2 and LLaVA
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Plot Florence-2 average CPU percentage over time
    ax1.plot(hours_from_start1, average_cpu_percentages1, 'deepskyblue', label='Florence-2 Average CPU Utilization', zorder=2)

    # Plot LLaVA average CPU percentage over time
    ax1.plot(hours_from_start3, average_cpu_percentages2, 'orange', label='LLaVA Average CPU Utilization', zorder=2)

    ax1.set_xlabel('Time (hours)', fontsize=18)
    ax1.set_ylabel('Average Overall CPU Utilization (%)', fontsize=18)
    ax1.tick_params(axis='y', labelsize=16)
    ax1.tick_params(axis='x', labelsize=16)
    ax1.set_title('Comparison of Average Overall CPU Utilization with Image Description Generation Over Time', fontsize=18)
    ax1.grid(True)

    # Synchronize tokens generated with CPU data timestamps for Florence-2
    for ts, token in zip(timestamps2, tokens_generated1):
        if token is not None:
            # Find the index of the closest timestamp in timestamps1 to ts
            closest_index = min(range(len(timestamps1)), key=lambda i: abs(timestamps1[i] - ts))
            closest_cpu_percentage = average_cpu_percentages1[closest_index]
            # Plot the red dot at the corresponding CPU percentage value
            ax1.scatter([hours_from_start1[closest_index]], [closest_cpu_percentage], color='darkmagenta', marker='o', label='Florence-2 Image Description Generation', zorder=3)

    # Synchronize tokens generated with CPU data timestamps for LLaVA
    for ts, token in zip(timestamps4, tokens_generated2):
        if token is not None:
            # Find the index of the closest timestamp in timestamps3 to ts
            closest_index = min(range(len(timestamps3)), key=lambda i: abs(timestamps3[i] - ts))
            closest_cpu_percentage = average_cpu_percentages2[closest_index]
            # Plot the red dot at the corresponding CPU percentage value
            ax1.scatter([hours_from_start3[closest_index]], [closest_cpu_percentage], color='red', marker='x', label='LLaVA Image Description Generation', zorder=3)

    plt.xlim(0, 10)

    # Add legend for both Florence-2 and LLaVA
    handles, labels = ax1.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='lower left', fontsize=18)
    plt.tight_layout()
    plt.show()

def plotRAMandRAM():
    # Extract timestamps, RAM, and SWAP usage
    timestamps = []
    ram_used = []
    ram_total = []
    ram2_used = []
    ram2_total = []

    for entry in data:
        timestamps.append(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S'))
        ram_usage = entry["RAM"].split('/')
        ram_used.append(int(ram_usage[0].replace('MB', '')))
        ram_total.append(int(ram_usage[1].replace('MB', '')))
    
    for entry in data3:
        timestamps.append(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S'))
        ram_usage = entry["RAM"].split('/')
        ram2_used.append(int(ram_usage[0].replace('MB', '')))
        ram2_total.append(int(ram_usage[1].replace('MB', '')))
    
    # Cut off after RAM_used ends
    min_length = min(len(ram_used), len(ram2_used))
    timestamps = timestamps[:min_length]
    ram_used = ram_used[:min_length]
    ram_total = ram_total[:min_length]
    ram2_used = ram2_used[:min_length]
    ram2_total = ram2_total[:min_length]

    # Calculate hours after start
    start_time = timestamps[0]
    hours_after_start = [(ts - start_time).total_seconds() / 3600 for ts in timestamps]

    # Plot RAM and SWAP usage over time
    plt.figure(figsize=(12, 6))

    # Plot RAM usage
    plt.subplot(2, 1, 1)
    plt.plot(hours_after_start, ram_used, label='RAM Used (MB)')
    plt.plot(hours_after_start, ram_total, label='RAM Total (MB)', linestyle='--')
    plt.xlabel('Hours After Start')
    plt.ylabel('RAM (MB)')
    plt.title('RAM Usage Over Time Florence-2')
    plt.legend()
    plt.tight_layout()

    # Plot SWAP usage
    plt.subplot(2, 1, 2)
    plt.plot(hours_after_start, ram2_used, label='RAM Used (MB)')
    plt.plot(hours_after_start, ram2_total, label='RAM Total (MB)', linestyle='--')
    plt.xlabel('Hours After Start')
    plt.ylabel('RAM (MB)')
    plt.title('RAM Usage Over Time LLaVA')
    plt.legend()
    plt.tight_layout()

    # Show the plot
    plt.show()

def plotRnR2():
    # Extract timestamps, RAM, and SWAP usage
    timestamps = []
    ram_used = []
    ram_total = []
    ram2_used = []
    ram2_total = []

    for entry in data:
        timestamps.append(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S'))
        ram_usage = entry["RAM"].split('/')
        ram_used.append(int(ram_usage[0].replace('MB', '')))
        ram_total.append(int(ram_usage[1].replace('MB', '')))
    
    for entry in data3:
        timestamps.append(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S'))
        ram_usage = entry["RAM"].split('/')
        ram2_used.append(int(ram_usage[0].replace('MB', '')))
        ram2_total.append(int(ram_usage[1].replace('MB', '')))
    
    # Cut off after RAM_used ends
    min_length = min(len(ram_used), len(ram2_used))
    timestamps = timestamps[:min_length]
    ram_used = ram_used[:min_length]
    ram_total = ram_total[:min_length]
    ram2_used = ram2_used[:min_length]
    ram2_total = ram2_total[:min_length]

    # Calculate hours after start
    start_time = timestamps[0]
    hours_after_start = [(ts - start_time).total_seconds() / 3600 for ts in timestamps]

    # Plot RAM and SWAP usage over time
    plt.figure(figsize=(12, 6))

    # Plot RAM and SWAP usage
    plt.plot(hours_after_start, ram_used, label='RAM Used while running Florence-2 (MB)')
    plt.plot(hours_after_start, ram_total, label='RAM Total (MB)', linestyle='--')
    plt.plot(hours_after_start, ram2_used, label='RAM used while running LLaVA (MB)')

    plt.xlabel('Hours After Start', fontsize=14)
    plt.ylabel('RAM (MB)',fontsize=14)
    plt.title('RAM Usage Over Time',fontsize=14)
    plt.legend(fontsize=14)
    plt.tight_layout()

    # Show the plot
    plt.show()

def plotTokensPerSecond():
    # Extract timestamps and tokens per second for both datasets
    timestamps_florence = []
    tokens_per_second_florence = []
    timestamps_llava = []
    tokens_per_second_llava = []

    for entry in data2:
        timestamps_florence.append(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S'))
        tokens_per_second_florence.append(entry["tokens per second"])
    
    for entry in data4:
        timestamps_llava.append(datetime.strptime(entry["timestamp"], '%Y-%m-%d %H:%M:%S'))
        tokens_per_second_llava.append(entry["tokens per second"])
    
    # Determine the start and end times based on the shorter timeframe
    start_time = max(timestamps_florence[0], timestamps_llava[0])
    end_time = min(timestamps_florence[-1], timestamps_llava[-1])

    # Filter data points within the shorter timeframe
    filtered_florence_times = [ts for ts in timestamps_florence if start_time <= ts <= end_time]
    filtered_florence_tokens = [tokens_per_second_florence[i] for i, ts in enumerate(timestamps_florence) if start_time <= ts <= end_time]
    filtered_llava_times = [ts for ts in timestamps_llava if start_time <= ts <= end_time]
    filtered_llava_tokens = [tokens_per_second_llava[i] for i, ts in enumerate(timestamps_llava) if start_time <= ts <= end_time]

    # Calculate hours after start
    hours_after_start_florence = [(ts - start_time).total_seconds() / 3600 for ts in filtered_florence_times]
    hours_after_start_llava = [(ts - start_time).total_seconds() / 3600 for ts in filtered_llava_times]

    # Plot tokens per second for both datasets
    plt.figure(figsize=(12, 6))

    # Plot Florence-2 tokens per second
    plt.plot(hours_after_start_florence, filtered_florence_tokens, label='Florence-2 Tokens per Second')
    
    # Plot LLaVA tokens per second
    plt.plot(hours_after_start_llava, filtered_llava_tokens, label='LLaVA Tokens per Second')

    # Calculate and plot trend lines
    if hours_after_start_florence and filtered_florence_tokens:
        z_florence = np.polyfit(hours_after_start_florence, filtered_florence_tokens, 1)
        p_florence = np.poly1d(z_florence)
        plt.plot(hours_after_start_florence, p_florence(hours_after_start_florence), linestyle='--', color='blue', label='Florence-2 Trend Line')

    if hours_after_start_llava and filtered_llava_tokens:
        z_llava = np.polyfit(hours_after_start_llava, filtered_llava_tokens, 1)
        p_llava = np.poly1d(z_llava)
        plt.plot(hours_after_start_llava, p_llava(hours_after_start_llava), linestyle='--', color='orange', label='LLaVA Trend Line')

    plt.xlabel('Hours After Start', fontsize=14)
    plt.ylabel('Tokens per Second', fontsize=14)
    plt.title('Tokens per Second Over Time with Trend Lines', fontsize=14)
    plt.legend(fontsize=14)
    plt.tight_layout()

    # Show the plot
    plt.show()

plotRnR2()
plotTokensPerSecond()
CPUPowerWithTokens()