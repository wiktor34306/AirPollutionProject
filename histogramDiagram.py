import matplotlib.pyplot as plt
from tkinter import messagebox
import requests

def generate_histogram(city, start_date, end_date, parameters):
    data_histogram = {
        'city': city,
        'start_date': start_date,
        'end_date': end_date,
        'parameters': parameters
    }

    title = f"Wykres histogramu zanieczyszczenia powietrza\n({start_date} - {end_date})"
    messagebox.showinfo("Wykres histogramu", f"Generowanie wykresu dla miasta: {city},\nData początkowa: {start_date},\nData końcowa: {end_date},\nParametry: {', '.join(parameters)}")

    # Pobieranie danych z API
    url = f"https://api.openaq.org/v2/measurements?date_from={start_date}&date_to={end_date}&limit=10000&page=1&offset=0&sort=desc&radius=10000&country_id=PL&city={city}&order_by=datetime"
    response = requests.get(url)
    data_histogram = response.json()

    pm10_data = []
    pm25_data = []

    if 'results' in data_histogram:
        measurements = data_histogram['results']
        for measurement in measurements:
            parameter = measurement['parameter']
            value = measurement['value']
            if parameter == 'pm10':
                pm10_data.append(value)
            elif parameter == 'pm25':
                pm25_data.append(value)

    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("Wartość")
    ax.set_ylabel("Liczebność")

    if "pm10" in parameters:
        ax.hist(pm10_data, bins=20, color='red', alpha=0.7, label="PM10")
    if "pm25" in parameters:
        ax.hist(pm25_data, bins=20, color='blue', alpha=0.7, label="PM2.5")

    ax.legend()

    plt.show()
