import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "db"))

from flask import Flask, request, redirect, url_for, flash, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from dbhelper import getall, getrecord, addrecord, init_db

app: Flask = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key-before-deploying")


@app.after_request
def after_request(response):
    # Stops the browser "Back" button from showing a cached page after logout.
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/userlogin", methods=["POST"])
def userlogin():
    email: str = request.form["email"]
    password: str = request.form["password"]
    user: list = getrecord("users", email=email)
    if len(user) > 0 and check_password_hash(user[0]["password"], password):
        session["email"] = user[0]["email"]
        session["name"] = user[0]["name"]
        return redirect(url_for("main"))
    flash("Invalid e-mail or password.", "error")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name: str = request.form["name"]
        email: str = request.form["email"]
        password: str = request.form["password"]
        confirm: str = request.form["confirm"]
        if not name or not email or not password or not confirm:
            flash("All fields are required.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        elif len(getrecord("users", email=email)) > 0:
            flash("That e-mail is already registered.", "error")
        else:
            addrecord("users", email=email, password=generate_password_hash(password), name=name)
            flash("Registration successful. You can now log in.", "success")
            return redirect(url_for("index"))
        return render_template("register.html", name=name, email=email)
    return render_template("register.html", name="", email="")


@app.route("/main")
def main():
    if "email" in session:
        return render_template("main.html", students=getall("students"))
    flash("Please log in first.", "error")
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)), debug=os.environ.get("FLASK_DEBUG") == "1")
