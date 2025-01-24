import streamlit as st
import pandas as pd
import altair as alt

class MyClass:
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

if "my_instance" not in st.session_state:
    st.session_state.my_instance = MyClass("foo", "bar")

st.write(isinstance(st.session_state.my_instance, MyClass))



st.button("Rerun")

# Load data
df = pd.read_csv("Data/dataset.csv")

# Streamlit app title
st.title("Logdata Visualization")

# Sidebar for filtering
tasks = st.sidebar.multiselect("Select Tasks to View", options=df["Task"].unique(), default=df["Task"].unique())
date_range = st.sidebar.date_input("Select Date Range", [df["Date"].min(), df["Date"].max()])

# Filter data
df_filtered = df[df["Task"].isin(tasks)]
df_filtered = df_filtered[(df_filtered["Date"] >= str(date_range[0])) & (df_filtered["Date"] <= str(date_range[1]))]

# Visualization 1: Task frequency by cycle
st.subheader("Task Frequency by Cycle")
chart1 = alt.Chart(df_filtered).mark_bar().encode(
    x="Cycle:N",
    y="count():Q",
    color="Task:N",
    tooltip=["Task", "count()"]
).properties(height=400, width=700)
st.altair_chart(chart1, use_container_width=True)

# Visualization 2: Error types distribution
st.subheader("Error Types Distribution")
chart2 = alt.Chart(df_filtered).mark_bar().encode(
    x="Errortype:N",
    y="count():Q",
    color="Errortype:N",
    tooltip=["Errortype", "count()"]
).properties(height=400, width=700)
st.altair_chart(chart2, use_container_width=True)

# Visualization 3: Duration by task
st.subheader("Average Duration by Task")
df_filtered["Duration"] = (pd.to_datetime(df_filtered["Stop"], format="%H:%M:%S") - pd.to_datetime(df_filtered["Start"], format="%H:%M:%S")).dt.total_seconds()
chart3 = alt.Chart(df_filtered).mark_bar().encode(
    x="Task:N",
    y="mean(Duration):Q",
    color="Task:N",
    tooltip=["Task", "mean(Duration)"]
).properties(height=400, width=700)
st.altair_chart(chart3, use_container_width=True)

# Visualization 4: Errors by cycle
st.subheader("Total Errors by Cycle")
chart4 = alt.Chart(df_filtered).mark_line(point=True).encode(
    x="Cycle:N",
    y="sum(Errors):Q",
    tooltip=["Cycle", "sum(Errors)"]
).properties(height=400, width=700)
st.altair_chart(chart4, use_container_width=True)

# Visualization 5: Task occurrence over time
st.subheader("Task Occurrence Over Time")
chart5 = alt.Chart(df_filtered).mark_area().encode(
    x="Date:T",
    y="count():Q",
    color="Task:N",
    tooltip=["Date", "count()"]
).properties(height=400, width=700)
st.altair_chart(chart5, use_container_width=True)

# Visualization 6: Error count by task
st.subheader("Error Count by Task")
chart6 = alt.Chart(df_filtered).mark_bar().encode(
    x="Task:N",
    y="sum(Errors):Q",
    color="Task:N",
    tooltip=["Task", "sum(Errors)"]
).properties(height=400, width=700)
st.altair_chart(chart6, use_container_width=True)

# Visualization 7: Task duration distribution
st.subheader("Task Duration Distribution")
chart7 = alt.Chart(df_filtered).mark_boxplot().encode(
    x="Task:N",
    y="Duration:Q",
    color="Task:N",
    tooltip=["Task"]
).properties(height=400, width=700)
st.altair_chart(chart7, use_container_width=True)

# Visualization 8: Task start time heatmap
st.subheader("Task Start Time Heatmap")
df_filtered["Start Hour"] = pd.to_datetime(df_filtered["Start"], format="%H:%M:%S").dt.hour
chart8 = alt.Chart(df_filtered).mark_rect().encode(
    x="Start Hour:O",
    y="Task:N",
    color="count():Q",
    tooltip=["Start Hour", "Task", "count()"]
).properties(height=400, width=700)
st.altair_chart(chart8, use_container_width=True)

# Visualization 9: Errors over time
st.subheader("Errors Over Time")
chart9 = alt.Chart(df_filtered).mark_line(point=True).encode(
    x="Date:T",
    y="sum(Errors):Q",
    tooltip=["Date", "sum(Errors)"]
).properties(height=400, width=700)
st.altair_chart(chart9, use_container_width=True)

# Visualization 10: Task proportion
st.subheader("Task Proportion")
chart10 = alt.Chart(df_filtered).mark_pie().encode(
    theta="count():Q",
    color="Task:N",
    tooltip=["Task", "count()"]
).properties(height=400, width=700)
st.altair_chart(chart10, use_container_width=True)


st.write("### Thank you for using the Logdata Visualization app!")
