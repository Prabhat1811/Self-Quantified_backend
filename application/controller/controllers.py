from flask import Flask, request, render_template
from main import app
from flask_security import login_required

# @app.route("/", methods=["GET"])
# def main():
#     return render_template("main_page.html")

# @app.route("/home", methods=["GET"])
# @login_required
# def home():
#     return "Home"