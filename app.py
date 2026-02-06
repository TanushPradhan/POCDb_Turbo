import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# -------------------------------------------------
# SUPABASE CONNECTION (READS FROM STREAMLIT SECRETS)
# -------------------------------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="POC Management System",
    page_icon="📇",
    layout="wide"
)

st.title("📇 School & College POC Management Platform")
st.caption("Centralized institutional contact database")

# -------------------------------------------------
# ADD NEW POC
# -------------------------------------------------
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

        supabase.table("poc_contacts").insert({
            "city": city,
            "institute_name": institute,
            "poc_name": poc_name,
            "mobile": mobile,
            "email": email,
            "status": status,
            "remarks": remarks,
            "meeting_schedule": meeting_schedule,
            "created_at": datetime.now().isoformat()
        }).execute()

        st.success("✅ POC saved successfully")

# -------------------------------------------------
# VIEW POC DATABASE
# -------------------------------------------------
st.markdown("---")
st.subheader("📊 POC Database")

response = supabase.table("poc_contacts") \
    .select("*") \
    .order("created_at", desc=True) \
    .execute()

df = pd.DataFrame(response.data)

if not df.empty:
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
else:
    st.info("No POC records found yet.")

st.caption("Powered by Streamlit + Supabase")
