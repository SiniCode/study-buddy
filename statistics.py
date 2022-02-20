from db import db

def get_user_stats(user_id):
    sql = "SELECT id, name FROM quizzes WHERE visible=1"
    quizzes = db.session.execute(sql).fetchall()

    data = ["Quiz: correct solutions / all attempts (success rate)"]
    for quiz in quizzes:
        sql = """SELECT COALESCE(SUM(score),0), COUNT(*)
                 FROM attempts
                 WHERE quiz_id=:quiz_id AND user_id=:user_id"""
        score = db.session.execute(sql, {"quiz_id":quiz[0], "user_id":user_id}).fetchone()
        if score[1] == 0:
            success_rate = 0
        else:
            success_rate = score[0]/score[1]*100
        result = f"{quiz[1]}: {score[0]} / {score[1]} points ({success_rate:.2f}%)"
        data.append(result)

    return data

def get_user_count():
    sql = "SELECT COUNT(*) FROM users"
    user_count = db.session.execute(sql).fetchone()[0]
    return user_count

def get_quiz_stats(user_id):
    sql = "SELECT role FROM users WHERE id=:user_id"
    role = db.session.execute(sql, {"user_id":user_id}).fetchone()[0]
    if role != "admin":
        return []

    data = ["Quiz (id): number of attempts"]
    sql = """SELECT Q.id, Q.name, COUNT(A.id)
             FROM quizzes Q LEFT JOIN attempts A ON Q.id=A.quiz_id
             WHERE Q.visible=1
             GROUP BY Q.id"""
    quizzes = db.session.execute(sql).fetchall()
    for quiz in quizzes:
        result = f"{quiz[1]} ({quiz[0]}): {quiz[2]}"
        data.append(result)
    return data
