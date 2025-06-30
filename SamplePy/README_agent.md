# Project README

## Project Overview

This project consists of a group of Python scripts located in the `SamplePy` directory. Each script handles specific tasks related to database operations, data processing, and visualization, particularly focused around wars and countries involved in those wars.

## File Descriptions

1. **NormalizeCountries.py:**
   - This script processes lists of countries involved in wars, maps them to canonical names using a mapping table, and categorizes them as aggressors or defenders. It performs data manipulation on a DataFrame, saves the results to a database, and generates CSV files for further analysis.

2. **analyze_import2.py:**
   - This script compares data from a CSV file and a SQLite database, focusing on identifying unique and duplicate war names. It validates data integrity between these two sources by checking for discrepancies and duplicates.

3. **database_operations.py:**
   - Provides functions for basic operations on a SQLite database such as resetting tables, deleting duplicates, inserting entries, and fetching wars or participants from the database.

4. **wars_barchartrace.py:**
   - Utilizes the `bar_chart_race` library to create animations that visualize changes in data over time. Specifically, it visualizes the participation of countries in wars using data from a CSV file.

## Setup and Installation

To work with these scripts, it is important to have Python and the necessary packages installed. These packages include:
- pandas
- sqlite3
- bar_chart_race
- csv

You can install the required Python packages using pip:
```bash
pip install pandas sqlite3 bar_chart_race
```

## Usage

- **Data Analysis and Processing:**
  - Run `NormalizeCountries.py` to normalize, process country data from wars, and update the database.
  - Use `analyze_import2.py` to compare the integrity of wars data between a CSV source and the database.
  - To perform database operations, leverage the functions provided in `database_operations.py`. These functions include resetting the database and fetching data related to wars.

- **Visualization:**
  - Use `wars_barchartrace.py` to generate a bar chart race video, visualizing either the participation of countries in different wars or the number victims associated with those wars over the years.

Simply execute the scripts in the Python environment, ensuring that the configuration variables (like file paths) match your setup.

## Conclusion

This project provides tools to handle war-related data processing, storage, and visualization. By efficiently managing the data through database operations and presenting it with clear visual aids, it supports deeper insights into historical war patterns and their impacts.

## Python Files

- SamplePy/NormalizeCountries.py
- SamplePy/analyze_import2.py
- SamplePy/database_operations.py
- SamplePy/wars_barchartrace.py