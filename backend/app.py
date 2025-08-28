import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from .insights import calculate_insights
from .dummy_data import DUMMY_WEIGHTS_ERIC

app = Flask(__name__)
CORS(app)
app.config['Database'] = './databases/database.db'

def insert_dummy_weights(cursor):
    for user_id, weight, entry_date in DUMMY_WEIGHTS_ERIC:
        cursor.execute(
            "INSERT INTO weights (user_id, weight, entry_date) VALUES (?, ?, ?)",
            (user_id, weight, entry_date)
        )

def init_db():
    conn = sqlite3.connect(app.config['Database'])
    cursor = conn.cursor()

    # THIS SHOULD BE REMOVED IF ACTUALLY RELEASING
    # Create a fresh testing database
    drop_users = "DROP TABLE IF EXISTS users"
    drop_weights = "DROP TABLE IF EXISTS weights"
    cursor.execute(drop_weights)
    cursor.execute(drop_users)

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

    # Insert dummy data for eventual layout when loading frontend
    cursor.execute(
            "INSERT INTO users (id, username, password, goal_weight, current_weight) \
                VALUES (?, ?, ?, ?, ?)", 
                (1, "Eric", "password", 170, 180)
        )
    
    insert_dummy_weights(cursor)    

    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(app.config['Database'])
    conn.row_factory = sqlite3.Row
    return conn

init_db()

######################## Flask Routes ##########################
@app.post('/weights')
def add_weight():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    # These are unsafe! Can add validation later
    # TODO: Add authentication
    user_id = data.get('user_id')
    weight = data.get('weight')

    try:
        user_id = int(user_id)
        weight = float(weight)
    except (TypeError, ValueError):
        return jsonify({'error': 'entered types are innacurate'}), 400
    
    # Everything looks good, so get the date and then add to the db
    entry_date = datetime.now().isoformat()
    
    # Format date into YYYY-MM-DD HH:MM:SS
    entry_date = entry_date.split('.')[0].replace('T', ' ')
    entry_date = entry_date[:19]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO weights (user_id, weight, entry_date) VALUES (?, ?, ?)', 
        (user_id, weight, entry_date)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Weight entry added successfully'}), 201


@app.get('/weights')
def get_weights():
    # Perform query validation
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    try:
        user_id = int(user_id)

        # TODO: Check if user exists

    except ValueError:
        return jsonify({'error': 'Invalid user_id'}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Maybe add pagination later if needed
    cursor.execute(
        'SELECT weight, entry_date FROM weights WHERE user_id = ? ORDER BY entry_date DESC', 
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    weights = [{'weight': row['weight'], 'entry_date': row['entry_date']} for row in rows]
    return jsonify(weights), 200

@app.get('/insights')
def get_insights():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    try:
        user_id = int(user_id)

        # TODO: Check if user exists
    
    except ValueError:
        return jsonify({'error': 'Invalid user_id'}), 400

    conn = get_db()
    cursor = conn.cursor()
    
    # Grab the user's goal weight
    cursor.execute(
        'SELECT goal_weight FROM users WHERE id = ?', 
        (user_id,)
    )
    row = cursor.fetchone()
    if not row:
        return jsonify({'error': 'User not found'}), 404
    goal_weight = row['goal_weight']

    # Grab the weight entires for the user
    cursor.execute(
        'SELECT weight, entry_date FROM weights WHERE user_id = ? ORDER BY entry_date DESC', 
        (user_id,)
    )
    rows = cursor.fetchall()
    weights = [{'weight': row['weight'], 'entry_date': row['entry_date']} for row in rows]

    # Pass info to the insights function
    insights = calculate_insights(weights, goal_weight)
    return jsonify(insights), 200

if __name__ == '__main__':
    app.run(debug=True)

