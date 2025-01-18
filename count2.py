import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF
import tempfile

# Initialize session state for counts
for key in ['gents', 'ladies', 'kids', 'service_name', 'history']:
    if key not in st.session_state:
        st.session_state[key] = 0 if key != 'service_name' and key != 'history' else "" if key == 'service_name' else []

# Functions to update counts
def update_count(category, increment=True):
    if increment:
        st.session_state[category] += 1
    else:
        if st.session_state[category] > 0:
            st.session_state[category] -= 1

def save_current_data():
    st.session_state.history.append({
        "Service Name": st.session_state.service_name,
        "Gents": st.session_state.gents,
        "Ladies": st.session_state.ladies,
        "Kids": st.session_state.kids,
        "Total": st.session_state.total
    })

# Page title and description
st.title("⛪ RATC Headcount Tracker")
st.markdown(
    """Track attendance for RATC services effortlessly. Use the buttons below to update counts for Gents, Ladies, and Kids, and download a detailed report with charts and summaries."""
)

# Service name input
st.markdown("### 📝 Enter Service Name")
service_name = st.text_input("Service Name:", value=st.session_state.service_name)
if service_name:
    st.session_state.service_name = service_name

# Buttons for headcount
st.markdown("### ✍️ Update Headcount")
col1, col2, col3 = st.columns(3)

with col1:
    st.button("➕ Add Gent", on_click=update_count, args=("gents", True))
    st.button("➖ Subtract Gent", on_click=update_count, args=("gents", False))

with col2:
    st.button("➕ Add Lady", on_click=update_count, args=("ladies", True))
    st.button("➖ Subtract Lady", on_click=update_count, args=("ladies", False))

with col3:
    st.button("➕ Add Kid", on_click=update_count, args=("kids", True))
    st.button("➖ Subtract Kid", on_click=update_count, args=("kids", False))

# Display counts
st.markdown("### 📊 Current Headcount")
st.markdown(f"- 👨 **Gents**: {st.session_state.gents}")
st.markdown(f"- 👩 **Ladies**: {st.session_state.ladies}")
st.markdown(f"- 👶 **Kids**: {st.session_state.kids}")

# Calculate total
st.session_state.total = st.session_state.gents + st.session_state.ladies + st.session_state.kids
st.markdown(f"**Total Attendance**: {st.session_state.total}")

# Save current data
if st.button("Save Data"):
    save_current_data()
    st.success("Data saved successfully!")

# Historical data
if st.session_state.history:
    st.markdown("### 📜 Historical Data")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)

# Bar graph for attendance counts
st.markdown("### 📊 Attendance Breakdown")
if st.session_state.total > 0:  # Ensure there is data before plotting
    fig_bar, ax_bar = plt.subplots()  # Make sure fig_bar is defined here
    categories = ['Gents', 'Ladies', 'Kids']
    counts = [st.session_state.gents, st.session_state.ladies, st.session_state.kids]
    colors_bar = ['#1f77b4', '#ff7f0e', '#2ca02c']

    ax_bar.bar(categories, counts, color=colors_bar)
    ax_bar.set_ylabel("Count", fontsize=12)
    ax_bar.set_xlabel("Category", fontsize=12)

    # Display bar graph
    st.pyplot(fig_bar)

    # Save bar graph to a temporary file
    bar_chart_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig_bar.savefig(bar_chart_path.name)  # Save the figure after it's created
else:
    st.info("No attendance data available to display a breakdown chart.")

# Pie chart for proportions
st.markdown("### 📈 Attendance Distribution")
if st.session_state.total > 0:  # Check if there is any data
    labels = ['Gents', 'Ladies', 'Kids']
    sizes = [st.session_state.gents, st.session_state.ladies, st.session_state.kids]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    fig, ax = plt.subplots()  # Ensure fig is created here
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')  # Equal aspect ratio ensures pie chart is drawn as a circle.
    st.pyplot(fig)

    # Save pie chart to a temporary file
    pie_chart_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.savefig(pie_chart_path.name)  # Save the figure after it's created
else:
    st.info("No attendance data available to display a distribution chart.")

# Data for report
st.markdown("### 📋 Attendance Summary Table")
data = {
    "Name of the Service": [st.session_state.service_name],
    "Gents": [st.session_state.gents],
    "Ladies": [st.session_state.ladies],
    "Kids": [st.session_state.kids],
    "Total": [st.session_state.total]
}
df = pd.DataFrame(data)

# Styled DataFrame
st.dataframe(df, use_container_width=True)
from io import BytesIO

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt=f"Service Headcount Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Service Name: {st.session_state.service_name}", ln=True, align='C')
    pdf.ln(10)

    # Table header
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(50, 10, txt="Category", border=1, align='C')
    pdf.cell(50, 10, txt="Count", border=1, align='C')
    pdf.ln()

    # Table data
    for category, count in zip(["Gents", "Ladies", "Kids", "Total"],
                               [st.session_state.gents, st.session_state.ladies, st.session_state.kids, st.session_state.total]):
        pdf.cell(50, 10, txt=category, border=1)
        pdf.cell(50, 10, txt=str(count), border=1, align='C')
        pdf.ln()

    pdf.ln(20)

    # Add bar graph to BytesIO
    bar_chart_io = BytesIO()
    fig_bar.savefig(bar_chart_io, format='png')
    bar_chart_io.seek(0)
    
    # Add pie chart to BytesIO
    pie_chart_io = BytesIO()
    fig.savefig(pie_chart_io, format='png')
    pie_chart_io.seek(0)

    # Add images to PDF
    pdf.cell(200, 10, txt="Attendance Breakdown", ln=True, align='C')
    pdf.image(bar_chart_io, x=50, y=None, w=100)
    
    # Add pie chart
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Attendance Proportion", ln=True, align='C')
    pdf.image(pie_chart_io, x=50, y=None, w=100)
    pdf.ln(75)

    # Save to BytesIO (ensure file is written into memory correctly)
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)  # Make sure to move the pointer to the start of the buffer
    return pdf_output


if st.button("Download Report"):
    pdf_report = generate_pdf()
    st.download_button(
        label="Download Report as PDF",
        data=pdf_report,
        file_name=f"{st.session_state.service_name}_headcount.pdf",
        mime="application/pdf"
    )