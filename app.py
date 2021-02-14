import os
import re
import bson
from datetime import datetime
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

        # If it does, display a flash message informing user that an
        # account already exists for this email address.
        if existing_user:
            flash("Account already exists for this email address.")
            return redirect(url_for("register"))

        # Otherwise, assign form inputs (values) to keys and
        # insert record into users collection.
        record = {
            "first_name": request.form.get("first-name").lower(),
            "last_name": request.form.get("last-name").lower(),
            "user_email_address": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(record)

        # Put the new users email address into session cookie and
        # display flash success message using their first name.
        session["user_email_address"] = request.form.get("email").lower()
        flash("Registration successful")
        # Redirect to account(username) function where
        # username is the users email address.
        return redirect(url_for(
            "account", username=session["user_email_address"]))

    # If method is not POST (i.e. GET), first check whether
    # the user_email_address exists in the session variable.
    if session.get("user_email_address"):
        # If so, redirect user back to their Account page
        # and display flash message.
        flash("No need to register again")
        return redirect(url_for(
            "account", username=session["user_email_address"]))
    # Else, render register.html template.
    return render_template("register.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    # Check if the message is POST
    if request.method == "POST":
        # Check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"user_email_address": request.form.get("email").lower()})

        # If user exists in database:
        if existing_user:
            # Ensure hashed password matches password input by user.
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                # If so then put the users email address into session cookie.
                session["user_email_address"] = existing_user[
                        "user_email_address"].lower()
                # And display flash success message.
                flash("Welcome back {}".format(
                    existing_user["first_name"].capitalize()))
                # Redirect to account(username) function where
                # username is the users email address.
                return redirect(url_for(
                    "account", username=session["user_email_address"]))
            else:
                # If password doesn't match, display flash message informing
                # the user and return them to a blank sign in page.
                flash("Incorrect Email Address and/or Password")
                return redirect(url_for("signin"))

        # If  email address doesn't exist in db, display flash message
        # informing the user and return them to a blank sign in page.
        else:
            flash("Incorrect Email Address and/or Password")
            return redirect(url_for("signin"))

    # If method is not POST (i.e. GET), first check whether
    # the user_email_address exists in the session variable.
    if session.get("user_email_address"):
        # If so, redirect user back to their Account page
        # and display flash message.
        flash("You are already signed in as " +
              session["user_email_address"])
        return redirect(url_for(
            "account", username=session["user_email_address"]))
    # Else, render signin.html template.
    return render_template("signin.html")


@app.route("/account/<username>")
def account(username):
    # Check whether the user_email_address exists in the session variable.
    if session.get("user_email_address"):
        # If so, ensure that any variable passed through is all lower case.
        username = username.lower()
        # Check whether the username is a valid email address.
        if validate_email(username):
            # Check whether the username passed through matches
            # the user email address in the session variable.
            if username == session["user_email_address"]:
                # Use email address passed through in username variable
                # to search users collection.  Asign results to user variable.
                user = mongo.db.users.find_one(
                    {"user_email_address": username})
                # Check whether any result is returned.
                if user:
                    # Remove the users password.
                    # Even though it is hashed, I don't
                    # want to pass this through.
                    user.pop("password")
                    # Use email address passed through in username variable
                    # to search meter_installs collection.
                    # Asign results to bookings.
                    # Sort by install date and then address.
                    bookings = list(mongo.db.meter_installs.find(
                        {"user_email_address": username}).sort(
                            [("install_date", 1), ("first_address_line", 1)]))
                    return render_template(
                            "account.html",
                            user=user,
                            bookings=bookings)
                # If email address is in session storage but no results found
                # in users collection, something must have gone wrong.
                # Redirect user to signout function.
                return redirect(url_for("signout"))
            # If username passed through differs from one in session variable
            # then redirect user to Account page using email address from
            # session variable.
            flash("You are already signed in as " +
                  session["user_email_address"])
            return redirect(url_for(
                "account", username=session["user_email_address"]))
        # If username is not valid, redirect user to Account page
        # using email address from session variable.
        flash("You are already signed in as " +
              session["user_email_address"])
        return redirect(url_for(
            "account", username=session["user_email_address"]))
    # If there is no user email address in session variable
    # redirect the user to the Sign In page.
    return redirect(url_for("signin"))


def validate_email(email):
    # Check whether a string matches the email regex.
    # Regex solution sourced from here:
    # https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    return re.search("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email)


@app.route("/signout")
def signout():
    # Check if there is a user email address saved
    # in session variable. If so remove it from the session variable.
    if session["user_email_address"]:
        session.pop("user_email_address")
    # Display flash message and redirect user to signin page.
    flash("You have been signed out.")
    return redirect(url_for("signin"))


@app.route("/book", methods=["GET", "POST"])
def book():
    # Check whether the user_email_address exists in the session variable.
    if session.get("user_email_address"):
        # If method is POST (i.e. form submitted),
        # add form data to meter installs collection.
        if request.method == "POST":
            # Check whether there is a meter install
            # already booked for this meter ID.
            existing_booking = mongo.db.meter_installs.find_one(
                {"meter_id": request.form.get("meter_id")})
            # If a record (booking) already exists for this meter ID,
            # display a flash message to the user.
            if existing_booking:
                flash("A smart meter installation has already been"
                      " booked for Meter ID " + request.form.get("meter_id"))
            # Else extract data from form and assign
            # to keys in the booking dictionary.
            else:
                # Check whether the supplier authorisation is
                # selected and asign True if so, False if not.
                authorised = True if request.form.get(
                    "supplier_authorisation") == "on" else False
                booking = {
                    "user_email_address": session["user_email_address"],
                    "meter_id": int(request.form.get("meter_id")),
                    "meter_serial_number": request.form.get(
                        "meter_serial_number"),
                    "first_address_line": request.form.get(
                        "first_address_line"),
                    "second_address_line": request.form.get(
                        "second_address_line"),
                    "third_address_line": request.form.get(
                        "third_address_line"),
                    "town": request.form.get("town"),
                    "county": request.form.get("county"),
                    "postcode": request.form.get("postcode"),
                    "meter_location": request.form.get("meter_location"),
                    "access_instructions": request.form.get(
                        "access_instructions"),
                    "parking_on_site": request.form.get("parking_on_site"),
                    "property_type": request.form.get("property_type"),
                    "supplier": request.form.get("supplier"),
                    "supplier_acc_no": request.form.get("supplier_acc_no"),
                    "meter_read_reg_1": int(request.form.get(
                        "meter_read_reg_1"))
                    if request.form.get("meter_read_reg_1") else "",
                    "meter_read_reg_2": int(request.form.get(
                        "meter_read_reg_2"))
                    if request.form.get("meter_read_reg_2") else "",
                    "install_date": datetime.strptime(
                        request.form.get("install_date"), "%d/%m/%Y"),
                    "supplier_authorisation": authorised,
                    "application_date": datetime.now()
                }
                # Insert the booking dictionary into
                # the meter_installs collection.
                mongo.db.meter_installs.insert_one(booking)
                # Display a flash message informing user
                # that booking has been successful.
                flash("Meter install successfully booked")
                # Redirect to account(username) function where
                # username is the users email address.
                return redirect(url_for(
                    "account", username=session["user_email_address"]))
        # If mehod is GET, render the Booking page.
        return render_template("book.html")
    # If the user is not signed in, redirect them to the Sign In page.
    flash("Please sign in before trying to book a smart meter install")
    return redirect(url_for("signin"))


@app.route("/view_booking/<booking_id>")
def view_booking(booking_id):
    # Check whether the user_email_address exists in the session variable.
    if session.get("user_email_address"):
        # Check whether the booking_id is valid
        if validate_id(booking_id):
            # Find the record with the corresponding
            # booking ID in the meter_installs collection.
            booking = mongo.db.meter_installs.find_one(
                {"_id": ObjectId(booking_id)})
            # Check if booking exists and that the user_email_address
            # matches the one in the session variable.
            if booking and booking["user_email_address"] == session[
               "user_email_address"]:
                # If so, render the view_booking.html template.
                return render_template("view_booking.html", booking=booking)
        # If the booking_id entered is not valid
        # return user to Account page with flash message.
        flash("The booking ID you are trying to find is not valid")
        return redirect(url_for(
                    "account", username=session["user_email_address"]))
    # If the user is not signed in, redirect them to the Sign In page.
    flash("Please sign in before trying to view a"
          " smart meter installation booking")
    return redirect(url_for("signin"))


def validate_id(id):
    return bson.objectid.ObjectId.is_valid(id)


@app.route("/delete_booking/<booking_id>")
def delete_booking(booking_id):
    # Find the booking in the meter_installs collection
    # with the booking id that's been passed through and delete it.
    mongo.db.meter_installs.delete_one({"_id": ObjectId(booking_id)})
    # Display a flash message informing user that the booking has been deleted.
    flash("Your meter install booking has been deleted")
    # Redirect the user back to the account page.
    return redirect(url_for(
        "account", username=session["user_email_address"]))


@app.route("/update_booking/<booking_id>", methods=["GET", "POST"])
def update_booking(booking_id):
    # Check whether the user_email_address exists in the session variable.
    if session.get("user_email_address"):
        # If method is POST (i.e. form submitted),
        # update the data in the meter_installs collection.
        if request.method == "POST":
            # Retrieve the original booking from the meter_installs collection.
            original_booking = mongo.db.meter_installs.find_one(
                {"_id": ObjectId(booking_id)})
            # Check whether the supplier authorisation is selected
            # and asign True if so, False if not.
            authorised = True if request.form.get(
                "supplier_authorisation") == "on" else False
            # Asign form elements to keys in update dict.
            update = {
                "user_email_address": session["user_email_address"],
                "meter_id": int(request.form.get("meter_id")),
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
                "meter_read_reg_1": int(request.form.get("meter_read_reg_1"))
                if request.form.get("meter_read_reg_1") else None,
                "meter_read_reg_2": int(request.form.get("meter_read_reg_2"))
                if request.form.get("meter_read_reg_2") else None,
                "install_date": datetime.strptime(
                    request.form.get("install_date"), "%d/%m/%Y"),
                "supplier_authorisation": authorised,
                "application_date": original_booking["application_date"]
            }
            # Check whether the meter_id has changed.
            if original_booking["meter_id"] != update["meter_id"]:
                # If so, check the meter_installs collection to see if
                # another booking has been made with the updated meter_id.
                existing_booking = mongo.db.meter_installs.find_one(
                    {"meter_id": update["meter_id"]})
                # If there is another meter found in the
                # meter_installs collection.
                if existing_booking:
                    # Display a flash message to the user advising them that
                    # there is an existing booking for the updated meter_id.
                    flash("A smart meter installation has already been"
                          "booked for Meter ID " + request.form.get(
                              "meter_id"))
                # Else, update the booking in the meter_installs collection.
                else:
                    # Find record with original booking id and update it.
                    mongo.db.meter_installs.update(
                        {"_id": ObjectId(booking_id)}, update)
                    # Display a flash message informing user that
                    # booking has been successfully updated.
                    flash("Meter install booking updated")
                    # Redirect to account(username) function where
                    # username is the users email address.
                    return redirect(url_for(
                        "account", username=session["user_email_address"]))
            # Else if meter_id has not changed
            else:
                # Then update  the booking in the meter_installs collection.
                mongo.db.meter_installs.update(
                    {"_id": ObjectId(booking_id)}, update)
                # Display a flash message informing user that
                # booking has been successfully updated.
                flash("Meter install booking updated")
                # Redirect to account(username) function where
                # username is the users email address.
                return redirect(url_for(
                    "account", username=session["user_email_address"]))

        # If method is GET, first check the booking_id is valid
        if validate_id(booking_id):
            # Find the record with the corresponding
            # booking ID in the meter_installs collection.
            booking = mongo.db.meter_installs.find_one(
                {"_id": ObjectId(booking_id)})
            # Check if booking exists and that the user_email_address
            # matches the one in the session variable.
            if booking and booking["user_email_address"] == session[
               "user_email_address"]:
                # If so, render the update_booking.html template.
                return render_template("update_booking.html", booking=booking)
        # If the booking_id entered is not valid
        # return user to Account page with flash message.
        flash("The booking ID you are trying to find is not valid")
        return redirect(url_for(
                    "account", username=session["user_email_address"]))
    # If the user is not signed in, redirect them to the Sign In page.
    flash("Please sign in before trying to update a"
          " smart meter installation booking")
    return redirect(url_for("signin"))


@app.route("/update_account/<username>", methods=["GET", "POST"])
def update_account(username):
    # Check whether the user_email_address exists in the session variable.
    if session.get("user_email_address"):
        # If so, ensure that any variable passed through is all lower case.
        username = username.lower()
        # Check whether the username is a valid email address.
        if validate_email(username):
            # Use email address that's been passed through
            # to search users collection.  Asign results to user.
            user = mongo.db.users.find_one(
                {"user_email_address": username})
            # Check that a record is found and if so, that
            # the user email address matches the one in the session variable.
            if user and user["user_email_address"] == session[
                             "user_email_address"]:
                # If method is POST (i.e. form submitted),
                # update the data in the meter_installs collection.
                if request.method == "POST":
                    # Check that the password the user has entered
                    # matches the users password in the users collection.
                    if check_password_hash(user["password"],
                                           request.form.get("password")):
                        # Create update_user dict containing
                        # the updated details.
                        # Password will be the existing hashed password.
                        update_user = {
                            "first_name": request.form.get(
                                "first-name").lower(),
                            "last_name": request.form.get(
                                "last-name").lower(),
                            "user_email_address": request.form.get(
                                "email").lower(),
                            "password": user["password"]
                        }
                        # Check if the user has changed their email address.
                        if user["user_email_address"] != request.form.get(
                           "email").lower():
                            # If so, check if new email address exists in db.
                            existing_user = mongo.db.users.find_one(
                                {"user_email_address": request.form.get(
                                    "email").lower()})
                            # If it does, display a flash message
                            # informing user that
                            # an account already exists for this email address.
                            if existing_user:
                                flash("Another account already exists for the "
                                      "email address you entered")
                                # Redirect user to update_account page.
                                return redirect(url_for(
                                    "update_account", username=username))
                            # Else, email address has changed
                            # but is unique in collection:
                            else:
                                # Use the update_many method to
                                # find all meter_installs
                                # records with old email address and
                                # update to the new email address.
                                # Solution reached referring to:
                                # https://www.w3schools.com/python/python_mongodb_update.asp
                                mongo.db.meter_installs.update_many({
                                    "user_email_address": user[
                                        "user_email_address"]
                                    }, {
                                        "$set": {
                                            "user_email_address": update_user[
                                                "user_email_address"]
                                        },
                                    }
                                )
                                # Update the users details in
                                # the users collection
                                # when the user has changed
                                # their email address.
                                session["user_email_address"] = update_user[
                                    "user_email_address"].lower()
                        # Update the existing record using the user id.
                        mongo.db.users.update(
                            {"_id": ObjectId(user["_id"])}, update_user)
                        # Display flash message informing user that account
                        # details have been successfully updated.
                        flash("Account details updated")
                        # Redirect to account(username) function where
                        # username is the users email address.
                        return redirect(url_for(
                            "account", username=session["user_email_address"]))
                    else:
                        # If password doesn't match, display flash message
                        # informing the user and ask them to try again.
                        flash("Incorrect password - try again")
                        # Redirect user back to update_account page.
                        return redirect(url_for(
                            "update_account", username=username))
                # If method is GET, remove the users password.
                # Even though it is hashed, I don't want to pass
                # this through for security reasons.
                user.pop("password")
                # Check if there is a user email address saved
                # in session variable, if so render update_account page.
                if session["user_email_address"]:
                    # Pass through the user variable defined above.
                    return render_template("update_account.html", user=user)
                # If there is no user email address saved in session variable,
                # redirect user to sign in page.
                return redirect(url_for("signin"))
        # If username is not valid, redirect user to Account page
        # using email address from session variable.
        flash("You are already signed in as " +
              session["user_email_address"])
        return redirect(url_for(
            "account", username=session["user_email_address"]))
    # If the user is not signed in, redirect them to the Sign In page.
    flash("Please sign in before trying to update "
          "account details")
    return redirect(url_for("signin"))


@app.route("/delete_account/<username>", methods=["POST"])
def delete_account(username):
    user = mongo.db.users.find_one(
        {"user_email_address": username})
    # Check to ensure user variable exists.
    if user:
        # Check whether the user has provided the correct password.
        if check_password_hash(
                user["password"], request.form.get("password")):
            # If so, find bookings in meter_installs collection with
            # corresponding user email address and delete them all.
            # Solution reached referring to:
            # https://www.w3schools.com/python/python_mongodb_delete.asp
            mongo.db.meter_installs.delete_many({
                "user_email_address": username})
            # Find the users record in the users collection and delete it.
            # There will only be one record with corresponding
            # email address but use the id anyway.
            mongo.db.users.delete_one({
                "_id": ObjectId(user["_id"])})
            # Delete the users email address out of session storage.
            session.pop("user_email_address")
            # Redirect user to the registration page and display flash message
            # informing them that account and bookings have been deleted.
            flash("Your account and all meter install "
                  "bookings have been deleted")
            return redirect(url_for(
                "register"))
        # Else if password user has entered is incorrect.
        else:
            # Display flash message and redirect back to account page.
            flash("Incorrect password - try again")
            return redirect(url_for(
                    "account", username=session["user_email_address"]))


@app.errorhandler(404)
def page_not_found(e):
    # This function handles 404 (page not found errors)
    # Solution copied from: https://flask.palletsprojects.com/en/master/errorhandling/
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
