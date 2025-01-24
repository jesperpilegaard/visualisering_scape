import pandas as pd

df = pd.read_csv("Data/df_with_fullcycle.csv")

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
df[['Cycle', 'Task', 'Start DateTime', 'End DateTime', 'Duration']].to_csv('Data/task_durations_fullcycle.csv', index=False)