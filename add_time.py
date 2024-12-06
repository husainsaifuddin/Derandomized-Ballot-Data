import json
import os

with open('all_votes_by_time.json', 'r') as f:
    time_dict = json.load(f)

for file in os.listdir('batch0_SF'):
    filename = f"batch0_SF/{file}"
    with open(filename, 'r') as cvr:
        # load cvr
        data = json.load(cvr)
        # get sessions array
        # get tab id of current cvr file
        tab_id = data['Sessions'][0]['TabulatorId']
        # loop through the dictionary with
        # print(len(time_dict))
        for item in time_dict:
            #print(f"searching for {tab_id}")
            #print(f"item tab id: {item["tab_id"]}")
            if item["tab_id"] == str(tab_id):
                for i, _ in enumerate(data['Sessions']):
                    if data['Sessions'][i]['RecordId'] != item['votes'][i]['voter_id']:
                        raise Exception(f"RecordId mismatch: {data['Sessions'][i]['RecordId']} vs. {item['votes'][i]['voter_id']}")
                    data['Sessions'][i]['Timestamp'] = item['votes'][i]['time_of_vote']
                    #print(sessions[i]['Timestamp'])
    with open(filename, 'w') as cvr:
        json.dump(data, cvr, indent=4)

# tab_id_to_find = 33
# filtered_elements = [item for item in data if item["tab_id"] == tab_id_to_find]
