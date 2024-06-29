import requests
from bs4 import BeautifulSoup
import sqlite3

def get_raised_amount(url):
    try:
        print(f"Fetching raised amount from {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        raised_amount_div = soup.find("div", class_="iveRaised pull-left")
        if raised_amount_div:
            raised_amount = raised_amount_div.find("h3", class_="money").text.strip()
            print(f"Raised amount fetched successfully: {raised_amount}")
            return raised_amount
        else:
            print("Raised amount div not found.")
            return "Could not find the raised amount on the page."
    except requests.RequestException as e:
        print(f"Error fetching raised amount: {e}")
        return "Error fetching raised amount"

def get_top_donors(url):
    try:
        print(f"Fetching top donors from {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        donors = []

        donation_elements = soup.find_all("div", class_="donation-filter")
        for donation in donation_elements:
            amount = float(donation["data-amount"]) - 0.89  # Remove 89 cents
            name = donation["data-name"]
            donors.append((name, amount))

        donors.sort(key=lambda x: x[1], reverse=True)
        top_donors = donors[:3]
        print(f"Top donors fetched successfully: {top_donors}")
        return top_donors
    except requests.RequestException as e:
        print(f"Error fetching top donors: {e}")
        return []

# URLs for the two teams
urls = {
    "team": "url",
    "team": "url"
}

all_donors = []
team_raised_amounts = {}

for team, url in urls.items():
    raised_amount = get_raised_amount(url)
    team_raised_amounts[team] = raised_amount
    top_donors = get_top_donors(url)
    all_donors.extend(top_donors)

all_donors.sort(key=lambda x: x[1], reverse=True)
top_three_donors = all_donors[:3]

# Create or connect to SQLite database
conn = sqlite3.connect('DtfC_database.db')
cursor = conn.cursor()

# Create tables if not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TeamAmounts (
        team TEXT PRIMARY KEY,
        raised_amount TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS TopDonors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        amount REAL
    )
''')

# Insert or update team amounts
for team, amount in team_raised_amounts.items():
    cursor.execute('''
        INSERT OR REPLACE INTO TeamAmounts (team, raised_amount)
        VALUES (?, ?)
    ''', (team, amount))

# Clear and insert top donors
cursor.execute('DELETE FROM TopDonors')
for donor in top_three_donors:
    cursor.execute('''
        INSERT INTO TopDonors (name, amount)
        VALUES (?, ?)
    ''', (donor[0], donor[1]))

# Commit and close
conn.commit()
conn.close()

print("Data has been saved to the database.")
