from app import app
from flask import render_template, request, redirect, session
import users
import quizzes
import chat
import statistics
import random

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", error="", prefill="")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("index.html", error="Invalid username or password. Please, try again!", prefill=username)

        return redirect("/home")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", error="", prefill="")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        error = ""

        if len(username) < 1 or len(username) > 20:
            error += "Make sure the username has 1 to 20 characters."
        if len(password) < 3 or len(password) > 20:
            error += " Make sure the password has 3 to 20 characters."
        if password != password2:
            error += " Make sure that the passwords match."

        if error != "":
            return render_template("register.html", error=error, prefill=username)

        if username == "Admin":
            if not users.register(username, password, "admin"):
                return render_template("register.html", error="Please select another username and try again.", prefill="")
            else:
                return redirect("/home")
        else:
            if not users.register(username, password, "buddy"):
                return render_template("register.html", error="This username might already be taken. Please, try choosing another username.", prefill="")

            return redirect("/home")

@app.route("/home")
def home():
    return render_template("home.html", quizzes=quizzes.get_quizzes())

@app.route("/play/<int:quiz_id>", methods=["GET", "POST"])
def play(quiz_id):
    quiz = quizzes.get_quiz_info(quiz_id)

    if request.method == "GET":
        user_id = users.user_id()
        if user_id == -1:
            return render_template("error.html", message="You must log in to play.")

        task = quizzes.get_random_task(quiz_id)
        return render_template("play.html", quiz_id=quiz_id, quiz_name=quiz[0], quiz_description=quiz[1], task=task[1], exercise_id=task[0], feedback="")

    feedback_pool = ["Well done, buddy!", "Great!", "Good job, buddy!", "Spot on!", "Amazing!", "Correct!", "Nice!"]
    if request.method == "POST":
        users.check_csrf()

        exercise_id = request.form["exercise_id"]
        answer = request.form["answer"].strip().lstrip("0")
        correct = quizzes.get_solution(exercise_id)

        if answer.lower() == correct.lower():
            quizzes.save_attempt(users.user_id(), quiz_id, 1)
            feedback = random.choice(feedback_pool)
        else:
            quizzes.save_attempt(users.user_id(), quiz_id, 0)
            feedback = f"Not quite, buddy... Your solution was {answer}, and the correct solution was {correct}. Keep going!"

        task = quizzes.get_random_task(quiz_id)
        return render_template("play.html", quiz_id=quiz_id, quiz_name=quiz[0], quiz_description=quiz[1], task=task[1], exercise_id=task[0], feedback=feedback)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/chat", methods=["GET", "POST"])
def questions():
    question_list = chat.get_questions()

    if request.method == "GET":
        return render_template("chat.html", questions=question_list, error_message="", prefill="")

    if request.method == "POST":
        users.check_csrf()
        content = request.form["content"].strip()
        if content == "":
            return render_template("chat.html", questions=question_list, error_message="You must type the question before sending it.", prefill="")
        elif len(content) > 1000:
            return render_template("chat.html", questions=question_list, error_message="The question can have 1000 characters at maximum.", prefill=content)

        if chat.send_question(content):
            return redirect("/chat")
        else:
            return render_template("chat.html", questions=question_list, error_message="Oops, something went wrong. Please, try again!", prefill=content)

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
        return render_template("question.html", question=question_info, answers=answer_list, error_message="", prefill="")

    if request.method == "POST":
        users.check_csrf()
        content = request.form["content"].strip()
        if content == "":
            return render_template("question.html", question=question_info, answers=answer_list, error_message="Type your answer", prefill="")
        elif len(content) > 1000:
            return render_template("question.html", question=question_info, answers=answer_list, error_message="The answer can have 1000 characters at maximum.", prefill=content)

        if chat.send_answer(question_id, content):
            url = f"/question/{question_id}"
            return redirect(url)
        else:
            return render_template("question.html", question=question_info, answers=answer_list, error_message="Oops, something went wrong. Please, try again.", prefill=content)

@app.route("/delete/<int:question_id>/<int:answer_id>", methods=["GET"])
def delete_answer(question_id, answer_id):
    if chat.delete_answer(answer_id):
        url = f"/question/{question_id}"
        return redirect(url)
    else:
        return render_template("error.html", message="You cannot delete this answer.")

