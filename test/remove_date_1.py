import pandas as pd

# Indlæs CSV-filen
file_path = "C:\\Users\\student\Visualisering Scape\Data\df_with_fullcycle.csv"  # Erstat med stien til din CSV-fil
df = pd.read_csv(file_path)

# Fjern dobbelte datoer i "Time End"-kolonnen
if "Time End" in df.columns:
    df["Time End"] = df["Time End"].str.replace(r"(\d{4}-\d{2}-\d{2}) \1", r"\1", regex=True)

# Gem det opdaterede DataFrame tilbage til en ny CSV-fil
output_file_path = "df_with_fullcycle.csv"  # Erstat med ønsket output-sti
df.to_csv(output_file_path, index=False)

print(f"Filen er opdateret og gemt som {output_file_path}")
