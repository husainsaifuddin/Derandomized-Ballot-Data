import os
import json
# import chardet

def search_logs(tabulator_id):
    logfile_folder = 'N20_BSM_Logs'
    target_line = "[ScannerThread] INFO : [Scanner] Ballot cast"
    # encoding: Windows-1252
    for f in os.listdir(logfile_folder):
        parts = f.split('_')
        # Get the third part, which is the tabulator ids
        log_tab = parts[2]
        # print(f"log_tab: {log_tab}")
        if log_tab == str(tabulator_id):
            # print(f"log_tab: {log_tab}")
            filename = f"{logfile_folder}/{f}"
            with open(filename, 'r', encoding='latin-1') as logfile:
                try: 
                    lines = logfile.read().splitlines()
                    # print(f"lines: {lines}")
                    matching_lines = [line.strip() for line in lines if target_line in line]
                    matching_lines = matching_lines[-212:]
                    # print(f"num lines: {len(matching_lines)}" )
                    return matching_lines
                except json.JSONDecodeError:
                    print(f"Could not decode JSON in file: {logfile}")

def main():
    tab_dict = {}
    for filename in os.listdir('batch0_SF'):
        if filename.endswith('.json'):
            file_path = os.path.join('batch0_SF', filename)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    ballots = data['Sessions']
                    # "Sessions":[{"TabulatorId":556,
                    tabulator_id = ballots[0]['TabulatorId']
                    matching = search_logs(tabulator_id)
                    tab_dict[tabulator_id] = matching
                except json.JSONDecodeError:
                    print(f"Could not decode JSON in file: {filename}")
    with open("output.txt", "w") as output_file:
        # Redirect print output to the file
        print(f"dict after running: {tab_dict}", file=output_file)




if __name__ == "__main__":
    main()