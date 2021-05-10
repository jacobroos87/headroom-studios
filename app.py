import os
import math
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)
# Variable used to reference current date/time
today = datetime.now()

# App Routes

@app.route("/")
@app.route("/home")
# This function renders the home page
def home():
    return render_template("home.html")


@app.route("/rehearsal_studios")
# This function renders the Rehearsal Studios page
def rehearsal_studios():
    return render_template("rehearsal_studios.html")


@app.route("/notice_board")
# This function renders the notice_board page and implements pagniation after 6 posts
def notice_board():
    posts = list(mongo.db.posts.find().sort([("_id", -1)]))
    page = request.args.get("page")
    # Pagination
    if page is not None:
        current_page = int(page)
    else:
        current_page = 1

    # Pagination Variables
    number_per_page = 6
    number_of_pages = math.ceil(len(posts) / number_per_page)
    if number_of_pages < 1:
        number_of_pages = 1

    begin = (current_page - 1) * number_per_page
    end = begin + number_per_page
    posts = posts[begin:end]

    return render_template(
        "notice_board.html", posts=posts,
        current_page=current_page, number_of_pages=number_of_pages)


# Next Page
@app.route("/next_page/<current_page>", methods=["GET", "POST"])
def next_page(current_page):
    if current_page == (request.args.get("number_of_pages")):
        page = current_page
        return redirect(url_for('notice_board', page=page))
    else:
        page = int(current_page) + 1
        return redirect(url_for('notice_board', page=page))


# Previous Page
@app.route("/prev_page/<current_page>", methods=["GET", "POST"])
def prev_page(current_page):
    if int(current_page) == 1:
        return redirect(url_for('notice_board', page=None))
    else:
        page = int(current_page) - 1
        return redirect(url_for('notice_board', page=page))


@app.route("/faq")
# This function renders the FAQ page
def faq():
    return render_template("faq.html")


@app.route("/login/", methods=["GET", "POST"])
# This function renders the login page and adds a new user to MongoDB
def login():

    today = date.today().strftime('%b %d/%Y')
    if request.method == "POST":
        # check if username exists in DB
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:

            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username").capitalize()))
                return redirect(url_for(
                    "profile", username=session["user"], today=today))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login", today=today))

        else:
            # username doesn't exist
            flash("Incorrect username and/or Password")
            return redirect(url_for("login", today=today))

    return render_template("login.html")


@app.route("/logout")
# This function logs out the current user
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/bookings")
# This function renders the bookings page
def bookings():
    return render_template("bookings.html")


@app.route("/check_availability", methods=["GET", "POST"])
# This function checks the inputted information against the database
# and returns a flash message
def check_availability():
    if request.method == "POST":
        # check if booking already exists in db
        date = datetime.strptime(
                request.form.get("date"), '%d %b %Y')
        date_formatted = request.form.get("date")
        slot = request.form.get("slot")

        # find appropriate studios
        studios = list(mongo.db.bookings.find({"date": date, "slot": slot}))

        # set default variables
        studio_one = studio_two = studio_three = ""

        # define each studio
        for studio in studios:
            if studio["studio"] == "1":
                studio_one = studio
            if studio["studio"] == "2":
                studio_two = studio
            if studio["studio"] == "3":
                studio_three = studio
        # check availability
        available_studios = ""
        if studio_one and not studio_two and not studio_three:
            available_studios = "2 & 3 are"
        elif studio_two and not studio_one and not studio_three:
            available_studios = "1 & 3 are"
        elif studio_three and not studio_one and not studio_two:
            available_studios = "1 & 2 are"
        elif studio_one and studio_two and not studio_three:
            available_studios = "3 is"
        elif studio_one and studio_three and not studio_two:
            available_studios = "2 is"
        elif studio_two and studio_three and not studio_one:
            available_studios = "1 is"
        elif studio_one and studio_two and studio_three:
            available_studios = "none"
        else:
            available_studios = "all"
        # flash messages
        if available_studios == "none":
            flash(
                f"All of our studios are fully booked on\
                    {date_formatted} for the {slot} slot")
        elif available_studios == "all":
            flash(
                f"Currently all three studios are available on\
                    {date_formatted} in the {slot}")
        else:
            flash(
                f"Studio {available_studios} currently available on\
                    {date_formatted} in the {slot}")
    return redirect(url_for("bookings"))


@app.route("/new_booking", methods=["GET", "POST"])
# This function adds a new bookings to the MondoDB database
def new_booking():
    if request.method == "POST":
        # Checks if another booking exists with same details
        existing_booking = mongo.db.bookings.find_one(
            {"studio": request.form.get("studio"), "date": request.form.get(
                "booking-date"), "slot": request.form.get("time-slot")})
        if existing_booking:
            flash("Booking unsuccessful check availability before booking")
            return redirect(url_for("bookings"))
        # Information added to DB
        booking = {
            "studio": request.form.get("studio"),
            "date": datetime.strptime(
                request.form.get("booking-date"), '%d %b %Y'),
            "slot": request.form.get("time-slot"),
            "contact_name": request.form.get("contact_name"),
            "additional_info": request.form.get("additional_info"),
            "created_by": session["user"]
        }
        # insert booking if no clashes
        mongo.db.bookings.insert_one(booking)
        flash("Booking Successful")
        return redirect(url_for(
            "profile", username=session["user"], today=today))

    return render_template("bookings.html")


