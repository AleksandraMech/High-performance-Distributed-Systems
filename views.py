from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import csv
import os
import cfg as cfg
import psycopg2
import json
import requests
from rabbitmq_sender import send_order_to_rabbitmq
from rabbitmq_receiver import receive_all_orders_from_rabbitmq  # Import the new function

views = Blueprint(__name__, "views")

def read_csv_and_save_to_database(file_path):
    data = []
    try:
        conn = psycopg2.connect(
            database=cfg.database,
            user=cfg.postgres_user,
            password=cfg.postgres_password,
            host=cfg.host,
            port=cfg.port
        )
        cur = conn.cursor()

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip the header row

            for row in csvreader:
                restaurant_name, category, dish, price = row
                price = price.replace('zł', '').replace('\xa0', '').replace(',', '.')
                
                # Check if price is valid
                try:
                    price_value = float(price)
                except ValueError:
                    price_value = None

                data.append({
                    "restaurant_name": restaurant_name,
                    "category": category,
                    "dish": dish,
                    "price": price if price_value is not None else "NULL"
                })

                # Insert data into the restaurant_data table
                if price_value is not None:
                    insert_query = """
                    INSERT INTO restaurant_data (restaurant_name, category, dish, price) 
                    VALUES (%s, %s, %s, %s)
                    """
                    cur.execute(insert_query, (restaurant_name, category, dish, price))
                else:
                    insert_query = """
                    INSERT INTO restaurant_data (restaurant_name, category, dish, price) 
                    VALUES (%s, %s, %s, NULL)
                    """
                    cur.execute(insert_query, (restaurant_name, category, dish))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Failed to save CSV data to the database: {e}")

    return data


def get_unique_values(data, key):
    return sorted(set(item[key] for item in data))

file_path = os.path.join(os.path.dirname(__file__), 'restaurants_menu.csv')
data = read_csv_and_save_to_database(file_path)

def save_order_to_database(order):
    try:
        conn = psycopg2.connect(
            database=cfg.database,
            user=cfg.postgres_user,
            password=cfg.postgres_password,
            host=cfg.host,
            port=cfg.port
        )
        cur = conn.cursor()
        zm = "INSERT INTO received_orders(order_data) VALUES (%s::jsonb)"
        cur.execute(zm, (json.dumps(order),))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Failed to save order to the database: {e}")

@views.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    dish_to_remove = request.form.get("dish")
    if "cart" in session:
        session["cart"] = [item for item in session["cart"] if item["dish"] != dish_to_remove]
        flash(f"Product '{dish_to_remove}' has been removed from the cart.")
    return redirect(url_for("views.cart"))

@views.route("/", methods=["GET", "POST"])
def home():
    filtered_data = data

    if request.method == "POST":
        restaurant_name_filter = request.form.get("restaurant_name")
        category_filter = request.form.get("category")

        if request.form.get("dish") and request.form.get("price"):
            dish = request.form.get("dish")
            price = request.form.get("price")

            if "cart" not in session:
                session["cart"] = []

            session["cart"].append({"dish": dish, "price": price})
            flash(f"Product '{dish}' has been added to the cart.")
            return redirect(url_for("views.home"))

        if restaurant_name_filter:
            filtered_data = [item for item in filtered_data if restaurant_name_filter.lower() in item["restaurant_name"].lower()]

        if category_filter:
            filtered_data = [item for item in filtered_data if category_filter.lower() in item["category"].lower()]

    headings = ['Restaurant Name', 'Category', 'Dish', 'Price', ' ']
    restaurant_names = get_unique_values(data, "restaurant_name")
    categories = get_unique_values(data, "category")

    return render_template("home.html", data=filtered_data, headings=headings, restaurant_names=restaurant_names, categories=categories)

@views.route("/cart")
def cart():
    cart = session.get("cart", [])
    total = sum(float(item["price"]) for item in cart)
    return render_template("cart.html", cart=cart, total=total)

@views.route("/send_order", methods=["POST"])
def send_order():
    cart = session.get("cart", [])

    if not cart:
        flash("Your cart is empty. Cannot send order.")
        return redirect(url_for("views.cart"))

    order_data = {
        "order": cart,
        "total": round(sum(float(item["price"]) for item in cart), 2)
    }

    if send_order_to_rabbitmq(order_data):
        flash("Order has been successfully sent.")
        session["cart"] = []  # Clear the cart after sending the order
    else:
        flash("Failed to send order to RabbitMQ.")

    return redirect(url_for("views.cart"))

@views.route("/received_orders", methods=["GET", "POST"])
def received_orders():
    try:
        conn = psycopg2.connect(
            database=cfg.database,
            user=cfg.postgres_user,
            password=cfg.postgres_password,
            host=cfg.host,
            port=cfg.port
        )
        cur = conn.cursor()

        if request.method == "POST":
            if request.form.get("action") == "receive_orders":
                new_orders = receive_all_orders_from_rabbitmq()
                if new_orders:
                    for order in new_orders:
                        save_order_to_database(order)
                    flash("All orders received from RabbitMQ.")
                else:
                    flash("No new orders in RabbitMQ.")
            elif request.form.get("action") == "remove_order":
                order_id = int(request.form.get("order_id"))
                update_query = "UPDATE received_orders SET accepted = TRUE WHERE id = %s"
                cur.execute(update_query, (order_id,))
                conn.commit()
                flash("Order has been accepted and removed from the list.")

        # Fetch non-accepted orders from the database
        select_query = "SELECT id, order_data FROM received_orders WHERE accepted = FALSE"
        cur.execute(select_query)
        received_orders = cur.fetchall()

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Failed to fetch received orders from the database: {e}")
        received_orders = []

    return render_template("received_orders.html", received_orders=received_orders)
