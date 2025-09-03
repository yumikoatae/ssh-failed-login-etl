# SSH Failed Login ETL Pipeline

This project implements a mini Extract, Transform, Load (ETL) pipeline to process and analyze SSH failed login logs. Using mock data, it simulates a real-world cybersecurity workflow to detect suspicious patterns, such as brute-force attacks, and generate insightful reports.

## Technologies Used

- Python
- MySQL
- Shell Script
- Pandas
- Matplotlib

## 📂 Project Structure

```plaintext
etl_project/
│
├─ data/
│  └─ mock_auth.log             # Mock SSH failed login logs
│
├─ scripts/
│  ├─ extract.sh                # (Optional) Script to filter raw logs
│  ├─ transform_logs.py         # Script to parse and structure log data
│  ├─ load.py                   # Script to load transformed data into MySQL
│  └─ analyze_logs.py           # Script to analyze data and generate reports
│
├─ sql/
│  └─ 01_create_table.sql       # Database table schema
│
├─ outputs/
│  ├─ top_users.csv             # Users with the most failed logins
│  ├─ top_users.png             # Chart of top users by failed logins
│  ├─ top_ips.csv               # IPs with the most failed logins
│  ├─ top_ips.png               # Chart of top IPs by failed logins
│  ├─ suspicious_ips.csv        # IPs flagged as potentially malicious
│  └─ suspicious_ips.png        # Chart of suspicious IPs
│
└─ .env                          # File for database credentials (not committed to Git)
```

## ✨ How It Works

The pipeline is a modular workflow designed to process log data from its raw format into actionable insights.

### 1. Extraction

The `scripts/extract.sh` script performs the initial extraction. It uses `grep` to efficiently filter a large, raw log file, isolating only the lines containing "Failed password". This creates a smaller, pre-filtered log file, making subsequent steps faster and more focused.

### 2. Transformation

The `scripts/transform_logs.py` script reads the pre-filtered log entries. Using regular expressions (regex), it parses each line to extract key information:

- The timestamp of the failed attempt.
- The username being targeted.
- The source IP address of the attempt.

The extracted data is then cleaned, standardized (e.g., converting the timestamp to a consistent format), and structured into a tabular format, which is then saved as a CSV file.

### 3. Load

The `scripts/load.py` script takes the structured CSV data and loads it into a `failed_logins` table in a MySQL database. This makes the data persistent and allows for efficient querying and analysis.

### 4. Analysis

Finally, `scripts/analyze_logs.py` queries the database to:

- Identify the top users and IP addresses with the highest number of failed login attempts.
- Flag suspicious IPs based on a defined threshold (in this mock scenario, any IP with more than two failures is considered suspicious).
- Generate summary reports in both `.csv` and `.png` (chart) formats, saving them to the `outputs/` directory.

## 🚀 Setup and Execution

Follow these steps to set up and run the project locally.

### 1. Prerequisites

- Python 3.8+
- A running MySQL server
- Git and a Unix-like environment (for the bash script)

### 2. Clone the Repository

```bash
git clone https://github.com/yumikoatae/ssh-failed-login-etl.git
cd ssh-failed-login-etl
```

### 3. Install Dependencies

It is recommended to use a virtual environment.

```bash
# Optional: Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install required packages
pip install pandas mysql-connector-python python-dotenv matplotlib
```

### 4. Configure the Database

Log in to your MySQL server and create a new database.

```sql
CREATE DATABASE logs;
```

Run the SQL script to create the `failed_logins` table within the `logs` database.

```bash
# Example of how to run the script from the command line
mysql -u your_user -p logs < sql/01_create_table.sql
```

Create a `.env` file in the root of the project directory. Add your database credentials as follows:

```env
DB_USER=root DB_PASSWORD=your_password_here DB_HOST=127.0.0.1 DB_NAME=logs
```

### 5. Run the Pipeline

Execute the scripts in the correct order to process the data from end to end.

```bash
# 1. (Optional ) Filter the raw log file to extract only failed attempts
# This step is only needed if your source log contains more than just failed logins.
bash scripts/extract.sh

# 2. Transform the filtered logs into structured data
python3 scripts/transform_logs.py

# 3. Load the structured data into the MySQL database
python3 scripts/load.py

# 4. Analyze the data and generate reports
python3 scripts/analyze_logs.py
```

## 📊 Expected Outputs

After running the pipeline, the `outputs/` directory will be populated with the following reports:

- `top_users.csv` / `top_users.png`: A list and a bar chart showing the users with the most failed login attempts.
- `top_ips.csv` / `top_ips.png`: A list and a bar chart showing the IP addresses with the most failed login attempts.
- `suspicious_ips.csv` / `suspicious_ips.png`: A report identifying IPs that have exceeded the failure threshold, indicating a potential brute-force attack.


