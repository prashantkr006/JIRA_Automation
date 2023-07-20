import os
import re
import sqlite3

# Database file name and path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(ROOT_DIR, "tickets.db")


def extract_number_from_issue_key(issue_key):
    if isinstance(issue_key, str):
        # Assuming the Issue Key is in the format "PROJ-XX"
        return int(issue_key.split("-")[1])
    elif isinstance(issue_key, set):
        # If issue_key is of type set, convert it to a string and extract the number
        issue_key_str = str(issue_key)
        match = re.search(r'PROJ-(\d+)', issue_key_str)
        if match:
            return int(match.group(1))
        else:
            raise ValueError("Invalid issue_key format. Expected 'PROJ-XX'.")
    else:
        raise ValueError("Invalid issue_key format. Expected str or set.")


def create_database():
    print('Creating Database...')
    # Connect to the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Create the 'tickets' table if it doesn't exist
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS tickets ("
            "Number INTEGER PRIMARY KEY,"
            "name TEXT,"
            "description TEXT,"
            "reporter TEXT,"
            "status TEXT,"
            "due_date TEXT)"
        )

        # Commit the changes to the database
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error creating database table: {e}")

    finally:
        # Close the database connection
        conn.close()


def save_ticket_to_database(ticket_data):
    print('Inserting tickets to database...')
    # Convert None values to None (not 'None' as a string)
    for key, value in ticket_data.items():
        if value is None:
            ticket_data[key] = None
        else:
            ticket_data[key] = str(value)

    # Connect to the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Check if the ticket with the same Issue Key already exists in the database
        cursor.execute("SELECT * FROM tickets WHERE Number = ?",
                       (extract_number_from_issue_key(ticket_data['Issue Key']),))
        existing_ticket = cursor.fetchone()

        if existing_ticket:
            # If the ticket with the same Issue Key exists, update the record
            cursor.execute(
                "UPDATE tickets SET name = ?, description = ?, reporter = ?, status = ?, due_date = ? WHERE Number = ?",
                (
                    ticket_data["Summary"],
                    ticket_data["Description"],
                    ticket_data["Reporter"],
                    ticket_data["Status"],
                    ticket_data["Due Date"],
                    extract_number_from_issue_key(ticket_data['Issue Key']),
                ),
            )
        else:
            # If the ticket doesn't exist, insert a new record
            cursor.execute(
                "INSERT INTO tickets (Number, name, description, reporter, status, due_date) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    extract_number_from_issue_key(ticket_data['Issue Key']),
                    ticket_data["Summary"],
                    ticket_data["Description"],
                    ticket_data["Reporter"],
                    ticket_data["Status"],
                    ticket_data["Due Date"],
                ),
            )

        # Commit the changes to the database
        conn.commit()
        print(
            f"Successfully saved ticket {ticket_data['Issue Key']} to the database.")

    except sqlite3.Error as e:
        print(f"Error saving ticket to database: {e}")

    finally:
        # Close the database connection
        conn.close()


def fetch_all_tickets_from_database(limit=None):
    print('Fetching all the tickets from the database...')
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM tickets")
            
        tickets = cursor.fetchall()

        # Convert the fetched data into a list of dictionaries
        ticket_list = []
        for ticket in tickets:
            ticket_data = {
                "number":ticket[0],
                "name": ticket[1],
                "description": ticket[2],
                "reporter": ticket[3],
                "status": ticket[4],
                "due Date": ticket[5]
            }
            ticket_list.append(ticket_data)

        return ticket_list

    except sqlite3.Error as e:
        print(f"Error fetching tickets from the database: {e}")
        return None

    finally:
        conn.close()
