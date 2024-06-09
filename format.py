import csv

# Ścieżka do oryginalnego pliku CSV
input_file_path = 'restaurants_menu.csv'

# Ścieżka do nowego pliku CSV
output_file_path = 'restaurants_menu_modified.csv'

# Otwórz oryginalny plik CSV do odczytu i nowy plik CSV do zapisu
with open(input_file_path, 'r', newline='', encoding='utf-8') as input_file, \
        open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)

    # Zapisz nagłówki
    headers = next(csv_reader)
    csv_writer.writerow(headers)

    # Zapisz dane w nawiasach klamrowych
    for row in csv_reader:
        csv_writer.writerow(['{' + cell + '}' for cell in row])
