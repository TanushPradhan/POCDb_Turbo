import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="POC Database",
    page_icon="📊",
    layout="wide"
)

st.title("📊 POC Database")
st.caption("School & College Point of Contact Management System")

# -------------------------------------------------
# SUPABASE CONNECTION
# -------------------------------------------------
try:
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except Exception as e:
    st.error("❌ Supabase connection failed.")
    st.code(str(e))
    st.stop()

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
        status = st.selectbox(
            "POC Status",
            ["Cold", "Warm", "Active", "Closed"]
        )

    with col3:
        meeting_date = st.date_input("Meeting Date")
        meeting_time = st.time_input("Meeting Time")
        remarks = st.text_area("Remarks")

    if st.button("💾 Save POC"):
        try:
            meeting_schedule = datetime.combine(
                meeting_date, meeting_time
            ).isoformat()

            result = supabase.table("poc_contacts").insert({
                "city": city,
                "institute_name": institute,
                "poc_name": poc_name,
                "mobile": mobile,
                "email": email,
                "status": status,
                "remarks": remarks,
                "meeting_schedule": meeting_schedule
            }).execute()

            if result.data:
                st.success("✅ POC saved successfully")
            else:
                st.error("❌ Save failed")
                st.write(result)

        except Exception as e:
            st.error("❌ Error while saving data")
            st.code(str(e))

# -------------------------------------------------
# LOAD DATA (SAFE + VERBOSE)
# -------------------------------------------------
st.markdown("---")
st.subheader("📋 POC Records")

df = pd.DataFrame()

try:
    result = supabase.table("poc_contacts").select("*").execute()

    if result.data:
        df = pd.DataFrame(result.data)

except Exception as e:
    st.error("❌ Error while loading data")
    st.code(str(e))
    st.stop()

# -------------------------------------------------
# DISPLAY DATA
# -------------------------------------------------
if df.empty:
    st.info("No POC records found.")
else:
    f1, f2, f3 = st.columns(3)

    with f1:
        city_filter = st.multiselect(
            "Filter by City",
            sorted(df["city"].dropna().unique())
        )

    with f2:
        institute_filter = st.multiselect(
            "Filter by Institute",
            sorted(df["institute_name"].dropna().unique())
        )

    with f3:
        status_filter = st.multiselect(
            "Filter by Status",
            sorted(df["status"].dropna().unique())
        )

    if city_filter:
        df = df[df["city"].isin(city_filter)]
    if institute_filter:
        df = df[df["institute_name"].isin(institute_filter)]
    if status_filter:
        df = df[df["status"].isin(status_filter)]

    st.dataframe(
        df.drop(columns=["id"]),
        use_container_width=True
    )

st.caption("Powered by Streamlit • Supabase • PostgreSQL")
