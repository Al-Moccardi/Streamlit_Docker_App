#Author: Alberto Moccardi
# Version: 1.0  
# Date: 2024-07-08
# Deep Learning for predictive maintenance course

import sqlite3
import random
import string
import time

# Database connection details
DB_PATH = 'data/users.db'

# Function to generate a random username
def generate_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

# Function to generate a random password
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Function to generate a random user
def generate_user():
    user = {
        'username': generate_username(),
        'password': generate_password(),
        'age': random.randint(18, 70),  # Age range from 18 to 70
        'annual_income': random.randint(1, 150),  # Annual income in thousands
        'spending_score': random.randint(1, 100)  # Spending score from 1 to 100
    }
    return user

# Function to insert user data into the database
def insert_user_to_db(user, db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO users (username, password, age, annual_income, spending_score) 
                VALUES (:username, :password, :age, :annual_income, :spending_score)
            ''', user)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting user into database: {e}")

# Ensure the users table exists
def create_users_table():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    age INTEGER,
                    annual_income REAL,
                    spending_score INTEGER
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating users table: {e}")

def main():
    create_users_table()
    while True:
        user = generate_user()
        insert_user_to_db(user, DB_PATH)
        print(f"Inserted user: {user}")
        time.sleep(1)  # Wait for 1 second

if __name__ == "__main__":
    main()
