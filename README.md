# Church Attendance Dashboard

This is a simple Tkinter-based Python application that helps to track church attendance for different groups: Gents, Ladies, and Kids. It allows the user to input the service name, update attendance counts, view a bar graph of the attendance by group, and save the data to a CSV file.

## Features

- **Service Name Input**: Allows the user to enter the name of the service currently taking place.
- **Attendance Counts**: Tracks the number of attendees for Gents, Ladies, and Kids.
- **Bar Graph Visualization**: Displays a bar graph of the current attendance counts for each group (Gents, Ladies, Kids).
- **Save to CSV**: Saves the attendance data to a CSV file with the service name, attendance counts, and timestamp.
- **Reset Functionality**: Resets all fields (attendance counts and service name) with a confirmation prompt before doing so.

## Requirements

To run this project, you need the following Python packages:

- **Tkinter**: For creating the graphical user interface (GUI).
- **Pandas**: For handling data and saving records to CSV.
- **Matplotlib**: For plotting the bar graph.

Install the required packages using `pip`:

```bash
pip install pandas matplotlib
