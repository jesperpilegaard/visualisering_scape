import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Logdata Visualization", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Logdata Visualization")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

st.sidebar.image(r"C:\Users\student\Visualisering Scape\Scape Logo + payoff and without backgroud.png", use_container_width=True)

# Drop files
st.sidebar.header("Upload data: ")

fl = st.sidebar.file_uploader(":file_folder: Upload a file", type=(["csv"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"C:\Users\student\Visualisering Scape\Data")
    df = pd.read_csv("task_durations_fullcycle.csv", encoding = "ISO-8859-1")

# Fjern outliers, hvor Duration er over 200 sekunder
data = df[df['Duration'] <= 20000000]

st.sidebar.subheader("Compare Cycles: ")
cycle = st.sidebar.multiselect("Pick up to 2 Cycles for Comparison", data["Cycle"].unique(), max_selections=2)

if len(cycle) == 0:
    st.warning("Please select at least one cycle for comparison.")
elif len(cycle) == 1:
    st.info("Select one more cycle for comparison, or continue with a single selection.")
    data_comparison = data[data["Cycle"].isin(cycle)]
    st.subheader(f"Visualization for Cycle: {cycle[0]}")

    # Define a color map for tasks to ensure consistent colors across charts
    task_colors = {task: f'rgba({(i * 50) % 255}, {(i * 100) % 255}, {(i * 150) % 255}, 0.8)' for i, task in enumerate(data_comparison['Task'].unique())}

    fig_single = px.bar(
        data_comparison,
        x="Task",
        y="Duration",
        color="Task",
        title=f"Task Duration for Cycle {cycle[0]}",
        labels={"Task": "Task Type", "Duration": "Duration (seconds)"},
        color_discrete_map=task_colors
    )
    st.plotly_chart(fig_single, use_container_width=True)
elif len(cycle) == 2:
    # Filter data for each cycle
    data_cycle1 = data[data["Cycle"] == cycle[0]]
    data_cycle2 = data[data["Cycle"] == cycle[1]]

    # Find the maximum y value for both cycles to set a common y-axis range
    max_y_value = max(data_cycle1['Duration'].max(), data_cycle2['Duration'].max())

    # Define a color map for tasks to ensure consistent colors across charts
    task_colors = {task: f'rgba({(i * 50) % 255}, {(i * 100) % 255}, {(i * 150) % 255}, 0.8)' for i, task in enumerate(data_cycle1['Task'].unique())}

    # Create side-by-side columns for comparison
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Task Duration for Cycle {cycle[0]}")
        fig_cycle1 = px.bar(
            data_cycle1,
            x="Task",
            y="Duration",
            color="Task",
            title=f"Task Duration for Cycle {cycle[0]}",
            labels={"Task": "Task Type", "Duration": "Duration (seconds)"},
            color_discrete_map=task_colors  # Use the same color map for both charts
        )
        # Set the y-axis range for the first chart
        fig_cycle1.update_layout(yaxis_range=[0, max_y_value])
        st.plotly_chart(fig_cycle1, use_container_width=True)

    with col2:
        st.subheader(f"Task Duration for Cycle {cycle[1]}")
        fig_cycle2 = px.bar(
            data_cycle2,
            x="Task",
            y="Duration",
            color="Task",
            title=f"Task Duration for Cycle {cycle[1]}",
            labels={"Task": "Task Type", "Duration": "Duration (seconds)"},
            color_discrete_map=task_colors  # Use the same color map for both charts
        )
        # Set the y-axis range for the second chart
        fig_cycle2.update_layout(yaxis_range=[0, max_y_value])
        st.plotly_chart(fig_cycle2, use_container_width=True)