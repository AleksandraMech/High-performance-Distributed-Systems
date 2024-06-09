from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import csv
import os

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
    return data

def get_unique_values(data, key):
    return sorted(set(item[key] for item in data))

# Przygotowanie danych do użycia globalnego
file_path = os.path.join(os.path.dirname(__file__), 'restaurants_menu.csv')
data = read_csv_and_save_to_database(file_path)

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
            flash(f"Product '{dish}' has been added to the cart.")
            return redirect(url_for("views.home"))
        
        if restaurant_name_filter:
            filtered_data = [item for item in filtered_data if restaurant_name_filter.lower() in item["restaurant_name"].lower()]
        
        if category_filter:
            filtered_data = [item for item in filtered_data if category_filter.lower() in item["category"].lower()]

    headings = ['Restaurant Name', 'Category', 'Dish', 'Price', ' ']
    restaurant_names = get_unique_values(data, "restaurant_name")
    categories = get_unique_values(data, "category")
    
    return render_template(
        "home.html", 
        data=filtered_data, 
        headings=headings, 
        restaurant_names=restaurant_names, 
        categories=categories
    )

@views.route("/cart")
def cart():
    cart = session.get("cart", [])
    total = sum(float(item["price"]) for item in cart)
    return render_template("cart.html", cart=cart, total=total)
