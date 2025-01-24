import re
import pandas as pd

# Logfil placering
log_file = "Data/run_scape.log"

# Regular expressions til at matche tasks og errors
task_pattern = r'ScapeDetailedTimingInfo for task "([^"]+)"'
error_pattern = r"IPL_ERROR:\s+(.+)"

# Initialiser variabler
task_counts = {}  # Antal gange hver task er i brug
task_error_counts = {}  # Antal fejl per task
total_tasks = 0  # Total antal tasks i logfilen
current_task = None  # Initialiser med None, så vi kan håndtere tilfælde uden task

# Læs logfilen
with open(log_file, "r") as file:
    for line in file:
        # Find tasknavn
        task_match = re.search(task_pattern, line)
        if task_match:
            current_task = task_match.group(1)  # Gem den aktuelle task
            if current_task not in task_counts:
                task_counts[current_task] = 0
                task_error_counts[current_task] = 0
            task_counts[current_task] += 1  # Tæl antallet af gange tasken vises
            total_tasks += 1  # Samlet antal tasks

        # Find errors og tilføj til den aktuelle task, hvis task er defineret
        if current_task:
            error_match = re.search(error_pattern, line)
            if error_match:
                task_error_counts[current_task] += 1  # Tæl fejl for den aktuelle task

# Beregn fejlprocent for hver task i forhold til, hvor mange gange tasken er kørt
task_data = []
for task in task_counts:
    total_task_count = task_counts[task]
    total_task_errors = task_error_counts[task]
   
    # Beregn fejlprocenten for den aktuelle task
    if total_task_count > 0:
        task_error_percentage = (total_task_errors / total_task_count)
    else:
        task_error_percentage = 0

    task_data.append([task, total_task_count, total_task_errors, task_error_percentage])

# Konverter til DataFrame
task_error_df = pd.DataFrame(task_data, columns=["Task", "Task Count", "Error Count", "Mean Error per Task"])

# Sorter efter fejlprocent
task_error_df = task_error_df.sort_values(by="Mean Error per Task", ascending=False).reset_index(drop=True)

# Gem til CSV (valgfrit)
task_error_df.to_csv("Data/task_error_counts.csv", index=False)

# Print DataFrame
print(task_error_df)