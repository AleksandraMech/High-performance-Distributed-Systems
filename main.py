import csv
import psycopg2
import cfg as cfg
import os
from datetime import datetime

def read_csv_and_save_to_database(file_path):
    try:
        # Create a connection to the PostgreSQL database
        conn = psycopg2.connect(
            database=cfg.database,
            user=cfg.postgres_user,
            password=cfg.postgres_password,
            host=cfg.host,
            port=cfg.port
        )

        if conn is not None:
            cur = conn.cursor()

            # Open the CSV file
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip the header row

                # Iterate through each row in the CSV file
                for row in csvreader:
                    # Extract data from the CSV row
                    restaurant_name, category, dish, price = row

                       # Print the data
#print("Restaurant Name:", restaurant_name)
                 #   print("Category:", category)
#print("Dish:", dish)
                 #   print("Price:", price)
#print("-----------------------------")

                    # Remove ' zł' from price and convert to float
                   # price = float(price.replace(' zł', '').replace(',', '.'))

                    # Get current datetime
                   # now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Insert data into the database
                   # zm = "INSERT INTO restaurants_menu(restaurant_name, category, dish, price) VALUES ( \'"+str(restaurant_name)+"\',  \'"+str(category)+"\',  \'"+str(dish)+"\',  \'"+str(price)+"\')"
                 #   zm = "INSERT INTO restaurants_menu(restaurant_name, category, dish, price) VALUES (%s, %s, %s, %s, %s)"
                 #   cur.execute(zm, (restaurant_name, category, dish, price))
#cur.execute(zm, (restaurant_name, category, dish, price, now))


            print("Data saved to the PostgreSQL database")

            # Commit and close the connection
            conn.commit()
            cur.close()
            conn.close()
        else:
            print("Failed to connect to the database")
    except Exception as e:
        print("Error: An unexpected error occurred while saving data to the database.")
        print(e)

def main():
    # Use absolute path for the CSV file
    file_path = os.path.join(os.path.dirname(__file__), 'restaurants_menu.csv')

    read_csv_and_save_to_database(file_path)
    

if __name__ == '__main__':
    main()
