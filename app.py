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
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/rehearsal_studios")
def rehearsal_studios():
    return render_template("rehearsal_studios.html")


@app.route("/notice_board")
def notice_board():
    return render_template("notice_board.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/login")
def login():
    return render_template("login.html")


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


@app.route("/profile")
def profile():
    return render_template("profile.html")


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