@app.route("/statistics", methods=["GET", "POST"])
def user_statistics():
    if request.method == "GET":
        user_id = users.user_id()
        if user_id == -1:
            return render_template("error.html", message="You must log in to see the stats.")

        stats = statistics.get_user_stats(user_id)
        return render_template("statistics.html", stats=stats, error="")

    if request.method == "POST":
        users.check_csrf()
        if users.delete_own_account():
            return redirect("/register")
        else:
            stats = statistics.get_user_stats(user_id)
            return render_template("statistics.html", stats=stats, error="Deletion didn't succeed. Please, try again.")

@app.route("/create", methods=["GET", "POST"])
def create_quiz():
    users.check_status()

    if request.method == "GET":
        return render_template("create.html", error="", prename="", predescription="", pre_exercises="task;solution")

    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"].strip()
        description = request.form["description"].strip()
        exercises = request.form["exercises"].strip()
        error = ""

        if len(name) < 1 or len(name) > 30:
            error += "The name must have 1 to 30 characters."
        if len(description) > 500:
            error += " The description can have 500 characters at maximum."
        if len(exercises) > 10000:
            error += " The exercise section can have 10000 characters at maximum."

        if error != "":
            return render_template("create.html", error=error, prename=name, predescription=description, pre_exercises=exercises)

        quiz_id = quizzes.add_quiz(name, description, exercises)
        return redirect("/play/"+str(quiz_id))

@app.route("/admin", methods=["GET"])
def admin():
    user_count = statistics.get_user_count()
    quiz_list = statistics.get_quiz_stats(users.user_id())
    deleted = quizzes.get_deleted_quizzes()

    return render_template("admin.html", user_count=user_count, quizzes=quiz_list, deleted=deleted, message="")

@app.route("/delete/user", methods=["POST"])
def delete_user():
    users.check_csrf()
    users.check_status()

    quiz_list = statistics.get_quiz_stats(users.user_id())
    deleted = quizzes.get_deleted_quizzes()

    username = request.form["username"]
    if users.delete_user(username):
        user_count = statistics.get_user_count()
        return render_template("admin.html", user_count=user_count, quizzes=quiz_list, deleted=deleted, message=f"User {username} was deleted.")
    else:
        user_count = statistics.get_user_count()
        return render_template("admin.html", user_count=user_count, quizzes=quiz_list, deleted=deleted, message=f"Deleting {username} didn't succeed. Check the username and try again.")

@app.route("/delete/quiz", methods=["POST"])
def delete_quiz():
    users.check_csrf()

    user_count = statistics.get_user_count()

    quiz_id = request.form["quiz_id"]
    if quizzes.delete_quiz(quiz_id):
        quiz_list = statistics.get_quiz_stats(users.user_id())
        deleted = quizzes.get_deleted_quizzes()
        return render_template("admin.html", user_count=user_count, quizzes=quiz_list, deleted=deleted, message="The quiz was deleted.")
    else:
        quiz_list = statistics.get_quiz_stats(users.user_id())
        deleted = quizzes.get_deleted_quizzes()
        return render_template("admin.html", user_count=user_count, quizzes=quiz_list, deleted=deleted, message="Deleting the quiz didn't succeed. Check the id number and try again.")

@app.route("/restore", methods=["POST"])
def restore_quiz():
    users.check_csrf()

    user_count = statistics.get_user_count()

    quiz_id = request.form["quiz_id"]
    if quizzes.restore_quiz(quiz_id):
        quiz_list = statistics.get_quiz_stats(users.user_id())
        deleted = quizzes.get_deleted_quizzes()
        return render_template("admin.html", user_count=user_count, quizzes=quiz_list, deleted=deleted, message="The quiz was restored!")
    else:
        quiz_list = statistics.get_quiz_stats(users.user_id())
        deleted = quizzes.get_deleted_quizzes()
        return render_template("admin.html", user_count=user_count, quizzes=quiz_list, deleted=deleted, message="Restoring the quiz didn't succeed. Check the id number and try again.")

@app.route("/rename", methods=["POST"])
def rename():
    users.check_csrf()

    user_count = statistics.get_user_count()

    quiz_id = request.form["quiz_id"]
    new_name = request.form["new_name"]
    if quizzes.rename_quiz(quiz_id, new_name):
        quiz_list = statistics.get_quiz_stats(users.user_id())
        deleted = quizzes.get_deleted_quizzes()
        return render_template("admin.html", user_count=user_count, quizzes=quiz_list, deleted=deleted, message="The quiz was renamed!")
    else:
        quiz_list = statistics.get_quiz_stats(users.user_id())
        deleted = quizzes.get_deleted_quizzes()
        return render_template("admin.html", user_count=user_count, quizzes=quiz_list, deleted=deleted, message="Restoring the quiz didn't succeed. Check the id and try again.")

