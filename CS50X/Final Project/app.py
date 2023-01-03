from flask import Flask, render_template, request, redirect
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Create a new Flask app
app = Flask(__name__)


@app.route("/")
def index():
    # Get the server ID from the query parameters of the request
    server_id = request.args.get("server")

    # If a server ID is present in the query parameters
    if server_id:
        # Retrieve the server information from the database
        server = db.execute("SELECT * FROM servers WHERE id = ?", server_id)

        # If the server is found in the database
        if len(server) == 1:
            # Retrieve data for the server from the database, ordered by date
            data = db.execute("SELECT * FROM data WHERE server_id = ? ORDER BY date", server_id)
            # Render the stats template with the server and data information
            return render_template("stats.html", server=server[0], data=data)

        # If the server is not found in the database
        else:
            # Redirect the user back to the root route
            return redirect("/")

    # If no server ID is present in the query parameters
    else:
        # Retrieve a list of all servers from the database
        server_list = db.execute("SELECT * FROM servers")
        # Render a template with the list of servers
        return render_template("index.html", server_list=server_list)
