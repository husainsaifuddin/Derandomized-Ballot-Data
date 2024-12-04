import os
import shutil

# Define paths
source_folder = 'Alaska_2022'
target_folder = 'batch0_AK_2022'
files_list_path = 'alaska_batch0_2022.txt'

# Create target folder if it doesn't exist
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# Read the file names from files.txt
with open(files_list_path, 'r') as f:
    files_to_move = f.read().splitlines()

# Search and move files from folder1 to batch0
for file_name in files_to_move:
    source_path = os.path.join(source_folder, file_name)
    target_path = os.path.join(target_folder, file_name)
    
    # Check if the file exists in folder1 before moving
    if os.path.exists(source_path):
        shutil.move(source_path, target_path)
        print(f"Moved {file_name} to {target_folder}")
    else:
        print(f"File {file_name} not found in {source_folder}")

print("File transfer complete.")
