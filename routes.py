from app import app
from flask import render_template, request, redirect, session
import users


@app.route("/", methods=["get", "post"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Invalid username or password. Please, try again!")

        return redirect("/home")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Make sure the username has 1 to 20 characters.")

        password = request.form["password"]
        if len(password) < 3 or len(password) > 20:
            return render_template("error.html", message="Make sure the password has 3 to 20 characters.")

        if not users.register(username, password, "buddy"):
            return render_template("error.html", message="Something went wrong. This username might already be taken. Please, try choosing another username.")

        return redirect("/home")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")
