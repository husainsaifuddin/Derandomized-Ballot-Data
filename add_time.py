import json
import os

with open('all_vote_by_time', 'r') as f:
    time_dict = json.load(f)

for file in os.listdir('batch0_SF', 'r'):
    filename = f"batch0_SF/{file}"
    with open(filename, 'r') as cvr:

