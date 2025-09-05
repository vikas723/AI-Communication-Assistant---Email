📧 AI Communication Assistant - Email
🚀 Overview

Modern organizations receive hundreds (sometimes thousands) of emails daily. Many of these are support-related (customer queries, requests, or help tickets).
Manually filtering, prioritizing, and drafting professional responses is time-consuming and error-prone.

This project implements an AI-Powered Communication Assistant that manages emails end-to-end:

Automatically retrieves and filters emails.

Analyzes sentiment & urgency.

Extracts key details (contacts, requests, metadata).

Generates context-aware AI responses.

Provides an interactive dashboard for tracking and managing communications.

The goal is to improve efficiency, response quality, and customer satisfaction while reducing manual effort.

🛠️ Features

✅ Email Retrieval & Filtering

Load from dataset (Dataset.csv) or fetch live emails (IMAP-ready).

Filters support-related subjects (Support, Query, Request, Help).

✅ Categorization & Prioritization

Sentiment analysis (Positive / Negative / Neutral).

Urgency detection using keywords (Urgent / Not Urgent).

Urgent emails automatically move to the top of the queue.

✅ Context-Aware Auto-Responses

Uses rule-based AI templates (extendable with Hugging Face or OpenAI models).

Empathetic responses for negative sentiment.

References products/issues mentioned in the email.

Drafts can be reviewed & edited before sending.

✅ Information Extraction

Extracts phone numbers, alternate emails, and customer details.

Helps support teams act faster.

✅ Interactive Dashboard (Streamlit + Plotly)

Clean, responsive UI.

Tabs for Inbox, Analytics, Settings.

Expandable email cards with priority/status icons.

Analytics include:

📌 Sentiment distribution

📌 Priority levels

📌 Status (Pending vs Resolved)

📈 Emails over time

Real-time stats (last 24h, pending, resolved).

🏗️ Tech Stack

Frontend/Dashboard → Streamlit
 + Plotly

Backend Processing → Python (pandas, nltk, re)

AI/NLP → NLTK Vader (sentiment), Regex (info extraction), Rule-based AI responses

Database → SQLite (emails.db)

Dataset → Provided Dataset.csv for demo/testing

(Optional) Email Retrieval → IMAP (Gmail/Outlook ready)