@app.route("/admin/<username>", methods=["GET", "POST"])
# This function renders the Admin Page
def admin(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    # All active bookings added to variable
    bookings = list(mongo.db.bookings.find())
    if session["user"]:
        return render_template(
            "admin.html", username=username,
            bookings=bookings, today=today)


@app.route("/edit_booking/<booking_id>", methods=["GET", "POST"])
# This function renders the Edit Booking Page
def edit_booking(booking_id):
    if request.method == "POST":
        # Checks if the booking exists
        existing_booking = mongo.db.bookings.find_one(
            {"studio": request.form.get("studio"), "date": request.form.get(
                "booking-date"), "slot": request.form.get("time-slot")})
        if existing_booking:
            flash("Update unsuccessful check availability before booking")
            return redirect(url_for("bookings"))
        # Information added to database
        submit = {
            "studio": request.form.get("studio"),
            "date": datetime.strptime(
                request.form.get("booking-date"), '%d %b %Y'),
            "slot": request.form.get("time-slot"),
            "contact_name": request.form.get("contact_name"),
            "additional_info": request.form.get("additional_info"),
            "created_by": session["user"]
        }
        # Updates information on the database
        mongo.db.bookings.update({"_id": ObjectId(booking_id)}, submit)
        flash("Booking Successfully Updated")
        return redirect(url_for("profile", username=session["user"]))

    booking = mongo.db.bookings.find_one({"_id": ObjectId(booking_id)})
    return render_template("edit_booking.html", booking=booking)


@app.route("/delete_booking/<booking_id>")
# This function removes the selected booking
def delete_booking(booking_id):
    # Removed based on ObjectId
    mongo.db.bookings.remove({"_id": ObjectId(booking_id)})
    # Return to Admin page if admin user
    if session["user"] == "admin":
        flash("Booking successfully deleted")
        return redirect(url_for("admin", username=session["user"]))
    # Else return to profile
    flash("Booking successfully deleted")
    return redirect(url_for("profile", username=session["user"]))


@app.route("/add_post", methods=["GET", "POST"])
# This function renders the Add Post page
# and adds a new post to the Notice Board
def add_post():
    if request.method == "POST":
        # Check to see if Is Urgent has been selected
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        # Information requested from the input form
        post = {
            "post_title": request.form.get("post_title"),
            "post_message": request.form.get("post_message"),
            "is_urgent": is_urgent,
            "category": request.form.get("category"),
            "created_by": session["user"],
            "email": request.form.get("email"),
            "date_posted": today
        }
        # Add information to MongoDB
        mongo.db.posts.insert_one(post)
        flash("Post Successfully Added")
        return redirect(url_for("notice_board"))

    return render_template("add_post.html")


@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
# This function edits an active post
def edit_post(post_id):
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        submit = {
            "post_title": request.form.get("post_title"),
            "post_message": request.form.get("post_message"),
            "category": request.form.get("category"),
            "is_urgent": is_urgent,
            "created_by": session["user"],
            "email": request.form.get("email"),
            "date_posted": today
        }
        # Updates submitted information on MongoDB
        mongo.db.posts.update({"_id": ObjectId(post_id)}, submit)
        flash("Post Successfully Updated")
        return redirect(url_for("notice_board"))

    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    return render_template("edit_post.html", post=post)


@app.route("/delete_post/<post_id>")
# This function removes an active post from MongoDB
def delete_post(post_id):
    mongo.db.posts.remove({"_id": ObjectId(post_id)})
    flash("Post successfully deleted")
    return redirect(url_for("notice_board"))


@app.route("/profile/<username>", methods=["GET", "POST"])
# This function renders the Profile page
def profile(username):
    # grab session user's username from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    # Variable to hold current bookings
    bookings = list(mongo.db.bookings.find())
    if session["user"]:
        return render_template(
            "profile.html", username=username, bookings=bookings, today=today)
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
# This function is linked to the Registration Form
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("home"))
        # Data taken from form input
        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        # Add new user to MongoDB
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template(url_for('home'))


@app.route("/subscribe", methods=["GET", "POST"])
# This function adds a user email to the Subscribers DB
def subscribe():
    if request.method == "POST":
        # check if username exists in DB
        existing_user = mongo.db.subscribers.find_one(
            {"email": request.form.get("subscribe").lower()})

        if existing_user:
            flash(" You are already signed up for our newsletter!")
            return redirect(url_for("home"))
            
        else:
            signup = {
                "email": request.form.get("subscribe").lower(),
            }
            # Add subscriber to DB
            mongo.db.subscribers.insert_one(signup)
            flash("You have successfully signed up to our mailinglist!")
            return redirect(url_for("home"))


@app.errorhandler(404)
# This function renders the 404 error page if there's a 404 error
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
