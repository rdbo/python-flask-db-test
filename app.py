from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask("test")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
user_count = 0

class UserInput(db.Model):
    uid = db.Column("user_id", db.String(10), unique=True, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, _username : str, _password : str):
        global user_count
        self.uid = user_count
        self.username = _username
        self.password = _password
        user_count += 1


@app.route("/", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
def index():
    global user_count
    if request.method == "POST":
        username = request.form["user"]
        password = request.form["pass"]
        if str(username) != "" and str(password) != "":
            data = UserInput(username, password)
            db.session.add(data)
            db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("index.html", user_list=UserInput.query.all())

db.create_all()
app.run()