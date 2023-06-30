import matplotlib.pyplot as plt
from tkinter import messagebox
import requests
import numpy as np
from sklearn.linear_model import LinearRegression
import mplcursors
from datetime import datetime

def generate_linear_regression(city, start_date, end_date, parameters):
    data_regression = {
        'city': city,
        'start_date': start_date,
        'end_date': end_date,
        'parameters': parameters
    }

    messagebox.showinfo("Regresja liniowa", f"Generowanie wykresu dla miasta: {city},\nData początkowa: {start_date},\nData końcowa: {end_date},\nParametry: {', '.join(parameters)}")

    # Pobieranie danych z API
    url = f"https://api.openaq.org/v2/measurements?date_from={start_date}&date_to={end_date}&limit=10000&page=1&offset=0&sort=desc&radius=10000&country_id=PL&city={city}&order_by=datetime"
    response = requests.get(url)
    data_regression = response.json()

    if 'results' in data_regression:
        measurements = data_regression['results']
        pm10_data = []
        pm25_data = []

        for measurement in measurements:
            parameter = measurement['parameter']
            value = measurement['value']
            if parameter == 'pm10':
                pm10_data.append(value)
            elif parameter == 'pm25':
                pm25_data.append(value)

        if "pm10" in parameters and pm10_data:
            x_pm10 = np.array([[i] for i in range(len(pm10_data))])
            y_pm10 = np.array(pm10_data)

            model_pm10 = LinearRegression()
            model_pm10.fit(x_pm10, y_pm10)
            y_pred_pm10 = model_pm10.predict(x_pm10)

            # Obliczanie odchylenia standardowego, współczynnika nachylenia, współczynnika przesunięcia i mediany
            std_dev_pm10 = np.std(pm10_data)
            slope_pm10 = model_pm10.coef_[0]
            intercept_pm10 = model_pm10.intercept_
            median_pm10 = np.median(pm10_data)

            fig_pm10, ax_pm10 = plt.subplots()
            ax_pm10.scatter(x_pm10, y_pm10, color='blue', label="Dane")
            ax_pm10.plot(x_pm10, y_pred_pm10, color='red', label="Regresja liniowa")
            ax_pm10.set_title("Regresja liniowa dla PM10")
            ax_pm10.set_xlabel("Indeks")
            ax_pm10.set_ylabel("Wartość")
            ax_pm10.legend()

            # Przekształcenie indeksu na datę i godzinę
            def format_date(index):
                date = measurements[index]['date']['utc']
                parsed_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
                return parsed_date.strftime("%Y-%m-%d %H:%M:%S")

            mplcursors.cursor(ax_pm10).connect(
                "add", lambda sel: sel.annotation.set_text(
                    f"Wartość: {sel.artist.get_offsets()[sel.target.index][1]}\nData: {format_date(sel.target.index)}"
                )
            )

            # Dodawanie informacji o odchyleniu standardowym, współczynniku nachylenia, współczynniku przesunięcia i medianie
            info_text = f"Odchylenie standardowe: {std_dev_pm10:.2f}\nWspółczynnik nachylenia: {slope_pm10:.2f}\nWspółczynnik przesunięcia: {intercept_pm10:.2f}\nMediana: {median_pm10:.2f}"
            ax_pm10.text(0.95, 0.95, info_text, transform=ax_pm10.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right')

            plt.show()
            plt.close(fig_pm10)

        if "pm25" in parameters and pm25_data:
            x_pm25 = np.array([[i] for i in range(len(pm25_data))])
            y_pm25 = np.array(pm25_data)

            model_pm25 = LinearRegression()
            model_pm25.fit(x_pm25, y_pm25)
            y_pred_pm25 = model_pm25.predict(x_pm25)

            # Obliczanie odchylenia standardowego, współczynnika nachylenia, współczynnika przesunięcia i mediany
            std_dev_pm25 = np.std(pm25_data)
            slope_pm25 = model_pm25.coef_[0]
            intercept_pm25 = model_pm25.intercept_
            median_pm25 = np.median(pm25_data)

            fig_pm25, ax_pm25 = plt.subplots()
            ax_pm25.scatter(x_pm25, y_pm25, color='blue', label="Dane")
            ax_pm25.plot(x_pm25, y_pred_pm25, color='red', label="Regresja liniowa")
            ax_pm25.set_title("Regresja liniowa dla PM2.5")
            ax_pm25.set_xlabel("Indeks")
            ax_pm25.set_ylabel("Wartość")
            ax_pm25.legend()

            mplcursors.cursor(ax_pm25).connect(
                "add", lambda sel: sel.annotation.set_text(
                    f"Wartość: {sel.artist.get_offsets()[sel.target.index][1]}\nData: {format_date(sel.target.index)}"
                )
            )

            # Dodawanie informacji o odchyleniu standardowym, współczynniku nachylenia, współczynniku przesunięcia i medianie
            info_text = f"Odchylenie standardowe: {std_dev_pm25:.2f}\nWspółczynnik nachylenia: {slope_pm25:.2f}\nWspółczynnik przesunięcia: {intercept_pm25:.2f}\nMediana: {median_pm25:.2f}"
            ax_pm25.text(0.95, 0.95, info_text, transform=ax_pm25.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right')

            plt.show()
            plt.close(fig_pm25)
