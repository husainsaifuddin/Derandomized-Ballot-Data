import chardet

# encoding: Windows-1252

target_line = "[ScannerThread] INFO : [Scanner] Ballot cast"

with open('N20_BSM_Logs/machinecontext_1_33_slog1.txt', 'r', encoding="Windows-1252") as f:
    lines = f.read().splitlines()

matching_lines = [line.strip() for line in lines if target_line in line]

for line in matching_lines[-212:]:
    print(line)
print(f"num lines: {len(matching_lines)}" )