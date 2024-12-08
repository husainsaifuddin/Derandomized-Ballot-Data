import re
from datetime import datetime
import os
import chardet
from charset_normalizer import detect

def count_errors(lines, keyword='ERROR :'):
    return sum(1 for line in lines if keyword in line)

def process_log_file(folder):
    # Initialize arrays for before 8am and after 3pm
    lines_before_8am = []
    lines_after_3pm = []
    voters_before_8am = 0
    voters_after_3pm = 0
    for file in os.listdir(folder):
        file_path = f"{folder}/{file}"
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()

            
            # Split based on the last occurrence of the target line
            target_line = "[Unit State] Unit state changed to Opened (Poll is open)"
            last_split_index = -1
            for index, line in enumerate(lines):
                if target_line in line:
                    last_split_index = index
            
            # Extract the part of the file after the last occurrence
            if last_split_index != -1:
                relevant_lines = lines[last_split_index + 1:]
            else:
                # If the target line doesn't exist, nothing to process
                return [], []
            
            # Regex pattern to extract timestamp (assuming the format is HH:MM:SS)
            time_pattern = re.compile(r'\b(\d{2}:\d{2}:\d{2})\b')
            
            # Process each relevant line
            for line in relevant_lines:
                match = time_pattern.search(line)
                if match:
                    timestamp_str = match.group(1)
                    timestamp = datetime.strptime(timestamp_str, '%H:%M:%S').time()
                    
                    # Add line to appropriate array based on time
                    if timestamp < datetime.strptime("08:00:00", '%H:%M:%S').time():
                        lines_before_8am.append(line)
                        if "Ballot saved successfully" in line:
                            voters_before_8am += 1
                    elif timestamp > datetime.strptime("15:00:00", '%H:%M:%S').time():
                        lines_after_3pm.append(line)
                        if "Ballot saved successfully" in line:
                            voters_after_3pm += 1

            
    return lines_before_8am, lines_after_3pm, voters_before_8am, voters_after_3pm

# Example usage
folder = "N20_BSM_Logs"
before_8am_lines, after_3pm_lines, voters_before_8am, voters_after_3pm = process_log_file(folder)

# Print results for verification
print("Lines before 8am:")
print('\n'.join(before_8am_lines[:10]))

print("\nLines after 3pm:")
print('\n'.join(after_3pm_lines[:10]))

before_8am_error_count = count_errors(before_8am_lines)
after_3pm_error_count = count_errors(after_3pm_lines)

errors_before_8 = before_8am_error_count / voters_before_8am
errors_after_3 = after_3pm_error_count / voters_after_3pm
print(f"errors_before_8: {errors_before_8}")
print(f"errors_after_3: {errors_after_3}")




