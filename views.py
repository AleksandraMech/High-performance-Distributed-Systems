from flask import Blueprint, render_template

from main import products

views = Blueprint(__name__,"views")

@views.route("/")
def home():
    return render_template("home.html", products=products)


@views.route("/cart")
def cart():
    return render_template("cart.html")




