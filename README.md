<h1>JIRA Automation with Python</h1>

<p>This project aims to automate JIRA tasks using Python. It provides a command-line interface to fetch JIRA tickets, update their status, and store them in a local SQLite database. Additionally, it offers a graphical user interface (GUI) built with Tkinter for a more user-friendly experience.</p>

<h2>Setup</h2>

<ol>
  <li>Clone the repository:</li>
  <pre><code>git clone https://github.com/prashantkr006/JIRA_Automation.git
  cd JIRA_Automation</code></pre>
  
  <li>Install the required packages:</li>
  <pre><code>pip install -r requirements.txt</code></pre>
  
  <li>Configure your JIRA domain, email, and API token in <code>api/jira_api.py #CONSTANTS</code>.</li>
</ol>

<h2>Commands</h2>

<ol>
  <li><strong>Fetch all tickets from Jira:</strong></li>
  <pre><code>python main.py --fetch [--limit LIMIT] [--page PAGE]</code></pre>
  
  <p>Fetches JIRA tickets and displays their information in the terminal. You can optionally specify the <code>--limit</code> parameter to fetch a specific number of tickets and the <code>--page</code> parameter to fetch tickets from a specific page. If no <code>--limit</code> and <code>--page</code> are provided, it will fetch all the tickets from all pages.</p>
  
  <p><strong>Example:</strong></p>
  <pre><code>python main.py --fetch --limit 10 --page 1</code></pre>
  <p>This command will fetch the first 10 tickets from Jira on page 1.</p>
  
  <li><strong>Insert fetched tickets into the database:</strong></li>
  <pre><code>python main.py --fetch --insert [--limit LIMIT] [--page PAGE]</code></pre>
  
  <p>Fetches JIRA tickets and inserts them into the local SQLite database. You can optionally specify the <code>--limit</code> parameter to fetch and insert a specific number of tickets and the <code>--page</code> parameter to fetch tickets from a specific page. If no <code>--limit</code> and <code>--page</code> are provided, it will fetch all the tickets from all pages and insert them into the database.</p>
  
  <p><strong>Example:</strong></p>
  <pre><code>python main.py --fetch --insert --limit 5 --page 2</code></pre>
  <p>This command will fetch 5 tickets from Jira on page 2 and insert them into the database.</p>
  
  <li><strong>Update the status and add a comment for a specific ticket:</strong></li>
  <pre><code>python main.py --update ISSUE_KEY COMMENT</code></pre>
  
  <p>Updates the status of the ticket with the provided <code>ISSUE_KEY</code> and adds the <code>COMMENT</code>. This command will change the status of the issue from open to close and add the comment to close the issue.</p>
  
  <p><strong>Example:</strong></p>
  <pre><code>python main.py --update PROJ-22 "My comment to close the issue."</code></pre>
  <p>This command will update the status of the ticket with the issue key <code>PROJ-22</code> and add the comment to close the issue.</p>
</ol>

<h2>Graphical User Interface (GUI)</h2>

<p>The project includes a user-friendly GUI built with Tkinter. To launch the GUI, run the following command:</p>
<pre><code>python main.py --gui</code></pre>

<p>The GUI window will open, displaying all the tickets fetched from Jira. It also provides the following features:</p>

<ul>
  <li><strong>Refresh Button:</strong> Clicking on the "Refresh" button will re-fetch or reload new tickets, if any, from Jira and update the displayed data in the GUI.</li>
  <li><strong>Insert Tickets to Database:</strong> The GUI also provides an "Insert to Database" button. Clicking on this button will insert all the fetched tickets into the local SQLite database.</li>
  <li><strong>Update Ticket Status and Comment:</strong> To update the status and add a comment for a specific ticket, select the ticket from the list and click on the "Update Status" button. You will be prompted to enter the comment, and the status will be updated accordingly.</li>
</ul>

<h2>Note</h2>

<p>Before running any commands or the GUI, make sure you have properly configured your JIRA domain, email, and API token in <code>api/jira_api.py #CONSTANTS</code>.</p>

<p>Enjoy automating your JIRA tasks with Python and the user-friendly GUI! 🚀</p>

<hr>

<p><strong>Disclaimer:</strong> This project is for educational purposes and should be used responsibly and in accordance with JIRA's terms of service.</p>
