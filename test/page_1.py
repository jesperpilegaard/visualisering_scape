import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from collections import Counter

# Indlæs data
logdata = pd.read_csv("Data/task_durations.csv")
error_data = pd.read_csv("Data/task_error_counts.csv")
error_df = pd.read_csv("Data/output_med_duration.csv")

# Fjern outliers, hvor Duration er over 200 sekunder
data = logdata[logdata['Duration'] <= 200]

# Beregn gennemsnitstid per task type
mean_times = logdata.groupby('Task')['Duration'].mean().reset_index()
mean_times.rename(columns={'Duration': 'Mean Duration'}, inplace=True)

# Beregn gennemsnitlige fejl per task type
mean_errors = error_data.groupby('Task')['Mean Error per Task'].mean().reset_index()

# Slå datasæt sammen
merged_df = pd.merge(mean_times, mean_errors, on='Task')

# Beregn korrelationen mellem Mean Duration og Mean Error
correlation = merged_df[['Mean Duration', 'Mean Error per Task']].corr()

# Streamlit-app
st.title("Logdata Visualizations")

# Beregn fordelingen af opgaver
task_distribution = logdata['Task'].value_counts().reset_index()
task_distribution.columns = ['Task', 'Count']

# 4. Lagkagediagram for Task Distribution
st.subheader("Task Distribution")
fig3 = px.pie(task_distribution,
              names='Task',
              values='Count',
              title="Task Distribution",
              labels={'Task': 'Task Type', 'Count': 'Frequency'})
st.plotly_chart(fig3, use_container_width=True)

# Handle possible NaN values and split the 'Error Types' column
error_types = error_df['Error Types'].dropna().astype(str).apply(lambda x: x.split(','))

# Flatten the list of error types
flat_error_types = [item for sublist in error_types for item in sublist]

# Count the occurrences of each error type
error_counts = pd.Series(flat_error_types).value_counts().reset_index()
error_counts.columns = ['Error Type', 'Count']

# Create the pie chart using Plotly
st.subheader("Error Type Distribution")
fig = px.pie(error_counts,
             names='Error Type',
             values='Count',
             title="Error Type Distribution",
             labels={'Error Type': 'Error Type', 'Count': 'Frequency'})

# Show the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# 4. Lagkagediagram for Error Types
#st.subheader("Error Type Distribution")
#fig3 = px.pie(task_distribution,
#              names='Error',
#              values='Count',
#              title="Error Distribution",
#              labels={'Error': 'Error Type', 'Count': 'Frequency'})
#st.plotly_chart(fig3, use_container_width=True)

# 1. Mean Time per Task Type
st.subheader("Mean Time per Task Type")
fig1 = px.bar(mean_times,
              x='Task',
              y='Mean Duration',
              labels={'x': 'Task Type', 'y': 'Mean Duration (seconds)'},
              title="Mean Time per Task Type")
st.plotly_chart(fig1, use_container_width=True)

# 2. Mean Errors per Task Type
st.subheader("Mean Errors per Task Type")
fig2 = px.bar(mean_errors,
              x='Task',
              y='Mean Error per Task',
              labels={'x': 'Task Type', 'y': 'Mean Errors'},
              title="Mean Errors per Task Type")
st.plotly_chart(fig2, use_container_width=True)

# 3. Korrelation mellem Mean Time og Mean Errors
st.subheader("Correlation between Mean Time and Mean Errors")
st.write("Correlation Matrix:")
st.write(correlation)