from app import app
from flask import render_template, request, redirect, session
import users
import quizzes
import chat
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
def questions():
    question_list = chat.get_questions()

    if request.method == "GET":
        return render_template("chat.html", questions=question_list, error_message="")

    if request.method == "POST":
        content = request.form["content"].strip()
        if content == "":
            return render_template("chat.html", questions=question_list, error_message="You must type the question before sending it.")
        elif len(content) > 1000:
            return render_template("chat.html", questions=question_list, error_message="The question can have 1000 characters at maximum.")

        if chat.send_question(content):
            return redirect("/chat")
        else:
            return render_template("chat.html", questions=question_list, error_message="Oops, something went wrong. Please, try again!")

@app.route("/delete/<int:question_id>", methods=["GET"])
def delete_question(question_id):
    if chat.delete_question(question_id):
        return redirect("/chat")
    else:
        return render_template("error.html", message="You cannot delete this message.")

@app.route("/question/<int:question_id>", methods=["GET", "POST"])
def see_answers(question_id):
    question_info = chat.get_question_by_id(question_id)
    answer_list = chat.get_answers_by_question(question_id)

    if request.method == "GET":
        return render_template("question.html", question=question_info, answers=answer_list, error_message="")

    if request.method == "POST":
        content = request.form["content"].strip()
        if content == "":
            return render_template("question.html", question=question_info, answers=answer_list, error_message="Type your answer")
        elif len(content) > 1000:
            return render_template("question.html", question=question_info, answers=answer_list, error_message="The answer can have 1000 characters at maximum.")

        if chat.send_answer(question_id, content):
            url = f"/question/{question_id}"
            return redirect(url)
        else:
            return render_template("question.html", question=question_info, answers=answer_list, error_message="Oops, something went wrong. Please, try again.")

@app.route("/delete/<int:question_id>/<int:answer_id>", methods=["GET"])
def delete_answer(question_id, answer_id):
    if chat.delete_answer(answer_id):
        url = f"/question/{question_id}"
        return redirect(url)
    else:
        return render_template("error.html", message="You cannot delete this answer.")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")
