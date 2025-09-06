
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from database import init_db, insert_email, fetch_emails, update_response
from processor import process_dataset
from response import generate_response

CSV_PATH = "Dataset.csv"

# ---------------------------
# Initialize DB
# ---------------------------
init_db()

st.set_page_config(
    page_title="AI Email Assistant",
    page_icon="📧",
    layout="wide"
)

st.title("📧 AI-Powered Communication Assistant")
st.markdown("### Manage, Analyze, and Respond to Support Emails Smarter 🚀")

# ---------------------------
# Load dataset into DB if first time
# ---------------------------
if st.button("📥 Load Emails from Dataset"):
    emails = process_dataset(CSV_PATH)
    for e in emails:
        # Ensure correct unpacking based on CSV + processing
        sender, subject, body, sent_date, sentiment, priority = e[:6]
        status = "Pending"
        response = ""
        insert_email(sender, subject, body, sent_date, sentiment, priority, status, response)
    st.success("✅ Emails loaded successfully!")

# ---------------------------
# Fetch emails from DB
# ---------------------------
emails = fetch_emails()

if emails:
    st.subheader("📩 Processed Emails")

    # Convert to DataFrame
    data = pd.DataFrame(
        emails,
        columns=["ID", "Sender", "Subject", "Body", "SentDate", "Sentiment", "Priority", "Status", "Response"]
    )

    # Ensure datetime conversion
    data["SentDate"] = pd.to_datetime(data["SentDate"], errors="coerce")

    # Sidebar filters
    st.sidebar.header("🔎 Filters")
    sentiment_filter = st.sidebar.multiselect("Filter by Sentiment", options=data["Sentiment"].unique())
    priority_filter = st.sidebar.multiselect("Filter by Priority", options=data["Priority"].unique())
    status_filter = st.sidebar.multiselect("Filter by Status", options=data["Status"].unique())

    filtered = data.copy()
    if sentiment_filter:
        filtered = filtered[filtered["Sentiment"].isin(sentiment_filter)]
    if priority_filter:
        filtered = filtered[filtered["Priority"].isin(priority_filter)]
    if status_filter:
        filtered = filtered[filtered["Status"].isin(status_filter)]

    # Search box
    search_query = st.sidebar.text_input("🔍 Search by Subject or Sender")
    if search_query:
        filtered = filtered[
            filtered["Subject"].str.contains(search_query, case=False, na=False)
            | filtered["Sender"].str.contains(search_query, case=False, na=False)
        ]

    # Display filtered emails
    for _, email in filtered.iterrows():
        with st.expander(f"📨 From: {email['Sender']} | {email['Subject']} | Priority: {email['Priority']} | Status: {email['Status']}"):
            st.write(f"**Received:** {email['SentDate']}")
            st.write(f"**Sentiment:** {email['Sentiment']}")
            st.write(f"**Body:** {email['Body']}")

            if email["Status"] == "Pending":
                draft = generate_response(email["Sentiment"], email["Subject"], email["Body"])
                new_response = st.text_area("✍️ AI-Generated Draft:", draft, key=f"resp_{email['ID']}")
                if st.button("✅ Send Response", key=f"send_{email['ID']}"):
                    update_response(email["ID"], new_response)
                    st.success("Response saved as sent!")

    # ---------------------------
    # Analytics Section
    # ---------------------------
    st.subheader("📊 Analytics Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📥 Total Emails", len(data))
    with col2:
        last_24h = data[data["SentDate"] >= datetime.now() - timedelta(hours=24)]
        st.metric("⏳ Last 24h", len(last_24h))
    with col3:
        resolved = len(data[data["Status"] == "Resolved"])
        st.metric("✅ Resolved", resolved)
    with col4:
        pending = len(data[data["Status"] == "Pending"])
        st.metric("🕒 Pending", pending)

    # Interactive Graphs
    st.markdown("### 📌 Visual Insights")

    priority_counts = data["Priority"].value_counts().reset_index()
    priority_counts.columns = ["Priority", "Count"]
    fig1 = px.bar(priority_counts, x="Priority", y="Count", color="Priority",
                  title="📌 Emails by Priority")
    st.plotly_chart(fig1, use_container_width=True)

    # Sentiment Distribution
    sentiment_counts = data["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]
    fig2 = px.pie(sentiment_counts, names="Sentiment", values="Count",
                  title="😊 Sentiment Distribution")
    st.plotly_chart(fig2, use_container_width=True)

    # Status Distribution
    status_counts = data["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig3 = px.bar(status_counts, x="Status", y="Count", color="Status",
                  title="📌 Emails by Status")
    st.plotly_chart(fig3, use_container_width=True)

    # Emails Over Time
    timeline = data.groupby(data["SentDate"].dt.date)["ID"].count().reset_index()
    timeline.columns = ["Date", "EmailCount"]
    fig4 = px.line(timeline, x="Date", y="EmailCount", title="📈 Emails Over Time")
    st.plotly_chart(fig4, use_container_width=True)


    # col_a, col_b = st.columns(2)

    # with col_a:
    #     fig1 = px.bar(data["Priority"].value_counts().reset_index(),
    #                   x="index", y="Priority", color="index",
    #                   title="📌 Emails by Priority")
    #     st.plotly_chart(fig1, use_container_width=True)

    # with col_b:
    #     fig2 = px.pie(data, names="Sentiment", title="😊 Sentiment Distribution")
    #     st.plotly_chart(fig2, use_container_width=True)

    # col_c, col_d = st.columns(2)
    # with col_c:
    #     fig3 = px.bar(data["Status"].value_counts().reset_index(),
    #                   x="index", y="Status", color="index",
    #                   title="📌 Emails by Status")
    #     st.plotly_chart(fig3, use_container_width=True)

    # with col_d:
    #     fig4 = px.line(data.sort_values("SentDate"),
    #                    x="SentDate", y=data.groupby("SentDate")["ID"].transform("count"),
    #                    title="📈 Emails Over Time")
    #     st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("⚠️ No emails found. Please load dataset first.")

