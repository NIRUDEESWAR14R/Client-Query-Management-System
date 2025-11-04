import streamlit as st
import mysql.connector
import pandas as pd
import hashlib
from datetime import datetime

# ==============================
# DATABASE CONNECTION FUNCTION
# ==============================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",           # your MySQL username
        password="12345",      # your MySQL password
        database="client_queries"  # your MySQL DB name
    )

# ==============================
# PASSWORD HASHING FUNCTION
# ==============================
def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ==============================
# CREATE USERS TABLE
# ==============================
def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(255) PRIMARY KEY,
            password_hash TEXT,
            role VARCHAR(50)
        )
    """)
    conn.commit()
    conn.close()

# ==============================
# CREATE QUERIES TABLE
# ==============================
def create_queries_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255),
            mobile VARCHAR(20),
            query_heading VARCHAR(255),
            query_description TEXT,
            query_created_time DATETIME,
            query_closed_time DATETIME,
            status VARCHAR(20)
        )
    """)
    conn.commit()
    conn.close()

# ==============================
# ADD NEW USER
# ==============================
def add_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                   (username, make_hash(password), role))
    conn.commit()
    conn.close()

# ==============================
# LOGIN VALIDATION
# ==============================
def login_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password_hash=%s AND role=%s",
                   (username, make_hash(password), role))
    data = cursor.fetchone()
    conn.close()
    return data

# ==============================
# INSERT CLIENT QUERY
# ==============================
def insert_query(email, mobile, heading, description):
    conn = get_connection()
    cursor = conn.cursor()
    query_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO queries (email, mobile, query_heading, query_description, query_created_time, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (email, mobile, heading, description, query_time, "Open"))
    conn.commit()
    conn.close()

# ==============================
# FETCH ALL QUERIES
# ==============================
def get_all_queries():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM queries", conn)
    conn.close()
    return df

# ==============================
# CLOSE QUERY
# ==============================
def close_query(query_id):
    conn = get_connection()
    cursor = conn.cursor()
    close_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE queries SET status=%s, query_closed_time=%s WHERE id=%s",
                   ("Closed", close_time, query_id))
    conn.commit()
    conn.close()

# ==============================
# STREAMLIT APP
# ==============================
st.set_page_config(page_title="Client Query Management System", layout="wide")

st.title("📞 Client Query Management System")
st.write("Manage, Track, and Resolve Client Queries Efficiently")

menu = ["Home", "Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

create_users_table()
create_queries_table()

# ==============================
# REGISTER PAGE
# ==============================
if choice == "Register":
    st.subheader("🔐 Create a New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Client", "Support"])

    if st.button("Register"):
        if username and password:
            try:
                add_user(username, password, role)
                st.success(f"Account created successfully for **{username}** as **{role}**!")
            except:
                st.warning("⚠️ Username already exists. Try a different one.")
        else:
            st.error("Please fill all fields.")

# ==============================
# LOGIN PAGE
# ==============================
elif choice == "Login":
    st.subheader("🔑 Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Client", "Support"])

    if st.button("Login"):
        user = login_user(username, password, role)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = role
            st.success(f"Welcome {username} ({role})!")
        else:
            st.error("Invalid credentials. Please check your username/password/role.")

# ==============================
# DASHBOARD (AFTER LOGIN)
# ==============================
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    role = st.session_state["role"]

    if role.lower() == "client":
        st.header("📝 Submit a New Query")
        email = st.text_input("Email ID")
        mobile = st.text_input("Mobile Number")
        heading = st.text_input("Query Heading")
        description = st.text_area("Query Description")

        if st.button("Submit Query"):
            if email and mobile and heading and description:
                insert_query(email, mobile, heading, description)
                st.success("✅ Query submitted successfully!")
            else:
                st.error("Please fill all fields.")

    elif role.lower() == "support":
        st.header("📊 Support Team Dashboard")
        df = get_all_queries()

        if df.empty:
            st.info("No queries found yet.")
        else:
            filter_status = st.selectbox("Filter by Status", ["All", "Open", "Closed"])
            if filter_status != "All":
                df = df[df["status"] == filter_status]

            st.dataframe(df)

            st.subheader("🔧 Close an Open Query")
            open_queries = df[df["status"] == "Open"]
            if not open_queries.empty:
                query_id = st.selectbox("Select Query ID to Close", open_queries["id"].tolist())
                if st.button("Close Query"):
                    close_query(query_id)
                    st.success(f"✅ Query ID {query_id} closed successfully!")
            else:
                st.info("No open queries to close right now.")

# ==============================
# HOME PAGE
# ==============================
else:
    if choice == "Home":
        st.image("https://cdn-icons-png.flaticon.com/512/906/906334.png", width=100)
        st.markdown("""
        ### Welcome to the Client Query Management System  
        This platform allows clients to raise queries and support teams to track and resolve them efficiently.

        **Modules:**
        - 🧑‍💻 Client Login → Submit and track your queries  
        - 🧰 Support Login → Manage and close queries  
        - 🔐 Secure Login System (hashed passwords)
        - 📊 MySQL database integration  
        - ⚡ Streamlit UI for easy use
        """)
