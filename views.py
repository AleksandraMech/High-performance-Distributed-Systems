from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import csv
import os
import cfg as cfg
import psycopg2
import requests


views = Blueprint(__name__, "views")

def read_csv_and_save_to_database(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row

        # Iterate through each row in the CSV file
        for row in csvreader:
            # Extract data from the CSV row
            restaurant_name, category, dish, price = row
            # Remove 'zł' and non-breaking spaces, convert comma to dot
            price = price.replace('zł', '').replace('\xa0', '').replace(',', '.')
            # Append the data to the list
            data.append({
                "restaurant_name": restaurant_name,
                "category": category,
                "dish": dish,
                "price": price
            })

            
         #   conn = psycopg2.connect( database=cfg.database, user=cfg.postgres_user,password=cfg.postgres_password, host=cfg.host, port=cfg.port)
          #  if conn is not None:
           #     cur = conn.cursor()
            #    zm = "INSERT INTO restaurants_menu(restaurant_name, category, dish, price) VALUES ( \'"+str(restaurant_name)+"\',  \'"+str(category)+"\',  \'"+str(dish)+"\',  \'"+str(price)+"\')"
             #   cur.execute(zm, (restaurant_name, category, dish, price))
              #  conn.commit()
               # cur.close()
                #conn.close()
            
    return data

def get_unique_values(data, key):
    return sorted(set(item[key] for item in data))

# Przygotowanie danych do użycia globalnego
file_path = os.path.join(os.path.dirname(__file__), 'restaurants_menu.csv')
data = read_csv_and_save_to_database(file_path)

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
            # Handle adding to cart
            dish = request.form.get("dish")
            price = request.form.get("price")
            
            if "cart" not in session:
                session["cart"] = []
            
            session["cart"].append({"dish": dish, "price": price})
           # conn = psycopg2.connect( database=cfg.database, user=cfg.postgres_user,password=cfg.postgres_password, host=cfg.host, port=cfg.port)
          #  if conn is not None:
             #   cur = conn.cursor()
           #     varying_array = dish.split(',')
            #    zm = "INSERT INTO order(dish, price) VALUES (%s)"
             #   cur.execute(zm, (varying_array))
              #  conn.commit()
               # cur.close()
                #conn.close()

            flash(f"Product '{dish}' has been added to the cart.")
            return redirect(url_for("views.home"))
        
        if restaurant_name_filter:
            filtered_data = [item for item in filtered_data if restaurant_name_filter.lower() in item["restaurant_name"].lower()]
        
        if category_filter:
            filtered_data = [item for item in filtered_data if category_filter.lower() in item["category"].lower()]

    headings = ['Restaurant Name', 'Category', 'Dish', 'Price', ' ']
    restaurant_names = get_unique_values(data, "restaurant_name")
    categories = get_unique_values(data, "category")
    
    return render_template( "home.html", data=filtered_data, headings=headings, restaurant_names=restaurant_names, categories=categories)

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

    # Przykładowy URL zewnętrznego serwisu (httpbin.org dla celów testowych)
    external_service_url = "https://httpbin.org/post"

    # Przygotowanie danych do wysłania
    order_data = {
        "order": cart,
        "total": round(sum(float(item["price"]) for item in cart), 2)
    }

    try:
        # Wysłanie danych do zewnętrznego serwisu
        response = requests.post(external_service_url, json=order_data)

        # Sprawdzenie odpowiedzi z serwisu
        if response.status_code == 200:
            flash("Order has been successfully sent.")
            session["cart"] = []  # Wyczyszczenie koszyka po wysłaniu zamówienia
        else:
            flash(f"Failed to send order. Error: {response.status_code}")
    except requests.RequestException as e:
        flash(f"An error occurred while sending the order: {e}")

    return redirect(url_for("views.cart"))

