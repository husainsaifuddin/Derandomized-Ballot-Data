import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Folder containing the JSON files
folder_path = "batch0_SF"

# Initialize a DataFrame to store vote data
vote_data = []
skip_ids = [38, 64, 67, 114, 120, 121, 133, 135, 187, 197, 198, 225, 226, 227, 238, 248, 
            250, 319, 328, 395, 400, 401, 477, 498, 499, 517, 545, 582, 593, 596, 606, 607, 616, 618]

# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as f:
            data = json.load(f)
            
            # Extract sessions
            sessions = data.get("Sessions", [])
            for session in sessions:
                if session['TabulatorId'] in skip_ids:
                    continue
                timestamp = session.get("Timestamp")
                cards = session.get("Original", {}).get("Cards", [])
                for card in cards:
                    contests = card.get("Contests", [])
                    for contest in contests:
                        undervotes = contest.get("Undervotes", 0)
                        total_votes = 1  # Count every contest as a vote
                        vote_data.append({
                            "Timestamp": timestamp,
                            "Undervotes": undervotes,
                            "TotalVotes": total_votes
                        })

# Convert vote data to DataFrame
df = pd.DataFrame(vote_data)

# Convert Timestamp to datetime and extract the hour
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%H:%M:%S', errors='coerce')
df['Hour'] = df['Timestamp'].dt.hour

# Group by hour and calculate totals for overvotes and total votes
grouped = df.groupby('Hour')[['Undervotes', 'TotalVotes']].sum()

# Calculate percentage of overvotes
grouped['UndervotePercentage'] = (grouped['Undervotes'] / grouped['TotalVotes']) * 100

# Plot the data
plt.figure(figsize=(10, 6))
grouped['UndervotePercentage'].plot(kind='bar', color='khaki', edgecolor='black')

# Customize the plot
plt.title("Percentage of Undervotes by Hour in SF 2020 Election")
plt.xlabel("Hour of the Day")
plt.ylabel("Percentage of Undervotes (%)")
plt.xticks(ticks=range(len(grouped.index)), labels=[f"{int(hour)}:00-{int(hour+1)}:00" for hour in grouped.index], rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save and show the plot
plt.tight_layout()
plt.savefig('undervotes_percentage_by_hour.png')

"""
# Convert vote data to DataFrame
df = pd.DataFrame(vote_data)

# Convert Timestamp to datetime and extract the hour
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%H:%M:%S', errors='coerce')
df['Hour'] = df['Timestamp'].dt.hour

# Group by hour and sum the overvotes
hourly_undervotes = df.groupby('Hour')['Undervotes'].sum()

# Plot the data
plt.figure(figsize=(10, 6))
hourly_undervotes.plot(kind='bar', color='khaki', edgecolor='black')

# Customize the plot
plt.title("Undervotes Counted by Hour in SF 2020 Election")
plt.xlabel("Hour of the Day")
plt.ylabel("Total Undervotes")
plt.xticks(ticks=range(len(hourly_undervotes.index)), labels=[f"{int(hour)}:00-{int(hour+1)}:00" for hour in hourly_undervotes.index], rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save and show the plot
plt.tight_layout()
plt.savefig('undervotes_by_hour.png')"""