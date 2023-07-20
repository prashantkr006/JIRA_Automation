import tkinter as tk
from tkinter import ttk
from api.jira_api import fetch_all_tickets
from api.database_manager import create_database, save_ticket_to_database, fetch_all_tickets_from_database


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("JIRA Automation with Python")
        self.geometry("1200x600")

        # Add a Reload button
        self.reload_button = tk.Button(
            self,
            text="Reload Tickets",
            command=self.reload_tickets
        )
        self.reload_button.pack()

        # Create a Treeview to display tickets in a table format
        self.tree = ttk.Treeview(self, columns=("Number", "Name", "Description", "Reporter", "Status", "Due Date"), show="headings")
        self.tree.heading("Number", text="Number")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Reporter", text="Reporter")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Load initial tickets from the database
        self.load_tickets_from_database()

    def load_tickets_from_database(self):
        # Fetch all tickets from the database
        tickets = fetch_all_tickets_from_database()

        # Display the tickets in the Treeview
        self.tree.delete(*self.tree.get_children())
        for ticket in tickets:
            self.tree.insert("", tk.END, values=(
                ticket["number"],
                ticket["name"],    # Make sure to use the correct key here
                ticket["description"],   # Make sure to use the correct key here
                ticket["reporter"],   # Make sure to use the correct key here
                ticket["status"],     # Make sure to use the correct key here
                ticket["due Date"]
            ))

    def reload_tickets(self):
        all_tickets = fetch_all_tickets()

        if all_tickets:
            create_database()
            for ticket in all_tickets:
                save_ticket_to_database(ticket)

            # Load updated tickets from the database
            self.load_tickets_from_database()
        else:
            print("Failed to reload tickets. Please check the console for details.")

if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()
