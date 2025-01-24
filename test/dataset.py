import pandas as pd
import random
from datetime import datetime, timedelta

# Define constants
CYCLES = 1240
TASKS = [
    "WaitForPickObjectToComplete",
    "GetSensorType",
    "IsReady",
    "TransferTasksToRobot",
    "InternalRecognizeWithIteration",
    "StartOfCycle",
    "PerformHeightInitialization",
    "InitializeProductGroup",
    "PickObject",
]
TASK_DURATIONS = {
    "WaitForPickObjectToComplete": 16.1,
    "GetSensorType": 0,
    "IsReady": 0,
    "TransferTasksToRobot": 1.4,
    "InternalRecognizeWithIteration": 16.9,
    "StartOfCycle": 0,
    "PerformHeightInitialization": 121.5,
    "InitializeProductGroup": 3.4,
    "PickObject": 64.2,
}
ERROR_TYPES = ["None", "ConnectionError", "TimeoutError", "ValidationError"]

# Generate random dataset
data = []
start_date = datetime.now()
for cycle in range(1, CYCLES + 1):
    num_tasks = random.randint(5, 60)  # Random number of tasks per cycle
    cycle_date = start_date + timedelta(days=cycle - 1)  # Same date for all tasks in the cycle
    for _ in range(num_tasks):
        task = random.choices(
            TASKS, weights=[1, 1, 1, 10, 1, 1, 1, 1, 1], k=1
        )[0]  # TransferTasksToRobot appears most frequently
        start_time = cycle_date + timedelta(minutes=random.randint(0, 1440))  # Random start time within the day
        mean_duration = TASK_DURATIONS[task]  # Mean duration for the task
        random_variation = random.uniform(-mean_duration * 0.1, mean_duration * 0.1)  # 20% variation
        duration = max(0, mean_duration + random_variation)  # Ensure non-negative duration
        stop_time = start_time + timedelta(seconds=duration)
        errors = random.randint(0, 5)  # Random number of errors
        error_type = random.choice(ERROR_TYPES) if errors > 0 else "None"

        data.append({
            "Cycle": cycle,
            "Task": task,
            "Date": cycle_date.date(),
            "Start": start_time.time(),
            "Stop": stop_time.time(),
            "Errors": errors,
            "Errortype": error_type,
        })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV (optional)
df.to_csv("Data/dataset.csv", index=False)

# Display the first few rows
print(df.head())