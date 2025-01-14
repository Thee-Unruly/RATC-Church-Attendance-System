import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np  # To handle NaN checks

# Initialize data
counts = {"Gents": 0, "Ladies": 0, "Kids": 0}
daily_records = []

def update_count(category):
    counts[category] += 1
    update_dashboard()

def reset_counts(category=None):
    if category:
        counts[category] = 0
    else:
        save_to_file()
        for key in counts:
            counts[key] = 0
    update_dashboard()

def save_to_file():
    global daily_records
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    service_name = service_name_var.get() if service_name_var.get() else "No service name"
    
    # Add service name to the record
    record = {"Date": today, "Service Name": service_name, **counts}
    daily_records.append(record)
    
    # Convert daily records to DataFrame
    df = pd.DataFrame(daily_records)
    
    # Save to CSV
    df.to_csv("church_attendance.csv", index=False)
    
    messagebox.showinfo("Saved", "Attendance recorded and saved successfully!")


def update_dashboard():
    # Update dashboard labels
    gents_count_label.config(text=f"👨‍🦱 Gents: {counts['Gents']}")
    ladies_count_label.config(text=f"👩‍🦱 Ladies: {counts['Ladies']}")
    kids_count_label.config(text=f"🧒 Kids: {counts['Kids']}")
    total_count_label.config(text=f"Total: {sum(counts.values())}")
    
    # Update service name
    service_name_label.config(text=f"Service: {service_name_var.get()}")
    
    # Update bar graph first
    update_bar_graph()
    
    # Update pie chart after the bar graph
    update_pie_chart()

# Create a figure for pie chart and bar graph
fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(12, 6))  # Bar graph comes first (ax2)

def update_bar_graph():
    ax2.clear()
    
    # Bar graph
    categories = list(counts.keys())
    values = list(counts.values())
    ax2.bar(categories, values, color=["blue", "pink", "yellow"])
    ax2.set_title("Headcount Bar Graph")
    ax2.set_xlabel("Categories")
    ax2.set_ylabel("Count")
    ax2.set_ylim(0, max(values) + 1)  # Set the y-axis range a bit higher than max value
    pie_canvas.draw()

def update_pie_chart():
    ax1.clear()
    
    # Ensure all count values are valid (not NaN or None)
    sizes = list(counts.values())
    if any(np.isnan(val) or val is None for val in sizes):
        print(f"Invalid data in counts: {sizes}, skipping pie chart update.")
        return

    print(f"Updating pie chart with sizes: {sizes}")  # Debugging output

    # Pie chart, where the slices will be ordered and categorized
    labels = counts.keys()
    try:
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=["blue", "pink", "yellow"])
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title("Headcount Distribution")
        pie_canvas.draw()
    except ValueError as e:
        print(f"Error in pie chart update: {e}")

def view_records():
    records_window = tk.Toplevel(root)
    records_window.title("Daily Records")
    records_window.geometry("600x400")

    columns = ["Date", "Gents", "Ladies", "Kids"]
    tree = ttk.Treeview(records_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(fill=tk.BOTH, expand=True)

    # Insert records into the tree
    for record in daily_records:
        tree.insert("", tk.END, values=[record[col] for col in columns])

# Main Tkinter window
root = tk.Tk()
root.title("Church Attendance System")
root.geometry("800x600")

# Dashboard Frame
dashboard_frame = tk.Frame(root)
dashboard_frame.pack(pady=10)

# Headcount Labels
gents_count_label = tk.Label(dashboard_frame, text="👨‍🦱 Gents: 0", font=("Arial", 14))
ladies_count_label = tk.Label(dashboard_frame, text="👩‍🦱 Ladies: 0", font=("Arial", 14))
kids_count_label = tk.Label(dashboard_frame, text="🧒 Kids: 0", font=("Arial", 14))
total_count_label = tk.Label(dashboard_frame, text="Total: 0", font=("Arial", 14))
service_name_label = tk.Label(dashboard_frame, text="Service: Not Set", font=("Arial", 14))

gents_count_label.grid(row=0, column=0, padx=10)
ladies_count_label.grid(row=0, column=1, padx=10)
kids_count_label.grid(row=0, column=2, padx=10)
total_count_label.grid(row=0, column=3, padx=10)
service_name_label.grid(row=1, column=0, columnspan=4, pady=10)

# Service Name Input
service_name_label = tk.Label(root, text="Enter Service Name:")
service_name_label.pack(pady=10)

service_name_var = tk.StringVar()

service_name_entry = tk.Entry(root, textvariable=service_name_var, font=("Arial", 12))
service_name_entry.pack(pady=5)

# Buttons Frame
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

# Buttons for each category
btn_gents = ttk.Button(buttons_frame, text="👨‍🦱 Add Gents", command=lambda: update_count("Gents"))
btn_gents.grid(row=0, column=0, padx=20, pady=10)
btn_gents.config(width=15)

btn_ladies = ttk.Button(buttons_frame, text="👩‍🦱 Add Ladies", command=lambda: update_count("Ladies"))
btn_ladies.grid(row=0, column=1, padx=20, pady=10)
btn_ladies.config(width=15)

btn_kids = ttk.Button(buttons_frame, text="🧒 Add Kids", command=lambda: update_count("Kids"))
btn_kids.grid(row=0, column=2, padx=20, pady=10)
btn_kids.config(width=15)

# Reset and Records Buttons
reset_frame = tk.Frame(root)
reset_frame.pack(pady=10)

btn_reset_all = ttk.Button(reset_frame, text="Reset All", command=reset_counts)
btn_reset_all.grid(row=0, column=0, padx=20, pady=10)
btn_reset_all.config(width=15)

btn_view_records = ttk.Button(reset_frame, text="View Records", command=view_records)
btn_view_records.grid(row=0, column=1, padx=20, pady=10)
btn_view_records.config(width=15)

# Matplotlib Canvas
pie_canvas = FigureCanvasTkAgg(fig, master=root)
pie_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Initialize the dashboard
update_dashboard()

# Run the Tkinter main loop
root.mainloop()
