📧 **AI Communication Assistant - Email**

🚀 **Overview**

Modern organizations receive hundreds (sometimes thousands) of emails daily. Many of these are support-related (customer queries, requests, or help tickets).
Manually filtering, prioritizing, and drafting professional responses is time-consuming and error-prone. An intelligent communication assistant that helps teams analyze, prioritize, and respond to emails automatically.Built for efficiency in customer support / helpdesk scenarios, this system performs sentiment analysis, priority detection, AI-driven response drafting, and analytics visualization — all in one streamlined dashboard.

**This project implements an AI-Powered Communication Assistant that manages emails end-to-end:**

Automatically retrieves and filters emails.

Analyzes sentiment & urgency.

Extracts key details (contacts, requests, metadata).

Generates context-aware AI responses.

Provides an interactive dashboard for tracking and managing communications.

The goal is to improve efficiency, response quality, and customer satisfaction while reducing manual effort.

🛠️ **Features**

✅ **Email Retrieval & Filtering**

Load from dataset (Dataset.csv) or fetch live emails (IMAP-ready).

Filters support-related subjects (Support, Query, Request, Help).

✅ **Categorization & Prioritization**

Sentiment analysis (Positive / Negative / Neutral).

Urgency detection using keywords (Urgent / Not Urgent).

Urgent emails automatically move to the top of the queue.

✅ **Context-Aware Auto-Responses**

Uses rule-based AI templates (extendable with Hugging Face or OpenAI models).

Empathetic responses for negative sentiment.

References products/issues mentioned in the email.

Drafts can be reviewed & edited before sending.

✅ **Information Extraction**

Extracts phone numbers, alternate emails, and customer details.

Helps support teams act faster.

✅ **Interactive Dashboard (Streamlit + Plotly)**

Clean, responsive UI.

Tabs for Inbox, Analytics, Settings.

Expandable email cards with priority/status icons.

🚀 **What It Does**

📥 **Email Ingestion :** Import emails from a dataset (Dataset.csv) or directly from the SQLite database (emails.db).

🧠 **Sentiment Analysis:** Uses NLP (VADER sentiment analysis) to classify emails as Positive, Neutral, Negative.

⚡ **Priority Detection:** Flags urgent issues using keyword-based detection (e.g., urgent, critical, fail, down).

✉️ **Smart Response Generation:** AI drafts personalized responses based on sentiment + priority, ready for review & sending.

📊 **Analytics Dashboard:** Interactive charts to monitor workload trends, sentiment distribution, resolution rates, and response efficiency.

🔍 **Search & Filters:** Quickly find emails by sender, subject, sentiment, or priority.

📂 **Database Persistence:** Stores emails, status, and responses in a lightweight SQLite database (emails.db).

**Analytics include:**

📌 Sentiment distribution → Positive, Neutral, Negative

📌 Priority levels → Urgent vs Not Urgent

📌 Status → Pending vs Resolved 

📌 Trend Over Time (emails received daily/weekly)

📌 Last 24h Activity for real-time monitoring

**📈 Emails over time**

Real-time stats (last 24h, pending, resolved).

📂 **Dataset The Dataset.csv contains:**

sender → Email sender address

subject → Subject line of the email

body → Full email content

sent_date → Timestamp of when the email was sent

During processing, additional fields are generated:

sentiment (Positive / Neutral / Negative)

priority (Urgent / Not Urgent)

ai_response (auto-drafted email reply)

🏗️ **Tech Stacks Used:**

Frontend → Streamlit Interactive UI for email review and analytics

Dashboard → Plotly Express Rich visualizations (bar, pie, line charts)

Backend Processing → Python (pandas, nltk, re)

AI/NLP → NLTK Vader Sentimental Analysis

Regex → Contact info extraction (phones, emails)

Rule-based AI + Templates → Automated response drafting (response.py)

Database → SQLite (emails.db) → Stores emails, metadata, and AI responses

Dataset → Provided Dataset.csv for demo/testing

(Optional) Email Retrieval → IMAP (Gmail/Outlook ready)
