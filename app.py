import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, date
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)
today = date.today().strftime('%d/%m/%Y')


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/rehearsal_studios")
def rehearsal_studios():
    return render_template("rehearsal_studios.html")


@app.route("/notice_board")
def notice_board():
    posts = list(mongo.db.posts.find().sort([("_id", -1)]))
    return render_template(
        "notice_board.html", posts=posts)



@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/login/", methods=["GET", "POST"])
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
                session.permanent = True
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
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/bookings")
def bookings():
    return render_template("bookings.html")


@app.route("/check_availability", methods=["GET", "POST"])
def check_availability():
    if request.method == "POST":
        # check if booking already exists in db
        date = request.form.get("date")
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
                    {date} for the {slot} slot")
        elif available_studios == "all":
            flash(
                f"Currently all three studios are available on\
                    {date} in the {slot}")
        else:
            flash(
                f"Studio {available_studios} currently available on\
                    {date} in the {slot}")
    return redirect(url_for("bookings"))


@app.route("/new_booking", methods=["GET", "POST"])
def new_booking():
    if request.method == "POST":
        existing_booking = mongo.db.bookings.find_one(
            {"studio": request.form.get("studio"), "date": request.form.get(
                "booking-date"), "slot": request.form.get("time-slot")})
        if existing_booking:
            flash("Booking unsuccessful check availability before booking")
            return redirect(url_for("bookings"))
        booking = {
            "studio": request.form.get("studio"),
            "date": request.form.get("booking-date"),
            "slot": request.form.get("time-slot"),
            "contact_name": request.form.get("contact_name"),
            "additional_info": request.form.get("additional_info"),
            "created_by": session["user"]
        }
        mongo.db.bookings.insert_one(booking)
        flash("Booking Successful")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("bookings.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/edit_booking")
def edit_booking():
    return render_template("edit_booking.html")


@app.route("/add_post")
def add_post():
    return render_template("add_post.html")


@app.route("/edit_post")
def edit_post():
    return render_template("edit_post.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab session user's username from the database
    today = date.today().strftime('%b %d/%Y')
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    bookings = list(mongo.db.bookings.find())
    if session["user"]:
        return render_template(
            "profile.html", username=username, bookings=bookings, today=today)
    return redirect(url_for("login"))


@app.route("/call_modal", methods=["GET", "POST"])
def call_modal():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("home"))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template(url_for('home'))


# 404 template error page:
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)