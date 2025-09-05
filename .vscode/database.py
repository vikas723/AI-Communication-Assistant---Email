import sqlite3

DB_NAME = "emails.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        subject TEXT,
        body TEXT,
        sent_date TEXT,
        sentiment TEXT,
        priority TEXT,
        status TEXT,
        response TEXT
    )''')
    conn.commit()
    conn.close()

def insert_email(sender, subject, body, sent_date, sentiment, priority):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO emails (sender, subject, body, sent_date, sentiment, priority, status) VALUES (?,?,?,?,?,?,?)",
                (sender, subject, body, sent_date, sentiment, priority, "Pending"))
    conn.commit()
    conn.close()



def fetch_emails():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM emails ORDER BY priority DESC, sent_date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_response(email_id, response):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE emails SET response=?, status='Resolved' WHERE id=?", (response, email_id))
    conn.commit()
    conn.close()
