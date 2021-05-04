import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime, date
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)
today = datetime.now()


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
    page = request.args.get("page")
    # Pagination
    if page is not None:
        current_page = int(page)
    else:
        current_page = 1

    # Pagination Variables
    number_per_page = 6
    number_of_pages = round(len(posts) / number_per_page)
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
            "date": datetime.strptime(
                request.form.get("booking-date"), '%b %d, %Y'),
            "slot": request.form.get("time-slot"),
            "contact_name": request.form.get("contact_name"),
            "additional_info": request.form.get("additional_info"),
            "created_by": session["user"]
        }
        mongo.db.bookings.insert_one(booking)
        flash("Booking Successful")
        return redirect(url_for(
            "profile", username=session["user"], today=today))

    return render_template("bookings.html")


@app.route("/admin/<username>", methods=["GET", "POST"])
def admin(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    bookings = list(mongo.db.bookings.find())
    if session["user"]:
        return render_template(
            "admin.html", username=username,
            bookings=bookings, today=today)


@app.route("/edit_booking/<booking_id>", methods=["GET", "POST"])
def edit_booking(booking_id):
    if request.method == "POST":

        existing_booking = mongo.db.bookings.find_one(
            {"studio": request.form.get("studio"), "date": request.form.get(
                "booking-date"), "slot": request.form.get("time-slot")})

        if existing_booking:
            flash("Update unsuccessful check availability before booking")
            return redirect(url_for("bookings"))

        submit = {
            "studio": request.form.get("studio"),
            "date": datetime.strptime(
                request.form.get("booking-date"), '%b %d, %Y'),
            "slot": request.form.get("time-slot"),
            "contact_name": request.form.get("contact_name"),
            "additional_info": request.form.get("additional_info"),
            "created_by": session["user"]
        }
        mongo.db.bookings.update({"_id": ObjectId(booking_id)}, submit)
        flash("Booking Successfully Updated")
        return redirect(url_for("profile", username=session["user"]))

    booking = mongo.db.bookings.find_one({"_id": ObjectId(booking_id)})
    return render_template("edit_booking.html", booking=booking)


@app.route("/delete_booking/<booking_id>")
def delete_booking(booking_id):
    mongo.db.bookings.remove({"_id": ObjectId(booking_id)})
    if session["user"] == "admin":
        flash("Booking successfully deleted")
        return redirect(url_for("admin", username=session["user"]))
    flash("Booking successfully deleted")
    return redirect(url_for("profile", username=session["user"]))


@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        post = {
            "post_title": request.form.get("post_title"),
            "post_message": request.form.get("post_message"),
            "is_urgent": is_urgent,
            "category": request.form.get("category"),
            "created_by": session["user"],
            "email": request.form.get("email"),
            "date_posted": today
        }
        mongo.db.posts.insert_one(post)
        flash("Post Successfully Added")
        return redirect(url_for("notice_board"))

    return render_template("add_post.html")


@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
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
            "date_posted": str(today)
        }
        mongo.db.posts.update({"_id": ObjectId(post_id)}, submit)
        flash("Post Successfully Updated")
        return redirect(url_for("notice_board"))

    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    return render_template("edit_post.html", post=post)


@app.route("/delete_post/<post_id>")
def delete_post(post_id):
    mongo.db.posts.remove({"_id": ObjectId(post_id)})
    flash("Post successfully deleted")
    return redirect(url_for("notice_board"))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab session user's username from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    bookings = list(mongo.db.bookings.find())
    if session["user"]:
        return render_template(
            "profile.html", username=username, bookings=bookings, today=today)
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
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


@app.route("/subscribe", methods=["GET", "POST"])
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
            mongo.db.subscribers.insert_one(signup)
            flash("You have successfully signed up to our mailinglist!")
            return redirect(url_for("home"))


# 404 template error page:
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)