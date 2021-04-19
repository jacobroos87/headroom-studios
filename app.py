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


# 404 template error page:
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)