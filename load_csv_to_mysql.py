import mysql.connector
import pandas as pd
import math

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="client_query_db"
)

cursor = db.cursor()

# Load CSV
data = pd.read_csv("synthetic_client_queries.csv")

# Clean NaN values
data = data.where(pd.notnull(data), None)

for _, row in data.iterrows():
    cursor.execute("""
        INSERT INTO queries (client_email, client_mobile, query_heading, query_description, status, date_raised, date_closed)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row['client_email'],
        row['client_mobile'],
        row['query_heading'],
        row['query_description'],
        row['status'],
        row['date_raised'],
        row['date_closed']
    ))

db.commit()
cursor.close()
db.close()

print("CSV data inserted successfully!")

