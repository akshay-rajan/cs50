import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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

    data = db.execute(
        "SELECT symbol, shares FROM shares_available WHERE user_id = ?",
        session["user_id"],
    )

    # A list of dictionaries for each transaction made by the user
    stocks = []
    for row in data:
        # A dictionary containing data for one row / transaction
        stock = {}
        stock["symbol"] = row["symbol"]
        stock["shares"] = row["shares"]
        stockdata = lookup(stock["symbol"])
        stock["pricePerShare"] = stockdata["price"]
        stock["totalValue"] = stock["shares"] * stock["pricePerShare"]
        stocks.append(stock)

    # Get the balance remaining in the user's account
    bal = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    balance = bal[0]["cash"]

    # Sum the total values
    grandTotal = 0
    for row in stocks:
        grandTotal += row["totalValue"]

    return render_template(
        "index.html", stocks=stocks, balance=balance, grandTotal=grandTotal
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # If the method is by POST, input the symbol, look up its price
    if request.method == "POST":
        user = session["user_id"]
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("Shares must be a positive integer!")

        stockLookup = lookup(symbol)
        if stockLookup is None:
            return apology("Invalid symbol")

        stock_price = stockLookup["price"]
        if stockLookup is None:
            return apology("Symbol does not exist!")

        # Get the data of user from the database
        rows = db.execute("SELECT * FROM users WHERE id = ?", user)
        cash = rows[0]["cash"]

        # If not enough money, render an apology. Else calculate balance after the purchase
        amount = stock_price * shares
        if amount > cash:
            return apology("Not enough balance!")
        balance = cash - amount

        # Insert transaction data into the database
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, amount, balance, timestamp, stock_price, type) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, 'BUY')",
            user,
            symbol.upper(),
            shares,
            amount,
            balance,
            stock_price,
        )
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, user)
        data = db.execute(
            "SELECT shares FROM shares_available WHERE user_id = ? AND symbol = ?",
            user,
            symbol,
        )
        # If the user has purchased the same stocks before
        if len(data) > 0:
            shares_present = data[0]["shares"]
            db.execute(
                "UPDATE shares_available SET shares = ? WHERE user_id = ? AND symbol = ?",
                shares_present + shares,
                user,
                symbol,
            )
        else:
            db.execute(
                "INSERT INTO shares_available (user_id, symbol, shares) VALUES (?, ?, ?)",
                user,
                symbol,
                shares,
            )

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user = session["user_id"]

    # Get transaction data from the database
    data = db.execute(
        "SELECT type, symbol, shares, stock_price, amount, timestamp FROM transactions WHERE user_id = ?",
        user,
    )
    stocks = []
    for row in data:
        stocks.append(row)

    return render_template("history.html", stocks=stocks)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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

    # If the request method is GET, render the html form to get the stock details
    if request.method == "GET":
        symbol = request.args.get("symbol")
        return render_template("quote.html")

    # If the request is by POST, get the symbol from the form and pass the data to "quoted.html"
    else:
        symbol = request.form.get("symbol")
        quote_lookup = lookup(symbol)
        if quote_lookup is None:
            return apology("Invalid symbol")
        return render_template("quoted.html", quote_lookup=quote_lookup)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Get username. Render an apology if username is blank or taken
        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not username:
            return apology("Username cannot be blank!")
        if len(rows) > 0:
            return apology("Username already taken!")

        # Get password. Render an apology if password blank or does not match with the confirmation
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or password != confirmation:
            return apology("Password empty or does not match!")

        # Add the user details to the database and return to login
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            generate_password_hash(password),
        )
        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user = session["user_id"]
    # Get the stocks and shares to sell. Render an apology if not enough stocks are available
    if request.method == "POST":
        # Get stocks to sell from html form
        symbol = request.form.get("symbol")
        symbol = symbol.upper()
        shares = request.form.get("shares")

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("Shares must be a positive integer!")

        # From 'shares' table, get shares currently holding by the user
        shareData = db.execute(
            "SELECT shares FROM shares_available WHERE user_id = ? AND symbol = ?",
            user,
            symbol.upper(),
        )
        sharesAvailable = 0
        try:
            if len(shareData) < 1:
                raise ValueError
            sharesAvailable = int(shareData[0]["shares"])
            if shares > sharesAvailable:
                raise ValueError
        except ValueError:
            return apology("Not enough shares!")

        # Get the current price of the stock
        stockLookup = lookup(symbol)
        stock_price = float(stockLookup["price"])

        # Get the cash available in the user's account
        rows = db.execute("SELECT * FROM users WHERE id = ?", user)
        cash = rows[0]["cash"]

        # Calculate new balance in the user's account
        amount = stock_price * shares
        balance = cash + amount

        # Enter data into the database
        if shares == sharesAvailable:
            # If there are no shares left of the particular stock
            db.execute(
                "DELETE FROM shares_available WHERE user_id = ? AND symbol = ?",
                user,
                symbol,
            )
        else:
            sharesAvailable -= shares
            db.execute(
                "UPDATE shares_available SET shares = ? WHERE user_id = ? AND symbol = ?",
                sharesAvailable,
                user,
                symbol,
            )
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, amount, balance, timestamp, stock_price, type) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, 'SELL')",
            user,
            symbol.upper(),
            shares,
            amount,
            balance,
            stock_price,
        )
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, user)

        return redirect("/")

    else:
        # Get all stocks currently holded by the user as a list
        symbols = []
        data = db.execute("SELECT symbol FROM shares_available WHERE user_id = ?", user)
        for row in data:
            symbol = row["symbol"]
            symbols.append(symbol)
        return render_template("sell.html", symbols=symbols)


# Personal Touch
@app.route("/newpassword", methods=["GET", "POST"])
@login_required
def newpassword():
    """Change password of the user"""

    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        oldpassword = request.form.get("oldpassword")
        # Check if the password entered is correct
        if not oldpassword or not check_password_hash(rows[0]["hash"], oldpassword):
            return apology("Incorrect password!")

        newpassword = request.form.get("newpassword")
        confirmation = request.form.get("confirmation")
        # Check if the passwords match
        if oldpassword == newpassword:
            return apology("You have entered the same password!")
        if not newpassword or newpassword != confirmation:
            return apology("Password empty or do not match!")

        # Update password in the database
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(newpassword),
            session["user_id"],
        )

        # Redirect to login after clearing the session
        session.clear()
        return redirect("/login")

    else:
        return render_template("newpassword.html")
