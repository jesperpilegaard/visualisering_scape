import pandas as pd
from datetime import timedelta

# Indlæs CSV-filen
file_path = "Data/run_scape_logdata_df_cleaned.csv"  # Skift til din filsti
df = pd.read_csv(file_path)

# Sørg for, at "Start" og "Stop" har millisekunder
df['Start'] = df['Start'].apply(lambda x: f"{x}.000" if len(str(x)) == 8 else str(x))
df['Stop'] = df['Stop'].apply(lambda x: f"{x}.000" if len(str(x)) == 8 else str(x))

# Beregn varighed
df['Duration'] = pd.to_datetime(df['Stop'], format='%H:%M:%S.%f') - pd.to_datetime(df['Start'], format='%H:%M:%S.%f')

# Juster for negative tider
df['Duration'] = df['Duration'].apply(lambda x: x + timedelta(days=1) if x < timedelta(0) else x)

# Flyt kolonnen mellem 'Stop' og 'Errors'
columns = list(df.columns)
columns.insert(columns.index('Errors'), 'Duration')
df = df[columns]

# Gem den nye fil
output_file_path = "Data/output_med_duration.csv"  # Skift til ønsket output-filnavn
df.to_csv(output_file_path, index=False)

print(f"Filen er gemt som: {output_file_path}")