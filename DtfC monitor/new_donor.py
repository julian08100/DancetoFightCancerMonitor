import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import json

# URLs for the two teams
urls = {
    "team": "url>
    "team": "url>
}

# Webhook URL
WEBHOOK_URL = "url"

# Path to the SQLite database
DB_PATH = 'donors_database.db'

# Function to fetch donors from a given URL
def fetch_donors(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")
        donors = []

        donation_elements = soup.find_all("div", class_="donation-filter")
        for donation in donation_elements:
            amount = float(donation["data-amount"])
            name = donation["data-name"]
            donors.append({"name": name, "amount": amount})

        return donors
    except requests.RequestException as e:
        print(f"Error fetching donors from {url}: {e}")
        return []

# Function to load previous donors from the database
def load_previous_donors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Donors (name TEXT, amount REAL, >
    cursor.execute('SELECT * FROM Donors')
    previous_donors = cursor.fetchall()
    conn.close()
    return previous_donors

# Function to save new donors to the database
def save_new_donors(new_donors):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for donor in new_donors:
        cursor.execute('INSERT INTO Donors (name, amount, team) VALUES (?, ?, ?>
    conn.commit()
    conn.close()

# Function to get new donors
def get_new_donors():
    new_donors = []
    previous_donors = load_previous_donors()

    for team, url in urls.items():
        donors = fetch_donors(url)
        for donor in donors:
            if (donor["name"], donor["amount"], team) not in previous_donors:
                donor["team"] = team
                new_donors.append(donor)

    return new_donors

# Function to send donors to the webhook
def send_donors_to_webhook(donors):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(WEBHOOK_URL, data=json.dumps(donors), headers=head>
    if response.status_code == 200:
        print("Donor sent successfully to the webhook.")
    else:
        print(f"Failed to send donor. Status code: {response.status_code}")
        print(f"Response: {response.text}")

def main():
    donor_queue = []

    while True:
        print("Fetching new donors...")
        new_donors = get_new_donors()
        if new_donors:
            print(f"Found {len(new_donors)} new donors.")
            donor_queue.extend(new_donors)
            save_new_donors(new_donors)
        else:
            print("No new donors found.")

        # Load previous donors if the queue is empty or insufficient
        if len(donor_queue) == 0:
            previous_donors = load_previous_donors()
            donor_queue.extend(previous_donors)

        if donor_queue:
            donor_to_send = donor_queue.pop(0)
            print(f"Sending donor {donor_to_send} to webhook...")
            send_donors_to_webhook([donor_to_send])
            print("Waiting for 60 seconds before sending the next donor...")
            time.sleep(60)  # Wait for 1 minute
        else:
            print("No donors in the queue. Waiting for the next check.")
            time.sleep(120)  # Wait for 1 minute if no donors are found

if __name__ == "__main__":
    main()

