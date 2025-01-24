# README

## Overview

This project consists of two Python scripts: `test_dashboard.py` and `combined_parser.py`. Together, they allow you to process log files and visualize the resulting statistics in a Streamlit-based dashboard.

---

## Requirements

Before running the scripts, ensure that the following requirements are met:

1. **Python Version**  
   Make sure Python 3.x is installed on your system.

2. **Dependencies**  
   Install the necessary Python packages by running:  
   ```bash
   pip install -r requirements.txt


## Instructions

The Streamlit app (test_dashboard.py) provides a dashboard to visualize your statistics. Follow these steps to run it locally:

1. Open a terminal in the project directory.

2. Run the following command:
streamlit run test_dashboard.py

3. A browser window should open automatically, displaying the app. If not, follow the link provided in the terminal.

## Parsing a new log file

If you have a new log file that needs to be processed before displaying its statistics in the dashboard, use the combined_parser.py script:

1. Place your new log file in the designated directory (update the script if necessary to point to your file's location).

2. Run the parser with the following command:
python combined_parser.py

3. Once processed, the new data will be ready to view in the Streamlit app.

## Notes

- Ensure that your log files are in the correct format to be processed by combined_parser.py.

- Make sure to rerun the Streamlit app (test_dashboard.py) after parsing new log files to update the displayed data.
