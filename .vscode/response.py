import random

# Simple templated responses
templates = {
    "Positive": [
        "Thank you for reaching out. We’re glad to assist you with your request.",
    ],
    "Negative": [
        "We understand your frustration and apologize for the inconvenience. Our team is working on this issue urgently.",
    ],
    "Neutral": [
        "Thank you for contacting us. We have noted your request and will respond shortly.",
    ]
}

def generate_response(sentiment, subject, body):
    base = random.choice(templates[sentiment])
    return f"{base}\n\nSubject: {subject}\nWe will get back to you with more details soon."
