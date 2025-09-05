# import streamlit as st
# from database import init_db, insert_email, fetch_emails, update_response
# from processor import process_dataset
# from response import generate_response

# CSV_PATH = "Dataset.csv"

# # Initialize DB
# init_db()

# st.title("📧 AI-Powered Communication Assistant")

# # Load dataset into DB if first time
# if st.button("Load Emails from Dataset"):
#     emails = process_dataset(CSV_PATH)
#     for e in emails:
#         insert_email(*e)
#     st.success("Emails loaded successfully!")

# # Display emails
# emails = fetch_emails()
# if emails:
#     st.subheader("📩 Processed Emails")
#     for email in emails:
#         email_id, sender, subject, body, sent_date, sentiment, priority, status, response = email
#         with st.expander(f"From: {sender} | {subject} | Priority: {priority} | Status: {status}"):
#             st.write(f"**Received:** {sent_date}")
#             st.write(f"**Sentiment:** {sentiment}")
#             st.write(f"**Body:** {body}")

#             if status == "Pending":
#                 draft = generate_response(sentiment, subject, body)
#                 new_response = st.text_area("AI-Generated Draft:", draft, key=email_id)
#                 if st.button("Send Response", key=f"send_{email_id}"):
#                     update_response(email_id, new_response)
#                     st.success("Response saved as sent!")

# # Analytics
# st.subheader("📊 Analytics")
# import pandas as pd
# data = pd.DataFrame(emails, columns=["ID","Sender","Subject","Body","SentDate","Sentiment","Priority","Status","Response"])
# st.bar_chart(data["Priority"].value_counts())
# st.bar_chart(data["Sentiment"].value_counts())
# st.bar_chart(data["Status"].value_counts())

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


# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from datetime import datetime, timedelta


# # ===== Page Config =====
# st.set_page_config(
#     page_title="AI Email Support Dashboard",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ===== Sidebar Filters =====
# st.sidebar.title("📂 Filters")
# priority_filter = st.sidebar.multiselect("Filter by Priority", ["High", "Medium", "Low"])
# sentiment_filter = st.sidebar.multiselect("Filter by Sentiment", ["Positive", "Neutral", "Negative"])
# time_filter = st.sidebar.selectbox("Time Range", ["Last 24 Hours", "Last 7 Days", "All Time"])

# # ===== Load & Process Dataset =====
# emails_df = process_dataset("D:/AI Email/.vscode/Dataset.csv")

# uploaded_file = st.file_uploader("Upload support email dataset (CSV)", type="csv")
# # if uploaded_file is not None:
# #     emails_df,  extracted_info = process_dataset(uploaded_file)

# # # Simulate timestamps for demo
# # if "timestamp" not in emails_df.columns:
# #     emails_df["timestamp"] = [datetime.now() - timedelta(hours=i*2) for i in range(len(emails_df))]

# if uploaded_file is not None:
#     # Correct unpacking
#     result = process_dataset(uploaded_file)

#     # Ensure it's a tuple of (df, info)
#     if isinstance(result, tuple):
#         emails_df, extracted_info = result
#     else:
#         emails_df = result
#         extracted_info = {}

#     # Simulate timestamps for demo
#     if "timestamp" not in emails_df.columns:
#         emails_df["timestamp"] = [datetime.now() - timedelta(hours=i*2) for i in range(len(emails_df))]

# # st.write("DEBUG emails_df type:", type(emails_df))

# # Apply filters
# emails_df, extracted_info = process_dataset(uploaded_file)
# filtered_emails = emails_df.copy()
# st.write("emails_df type:", type(emails_df))


# if priority_filter:
#     filtered_emails = filtered_emails[filtered_emails["priority"].isin(priority_filter)]
# if sentiment_filter:
#     filtered_emails = filtered_emails[filtered_emails["sentiment"].isin(sentiment_filter)]
# if time_filter == "Last 24 Hours":
#     filtered_emails = filtered_emails[filtered_emails["timestamp"] >= datetime.now() - timedelta(days=1)]
# elif time_filter == "Last 7 Days":
#     filtered_emails = filtered_emails[filtered_emails["timestamp"] >= datetime.now() - timedelta(days=7)]

# # ===== Dashboard Header =====
# st.title("📧 AI-Powered Email Support Dashboard")
# st.markdown("Manage, analyze, and respond to support emails efficiently with AI assistance.")

# # ===== Metrics Section =====
# col1, col2, col3, col4 = st.columns(4)
# col1.metric("📨 Total Emails", len(filtered_emails))
# col2.metric("✅ Resolved", len(filtered_emails[filtered_emails["status"] == "Resolved"]))
# col3.metric("⏳ Pending", len(filtered_emails[filtered_emails["status"] == "Pending"]))
# col4.metric("⚡ High Priority", len(filtered_emails[filtered_emails["priority"] == "High"]))

# # ===== Interactive Graphs =====
# st.subheader("📊 Analytics & Trends")
# tab1, tab2 = st.tabs(["📌 Categories", "📈 Trends Over Time"])

# with tab1:
#     if not filtered_emails.empty:
#         category_fig = px.histogram(filtered_emails, x="sentiment", color="priority",
#                                     title="Email Distribution by Sentiment & Priority",
#                                     barmode="group")
#         st.plotly_chart(category_fig, use_container_width=True)
#     else:
#         st.info("No emails found for selected filters.")

# with tab2:
#     if not filtered_emails.empty:
#         trend_fig = px.line(filtered_emails, x="timestamp", y="priority", color="status",
#                             title="Email Trends Over Time", markers=True)
#         st.plotly_chart(trend_fig, use_container_width=True)
#     else:
#         st.info("No trend data available for selected filters.")

# # ===== Email List Section =====
# st.subheader("📬 Filtered Support Emails")
# if not filtered_emails.empty:
#     for idx, row in filtered_emails.iterrows():
#         with st.expander(f"📩 {row['subject']} - [{row['priority']}]"):
#             st.write(f"**From:** {row['sender']}")
#             st.write(f"**Sentiment:** {row['sentiment']}")
#             st.write(f"**Status:** {row['status']}")
#             st.write(f"**Content:** {row['body']}")
#             st.write("---")
            
#             st.markdown("### 🤖 AI-Generated Response")
#             ai_response = row.get("ai_response", "This is a placeholder AI response.")
#             edited_response = st.text_area("Edit Response Before Sending:", ai_response, key=f"resp_{idx}")
#             if st.button("✅ Send Response", key=f"send_{idx}"):
#                 st.success(f"Response sent to {row['sender']}")
# else:
#     st.warning("No emails match the selected filters.")
