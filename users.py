import os
from db import db
from flask import abort, request, session
from werkzeug.security import generate_password_hash, check_password_hash


def login(username, password):
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        return False
    if not check_password_hash(user[1], password):
        return False

    session["user_id"] = user[0]
    session["username"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()

    return True

def register(username, password, role):
    hash_value = generate_password_hash(password)

    try:
        sql = """INSERT INTO users (username, password, role)
                 VALUES (:username, :password, :role)"""
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False

    return login(username, password)

def logout():
    del session["user_id"]
    del session["username"]
    del session["user_role"]

def user_id():
    return session.get("user_id", -1)

def check_status():
    status = session.get("user_role", "")
    if status != "admin":
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def get_users():
    sql = "SELECT username FROM users"
    result = db.session.execute(sql).fetchall()
    usernames = []
    for tuple in result:
        usernames.append(tuple[0])
    return usernames

def delete_user(username):
    if username == "Admin":
        return False

    users = get_users()
    if not username in users:
        return False

    try:
        sql = "DELETE FROM users WHERE username=:username"
        db.session.execute(sql, {"username":username})
        db.session.commit()
    except:
        return False
    return True

def delete_own_account():
    status = session.get("user_role", "")
    if status == "admin":
        return False

    user_id = session.get("user_id", -1)
    if user_id == -1:
        return False

    try:
        sql = "DELETE from users WHERE id=:id"
        db.session.execute(sql, {"id":user_id})
        db.session.commit()
    except:
        return False
    logout()
    return True
