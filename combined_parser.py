import re
import pandas as pd
from datetime import datetime

# Indstillinger
log_file = "Data/Full_run_scape run4.log"
output_file = "Data/test_logdata.csv"
timeformat = "%H-%M-%S.000"  # Format til sammenligning af tid
MyColumns = ['Cycle', 'Task', 'Time Start', 'Time End']  # Kolonne-navne

# Regular expressions
cycle_pattern = r"\*\*\* LogCounter: (\d+)  Time: .*? LOG_TIME_CODE: (\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2})"
task_pattern = r'ScapeDetailedTimingInfo for task \"(.*?)\":'
start_time_pattern = r"  Start Time: (\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}.\d{3})"
end_time_pattern = r"  End Time:   (\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}.\d{3})"
reset_stats_pattern = r"SCAPE_EC_API_COMMAND: EC_API_START_OF_CYCLE\s+RESET_STATS:\s+[01]\s+Time: (.+)"
error_pattern = r"IPL_ERROR: Exception: (\d+)\s+(.*)"
image_file_pattern = r"(\d+_\d+_recog_cam\d+_pz\d+_sz\d+\.png)"

# Initialiser variabler
log_data = []
current_cycle = None
full_cycle_start = None
reset_end_time = None
current_error = []
image_files = set()

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
        # Match errors først
        error_match = re.search(error_pattern, line)
        if error_match:
            current_error = error_match.group(1)  # Gem kun fejlkoden
            print(f"Error code matched: {current_error}")  # Debugging print
            continue

        # Match starten af en cyklus
        cycle_match = re.search(cycle_pattern, line)
        if cycle_match:
            if current_cycle is not None and full_cycle_start is not None and reset_end_time is not None:
                log_data.append({
                    "Cycle": current_cycle,
                    "Task": "FullCycle",
                    "Time Start": f"{current_date} {full_cycle_start}",
                    "Time End": f"{current_date} {reset_end_time}",
                    "ErrorType": [],
                    "LoggedImageFiles": ','.join(image_files)
                })
            current_cycle = int(cycle_match.group(1))
            current_date = cycle_match.group(2).split(" ")[0]
            full_cycle_start = cycle_match.group(2).split(" ")[1] + ".000"
            reset_end_time = None
            image_files = set()
            current_error = None  # Nulstil fejl ved ny cyklus
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
            if current_cycle is not None and current_task:
                log_data.append({
                    "Cycle": current_cycle,
                    "Task": current_task,
                    "Time Start": start_time,
                    "Time End": end_time,
                    "ErrorType": current_error,  # Gem fejl for tasken
                    "LoggedImageFiles": ','.join(image_files)
                })
            # Nulstil fejl efter tasken er gemt
            current_error = None
            continue

        # Match RESET_STATS-tid
        reset_match = re.search(reset_stats_pattern, line)
        if reset_match:
            raw_reset_time = reset_match.group(1)
            reset_end_time = convert_reset_time(raw_reset_time)
            continue

        # Match billedfiler
        image_file_match = re.search(image_file_pattern, line)
        if image_file_match:
            image_files.add(image_file_match.group(1))
            continue

# Tilføj den sidste "FullCycle", hvis der stadig er en igangværende cyklus
if current_cycle is not None and full_cycle_start is not None and reset_end_time is not None:
    print(f"Adding FullCycle: {current_cycle}, {full_cycle_start}, {reset_end_time}")  # Debugging print for FullCycle
    log_data.append({
        "Cycle": current_cycle,
        "Task": "FullCycle",
        "Time Start": f"{current_date} {full_cycle_start}",
        "Time End": f"{current_date} {reset_end_time}",
        "ErrorType": None,
        "LoggedImageFiles": ','.join(image_files)
    })

# Opret DataFrame og gem som CSV
df = pd.DataFrame(log_data)

# Fjern Date-kolonnen, hvis den findes
df = df.drop(columns=['Date'], errors='ignore')

df.to_csv(output_file, index=False)

# Indlæs CSV-filen
df = pd.read_csv(output_file)

# Fjern dobbelte datoer i "Time End"-kolonnen
if "Time End" in df.columns:
    df["Time End"] = df["Time End"].str.replace(r"(\d{4}-\d{2}-\d{2}) \1", r"\1", regex=True)

# Kombiner dato og tid til datetime-objekter
df['Start DateTime'] = pd.to_datetime(df['Time Start'], format='%Y-%m-%d %H-%M-%S.%f')
df['End DateTime'] = pd.to_datetime(df['Time End'], format='%Y-%m-%d %H-%M-%S.%f', errors='coerce')

# Håndter tilfælde, hvor Time End er mindre end Time Start
df['End DateTime'] = df.apply(
    lambda row: row['End DateTime'] if row['End DateTime'] >= row['Start DateTime'] 
    else row['End DateTime'] + pd.Timedelta(days=1), 
    axis=1
)

# Beregn varighed
df['Duration'] = (df['End DateTime'] - df['Start DateTime']).dt.total_seconds()

# Gem til ny CSV-fil
df[['Cycle', 'Task', 'Start DateTime', 'End DateTime', 'Duration', 'ErrorType', 'LoggedImageFiles']].to_csv('Data/test_logdata.csv', index=False)

print(f"Filen er opdateret og gemt som test_logdata.csv")