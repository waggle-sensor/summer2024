import sage_data_client # IT MISSED THIS IMPORT
import pandas as pd
import matplotlib.pyplot as plt

def plot_pressure_and_hist():
    # Filter data for node W0B0 from the last 3 hours and only consider pressure
    df = sage_data_client.query(
        start="-3h",
        filter={
            "name": "env.pressure",
            "vsn": "W0B0",
            "sensor": "bme280"
        }
    )

    # Create a line plot for pressure
    df.set_index("timestamp").value.plot(label="Pressure")

    plt.legend()
    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.title("Line Plot of Pressure for W0B0")
    plt.show()

    # Create a histogram for pressure
    df.value.hist(bins=100)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Histogram of Pressure for W0B0")
    plt.show()

def plot_temperature_and_hist():
    # Filter data for node W0B0 from the last 3 hours and only consider temperature
    df = sage_data_client.query(
        start="-3h",
        filter={
            "name": "env.temperature",
            "vsn": "W0B0",
            "sensor": "bme280"
        }
    )

    # Create a line plot for temperature
    df.set_index("timestamp").value.plot(label="Temperature")

    plt.legend()
    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.title("Line Plot of Temperature for W0B0")
    plt.show()

    # Create a histogram for temperature
    df.value.hist(bins=100)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Histogram of Temperature for W0B0")
    plt.show()


## ADDED TO TEST FUNCTIONALITY
plot_pressure_and_hist()
plot_temperature_and_hist()