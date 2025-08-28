import pytest
import sqlite3
from backend.app import app, get_db, init_db
from datetime import datetime

def init_db_test():
    conn = sqlite3.connect(app.config['Database'])
    cursor = conn.cursor()

    # Create a fresh testing database
    drop_users = "DROP TABLE IF EXISTS users"
    drop_weights = "DROP TABLE IF EXISTS weights"
    cursor.execute(drop_weights)
    cursor.execute(drop_users)

    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            goal_weight REAL,
            current_weight REAL
        )  
    ''')

    cursor.execute('''
        CREATE TABLE weights (
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

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['Database'] = 'test.db'
    init_db_test()

    with app.test_client() as client:
        # Insert sample users
        db = get_db()
        db.execute(
            "INSERT INTO users (id, username, password, goal_weight, current_weight) \
                VALUES (?, ?, ?, ?, ?)", 
                (1, "Eric", "password", 170, 180)
        )
        db.execute(
            "INSERT INTO users (id, username, password, goal_weight, current_weight) \
                VALUES (?, ?, ?, ?, ?)", 
                (2, "Richard", "password!", 250, 240)
        )
        db.commit()
        yield client
    
def sample_weights():
    return [
        (1, 1, 70.5, '2023-10-01 10:00:00'),
        (2, 1, 69.8, '2023-10-02 10:00:00'),
        (3, 2, 80.0, '2023-10-01 11:00:00'),
    ]

def test_add_weight(client):
    # Add a weight entry for Eric
    weights = sample_weights()
    eric_post = weights[0]
    response = client.post('/weights', json={
        'user_id': eric_post[1],
        'weight': eric_post[2],
        'entry_date': eric_post[3]
    })
    assert response.status_code == 201

    # Add another one for Richard
    richard_post = weights[2]
    response = client.post('/weights', json={
        'user_id': richard_post[1],
        'weight': richard_post[2],
        'entry_date': richard_post[3]
    })
    assert response.status_code == 201

def test_get_weights(client):
    # Add sample weights
    weights = sample_weights()
    for w in weights:
        client.post('/weights', json={
            'user_id': w[1],
            'weight': w[2],
            'entry_date': w[3]
        })

    # Get weights for Eric
    res = client.get('/weights', query_string={'user_id': 1})
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 2
    assert data[0]['weight'] == 70.5
    assert data[1]['weight'] == 69.8


# THIS IS INTENDED, in future will add correct response for user not existing
def test_get_weights_empty(client):
    # No weights for user 3
    res = client.get('/weights', query_string={'user_id': 3})
    assert res.status_code == 200
    data = res.get_json()
    assert data == []

# TODO: Add tests for invalid inputs, user not existing, more complex operations, etc.