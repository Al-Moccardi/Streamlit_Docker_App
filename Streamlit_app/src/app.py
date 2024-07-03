# Author: Alberto Moccardi
# Version: 1.0  
# Date: 2024-07-08
# Deep Learning for predictive maintenance course


import streamlit as st
import sqlite3
import os
from hashlib import sha256

# Setup the database directory and path
db_dir = 'data'
db_file = 'users.db'
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, db_file)

# Function to create the users table
def create_users_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT,
            age INTEGER,
            annual_income REAL,
            spending_score INTEGER)
    ''')
    conn.commit()
    conn.close()

# Function to add new user data
def add_userdata(username, password, age, annual_income, spending_score):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password, age, annual_income, spending_score) VALUES (?, ?, ?, ?, ?)',
              (username, password, age, annual_income, spending_score))
    conn.commit()
    conn.close()

# Function to login user
def login_user(username, password):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return data

# Hashing function for passwords
def make_hashes(password):
    return sha256(str.encode(password)).hexdigest()

# Main function defining the app's interface and logic
def main():
    st.title("Welcome to Our Streamlit App")

    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to Our Advanced Customer Segmentation Tool")
        st.markdown("""
            - Explore different segments of customers based on real-time data analysis.
            - Engage with visual analytics to understand customer behaviors.
            - Customize your strategies with actionable insights.
        """)
        st.image("https://source.unsplash.com/collection/190727/800x300", caption="Customer Engagement")

    elif choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.button("Login"):
            create_users_table()
            hashed_pswd = make_hashes(password)
            result = login_user(username, hashed_pswd)
            if result:
                st.success(f"Logged In as {username}")
                st.balloons()
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        age = st.number_input("Age", min_value=18)
        annual_income = st.number_input("Annual Income (k$)", min_value=0, format='%d')
        spending_score = st.number_input("Spending Score (1-100)", min_value=0, max_value=100, format='%d')
        if st.button("Signup"):
            create_users_table()
            add_userdata(new_user, make_hashes(new_password), age, annual_income, spending_score)
            st.success("You have successfully created a valid account")
            st.info("Go to the Login Menu to login")

if __name__ == '__main__':
    main()
