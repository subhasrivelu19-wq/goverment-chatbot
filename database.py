import sqlite3
from datetime import datetime

DB_NAME = "chatbot_history.db"

def init_db():
    with sqlite3.connect(DB_NAME) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                result_count INTEGER NOT NULL,
                searched_at TEXT NOT NULL
            )
        """)

def log_search(query: str, result_count: int):
    with sqlite3.connect(DB_NAME) as con:
        con.execute(
            "INSERT INTO search_history (query, result_count, searched_at) VALUES (?, ?, ?)",
            (query, int(result_count), datetime.now().isoformat(timespec="seconds"))
        )
