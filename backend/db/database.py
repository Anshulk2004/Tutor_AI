import sqlite3

def init_db():
    conn = sqlite3.connect("tutor.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS content
             (id INTEGER PRIMARY KEY, user_id TEXT, type TEXT, content TEXT, timestamp DATETIME)''')
    c.execute('''CREATE TABLE IF NOT EXISTS query_history
                    (id INTEGER PRIMARY KEY, user_id TEXT, query TEXT, subject TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()
       

def save_content(user_id, content_type, content):
    conn = sqlite3.connect("tutor.db")
    c = conn.cursor()
    c.execute("INSERT INTO content (user_id, type, content, timestamp) VALUES (?, ?, ?, datetime('now'))",
                 (user_id, content_type, content))
    conn.commit()
    conn.close()

def save_query(user_id, query, subject):
    conn = sqlite3.connect("tutor.db")
    c = conn.cursor()
    c.execute("INSERT INTO query_history (user_id, query, subject, timestamp) VALUES (?, ?, ?, datetime('now'))",
                 (user_id, query, subject))
    conn.commit()
    conn.close()

def get_query_history(user_id, limit=5):
    conn = sqlite3.connect("tutor.db")
    c = conn.cursor()
    c.execute("SELECT query, subject FROM query_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
                 (user_id, limit))
    result = c.fetchall()
    conn.close()
    return [{"query": row[0], "subject": row[1]} for row in result]

def get_content(user_id, content_type):
    conn = sqlite3.connect("tutor.db")
    c = conn.cursor()
    c.execute("SELECT content FROM content WHERE user_id = ? AND type = ?", (user_id, content_type))
    result = c.fetchall()
    conn.close()
    return [row[0] for row in result]