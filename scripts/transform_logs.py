# transform_logs.py
import re
import pandas as pd
from datetime import datetime
import os

INPUT = "data/mock_auth.log"
OUTPUT = "data/failed_logins.csv"

data = []

# Regex to extract timestamp, username and IP
# Example line:
# "Sep  3 10:12:34 myhost sshd[12345]: Failed password for root from 192.168.0.1 port 22 ssh2"
pattern = re.compile(r"^(\w+\s+\d+\s+\d+:\d+:\d+).+Failed password for (\w+) from ([\d\.]+)")

with open(INPUT) as f:
    for line in f:
        match = pattern.search(line)
        if match:
            timestamp_str = match.group(1)
            # Convert to datetime (use current year)
            timestamp = datetime.strptime(timestamp_str + f" {datetime.now().year}", "%b %d %H:%M:%S %Y")
            username = match.group(2)
            ip = match.group(3)
            data.append([timestamp, username, ip])

# Create DataFrame
df = pd.DataFrame(data, columns=['timestamp', 'username', 'ip'])

# Ensure data folder exists
os.makedirs("data", exist_ok=True)
df.to_csv(OUTPUT, index=False)
print(f"Transformation completed! {len(df)} rows written to {OUTPUT}")

