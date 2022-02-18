from app import app
from flask import render_template, request, redirect, session
import users
import quizzes
from chat import get_questions, get_answers_by_question, send_question, send_answer, delete_question, delete_answer
import statistics

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Invalid username or password. Please, try again!")

        return redirect("/home")

@app.route("/register", methods=["GET", "POST"])
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
            return render_template("error.html", message="This username might already be taken. Please, try choosing another username.")

        return redirect("/home")

@app.route("/home")
def home():
    return render_template("home.html", quizzes=quizzes.get_quizzes())

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    question_list = get_questions()

    if request.method == "GET":
        return render_template("chat.html", questions=question_list, error_message="")

    if request.method == "POST":
        content = request.form["content"].strip()
        if content == "":
            return render_template("chat.html", questions=question_list, error_message="You must type the question before sending it.")
        elif len(content) > 1000:
            return render_template("chat.html", questions=question_list, error_message="The question can have 1000 characters at maximum.")

        if send_question(content):
            return redirect("/chat")
        else:
            return render_template("chat.html", questions=question_list, error_message="Oops, something went wrong. Please, try again!")

@app.route("/delete/<int:question_id>", methods=["GET"])
def delete_q(question_id):
    if delete_question(question_id):
        return redirect("/chat")
    else:
        return render_template("error.html", message="You cannot delete this message.")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")
