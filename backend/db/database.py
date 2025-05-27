import sqlite3
from datetime import datetime

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect("tutor.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            query TEXT,
            subject TEXT,
            timestamp DATETIME
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            content_type TEXT,
            content TEXT,
            timestamp DATETIME
        )
    """)
    conn.commit()
    conn.close()

def save_query(user_id: str, query: str, subject: str):
    """Save query to database"""
    conn = sqlite3.connect("tutor.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO queries (user_id, query, subject, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, query, subject, datetime.now())
    )
    conn.commit()
    conn.close()

def get_query_history(user_id: str, limit: int = 3) -> list:
    """Retrieve query history for user"""
    conn = sqlite3.connect("tutor.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT query, subject FROM queries WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    )
    history = [{"query": row[0], "subject": row[1]} for row in cursor.fetchall()]
    conn.close()
    return history

def save_content(user_id: str, content_type: str, content: str):
    """Save content (e.g., evaluation feedback) to database"""
    conn = sqlite3.connect("tutor.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO content (user_id, content_type, content, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, content_type, content, datetime.now())
    )
    conn.commit()
    conn.close()
