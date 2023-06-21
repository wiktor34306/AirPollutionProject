import requests
import psycopg2

# Dane dostępowe do bazy danych
DB_HOST = '195.150.230.208'
DB_PORT = '5432'
DB_NAME = '2022_cich_bartlomiej'
DB_USER = '2022_cich_bartlomiej'
DB_PASSWORD = '33642'

# Klucz API
API_KEY = "05b1a42bda64f294587fd9a738864c30017b0173"

# Adres URL API
API_URL = "https://api.waqi.info/feed/{city}/?token={API_KEY}"

# Miasta w Polsce, dla których chcesz pobrać dane
cities = ["Warszawa", "Kraków", "Gdańsk", "Poznań", "Wrocław", "Lublin", "Łódź", "Gdynia", "Tarnów", "Szczecin", "Bydgoszcz", "Toruń", "Zamość", "Rzeszów", "Nowy Sącz", "Dębica", "Białystok", "Opole", "Przemyśl", "Bydgoszcz", "Gorzów Wielkopolski", "Katowice", "Zielona Góra"]

try:
    # Przechodzenie przez każde miasto
    for city in cities:
        # Pobranie danych z API
        response = requests.get(API_URL.format(city=city, API_KEY=API_KEY))
        data = response.json()

        # Przetwarzanie danych i dodawanie do bazy danych
        city_name = data['data']['city']['name']
        country = city_name.split(",")[-1].strip()

        # Sprawdzenie czy dane są dostępne dla Polski
        if country in ['Poland']:
            # Połączenie z bazą danych
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = conn.cursor()

            aqi = data['data']['aqi']
            index_name = data['data']['dominentpol']
            index_value = data['data']['iaqi'][index_name]['v']
            date = data['data']['time']['s']

            # Pobranie wartości PM10
            pm10_value = data['data']['iaqi'].get('pm10', {}).get('v')

            # Sprawdzenie czy rekord o takim samym mieście i dacie już istnieje
            query_check_duplicate = "SELECT 1 FROM widok.pomiary_nowe WHERE miasto = %s AND data = %s"
            values_check_duplicate = (city_name, date)
            cursor.execute(query_check_duplicate, values_check_duplicate)
            if cursor.fetchone() is None:
                # Jeśli rekord nie istnieje, wykonaj operacje wstawiania i aktualizacji
                # Tworzenie i wykonanie zapytania SQL
                query_insert = "INSERT INTO widok.pomiary_nowe (miasto, kraj, indeks_powietrza, nazwa_indeksu, wartosc_indeksu, data) " \
                               "VALUES (%s, %s, %s, %s, %s, %s)"
                values_insert = (city_name, country, aqi, index_name, index_value, date)
                cursor.execute(query_insert, values_insert)

                if pm10_value is not None and pm10_value == data['data']['iaqi'].get('pm25', {}).get('v'):
                    # Dodanie wartości PM10 do kolumny "nazwa_indeksu"
                    query_update_pm10 = "UPDATE widok.pomiary_nowe SET nazwa_indeksu = %s WHERE miasto = %s AND data = %s"
                    values_update_pm10 = ("pm10", city_name, date)
                    cursor.execute(query_update_pm10, values_update_pm10)

                print(f"Dane dla miasta {city_name} zostały dodane do bazy danych.")
            else:
                print(f"Dane dla miasta {city_name} i daty {date} już istnieją w bazie danych.")

            # Zatwierdzenie zmian i zamknięcie połączenia z bazą danych
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print(f"Brak danych dla miasta {city} w Polsce.")

except (requests.RequestException, psycopg2.Error, ValueError) as error:
    print("Wystąpił błąd:", str(error))

