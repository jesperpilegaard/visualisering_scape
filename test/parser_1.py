import re
import pandas as pd
from datetime import datetime

# Indstillinger
log_file = "Data/Full_run_scape run4.log"
output_file = "Data/df_with_fullcycle.csv"
timeformat = "%H-%M-%S.000"  # Format til sammenligning af tid
MyColumns = ['Cycle', 'Task', 'Time Start', 'Time End']  # Kolonne-navne

# Regular expressions
cycle_pattern = r"\*\*\* LogCounter: (\d+)  Time: .*? LOG_TIME_CODE: (\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2})"
task_pattern = r'ScapeDetailedTimingInfo for task \"(.*?)\":'
start_time_pattern = r"  Start Time: (\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}.\d{3})"
end_time_pattern = r"  End Time:   (\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}.\d{3})"
reset_stats_pattern = r"SCAPE_EC_API_COMMAND: EC_API_START_OF_CYCLE\s+RESET_STATS:\s+[01]\s+Time: (.+)"

# Initialiser variabler
log_data = []
current_cycle = None
full_cycle_start = None
reset_end_time = None

# Hjælpefunktion til at konvertere tiden fra RESET_STATS
def convert_reset_time(raw_time):
    try:
        # Konverter tiden fra linjen med RESET_STATS
        dt = datetime.strptime(raw_time, "%a %b %d %H:%M:%S %Y")  # Format fra RESET_STATS
        return dt.strftime("%Y-%m-%d %H-%M-%S.000")  # Kombiner dato og tid
    except ValueError:
        return None

# Læs filen linje for linje
with open(log_file, "r") as file:
    for line in file:
        # Match starten af en cyklus
        cycle_match = re.search(cycle_pattern, line)
        if cycle_match:
            # Hvis der er en igangværende cyklus, tilføj FullCycle
            if current_cycle is not None and full_cycle_start is not None and reset_end_time is not None:
                log_data.append({
                    "Cycle": current_cycle,
                    "Task": "FullCycle",
                    "Time Start": f"{current_date} {full_cycle_start}",
                    "Time End": f"{current_date} {reset_end_time}",
                })
            # Start en ny cyklus
            current_cycle = int(cycle_match.group(1))
            current_date = cycle_match.group(2).split(" ")[0]
            full_cycle_start = cycle_match.group(2).split(" ")[1] + ".000"  # Tilføj .000 til starten
            reset_end_time = None  # Nulstil sluttid for FullCycle
            continue

        # Match task
        task_match = re.search(task_pattern, line)
        if task_match:
            current_task = task_match.group(1)
            start_time = None
            end_time = None
            continue

        # Match starttid
        start_match = re.search(start_time_pattern, line)
        if start_match:
            start_time = start_match.group(1)
            continue

        # Match sluttid
        end_match = re.search(end_time_pattern, line)
        if end_match:
            end_time = end_match.group(1)
            # Gem data for tasken
            if current_cycle is not None and current_task:
                log_data.append({
                    "Cycle": current_cycle,
                    "Task": current_task,
                    "Time Start": start_time,
                    "Time End": end_time,
                })
            continue

        # Match RESET_STATS-tid
        reset_match = re.search(reset_stats_pattern, line)
        if reset_match:
            raw_reset_time = reset_match.group(1)
            reset_end_time = convert_reset_time(raw_reset_time)  # Konverter til task-tidsformat
            print(f"Reset Time Found: {reset_end_time}")  # Debugging print for RESET_STATS
            continue

# Tilføj den sidste "FullCycle", hvis der stadig er en igangværende cyklus
if current_cycle is not None and full_cycle_start is not None and reset_end_time is not None:
    print(f"Adding FullCycle: {current_cycle}, {full_cycle_start}, {reset_end_time}")  # Debugging print for FullCycle
    log_data.append({
        "Cycle": current_cycle,
        "Task": "FullCycle",
        "Time Start": f"{current_date} {full_cycle_start}",
        "Time End": f"{current_date} {reset_end_time}",
    })

# Opret DataFrame
df = pd.DataFrame(log_data)

# Fjern Date-kolonnen, hvis den findes
df = df.drop(columns=['Date'], errors='ignore')

# Gem som CSV
df.to_csv(output_file, index=False)

# Vis DataFrame
print(df.head())