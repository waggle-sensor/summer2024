import sage_data_client # >>>>>>>>> MISSED THIS IMPORT <<<<<<<<<
import pandas as pd
import matplotlib.pyplot as plt

# Filter data for node W0B0 from the last 3 hours
df = sage_data_client.query(
    start="-3h",
    filter={
        "name": ["env.pressure", "env.temperature"],
        "vsn": "W0B0",
        "sensor": ["bme280", "bme280"]
    }
)

# Create a line plot for pressure and temperature
df[df["name"] == "env.pressure"].set_index("timestamp").value.plot(label="Pressure")
df[df["name"] == "env.temperature"].set_index("timestamp").value.plot(label="Temperature")

plt.legend()
plt.xlabel("Timestamp")
plt.ylabel("Value")
plt.title("Line Plot of Pressure and Temperature for W0B0")
plt.show()

# Create a histogram for pressure and temperature
df[df["name"] == "env.pressure"].value.hist(bins=100, label="Pressure", alpha=0.5)
df[df["name"] == "env.temperature"].value.hist(bins=100, label="Temperature", alpha=0.5)

plt.legend()
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Histogram of Pressure and Temperature for W0B0")
plt.show()