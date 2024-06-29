import os
import sqlite3
import json
import requests

# Webhook URL
WEBHOOK_URL = "url"

# Path to the SQLite database
DB_PATH = 'DtfC_database.db'
PREVIOUS_DATA_FILE = 'previous_data.json'

# Function to fetch the current data
def fetch_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch team amounts
    cursor.execute('SELECT * FROM TeamAmounts')
    team_rows = cursor.fetchall()
    
   # Fetch top donors
    cursor.execute('SELECT * FROM TopDonors ORDER BY amount DESC LIMIT 3')
    donor_rows = cursor.fetchall()

    conn.close()

    data = {
        "teams": [{"team": row[0], "raised_amount": row[1]} for row in team_row>
        "top_donors": [{"name": row[1], "amount": row[2]} for row in donor_rows]
    }

    return data

# Function to send data to the webhook
def send_data_to_webhook(data):
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 200:
        print("Data sent successfully to the webhook.")
    else:
        print(f"Failed to send data. Status code: {response.status_code}")
        print(f"Response: {response.text}")

# Function to load previous data
def load_previous_data():
    if os.path.exists(PREVIOUS_DATA_FILE):
        with open(PREVIOUS_DATA_FILE, 'r') as f:
            return json.load(f)
    return None

# Function to save current data
def save_current_data(data):
    with open(PREVIOUS_DATA_FILE, 'w') as f:
        json.dump(data, f)

# Monitor function that runs once
def monitor():
    current_data = fetch_data()
    previous_data = load_previous_data()

    if current_data != previous_data:
        print("Data has changed, sending to webhook...")
        send_data_to_webhook(current_data)
        save_current_data(current_data)
    else:
        print("Data has not changed, not sending to webhook.")

if __name__ == "__main__":
    monitor()
