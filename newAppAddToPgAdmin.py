import requests
import psycopg2
import matplotlib.pyplot as plt

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

# Tworzenie pustych list na dane do wykresów
city_name_list = []
co_list = []
dew_list = []
h_list = []
no2_list = []
o3_list = []
p_list = []
pm10_list = []
pm25_list = []
r_list = []
so2_list = []
t_list = []
w_list = []

try:
    # Przechodzenie przez każde miasto
    for city in cities:
        # Pobranie danych z API
        response = requests.get(API_URL.format(city=city, API_KEY=API_KEY))
        data = response.json()

        # Wypełnienie list. Dane dla jednego miasta mają te same indeksy
        try:
            no_country = data['data']['city']['name'].split(', ')
            city_name_list.append(', '.join(no_country[:-1]))
            #city_name_list.append(data['data']['city']['name'].split(',')[-1])
        except KeyError:
            city_name_list.append(0)
        try:
            co_list.append(data['data']['iaqi']['co']['v'])
        except KeyError:
            co_list.append(0)
        try:
            dew_list.append(data['data']['iaqi']['dew']['v'])
        except KeyError:
            dew_list.append(0)
        try:
            h_list.append(data['data']['iaqi']['h']['v'])
        except KeyError:
            h_list.append(0)
        try:
            no2_list.append(data['data']['iaqi']['no2']['v'])
        except KeyError:
            no2_list.append(0)
        try:
            o3_list.append(data['data']['iaqi']['o3']['v'])
        except KeyError:
            o3_list.append(0)
        try:
            p_list.append(data['data']['iaqi']['p']['v'])
        except KeyError:
            p_list.append(0)
        try:
            pm10_list.append(data['data']['iaqi']['pm10']['v'])
        except KeyError:
            pm10_list.append(0)
        try:
            pm25_list.append(data['data']['iaqi']['pm25']['v'])
        except KeyError:
            pm25_list.append(0)
        try:
            r_list.append(data['data']['iaqi']['r']['v'])
        except KeyError:
            r_list.append(0)
        try:
            so2_list.append(data['data']['iaqi']['so2']['v'])
        except KeyError:
            so2_list.append(0)
        try:
            t_list.append(data['data']['iaqi']['t']['v'])
        except KeyError:
            t_list.append(0)
        try:
            w_list.append(data['data']['iaqi']['w']['v'])
        except KeyError:
            w_list.append(0)

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

chart_data = [co_list, dew_list, h_list, no2_list, o3_list, p_list, pm10_list, pm25_list, r_list, so2_list, t_list,
              w_list]
param_name = ['co', 'dew', 'h', 'no2', 'o3', 'p', 'pm10', 'pm25', 'r', 'so2', 't', 'w']
for i in range(len(chart_data)):
    plt.bar(city_name_list, chart_data[i])
    plt.xlabel('Miasto')
    plt.xticks(rotation=45, fontsize=6)
    plt.ylabel('Wartość')
    plt.title(param_name[i])
    plt.show()
