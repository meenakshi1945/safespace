import sqlite3
import json
from datetime import datetime

class ChatDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('safespace.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS messages
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             sender TEXT NOT NULL,
             message TEXT NOT NULL,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
        ''')
        self.conn.commit()
    
    def save_message(self, sender, encrypted_message):
        self.conn.execute(
            "INSERT INTO messages (sender, message) VALUES (?, ?)",
            (sender, encrypted_message)
        )
        self.conn.commit()
    
    def get_message_history(self):
        cursor = self.conn.execute(
            "SELECT sender, message, timestamp FROM messages ORDER BY timestamp DESC LIMIT 50"
        )
        return cursor.fetchall()