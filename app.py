from os import getenv
from flask import Flask
import routes

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
