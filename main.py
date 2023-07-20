# main.py

import argparse
from api.jira_api import fetch_all_tickets, get_transitions_for_issue, update_ticket_status_and_comment
from api.database_manager import create_database, save_ticket_to_database
from UI.main_window import MainWindow

def main():
    parser = argparse.ArgumentParser(description='JIRA Automation with Python')

    # Add optional arguments for fetching and inserting data
    parser.add_argument("--fetch", action="store_true",
                        help="Fetch all tickets from Jira")
    parser.add_argument("--insert", action="store_true",
                        help="Insert all fetched tickets into the database")
    parser.add_argument("--limit", type=int, default=100,
                        help="Number of tickets to fetch per page (default is 5)")
    parser.add_argument("--page", type=int, default=0,
                        help="Page number to fetch (default is 1)")

    # Add optional arguments for updating a ticket
    parser.add_argument("--update", action="store_true",
                        help="Update the status and add a comment for a specific ticket")
    parser.add_argument("--issue_key", type=str,
                        help="Issue key of the ticket to update")
    parser.add_argument("--comment", type=str,
                        help="Comment to add for the ticket")

    # Add optional argument for launching the GUI
    parser.add_argument("--gui", action="store_true",
                        help="Launch the MainWindow GUI")

    args = parser.parse_args()

    # If the '--fetch' argument is provided, fetch tickets from Jira
    if args.fetch:
        # Calculate the start index for pagination based on the page number and limit
        start_at = (args.page - 1) * args.limit

        print(
            f"Fetching page {args.page} (limit: {args.limit}) of tickets from Jira...")
        all_tickets = fetch_all_tickets(limit=args.limit, start_at=start_at)

        # Check if tickets were fetched successfully before processing them
        if all_tickets is not None:
            # If the '--insert' argument is provided, insert all fetched tickets into the database
            if args.insert:
                create_database()
                for ticket in all_tickets:
                    save_ticket_to_database(ticket)
                print("All fetched tickets have been inserted into the database.")
            else:
                # If '--insert' argument is not provided, simply display the fetched tickets
                for ticket in all_tickets:
                    print(ticket)
        else:
            print("Failed to fetch tickets from Jira. Please check your Jira settings and credentials.")

    # If the '--update' argument is provided, update the status and add a comment for the specific ticket
    if args.update:
        if args.issue_key and args.comment:
            print("Updating ticket status and adding comment...")
            transition_id = get_transitions_for_issue(args.issue_key)
            update_ticket_status_and_comment(
                args.issue_key, transition_id, args.comment)
        else:
            print("Please provide both --issue_key and --comment arguments to update the ticket.")

    # If the '--gui' argument is provided, launch the GUI
    if args.gui:
        print("Launching the GUI...")
        window = MainWindow()
        window.mainloop()


if __name__ == "__main__":
    main()
