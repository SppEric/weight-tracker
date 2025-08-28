import sqlite3
from flask import Flask, request, jsonify
from datetime import date
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            goal_weight REAL,
            current_weight REAL
        )  
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weights (
            id INTEGER,
            user_id INTEGER,
            weight REAL,
            entry_date TEXT,
            PRIMARY KEY (id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


init_db()
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

print(get_db().execute('SELECT * FROM users').fetchall())