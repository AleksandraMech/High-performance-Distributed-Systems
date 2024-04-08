from flask import Blueprint, render_template
<<<<<<< HEAD
from main import products

views = Blueprint(__name__,"views")

@views.route("/")
def home():
    return render_template("index.html", products=products)

=======

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")
>>>>>>> 971d77e30fcdaf8951b730a780c33b46d59585da
