# api/jira_api.py
import requests
from requests.auth import HTTPBasicAuth

# CONSTANTS
email = "prashantkr006@gmail.com"
api_token = "ATATT3xFfGF0wbjX7-CcOvRwfGdAjI6Zph6QfcTgcvUxMpQh4vYwDSgy3mt-GDzyz4EfDX3hzI3fQXV8qdXGPlhe9BYBDTqRDhBziDZyWW4IwPocB9GJmDZf00Z6A1u-uQfBeJJefbzFA_zCzNAsCoX2svo1UL0cCMBotf8jbroQh9LIaVAArZM=900B6CB8"
jira_domain = "prashantkr006"


def fetch_all_tickets(limit=100, start_at=0):
    print(
        f"Fetching page {start_at//limit + 1} (limit: {limit}) of tickets from Jira...")
    # specific Jira domain
    url = f"https://{jira_domain}.atlassian.net/rest/api/2/search"

    auth = HTTPBasicAuth(email, api_token)

    # JQL query to fetch all issues (remove or customize the JQL as needed)
    jql_query = "project = PROJ"

    headers = {
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers,
                                auth=auth, params={"jql": jql_query, "maxResults": limit, "startAt": start_at})

        # clear

        response.raise_for_status()
        data = response.json()

        # Extract information from the API response
        total_issues = data.get("total", 0)
        issues = data.get("issues", [])

        # Check if there are any issues returned by the API
        if not issues:
            print("No issues found in Jira.")
            return []

        # Initialize a list to store the formatted ticket data
        formatted_tickets = []
        for issue in issues:
            # Extract ticket data
            issue_key = issue['key']
            summary = issue['fields'].get('summary', 'N/A')
            description = issue['fields'].get('description', 'N/A')
            reporter = issue['fields'].get('reporter', {}).get(
                'displayName', 'Unassigned')
            status = issue['fields'].get('status', {}).get('name', 'Unknown')
            due_date = issue['fields'].get('duedate', 'N/A')

            # Format the ticket data
            formatted_ticket = {
                "Issue Key": issue_key,
                "Summary": summary,
                "Description": description,
                "Reporter": reporter,
                "Due Date": due_date,
                "Status": status,
            }
            print(formatted_ticket)
            # Append the formatted ticket to the list
            formatted_tickets.append(formatted_ticket)

        print(f"Total issues in Jira: {total_issues}")
        return formatted_tickets

    except requests.RequestException as e:
        print(f"API call failed with error: {e}")
        return None

    except ValueError as e:
        print(f"JSON decoding error: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_transitions_for_issue(issue_key):
    print('finding transition Id')

    # Replace "your-domain" with your specific Jira domain
    url = f"https://{jira_domain}.atlassian.net/rest/api/2/issue/{issue_key}/transitions"

    auth = HTTPBasicAuth(email, api_token)

    headers = {
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, auth=auth)

        # Check the status code of the API response
        response.raise_for_status()

        data = response.json()
        transitions = data.get("transitions", [])

        for transition in transitions:
            if transition.get("to", {}).get("name") == "Close":
                return transition.get("id")

        print("Transition ID not found for 'Close' status.")
        return None

    except requests.RequestException as e:
        print(f"API call failed with error: {e}")
        return None

    except ValueError as e:
        print(f"JSON decoding error: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def update_ticket_status_and_comment(issue_key, transition_id, comment):

    print('updating ticket status to close by commenting on it...')
    url = f"https://{jira_domain}.atlassian.net/rest/api/2/issue/{issue_key}/transitions"
    auth = HTTPBasicAuth(email, api_token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "transition": {
            "id": transition_id
        },
        "update": {
            "comment": [
                {
                    "add": {
                        "body": comment
                    }
                }
            ]
        }
    }

    try:
        response = requests.post(url, headers=headers, auth=auth, json=payload)

        # Check the status code of the API response
        response.raise_for_status()

        print(
            f"Ticket {issue_key} status updated to 'Close' with the following comment:")
        print(comment)

    except requests.RequestException as e:
        print(f"API call failed with error: {e}")

    except ValueError as e:
        print(f"JSON decoding error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
