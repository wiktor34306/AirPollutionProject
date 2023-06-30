import matplotlib.pyplot as plt
from tkinter import messagebox
import requests

def generate_boxplot(city, start_date, end_date, parameters):
    data_boxplot = {
        'city': city,
        'start_date': start_date,
        'end_date': end_date,
        'parameters': parameters
    }

    title = f"Wykres pudełkowy zanieczyszczenia powietrza\n({start_date} - {end_date})"
    messagebox.showinfo("Wykres pudełkowy", f"Generowanie wykresu dla miasta: {city},\nData początkowa: {start_date},\nData końcowa: {end_date},\nParametry: {', '.join(parameters)}")

    # Pobieranie danych z API
    url = f"https://api.openaq.org/v2/measurements?date_from={start_date}&date_to={end_date}&limit=10000&page=1&offset=0&sort=desc&radius=10000&country_id=PL&city={city}&order_by=datetime"
    response = requests.get(url)
    data_boxplot = response.json()

    pm10_data = []
    pm25_data = []

    if 'results' in data_boxplot:
        measurements = data_boxplot['results']
        for measurement in measurements:
            parameter = measurement['parameter']
            value = measurement['value']
            if parameter == 'pm10':
                pm10_data.append(value)
            elif parameter == 'pm25':
                pm25_data.append(value)

    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("Parametr")
    ax.set_ylabel("Wartość")

    if "pm10" in parameters:
        ax.boxplot(pm10_data, positions=[1], widths=0.6, showfliers=False, labels=["PM10"])
    if "pm25" in parameters:
        ax.boxplot(pm25_data, positions=[2], widths=0.6, showfliers=False, labels=["PM2.5"])

    plt.show()