import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Indlæs data
logdata = pd.read_csv("Data/task_durations.csv")

# Fjern outliers, hvor Duration er over 200 sekunder
data = logdata[logdata['Duration'] <= 200]

# Streamlit-app
st.title("Logdata Visualizations")

# 2. Boxplot for Task Durations
st.subheader("Task Duration Boxplot")
fig2 = px.box(data,
              x='Task',
              y='Duration',
              labels={'Task': 'Task Type', 'Duration': 'Duration (seconds)'},
              title="Boxplot of Task Durations")
st.plotly_chart(fig2, use_container_width=True)

# 3. Task-specific Duration per Cycle
st.subheader("Duration per Cycle for Selected Task")
task_type = st.selectbox("Select a Task Type", data['Task'].unique())

filtered_logdata = data[data['Task'] == task_type]

fig3 = px.line(filtered_logdata,
               x='Cycle',
               y='Duration',
               labels={'Cycle': 'Cycle', 'Duration': 'Duration (seconds)'},
               title=f"Duration for {task_type} per Cycle")
st.plotly_chart(fig3, use_container_width=True)