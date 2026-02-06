import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# ------------------ DATABASE SETUP ------------------
DB_PATH = "database/poc_database.db"
os.makedirs("database", exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS poc_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    institute_name TEXT,
    poc_name TEXT,
    mobile TEXT,
    email TEXT,
    status TEXT,
    remarks TEXT,
    meeting_schedule TEXT,
    created_at TEXT
)
""")
conn.commit()

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="POC Management System",
    page_icon="📇",
    layout="wide"
)

st.title("📇 School & College POC Management Platform")
st.caption("Centralized institutional contact database")

# ------------------ ADD POC FORM ------------------
with st.expander("➕ Add New POC", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        city = st.text_input("City")
        institute = st.text_input("Institute Name")
        poc_name = st.text_input("POC Name")

    with col2:
        mobile = st.text_input("POC Mobile Number")
        email = st.text_input("POC Email ID")
        status = st.selectbox("POC Status", ["Cold", "Warm", "Active", "Closed"])

    with col3:
        meeting_date = st.date_input("Meeting Date")
        meeting_time = st.time_input("Meeting Time")
        remarks = st.text_area("Remarks")

    if st.button("💾 Save POC"):
        meeting_schedule = f"{meeting_date} {meeting_time}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO poc_contacts (
            city, institute_name, poc_name,
            mobile, email, status,
            remarks, meeting_schedule, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            city, institute, poc_name,
            mobile, email, status,
            remarks, meeting_schedule, created_at
        ))
        conn.commit()
        st.success("✅ POC saved successfully")

# ------------------ VIEW DATA ------------------
st.markdown("---")
st.subheader("📊 POC Database")

df = pd.read_sql("SELECT * FROM poc_contacts ORDER BY created_at DESC", conn)

f1, f2, f3 = st.columns(3)
with f1:
    city_filter = st.multiselect("Filter by City", df["city"].dropna().unique())
with f2:
    institute_filter = st.multiselect("Filter by Institute", df["institute_name"].dropna().unique())
with f3:
    status_filter = st.multiselect("Filter by Status", df["status"].dropna().unique())

if city_filter:
    df = df[df["city"].isin(city_filter)]
if institute_filter:
    df = df[df["institute_name"].isin(institute_filter)]
if status_filter:
    df = df[df["status"].isin(status_filter)]

st.dataframe(df.drop(columns=["id"]), use_container_width=True)

st.caption("Built with Streamlit • GitHub ready • Deployable")
