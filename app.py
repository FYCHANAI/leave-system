import streamlit as st
import pandas as pd
import os
from datetime import datetime

# File path for storing data
DATA_FILE = "leave_data.csv"

def load_data():
    """Load leave data from CSV file."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Create an empty dataframe with columns if file doesn't exist
        return pd.DataFrame(columns=["Submission Time", "Name", "Start Date", "End Date", "Leave Type", "Reason", "Status"])

def save_data(df):
    """Save leave data to CSV file."""
    df.to_csv(DATA_FILE, index=False)

def main():
    st.set_page_config(page_title="Employee Leave Management System", layout="wide")
    st.title("NTAM Employee Leave Management System")

    # Sidebar Navigation
    menu = ["Employee Application", "Manager Review"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Employee Application":
        st.header("Employee Leave Application")
        
        with st.form("leave_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Employee Name")
                leave_type = st.selectbox("Leave Type", ["Sick Leave", "Personal Leave", "Annual Leave", "Bereavement Leave", "Other"])
            
            with col2:
                start_date = st.date_input("Start Date", min_value=datetime.today())
                end_date = st.date_input("End Date", min_value=datetime.today())
            
            reason = st.text_area("Reason for Leave")
            
            submitted = st.form_submit_button("Submit Application")
            
            if submitted:
                if name and reason and start_date <= end_date:
                    df = load_data()
                    new_entry = {
                        "Submission Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Name": name,
                        "Start Date": start_date,
                        "End Date": end_date,
                        "Leave Type": leave_type,
                        "Reason": reason,
                        "Status": "Pending" # Default status
                    }
                    # Append new data
                    new_df = pd.DataFrame([new_entry])
                    df = pd.concat([df, new_df], ignore_index=True)
                    save_data(df)
                    st.success(f"Leave application for {name} submitted successfully!")
                else:
                    st.error("Please fill in all fields correctly. Ensure End Date is after Start Date.")

    elif choice == "Manager Review":
        st.header("Manager Review Dashboard")
        
        df = load_data()
        
        if not df.empty:
            # Statistics
            st.subheader("Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Applications", len(df))
            col2.metric("Pending Reviews", len(df[df['Status'] == 'Pending']))
            
            # Leave Type Breakdown
            type_counts = df['Leave Type'].value_counts()
            st.bar_chart(type_counts)

            # Data Table
            st.subheader("All Applications")
            st.dataframe(df, use_container_width=True)
            
            # Optional: Simple status toggle could be added here, 
            # but sticking to core requirements of "Read and Display" + "Stats" first.
        else:
            st.info("No leave applications found.")

if __name__ == "__main__":
    main()

