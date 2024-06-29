import sqlite3

def display_current_data():
    conn = sqlite3.connect('DtfC_database.db')
    cursor = conn.cursor()

    # Fetch team amounts
    cursor.execute('SELECT * FROM TeamAmounts')
    team_rows = cursor.fetchall()

    # Fetch top donors
    cursor.execute('SELECT * FROM TopDonors ORDER BY amount DESC LIMIT 3')
    donor_rows = cursor.fetchall()

    # Close the connection
    conn.close()

    print("Current Team Amounts:")
    for row in team_rows:
        print(f"Team: {row[0]}, Raised Amount: {row[1]}")
        
    print("\nCurrent Top 3 Donors:")
    for row in donor_rows:
        print(f"Name: {row[1]}, Amount: €{row[2]:.2f}")

def update_team_amount(team, amount):
    conn = sqlite3.connect('DtfC_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO TeamAmounts (team, raised_amount)
        VALUES (?, ?)
    ''', (team, amount))
    conn.commit()
    conn.close()
    print(f"Updated {team} with amount {amount}")

def update_top_donor(name, amount, rank):
    conn = sqlite3.connect('DtfC_database.db')
    cursor = conn.cursor()

   # Check if the rank is valid
    if rank < 1 or rank > 3:
        print("Rank must be between 1 and 3")
        return

    # Fetch current top donors
    cursor.execute('SELECT * FROM TopDonors ORDER BY amount DESC LIMIT 3')
    donor_rows = cursor.fetchall()

    if rank <= len(donor_rows):
        donor_id = donor_rows[rank - 1][0]
        cursor.execute('''
            UPDATE TopDonors
            SET name = ?, amount = ?
            WHERE id = ?
        ''', (name, amount, donor_id))
    else:
        cursor.execute('''
            INSERT INTO TopDonors (name, amount)
            VALUES (?, ?)
        ''', (name, amount))

    conn.commit()
    conn.close()
    print(f"Updated top donor at rank {rank} with name {name} and amount €{amou>

def get_existing_teams():
    conn = sqlite3.connect('DtfC_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT team FROM TeamAmounts')
    teams = [row[0] for row in cursor.fetchall()]
    conn.close()
    return teams

if __name__ == "__main__":
    while True:
        display_current_data()
        print("\nOptions:")
        print("1. Update team amount")
        print("2. Update top donor")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            existing_teams = get_existing_teams()
            print("\nExisting Teams:")
            for idx, team in enumerate(existing_teams, start=1):
                print(f"{idx}. {team}")
            team_choice = int(input("Select a team by number: ").strip())
            if 1 <= team_choice <= len(existing_teams):
                team = existing_teams[team_choice - 1]
                amount = input(f"Enter new raised amount for {team}: ").strip()
                update_team_amount(team, amount)
            else:
                print("Invalid team selection.")
        elif choice == "2":
            name = input("Enter donor name: ").strip()
            amount = float(input("Enter donor amount: ").strip())
            rank = int(input("Enter donor rank (1-3): ").strip())
            update_top_donor(name, amount, rank)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
