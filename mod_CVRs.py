import os
import json

sub_cipher = [5, 0, 8, 3, 2, 6, 1, 9, 4, 7]
reorder_cipher = [2, 3, 1, 5, 0, 4]
# Function to apply a digit substitution cipher
def substitute_digits(number, cipher):
    # Convert the number to a zero-padded 6-digit string
    number_str = str(number).zfill(6)
    
    # Initialize an empty string to store the substituted digits
    substituted_digits = ""
    
    # Iterate over each character in the 6-digit string
    for digit in number_str:
        # Convert the character to an integer, apply the cipher, and convert back to a string
        substituted_digit = str(cipher[int(digit)])
        # Append the substituted digit to the result string
        substituted_digits += substituted_digit
    # Convert the final string of substituted digits back to an integer
    return reorder_digits(int(substituted_digits), reorder_cipher)


# Function to apply a digit permutation
def reorder_digits(number, permutation):
    # Convert the number to a zero-padded 6-digit string
    digits = str(number).zfill(6)
    
    # Initialize an empty string to store the permuted digits
    permuted_digits = ""
    
    # Iterate over each index in the permutation list
    for i in permutation:
        # Append the digit at the current index in `digits` to the permuted string
        permuted_digits += digits[i]
    
    # Convert the final string of permuted digits back to an integer
    return int(permuted_digits)


# Path to the folder containing Cast Vote Record JSONs
folder_path = "batch0_SF"
# Path to the second JSON file
order_json_path = "SF_dict.json"

# Load the order mapping
with open(order_json_path, 'r') as f:
    order_mapping = json.load(f)

# Process files in the folder
json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
sorted_records = []

for file_name in json_files:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as f:
        print(file_path)
        data = json.load(f)
        tab_id = data['Sessions'][0]["TabulatorId"]
        print(tab_id)
        desired_order = order_mapping[str(tab_id)]
        just_record_ids = [sublist[1] for sublist in desired_order]

        print((just_record_ids))

        for i in range(len(data["Sessions"])):
            #data['Sessions'][i]['RecordId'] = substitute_digits(data['Sessions'][i]["RecordId"], sub_cipher)
            data['Sessions'][i]['RecordId'] = data['Sessions'][i]['RecordId'] % 1000000

        current_order = [x["RecordId"] for x in data['Sessions']]
        print((current_order))

        record_id_position = {record_id: index for index, record_id in enumerate(just_record_ids)}
        # Sort the 'Sessions' list based on the record_ids_order
        sorted_sessions = sorted(data['Sessions'], key=lambda x: record_id_position.get(x['RecordId'], len(just_record_ids)))
        data['Sessions'] = sorted_sessions

        new_order = [x["RecordId"] for x in data['Sessions']]
        print((new_order))
        #print(json.dumps(data, indent=4))
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)