import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Check if the message is POST
    if request.method == "POST":
        # Check if email address exists in db
        existing_user = mongo.db.users.find_one(
            {"user_email_address": request.form.get(
                "email").lower()})

        # If it doesn, display a flash message informing user that the an account already exists for this email address.
        if existing_user:
            flash("Account already exists for this email address.")
            return redirect(url_for("register"))

        # Otherwise, assign form inputs (values) to keys and insert record into users collection.
        record = {
            "first_name": request.form.get("first-name").lower(),
            "last_name": request.form.get("last-name").lower(),
            "user_email_address": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(record)

        # Then, put the new users email address into session cookie and display flash success message.
        session["user"] = request.form.get("email").lower()
        flash("Registration successful")

    # If method is not POST (i.e. GET) render register.html template.
    return render_template("register.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    # Check if the message is POST
    if request.method == "POST":
        # Check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"user_email_address": request.form.get(
                "email").lower()})

        if existing_user:
            # Ensure hashed password matches password input by user
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    # If so, put the new users email address into session cookie and display flash success message.
                    session["user"] = request.form.get("email").lower()
                    flash("Welcome back {}".format(
                        existing_user["first_name"].capitalize()))
            else:
                # If password doesn't match, display flash message informing the user and return them to a blank sign in page.
                flash("Incorrect Email Address and/or Password")
                return redirect(url_for("signin"))

        # If  email address doesn't exist in db, display flash message informing the user and return them to a blank sign in page.
        else:
            flash("Incorrect Email Address and/or Password")
            return redirect(url_for("signin"))

    # If method is not POST (i.e. GET) render register.html template.
    return render_template("signin.html")


@app.route("/account")
def account():
    return render_template("account.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
