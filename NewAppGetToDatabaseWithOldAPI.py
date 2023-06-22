import requests
import psycopg2

# Dane dostępowe do bazy danych
DB_HOST = '195.150.230.208'
DB_PORT = '5432'
DB_NAME = '2022_cich_bartlomiej'
DB_USER = '2022_cich_bartlomiej'
DB_PASSWORD = '33642'

# Adres URL API OpenAQ
API_URL = "https://api.openaq.org/v2/latest"

try:
    # Pobranie danych z API OpenAQ dla polskich miast
    params = {
        'country': 'PL',
        'limit': 100000
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    # Połączenie z bazą danych
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    # Przetwarzanie danych i zapis do bazy danych
    measurements = data['results']
    for measurement in measurements:
        location = measurement['location']
        city = measurement['city']
        coordinates = measurement['coordinates']
        latitude = coordinates['latitude']
        longitude = coordinates['longitude']

        if city is not None:
            pm10_value = None
            pm25_value = None
            pm10_last_updated = None
            pm25_last_updated = None

            for measurement_data in measurement['measurements']:
                parameter = measurement_data['parameter']
                if parameter == 'pm10':
                    pm10_value = measurement_data['value']
                    pm10_last_updated = measurement_data['lastUpdated']
                elif parameter == 'pm25':
                    pm25_value = measurement_data['value']
                    pm25_last_updated = measurement_data['lastUpdated']

            # Sprawdzenie, czy wartości nie są None i czy nie ma już takich danych w bazie
            if (pm10_value is not None or pm25_value is not None or pm10_last_updated is not None or pm25_last_updated is not None) and not (
                    pm10_value == '' and pm25_value == ''):
                # Sprawdzenie, czy dane już istnieją w bazie
                query = "SELECT * FROM widok.pomiary_stare_api WHERE miasto = %s"
                cursor.execute(query, (location,))
                existing_data = cursor.fetchone()

                if existing_data is None:
                    # Wstawianie danych do tabeli
                    query = "INSERT INTO widok.pomiary_stare_api(miasto, pm10, pm25, data_pm10, data_pm25) VALUES (%s, %s, %s, %s, %s)"
                    values = (location, pm10_value, pm25_value, pm10_last_updated, pm25_last_updated)
                    cursor.execute(query, values)

    # Zatwierdzenie zmian i zamknięcie połączenia z bazą danych
    conn.commit()
    cursor.close()
    conn.close()

    print("Dane zostały pobrane i zapisane do bazy danych.")

except (requests.RequestException, psycopg2.Error) as error:
    print("Wystąpił błąd:", str(error))