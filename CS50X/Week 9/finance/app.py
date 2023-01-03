import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    id = session["user_id"]
    portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = ?", id)
    list = []
    total = 0
    for stock in portfolio:
        data = lookup(stock["stock"])
        data["shares"] = stock["shares"]
        data["total"] = usd(stock["shares"] * data["price"])
        total += data["price"]
        data["price"] = usd(data["price"])
        list.append(data)

    balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    total += int(balance)

    return render_template("index.html", data=list, balance=usd(balance), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    balance = int(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol and not shares:
            return apology("all fields are required")

        if not shares.isnumeric() or int(shares) < 1:
            return apology("shares must be a positive number")

        shares = int(shares)

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol")
        price = quote["price"]
        total = price * shares

        if balance < total:
            return apology("insufficient funds")
        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", balance - total, session["user_id"])
            currently = db.execute("SELECT shares FROM portfolio WHERE user_id = ? AND stock = ?", session["user_id"], symbol)
            if currently:
                db.execute("UPDATE portfolio SET shares = ? WHERE user_id = ? AND stock = ?",
                           currently + shares, session["user_id"], symbol)
            else:
                db.execute("INSERT INTO portfolio (user_id, stock, shares) VALUES (?, ?, ?)", session["user_id"], symbol, shares)

            db.execute("INSERT INTO history (user_id, action, stock, price, shares) VALUES (?, 'BUY', ?, ?, ?)",
                       session["user_id"], symbol, price, shares)
            return redirect("/")

    else:
        return render_template("buy.html", balance=usd(balance))


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return render_template("history.html", history=db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY time DESC", session["user_id"]))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Invalid symbol")

        quote["price"] = usd(quote["price"])
        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Must provide username")

        if len(db.execute("SELECT * FROM users WHERE username = ?", username)) != 0:
            return apology("Username is already taken")

        password = request.form.get("password")
        if not password:
            return apology("Must provide password")

        confirmation = request.form.get("confirmation")
        if confirmation != password:
            return apology("confirmation those not matches password")

        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ? AND hash = ?", username, hash)[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares.isnumeric():
            return apology("invalid number of shares")

        shares = int(shares)
        owned_shares = db.execute("SELECT shares FROM portfolio WHERE user_id = ? AND stock = ?", session["user_id"], symbol)
        if not owned_shares or shares > int(owned_shares[0]["shares"]):
            return apology("invalid stock or shares")

        price = lookup(symbol)["price"]

        db.execute("UPDATE portfolio SET shares = ? WHERE user_id = ? AND stock = ?",
                   int(owned_shares[0]["shares"]) - shares, session["user_id"], symbol)
        db.execute("INSERT INTO history (user_id, action, stock, price, shares) VALUES (?, 'SELL', ?, ?, ?)",
                   session["user_id"], symbol, price, shares)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", db.execute("SELECT cash FROM users WHERE id = ?",
                   session["user_id"])[0]["cash"] + (price * shares), session["user_id"])

        return redirect("/")

    else:
        return render_template("sell.html", stocks=db.execute("SELECT stock FROM portfolio WHERE user_id = ?", session["user_id"]))


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":

        if request.form.get("old") and request.form.get("password") and request.form.get("confirmation"):
            if request.form.get("password") == request.form.get("confirmation"):

                if check_password_hash(db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])[0]["hash"], request.form.get("old")):
                    db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(
                        request.form.get("password"), method='pbkdf2:sha256', salt_length=8), session["user_id"])
                    return redirect("/")
                else:
                    return apology("wrong password")
            else:
                return apology("new password doesn't matches confirmation")
        else:
            return apology("all fields are required")
    else:
        return render_template("password.html")