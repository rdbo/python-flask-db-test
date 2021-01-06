from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask("test")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class UserInput(db.Model):
    uid = db.Column("user_id", db.String(10), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, _username : str, _password : str):
        self.username = _username
        self.password = _password


@app.route("/", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["user"]
        password = request.form["pass"]
        if str(username) != "" and str(password) != "":
            data = UserInput(username, password)
            db.session.add(data)
            db.session.commit()
    else:
        return render_template("index.html", user_list=UserInput.query.all())

db.create_all()
app.run()