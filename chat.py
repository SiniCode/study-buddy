from db import db
import users

def get_questions():
    sql = """SELECT Q.id, U.id, U.username, Q.sent_at, Q.content
             FROM users U, questions M
             WHERE Q.user_id=U.id AND Q.visible=1
             ORDER BY Q.id"""
    questions = db.session.execute(sql)
    return questions.fetchall()

def get_answers_by_question(question_id):
    sql = """SELECT A.id, U.id, U.username, A.sent_at, A.content
             FROM users U, Answers A
             WHERE A.user_id=U.id AND A.question_id=:question_id AND A.visible=1
             ORDER BY A.id"""
    answers = db.session.execute(sql)
    return answers.fetchall()

def send_question(content):
    user_id = users.user_id()
    if user_id == -1:
        return False
    sql = """INSERT INTO questions (user_id, sent_at, content, visible)
             VALUES (:user_id, NOW(), :content, 1)"""
    db.session.execute(sql, {"user_id":user_id, "content":content})
    db.session.commit()
    return True

def send_answer(question_id, content):
    user_id = users.user_id()
    if user_id == -1:
        return False
    sql = """INSERT INTO answers (question_id, user_id, sent_at, content, likes, visible)
             VALUES (:question_id, :user_id, NOW(), :content, 0, 1)"""
    db.session.execute(sql, {"question_id":question_id, "user_id":user_id, "content":content})
    db.session.commit()
    return True

def delete_question(question_id):
    user_id = users.user_id()
    if user_id == -1:
        return False
    sql = """UPDATE questions SET visible=0
             WHERE id=:id AND user_id=:user_id"""
    db.session.execute(sql, {"id":question_id, "user_id":user_id})
    return True

def delete_answer(answer_id):
    user_id = users.user_id()
    if user_id == -1:
        return False
    sql = """UPDATE answers SET visible=0
             WHERE id=:id AND user_id=:user_id"""
    db.session.execute(sql, {"id":answer_id, "user_id":user_id})
    return True
