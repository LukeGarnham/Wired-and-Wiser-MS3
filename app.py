import os
from datetime import date
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

        # If it doesn't, display a flash message informing user that an account already exists for this email address.
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

        # Put the new users email address into session cookie and display flash success message using their first name.
        session["user_email_address"] = request.form.get("email").lower()
        flash("Registration successful")
        # Redirect to account(username) function where username is the users email address.
        return redirect(url_for(
            "account", username=session["user_email_address"]))

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

        # If user exists in database:
        if existing_user:
            # Ensure hashed password matches password input by user.
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    # If so then put the users email address into session cookie and display flash success message.
                    session["user_email_address"] = existing_user["user_email_address"].lower()
                    flash("Welcome back {}".format(
                        existing_user["first_name"].capitalize()))
                    # Redirect to account(username) function where username is the users email address.
                    return redirect(url_for(
                        "account", username=session["user_email_address"]))
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


@app.route("/account/<username>", methods=["GET", "POST"])
def account(username):
    # Use email address in session storage to search users collection.  Asign email address as username.
    username = mongo.db.users.find_one(
        {"user_email_address": session["user_email_address"]})["user_email_address"]
    # Use email address in session storage to search users collection.  Asign results to user.
    user = mongo.db.users.find_one(
        {"user_email_address": session["user_email_address"]})
    # Remove the users password.  Even though it is hashed, I don't want to pass this through.
    user.pop("password")
    # Use email address in session storage to search meter_installs collection.  Asign results to bookings.  Sort by install date and then address.
    bookings = list(mongo.db.meter_installs.find(
        {"user_email_address": session["user_email_address"]}).sort([("install_date", 1),("first_address_line", 1)]))

    # Check if there is a user email address saved in session variable, if so render account page.
    if session["user_email_address"]:
        # Render template.  Pass through the username, user and bookings variables defined above.
        return render_template(
            "account.html", 
            username=username,
            user=user,
            bookings=bookings)
    # If there is no user email address saved in session variable, redirect user to sign in page.
    return redirect(url_for("signin"))


@app.route("/signout")
def signout():
    # Remove the users email address from session cookies.
    flash("You have been signed out.")
    session.pop("user_email_address")
    return redirect(url_for("signin"))


@app.route("/book", methods=["GET", "POST"])
def book():
    # If method is POST (i.e. form submitted), add form data to meter installs collection.
    if request.method == "POST":
        # Check whether there is a meter install already booked for this meter ID.
        existing_booking = mongo.db.meter_installs.find_one(
            {"meter_id": request.form.get(
                "meter_id")})
        # If a record (booking) already exists for this meter ID, display a flash message to the user.
        if existing_booking:
            flash("A smart meter installation has already been booked for Meter ID "+ request.form.get("meter_id"))
        # Else extract data from form and assign to keys in the booking dictionary.
        else:
            booking = {
                "user_email_address": session["user_email_address"],
                "meter_id": request.form.get("meter_id"),
                "meter_serial_number": request.form.get("meter_serial_number"),
                "first_address_line": request.form.get("first_address_line"),
                "second_address_line": request.form.get("second_address_line"),
                "third_address_line": request.form.get("third_address_line"),
                "town": request.form.get("town"),
                "county": request.form.get("county"),
                "postcode": request.form.get("postcode"),
                "meter_location": request.form.get("meter_location"),
                "access_instructions": request.form.get("access_instructions"),
                "parking_on_site": request.form.get("parking_on_site"),
                "property_type": request.form.get("property_type"),
                "supplier": request.form.get("supplier"),
                "supplier_acc_no": request.form.get("supplier_acc_no"),
                "meter_read_reg_1": request.form.get("meter_read_reg_1"),
                "meter_read_reg_2": request.form.get("meter_read_reg_2"),
                "install_date": request.form.get("install_date"),
                "application_date": date.today().strftime("%d/%m/%Y"),
                "installation_complete": False
            }
            # Insert the booking dictionary into the meter_installs collection.
            mongo.db.meter_installs.insert_one(booking)
            # Display a flash message informing user that booking has been successful.
            flash("Meter install successfully booked")
            # Redirect to account(username) function where username is the users email address.
            return redirect(url_for(
                "account", username=session["user_email_address"]))

    return render_template("book.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
