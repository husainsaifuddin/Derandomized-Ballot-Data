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
                        if contest.get("Id") == 2:  # Filter ContestId: 1
                            marks = contest.get("Marks", [])
                            for mark in marks:
                                candidate_id = mark.get("CandidateId")
                                if candidate_id in [117, 116]:  # Pelosi (116) or Buttar (117)
                                    vote_data.append({
                                        "Timestamp": timestamp,
                                        "CandidateId": candidate_id
                                    })

# Convert vote data to DataFrame
df = pd.DataFrame(vote_data)

# Convert Timestamp to datetime and extract the hour
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%H:%M:%S')
df['Hour'] = df['Timestamp'].dt.hour

# Map CandidateId to names
candidate_map = {117: "Shahid Buttar", 116: "Nancy Pelosi"}
df['Candidate'] = df['CandidateId'].map(candidate_map)

# Group by hour and candidate
grouped = df.groupby(['Hour', 'Candidate']).size().unstack(fill_value=0)

# Plot the data
colors = ['blue', 'red']  # Blue for Pelosi, Red for Buttar
grouped.plot(kind='bar', figsize=(12, 6), width=0.8, color=colors)

# Customize the plot
plt.title("Vote Distribution by Hour 2020 US House California District 12 (Pelosi vs. Buttar)")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Votes")
plt.xticks(ticks=range(len(grouped.index)), labels=[f"{int(hour)}:00-{int(hour+1)}:00" for hour in grouped.index], rotation=45)
plt.legend(title="Candidate")
plt.tight_layout()
plt.grid(axis='y')
plt.savefig('2020house_district_12_bar_graph.png')

