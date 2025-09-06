import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download VADER lexicon if not already available
nltk.download("vader_lexicon", quiet=True)

# --- Sentiment Analyzer ---
sentiment_analyzer = SentimentIntensityAnalyzer()

# --- Priority keywords ---
URGENT_KEYWORDS = ["immediately", "urgent", "critical", "cannot access", "asap", "important", "fail", "down"]

def categorize_priority(text):
    """Check if email text contains urgent keywords."""
    if any(keyword.lower() in str(text).lower() for keyword in URGENT_KEYWORDS):
        return "Urgent"
    return "Not Urgent"

def analyze_sentiment(text):
    """Return Positive / Negative / Neutral sentiment for email body."""
    scores = sentiment_analyzer.polarity_scores(str(text))
    compound = scores["compound"]
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def extract_contact_info(text):
    """Extract phone numbers and emails from email body."""
    phones = re.findall(r"\+?\d[\d\-\s]{7,}\d", str(text))
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", str(text))
    return {"phones": phones, "emails": emails}

def generate_ai_response(subject, body, sentiment, priority):
    """Generate a simple AI-like response (rule-based placeholder)."""
    response = f"Hello,\n\nThank you for reaching out regarding '{subject}'.\n"
    
    if priority == "Urgent":
        response += "We understand this issue is urgent and our team is addressing it with top priority.\n"
    if sentiment == "Negative":
        response += "We’re sorry for the inconvenience caused and appreciate your patience.\n"
    response += "Our support team will get back to you with a resolution shortly.\n\nBest regards,\nSupport Team"
    
    return response

def process_dataset(csv_path):
    """Process dataset: sentiment, priority, info extraction, AI responses."""
    df = pd.read_csv(csv_path)

    # Ensure required columns exist
    if "body" not in df.columns or "subject" not in df.columns:
        raise ValueError("CSV must contain at least 'subject' and 'body' columns.")

    # Apply processing
    df["sentiment"] = df["body"].apply(analyze_sentiment)
    df["priority"] = df["body"].apply(categorize_priority)
    df["contact_info"] = df["body"].apply(extract_contact_info)
    df["ai_response"] = df.apply(
        lambda row: generate_ai_response(row["subject"], row["body"], row["sentiment"], row["priority"]), axis=1
    )

    # Convert extracted info to list of dicts (for structured use if needed)
    extracted_info = df.to_dict(orient="records")

    return df, extracted_info
