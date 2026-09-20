import re
import pandas as pd
import matplotlib.pyplot as plt


# Read the log file
records = []

with open("server.log", "r") as file:
    for line in file:

        match = re.search(
            r"(\d{2}:\d{2}) CPU=(\d+)% Memory=(\d+)% ResponseTime=(\d+)ms",
            line
        )

        if match:
            records.append({
                "Timestamp": match.group(1),
                "CPU": int(match.group(2)),
                "Memory": int(match.group(3)),
                "Response_Time": int(match.group(4))
            })


# Convert to DataFrame
df = pd.DataFrame(records)


# Calculate basic statistics
print("Basic Statistics:")
print(df[["CPU", "Memory", "Response_Time"]].describe())


# Thresholds
CPU_THRESHOLD = 90
MEMORY_THRESHOLD = 90
RESPONSE_TIME_THRESHOLD = 300


# Detect anomalies
df["Anomaly"] = (
    (df["CPU"] > CPU_THRESHOLD) |
    (df["Memory"] > MEMORY_THRESHOLD) |
    (df["Response_Time"] > RESPONSE_TIME_THRESHOLD)
)


# Get anomalous records
anomalies = df[df["Anomaly"]]


# Required output
print()
print(f"Total records: {len(df)}")
print(f"Anomalies detected: {len(anomalies)}")

print()
print(f"{'Timestamp':<16}{'CPU':<10}{'Status'}")

for _, row in anomalies.iterrows():
    print(
        f"{row['Timestamp']:<16}"
        f"{row['CPU']}%{'':<8}"
        f"ANOMALY"
    )


# Graph
plt.figure(figsize=(10, 5))

plt.plot(
    df["Timestamp"],
    df["CPU"],
    marker="o",
    label="CPU Usage"
)

plt.plot(
    df["Timestamp"],
    df["Memory"],
    marker="o",
    label="Memory Usage"
)

plt.scatter(
    anomalies["Timestamp"],
    anomalies["CPU"],
    marker="x",
    s=100,
    label="Anomaly"
)

plt.axhline(
    CPU_THRESHOLD,
    linestyle="--",
    label="CPU Threshold"
)

plt.xlabel("Timestamp")
plt.ylabel("Usage (%)")
plt.title("AIOps Log Anomaly Detection")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig("anomaly_graph.png")

print("\nGraph saved as anomaly_graph.png")