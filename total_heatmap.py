import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Directory containing the JSON files
data_dir = 'batch0_SF'

# Initialize dictionaries to store the votes count
votes_by_time = {}
skip_ids = [38, 64, 67, 114, 120, 121, 133, 135, 187, 197, 198, 225, 226, 227, 238, 248,
            250, 319, 328, 395, 400, 401, 477, 498, 499, 517, 545, 582, 593, 596, 606, 607, 616, 618]

def parse_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        for session in data['Sessions']:
            if session['TabulatorId'] in skip_ids:
                return
            timestamp = session['Timestamp']
            time_key = datetime.strptime(timestamp, "%H:%M:%S").replace(second=0)
            if time_key not in votes_by_time:
                votes_by_time[time_key] = {'count': 0}
            votes_by_time[time_key]['count'] += 1

# Parse all JSON files in the directory
for filename in os.listdir(data_dir):
    if filename.endswith(".json"):
        parse_json_file(os.path.join(data_dir, filename))

df = pd.DataFrame.from_dict(votes_by_time, orient='index')
df.index = pd.to_datetime(df.index)

df = df.sort_index()
df = df.resample("1T").mean()

print(df)

# Pivot for heatmap (hours vs. minutes)
df["hour"] = df.index.hour
df["minute"] = df.index.minute
heatmap_data = df.pivot_table(index="hour", columns="minute", values="count", fill_value=0)

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(
    heatmap_data,
    center=0,
    cmap="Purples",         # Center the color scale at 0
    annot=False,      # Set to True if you want annotations on the heatmap
    cbar_kws={"label": "Bias (Republican - Democrat)"}
)

plt.title("Voting Bias Heatmap - SF 2020 General Election")
plt.xlabel("Minute")
plt.ylabel("Hour")
plt.tight_layout()
plt.show()
