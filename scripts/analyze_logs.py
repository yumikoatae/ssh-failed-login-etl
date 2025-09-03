# analyze_logs.py
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# ================================
# Load environment variables
# ================================
load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")

# ================================
# Connect to MySQL
# ================================
conn = mysql.connector.connect(
    user=USER,
    password=PASSWORD,
    host=HOST,
    database=DATABASE
)

# ================================
# Queries
# ================================
# Top users with failed logins
query_users = """
SELECT username, COUNT(*) AS failures 
FROM failed_logins 
GROUP BY username 
ORDER BY failures DESC
"""
df_users = pd.read_sql(query_users, conn)

# Top IPs with failed logins
query_ips = """
SELECT ip, COUNT(*) AS failures 
FROM failed_logins 
GROUP BY ip 
ORDER BY failures DESC
"""
df_ips = pd.read_sql(query_ips, conn)

# Brute-force detection (IPs with more than 2 failures)
query_suspicious = """
SELECT ip, COUNT(*) AS failures
FROM failed_logins
GROUP BY ip
HAVING COUNT(*) > 2
"""
df_suspicious = pd.read_sql(query_suspicious, conn)

conn.close()

# ================================
# Create outputs directory
# ================================
os.makedirs("outputs", exist_ok=True)

# ================================
# Save CSV summaries
# ================================
df_users.to_csv("outputs/top_users.csv", index=False)
df_ips.to_csv("outputs/top_ips.csv", index=False)
df_suspicious.to_csv("outputs/suspicious_ips.csv", index=False)

# ================================
# Plot graphs
# ================================
# Top users
df_users.plot(kind='bar', x='username', y='failures', legend=False)
plt.title("Top Users with Failed Logins")
plt.ylabel("Number of Failures")
plt.tight_layout()
plt.savefig("outputs/top_users.png")
plt.close()

# Top IPs
df_ips.plot(kind='bar', x='ip', y='failures', legend=False)
plt.title("Top IPs with Failed Logins")
plt.ylabel("Number of Failures")
plt.tight_layout()
plt.savefig("outputs/top_ips.png")
plt.close()

# Suspicious IPs
if not df_suspicious.empty:
    df_suspicious.plot(kind='bar', x='ip', y='failures', color='red', legend=False)
    plt.title("Suspicious IPs (Possible Brute Force)")
    plt.ylabel("Number of Failures")
    plt.tight_layout()
    plt.savefig("outputs/suspicious_ips.png")
    plt.close()

print("Analysis completed! CSVs and graphs saved in 'outputs/'")

