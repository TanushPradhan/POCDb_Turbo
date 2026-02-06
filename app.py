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
# SUPABASE CONNECTION (SERVER-SIDE)
# -------------------------------------------------
try:
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]  # sb_secret_ key
    )
except Exception as e:
    st.error("❌ Supabase connection failed")
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

            supabase.table("poc_contacts").insert({
                "city": city,
                "institute_name": institute,
                "poc_name": poc_name,
                "mobile": mobile,
                "email": email,
                "status": status,
                "remarks": remarks,
                "meeting_schedule": meeting_schedule
            }).execute()

            st.success("✅ POC saved successfully")
            st.rerun()

        except Exception as e:
            st.error("❌ Error saving POC")
            st.code(str(e))

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
st.markdown("---")
st.subheader("📋 POC Records")

try:
    response = supabase.table("poc_contacts").select("*").order("id", desc=True).execute()
    df = pd.DataFrame(response.data or [])
except Exception as e:
    st.error("❌ Error loading data")
    st.code(str(e))
    st.stop()

# -------------------------------------------------
# DISPLAY + DELETE
# -------------------------------------------------
if df.empty:
    st.info("No POC records found.")
else:
    for _, row in df.iterrows():
        with st.container():
            cols = st.columns([3, 3, 3, 2, 2, 2, 1])

            cols[0].write(row["poc_name"])
            cols[1].write(row["institute_name"])
            cols[2].write(row["city"])
            cols[3].write(row["mobile"])
            cols[4].write(row["email"])
            cols[5].write(row["status"])

            if cols[6].button("🗑️", key=f"delete_{row['id']}"):
                try:
                    supabase.table("poc_contacts").delete().eq("id", row["id"]).execute()
                    st.success(f"🗑️ Deleted POC: {row['poc_name']}")
                    st.rerun()
                except Exception as e:
                    st.error("❌ Delete failed")
                    st.code(str(e))

st.caption("Powered by Streamlit • Supabase • PostgreSQL")
