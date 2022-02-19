from random import randint
from db import db


def add_quiz(name, description, exercises, visible=1):
    sql = """INSERT INTO quizzes (name, description, visible)
             VALUES (:name, :description, :visible) RETURNING id"""
    quiz_id = db.session.execute(sql, {"name":name, "description":description, "visible":visible}).fetchone()[0]

    for exercise in exercises.split("\n"):
        parts = exercise.strip().split(";")
        if len(parts) != 2:
            continue

        sql = """INSERT INTO exercises (quiz_id, task, solution)
                 VALUES (:quiz_id, :task, :solution)"""
        db.session.execute(sql, {"quiz_id":quiz_id, "task":parts[0], "solution":parts[1]})

    db.session.commit()
    return quiz_id

def count_exercises(quiz_id):
    sql = "SELECT COUNT(*) FROM exercises WHERE quiz_id=:quiz_id"
    return db.session.execute(sql, {"quiz_id":quiz_id}).fetchone()

def get_random_task(quiz_id):
    ex_count = int(count_exercises(quiz_id)[0])
    pos = randint(0, ex_count-1)
    sql = "SELECT id, task FROM exercises WHERE quiz_id=:quiz_id LIMIT 1 OFFSET :pos"
    return db.session.execute(sql, {"quiz_id":quiz_id, "pos":pos}).fetchone()

def get_solution(exercise_id):
    sql = "SELECT solution FROM exercises WHERE id=:exercise_id"
    return db.session.execute(sql, {"exercise_id":exercise_id}).fetchone()[0]

def get_quizzes():
    sql = "SELECT id, name FROM quizzes WHERE visible=1"
    return db.session.execute(sql).fetchall()

def get_quiz_info(quiz_id):
    sql = "SELECT name, description FROM quizzes WHERE id=:quiz_id"
    return db.session.execute(sql, {"quiz_id":quiz_id}).fetchone()
