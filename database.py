import sqlite3
import asyncio
import random
import string
from config import Config

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Create tables if they don't exist"""
        conn = self._connect()
        cursor = conn.cursor()
        
        # Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Files Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unique_id TEXT UNIQUE,
                file_id TEXT,
                file_type TEXT,
                user_id INTEGER,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Banned Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS banned_users (
                user_id INTEGER PRIMARY KEY
            )
        """)
        
        conn.commit()
        conn.close()

    async def add_user(self, user_id, username):
        def _add():
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
            conn.commit()
            conn.close()
        await asyncio.to_thread(_add)

    async def is_banned(self, user_id):
        def _check():
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM banned_users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        return await asyncio.to_thread(_check)

    async def ban_user(self, user_id):
        def _ban():
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO banned_users (user_id) VALUES (?)", (user_id,))
            conn.commit()
            conn.close()
        await asyncio.to_thread(_ban)

    async def unban_user(self, user_id):
        def _unban():
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
        await asyncio.to_thread(_unban)

    async def save_file(self, file_id, file_type, user_id):
        unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        def _save():
            conn = self._connect()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO files (unique_id, file_id, file_type, user_id) VALUES (?, ?, ?, ?)", 
                               (unique_id, file_id, file_type, user_id))
                conn.commit()
                return unique_id
            except sqlite3.IntegrityError:
                # Rare collision, retry logic could be added, returning None for simplicity
                return None
            finally:
                conn.close()
        return await asyncio.to_thread(_save)

    async def get_file(self, unique_id):
        def _get():
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT file_id, file_type FROM files WHERE unique_id = ?", (unique_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        return await asyncio.to_thread(_get)

    async def get_stats(self):
        def _stats():
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            users = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM files")
            files = cursor.fetchone()[0]
            conn.close()
            return users, files
        return await asyncio.to_thread(_stats)

    async def get_all_users(self):
        def _get():
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users")
            ids = [row[0] for row in cursor.fetchall()]
            conn.close()
            return ids
        return await asyncio.to_thread(_get)

# Initialize DB
db = Database(Config.DB_PATH)
