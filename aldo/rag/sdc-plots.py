import sage_data_client
import pandas as pd
import matplotlib.pyplot as plt

def plot_temperature():
    # query temperature data for node W0B0 and last 3 hours
    df = sage_data_client.query(
        start='-3h',
        filter={
            "name": "env.temperature",
            "vsn": "W0B0"
        }
    )
    
    # plot line graph of temperature over time
    plt.figure(figsize=(10,6))
    plt.plot(df['timestamp'], df['value'])
    plt.title('Temperature (degF) for Node W0B0')
    plt.xlabel('Time')
    plt.ylabel('Temperature (degF)')
    plt.show()

def plot_pressure():
    # query pressure data for node W0B0 and last 3 hours
    df = sage_data_client.query(
        start='-3h',
        filter={
            "name": "env.pressure",
            "vsn": "W0B0"
        }
    )
    
    # plot histogram of pressure values
    plt.figure(figsize=(10,6))
    plt.hist(df['value'], bins=20)
    plt.title('Pressure Histogram for Node W0B0')
    plt.xlabel('Pressure (in)')
    plt.ylabel('Frequency')
    plt.show()

# call functions to generate plots
plot_temperature()
plot_pressure()