import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",   # replace with your MySQL password
)

cursor = db.cursor()

# Step 1: Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS client_query_db;")
cursor.execute("USE client_query_db;")

# Step 2: Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('Client', 'Support') NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_email VARCHAR(255),
    client_mobile VARCHAR(20),
    query_heading VARCHAR(255),
    query_description TEXT,
    status ENUM('Open', 'Closed') DEFAULT 'Open',
    date_raised DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_closed DATETIME NULL
);
""")

print("Database and tables created successfully!")

db.close()

