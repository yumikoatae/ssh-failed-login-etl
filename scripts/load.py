# load.py
from dotenv import load_dotenv
import os
import pandas as pd
import mysql.connector

# ================================
# Load environment variables
# ================================
load_dotenv()  

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")
TABLE = "failed_logins"

# ================================
# Read transformed CSV
# ================================
INPUT_CSV = "data/failed_logins.csv"
df = pd.read_csv(INPUT_CSV)

# ================================
# Connect to MySQL
# ================================
conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)
cursor = conn.cursor()

# ================================
# Create table if it doesn't exist
# ================================
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    username VARCHAR(50),
    ip VARCHAR(50)
)
""")

# ================================
# Clear table before inserting (optional)
# ================================
cursor.execute(f"TRUNCATE TABLE {TABLE}")

# ================================
# Insert data from CSV
# ================================
for _, row in df.iterrows():
    cursor.execute(f"""
    INSERT INTO {TABLE} (timestamp, username, ip)
    VALUES (%s, %s, %s)
    """, (row['timestamp'], row['username'], row['ip']))

# ================================
# Commit and close connection
# ================================
conn.commit()
conn.close()

print("Load completed!")

