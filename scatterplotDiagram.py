import matplotlib.pyplot as plt
from tkinter import messagebox
import requests
import mplcursors
from datetime import datetime
import statistics
import numpy as np
from scipy.stats import pearsonr

def generate_scatterplot(city, start_date, end_date, parameters):
    data_scatterplot = {
        'city': city,
        'start_date': start_date,
        'end_date': end_date,
        'parameters': parameters
    }

    title = f"Wykres punktowy zanieczyszczenia powietrza\n({start_date} - {end_date})"
    messagebox.showinfo("Wykres punktowy", f"Generowanie wykresu dla miasta: {city},\nData początkowa: {start_date},\nData końcowa: {end_date},\nParametry: {', '.join(parameters)}")

    # Pobieranie danych z API
    url = f"https://api.openaq.org/v2/measurements?date_from={start_date}&date_to={end_date}&limit=10000&page=1&offset=0&sort=desc&radius=10000&country_id=PL&city={city}&order_by=datetime"
    response = requests.get(url)
    data_scatterplot = response.json()

    pm10_data = []
    pm25_data = []
    pm10_dates = []
    pm25_dates = []

    if 'results' in data_scatterplot:
        measurements = data_scatterplot['results']
        for measurement in measurements:
            parameter = measurement['parameter']
            value = measurement['value']
            date = measurement['date']['utc']
            if parameter == 'pm10':
                pm10_data.append(value)
                pm10_dates.append(date)
            elif parameter == 'pm25':
                pm25_data.append(value)
                pm25_dates.append(date)

    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("Parametr")
    ax.set_ylabel("Wartość")

    if "pm10" in parameters:
        pm10_scatter = ax.scatter(["PM10"] * len(pm10_data), pm10_data, c='red', label="PM10")
        mplcursors.cursor([pm10_scatter]).connect("add", lambda sel: sel.annotation.set_text(f"Wartość: {sel.artist.get_offsets()[sel.target.index][1]}\nData: {format_date(pm10_dates[sel.target.index])}"))
    if "pm25" in parameters:
        pm25_scatter = ax.scatter(["PM2.5"] * len(pm25_data), pm25_data, c='blue', label="PM2.5")
        mplcursors.cursor([pm25_scatter]).connect("add", lambda sel: sel.annotation.set_text(f"Wartość: {sel.artist.get_offsets()[sel.target.index][1]}\nData: {format_date(pm25_dates[sel.target.index])}"))

    if len(pm10_data) > 0:
        pm10_mean = statistics.mean(pm10_data)
        pm10_scatter = ax.scatter(["PM10"], [pm10_mean], c='green', label="Średnia PM10")
        mplcursors.cursor(pm10_scatter).connect("add", lambda sel: sel.annotation.set_text(f"Średnia: {pm10_mean}"))
    if len(pm25_data) > 0:
        pm25_mean = statistics.mean(pm25_data)
        pm25_scatter = ax.scatter(["PM2.5"], [pm25_mean], c='purple', label="Średnia PM2.5")
        mplcursors.cursor(pm25_scatter).connect("add", lambda sel: sel.annotation.set_text(f"Średnia: {pm25_mean}"))

    # Obliczanie współczynnika korelacji Pearsona
    if len(pm10_data) > 0 and len(pm25_data) > 0:
        correlation_coefficient, _ = pearsonr(pm10_data, pm25_data)
        correlation_text = f"Współczynnik korelacji Pearsona: {correlation_coefficient:.2f}"
        ax.text(0.5, 0.02, correlation_text, transform=ax.transAxes, ha='center', fontsize=10)

    ax.legend()

    # Przekształcenie daty na postać normalną (rok, miesiąc, dzień, godzina)
    def format_date(date):
        parsed_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
        return parsed_date.strftime("%Y-%m-%d %H:%M:%S")

    fig.canvas.manager.window.attributes('-topmost', 1)
    fig.canvas.manager.window.after_idle(fig.canvas.manager.window.attributes, '-topmost', 0)
    plt.show(block=True)
