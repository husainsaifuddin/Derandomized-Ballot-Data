# encoding: Windows-1252
import json
import chardet
from charset_normalizer import detect

def get_log_times(expected_num_ballots, tabulator_id):
    target_line = "[ScannerThread] INFO : [Scanner] Ballot cast"
    num_ballots_text = "INFO : [Counters] Number of ballots cast:"

    with open(f'N20_BSM_Logs/machinecontext_1_{tabulator_id}_slog.txt', 'rb') as f:
        rawdata = f.read()
        try:
            lines = rawdata.decode('Windows-1252').splitlines()
        except UnicodeDecodeError:
            try:
                lines = rawdata.decode('MacRoman').splitlines()
            except:
                result = detect(rawdata)
                encoding = result['encoding']
                if not encoding:
                    encoding = chardet.detect(rawdata)['encoding']
                print(encoding)
                lines = rawdata.decode(encoding).splitlines()

    num_ballots_cast = [line.strip() for line in lines if num_ballots_text in line]
    num_ballots_cast = int(num_ballots_cast[-1].split("cast: ")[1])

    if num_ballots_cast != expected_num_ballots:
        print(f'Number of votes in tabulator {tabulator_id} logs ({num_ballots_cast}) does not match up with amount from DVSorder ({expected_num_ballots}).')
        return None
    
    matching_lines = [line.strip() for line in lines if target_line in line]

    times_list = []
    for line in matching_lines[-num_ballots_cast:]:
        times_list.append(line[12:20])
    print(f"successfully parsed machinecontext_1_{tabulator_id}_slog.txt")
    return times_list

def create_time_dictionary(expected_ballot_counts):
    log_file_times = {}
    for index in range(33, 621):
        try:
            log_file_times[index] = get_log_times(len(expected_ballot_counts[str(index)]), index)
            # if return is none, remove from dataset bc ballot counts between logs and DVSo didn't match up
            if not log_file_times[index]:
                log_file_times.pop(index)
        # we move on past UnicodeDecode errors in case the decoding failed
        except UnicodeDecodeError:
            print(f"SKIP: failed to decode log file: machinecontext_1_{index}_slog.txt")
            continue
        # we move past FileNotFound because the logs are oddly missing some files (eg 14)
        except FileNotFoundError:
            print(f"SKIP: log file not found: machinecontext_1_{index}_slog.txt")
            continue
        # we move past KeyError because DVSorder is oddly missing some tabulators (eg 38)
        except KeyError:
            print(f"SKIP: tabulator ID {index} not found in in DVSorder unscramble")
            continue
    return log_file_times

def main():
    # store SF_dict.json (which contains a dict with keys of tabIDs (strings) and vals of ordered vote lists)
    # form of SF_dict: {33: [[0,32435], [1,23423], [2,45645],etc], 34: [[0,57643], [1,97728], etc], etc}
    with open('SF_dict.json', 'r') as f:
        ordered_dict = json.load(f)
    print("ordered_dict successfully loaded")

    # create time_dict which is a dict of tabIds as keys and list of timestamps as vals
    # form: {33: ['07:11:01', '07:13:32', etc], 34: ['07:11:01', '07:13:32', etc], etc}
    time_dict = create_time_dictionary(ordered_dict)
    print("time_dictionary successfully created")
    # print(json.dumps(time_dict, indent=4))
    # print(time_dict[33])

    all_votes_by_time = []
    # loop through the ordered dictionary given to us by the DVSorder code
    for tab_id, orders in ordered_dict.items():
        votes_list = []
        # loop through the list of timestamps for each  
        try:
            for index, vote_time in enumerate(time_dict[int(tab_id)]):
                temp = {'voter_pos': index,
                        'voter_id': orders[index][1],
                        'time_of_vote': vote_time
                        }
                votes_list.append(temp)
            tabulator_dict = {
                'tab_id': tab_id,
                'votes': votes_list
            }
            all_votes_by_time.append(tabulator_dict)
        # there will be key errors bc not all DVSo tabulators end up in the time_dict, so just skip past 
        # Seemingly the skipped logs end up in it tho?? Need to look into that
        except KeyError:
            print(f"Skipping tabulator id {tab_id}")
            continue

    with open('all_votes_by_time.json', 'w') as f:
        json.dump(all_votes_by_time, f, indent=4)
    print("Final json successfully created")

main()
    # form = [
    #             {
    #                 'tab_id': 33,
    #                 'precinct': 1,
    #                 'votes': [
    #                     {'voter_pos': 0, 'voter_id':64732, 'time_of_vote':'11:22:21'},
    #                     {'voter_pos': 1, 'voter_id':64353, 'time_of_vote':'11:22:29'}
    #                 ]
    #             },
    #             {
    #                 'tab_id': 33,
    #                 'precinct': 1,
    #                 'votes': [
    #                     {'voter_pos': 0, 'voter_id':64732, 'time_of_vote':'11:22:21'},
    #                     {'voter_pos': 1, 'voter_id':64353, 'time_of_vote':'11:22:29'}
    #                 ]
    #             }
    #         ]
