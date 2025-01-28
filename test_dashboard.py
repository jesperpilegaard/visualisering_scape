import streamlit as st
import plotly.express as px
from streamlit_plotly_events import plotly_events
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Logdata Visualization", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Logdata Visualization")
st.info("The purpose of this dashboard is to gain deeper insights into a robot's performance. We get insights into the various tasks as well as error messages, and users can take a closer look at individual cycles and tasks. Additionally, you can view the images the robot has taken during a task by clicking on the line chart. Furthermore, it is possible to compare cycles and dates with each other. This dashboard is created with synthetic data solely for demonstration purposes. Therefore, the data is "cleaner" than it would have been with the real data.")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# Arbejdsmappen sættes automatisk af din Streamlit app
os.chdir(os.path.dirname(__file__))  # Skift til mappen hvor scriptet ligger

st.sidebar.image("images/Scape Logo + payoff and without backgroud.png", use_container_width=True)

# Drop files
st.sidebar.header("Upload data: ")

fl = st.sidebar.file_uploader(":file_folder: Upload a file", type=(["csv"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(fl, encoding="ISO-8859-1")  # Læs direkte fra fil-uploader objektet
else:
    df = pd.read_csv("Data/sorted_data.csv", encoding="ISO-8859-1")  # Brug relativ sti til standardfil

task_distribution = df['Task'].value_counts().reset_index()
task_distribution.columns = ['Task', 'Count']

# Fjern outliers, hvor Duration er over 200 sekunder
data = df[df['Duration'] <= 20000000]

# Beregn gennemsnitstid per task type
mean_times = data.groupby('Task')['Duration'].mean().reset_index()
mean_times.rename(columns={'Duration': 'Mean Duration'}, inplace=True)

# Sidebar
st.sidebar.header("Choose your filter: ")
cycle = st.sidebar.multiselect("Pick your Cycle", data["Cycle"].unique())
if not cycle:
    data2 = data.copy()
else:
    data2 = data[data["Cycle"].isin(cycle)]

task = st.sidebar.multiselect("Pick your Task", data2["Task"].unique())
if not task:
    data3 = data2.copy()
else:
    data3 = data2[data2["Task"].isin(task)]

# Check if the filtered dataset is empty
if data3.empty:
    st.warning("No data available for the selected filters. Please adjust your filters.")

col1, col2 = st.columns((2))

# Beregn fordelingen af opgaver
with col1:
    # 4. Lagkagediagram for Task Distribution
    st.subheader("Task Distribution")
    filtered_task_distribution = data3['Task'].value_counts().reset_index()
    filtered_task_distribution.columns = ['Task', 'Count']
    fig3 = px.pie(filtered_task_distribution,
              names='Task',
              values='Count',
              title="Task Distribution",
              labels={'Task': 'Task Type', 'Count': 'Frequency'})
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("<p style='text-align: left; margin-top: -15px;'>This pie chart shows the distribution of different tasks in the dataset. The size of each slice indicates the frequency of the task. Choose filters to see the distribution in specific cycles or look into specific tasks.</p>", unsafe_allow_html=True)

with col2:
    # Create the pie chart using Plotly
    st.subheader("Error Type Distribution")
    filtered_error_distribution = data3['ErrorType'].value_counts().reset_index()
    filtered_error_distribution.columns = ['ErrorType', 'Count']
    filtered_error_distribution = filtered_error_distribution[filtered_error_distribution['ErrorType'] != '[]']
    fig = px.pie(filtered_error_distribution,
        names='ErrorType',
        values='Count',
        title="Error Type Distribution",
        labels={'Error Type': 'Error Type', 'Count': 'Frequency'})
    st.plotly_chart(fig, use_container_width=True)
    st.caption("<p style='text-align: left; margin-top: -15px; margin-bottom: 39px;'>This pie chart visualizes the distribution of different error types recorded in the dataset. Each slice represents the frequency of a specific error type.</p>", unsafe_allow_html=True)

with col1:
    # 1. Mean Time per Task Type
    st.subheader("Mean Time per Task Type")
    filtered_mean_times = data3.groupby('Task')['Duration'].mean().reset_index()
    filtered_mean_times.rename(columns={'Duration': 'Mean Duration'}, inplace=True)
    fig1 = px.bar(filtered_mean_times,
                x='Task',
                y='Mean Duration',
                labels={'x': 'Task Type', 'y': 'Mean Duration (seconds)'},
                title="Mean Time per Task Type")
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("<p style='text-align: left; margin-top: -15px;'>This bar chart shows the average time taken to complete each task type. Use it to identify tasks with longer durations. Choose filters to see the mean time in specific cycles and/or look into specific tasks.</p>", unsafe_allow_html=True)

with col2:
    # 2. Boxplot for Task Durations
    st.subheader("Task Duration Boxplot")
    fig2 = px.box(data3,
                x='Task',
                y='Duration',
                labels={'Task': 'Task Type', 'Duration': 'Duration (seconds)'},
                title="Boxplot of Task Durations")
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("<p style='text-align: left; margin-top: -15px;'>This boxplot illustrates the distribution of task durations for each task type. It highlights the variability and potential outliers in durations. Choose filters to see the plot for specific cycles and/or look into specific tasks.</p>", unsafe_allow_html=True)

# Line chart for duration per cycle for a selected task
st.subheader("Duration per Cycle for Selected Task")
task_type = st.selectbox("Select a Task Type", df['Task'].unique(), index=list(df['Task'].unique()).index("FullCycle") if "FullCycle" in df['Task'].unique() else 0)

filtered_logdata = df[df['Task'] == task_type]

if filtered_logdata.empty:
    st.warning(f"No data available for the selected task: {task_type}")
else:
    # Create line chart with Plotly and enable click events
    fig4 = px.line(
        filtered_logdata,
        x='Cycle',
        y='Duration',
        labels={'Cycle': 'Cycle', 'Duration': 'Duration (seconds)'},
        title=f"Duration for {task_type} per Cycle"
    )
    fig4.update_traces(mode="markers+lines", hovertemplate="Cycle: %{x}<br>Duration: %{y}")

    # Use `plotly_events` to capture click data
    selected_points = plotly_events(fig4, click_event=True, hover_event=False, select_event=False)
    
    # Display selected cycle
    if selected_points:
        selected_cycle = int(selected_points[0]["x"])  # Get cycle from clicked point
        st.subheader(f"Images for Cycle {selected_cycle}")

        # Function to show images for the selected cycle
        def show_images_for_cycle(cycle):
            cycle_data = df[df['Cycle'] == cycle]
            if 'LoggedImageFiles' in cycle_data.columns:
                logged_images = cycle_data['LoggedImageFiles'].iloc[-1]
                if pd.notna(logged_images):
                    image_files = [image.strip() for image in logged_images.split(',')]
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    image_dir = os.path.join(script_dir, 'images')
                    for image_file in image_files:
                        image_path = os.path.join(image_dir, image_file)
                        if os.path.exists(image_path):
                            st.image(image_path, caption=image_file, use_container_width=True)
                        else:
                            st.warning(f"Image file {image_file} was not found.")
                else:
                    st.warning("No images found for this cycle.")
            else:
                st.warning("No image data available for this cycle.")

        # Display images for the selected cycle
        show_images_for_cycle(selected_cycle)
    else:
        st.info("Click a point in the chart to view images for the corresponding cycle.")

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

data["DateTime"] = pd.to_datetime(data["Start DateTime"])  # Konverter til datetime
data["Date"] = data["DateTime"].dt.date  # Ekstraher dato

st.sidebar.subheader("Compare Tasks Across Two Time Intervals:")

st.sidebar.subheader("Compare Tasks Across Two Time Intervals:")

# Multiselect for picking tasks
selected_tasks = st.sidebar.multiselect("Select tasks for comparison", data["Task"].unique(), default=["FullCycle"])

# Extract available dates from the dataset
available_dates = data["Date"].unique()
available_dates.sort()  # Sortér datoerne

# Date pickers for selecting two dates
st.sidebar.subheader("Select Dates for Comparison")
selected_date_1 = st.sidebar.selectbox("Pick Date 1 for comparison", options=available_dates)
selected_date_2 = st.sidebar.selectbox("Pick Date 2 for comparison", options=available_dates)

# Time interval 1 selection
st.sidebar.subheader("Time Interval 1")
start_time_1 = st.sidebar.time_input("Start time (Interval 1)", value=pd.Timestamp("00:00:00").time())
end_time_1 = st.sidebar.time_input("End time (Interval 1)", value=pd.Timestamp("12:00:00").time())

# Time interval 2 selection
st.sidebar.subheader("Time Interval 2")
start_time_2 = st.sidebar.time_input("Start time (Interval 2)", value=pd.Timestamp("12:00:00").time())
end_time_2 = st.sidebar.time_input("End time (Interval 2)", value=pd.Timestamp("23:59:59").time())

# Validate time intervals
if start_time_1 >= end_time_1 or start_time_2 >= end_time_2:
    st.warning("End time must be after start time for both intervals.")
else:
    # Combine date with time intervals for both selected dates
    start_datetime_1 = pd.Timestamp.combine(selected_date_1, start_time_1)
    end_datetime_1 = pd.Timestamp.combine(selected_date_1, end_time_1)
    start_datetime_2 = pd.Timestamp.combine(selected_date_2, start_time_2)
    end_datetime_2 = pd.Timestamp.combine(selected_date_2, end_time_2)

    # Filter data for each time interval and date
    filtered_data_1 = data[
        (data["Task"].isin(selected_tasks)) &
        (data["DateTime"] >= start_datetime_1) & 
        (data["DateTime"] <= end_datetime_1) &
        (data["Date"] == selected_date_1)  # Add date filter
    ]
    filtered_data_2 = data[
        (data["Task"].isin(selected_tasks)) &
        (data["DateTime"] >= start_datetime_2) &
        (data["DateTime"] <= end_datetime_2) &
        (data["Date"] == selected_date_2)  # Add date filter
    ]

    # Check if there is data for both intervals
    if filtered_data_1.empty or filtered_data_2.empty:
        st.warning("No data available for one or both time intervals.")
    else:
        # Calculate the mean duration for each task and interval
        mean_duration_1 = filtered_data_1.groupby(["Task"])["Duration"].mean().reset_index()
        mean_duration_1["Interval"] = f"Interval 1 ({selected_date_1})"  # Label for interval 1

        mean_duration_2 = filtered_data_2.groupby(["Task"])["Duration"].mean().reset_index()
        mean_duration_2["Interval"] = f"Interval 2 ({selected_date_2})"  # Label for interval 2

        # Combine the two dataframes
        comparison_data = pd.concat([mean_duration_1, mean_duration_2])

        # Create the bar chart
        fig8 = px.bar(
            comparison_data,
            x="Task",  # X-axis as the task
            y="Duration",  # Y-axis as the mean duration
            color="Interval",  # Color bars by interval
            barmode="group",  # Group bars by task and interval
            title=f"Average Task Duration Comparison ({selected_date_1} vs {selected_date_2})",
            labels={"Task": "Task Type", "Duration": "Average Duration (seconds)", "Interval": "Time Interval"},
        )

        # Show the plot
        st.plotly_chart(fig8, use_container_width=True)
