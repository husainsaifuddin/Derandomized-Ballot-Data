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
                votes_by_time[time_key] = {'democrat': 0, 'republican': 0}
            for card in session['Original']['Cards']:
                for contest in card['Contests']:
                    if contest['Id'] == 1:  # Presidential election
                        for mark in contest['Marks']:
                            if mark['CandidateId'] == 59:
                                votes_by_time[time_key]['democrat'] += 1
                            elif mark['CandidateId'] == 54:
                                votes_by_time[time_key]['republican'] += 1
                    else:
                        for mark in contest['Marks']:
                            if "PartyId" in mark:
                                if mark["PartyId"] == 1:
                                    votes_by_time[time_key]['democrat'] += 1
                                elif mark["PartyId"] == 2:
                                    votes_by_time[time_key]['republican'] += 1
                                                            

# Parse all JSON files in the directory
for filename in os.listdir(data_dir):
    if filename.endswith(".json"):
        parse_json_file(os.path.join(data_dir, filename))

times = pd.date_range(start="1900-01-01 07:00:00", periods=10, freq="1T")
# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(votes_by_time, orient='index')
print(f"total rep votes: {df['republican'].sum()}")
print(f"total dem votes: {df['democrat'].sum()}")


df.index = pd.to_datetime(df.index)

# Sort by the index (optional, but often useful)
df = df.sort_index()
# Compute a "bias" score
df["bias"] = df["democrat"] - df["republican"]
print(df["bias"].describe())
print(df["bias"].min())
min_idx = df["bias"].idxmin()
print(df.loc[min_idx])

# Resample to ensure a regular grid (e.g., per minute or any desired frequency)
df = df.resample("1T").mean()

# Pivot for heatmap (hours vs. minutes)
df["hour"] = df.index.hour
df["minute"] = df.index.minute
heatmap_data = df.pivot_table(index="hour", columns="minute", values="bias", fill_value=0)

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(
    heatmap_data,
    cmap="coolwarm_r",  # Blue for Democrat, Red for Republican
    center=0,         # Center the color scale at 0
    annot=False,      # Set to True if you want annotations on the heatmap
    cbar_kws={"label": "Bias (Republican - Democrat)"}
)
plt.title("Voting Bias Heatmap - SF 2020 General Election")
plt.xlabel("Minute")
plt.ylabel("Hour")
plt.tight_layout()
plt.savefig('party_affiliate_heatmap.png')
