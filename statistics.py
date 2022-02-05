from db import db

def get_user_stats(user_id):
    sql = "SELECT id, name FROM quizzes WHERE visible=1"
    quizzes = db.session.execute(sql).fetchall()

    data = []
    for quiz in quizzes:
        sql = """SELECT COALESCE(SUM(score),0), COUNT(*)
                 FROM attempts a
                 WHERE quiz_id=:quiz_id AND user_id=:user_id"""
        score = db.session.execute(sql, {"quiz_id":quiz[0], "user_id":user_id).fetchone()
        result = f"{quiz[1]}: {score[0]} / {score[1]} points"
        data.append(result)

    return data

def get_app_stats(user_id):
    sql = "SELECT role FROM users WHERE id=:user_id"
    role = db.session.execute(sql, {"id":user_id}).fetchone()[0]
    if role != "admin":
        return []

    sql = "SELECT COUNT(*) FROM users"
    user_count = db.session.execute(sql).fetchone()[0]

    sql = """SELECT q.id, q.name, COUNT(a.id) FROM attempts a, quizzes q
             WHERE q.id=a.quiz_id GROUP BY q.id"""
    data = db.session.execute(sql).fetchall()

    return [user_count, data]
