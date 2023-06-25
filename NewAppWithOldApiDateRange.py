import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import requests
import datetime

API_KEY = "05b1a42bda64f294587fd9a738864c30017b0173"

QUALITY_LEVELS = {
    (0, 50): "Dobra",
    (51, 100): "Średnia",
    (101, 150): "Niezdrowa dla osób wrażliwych",
    (151, 200): "Niezdrowa",
    (201, 300): "Bardzo niezdrowa",
    (300, float("inf")): "Zagrożenie dla życia"
}

def get_quality_text(air_quality):
    for level, text in QUALITY_LEVELS.items():
        if level[0] <= air_quality <= level[1]:
            return text
    return "Brak danych"

def get_air_quality_data():
    city = entry.get()
    start_date_str = start_date_entry.get_date()
    end_date_str = end_date_entry.get_date()
    parameters = []
    if pm10_var.get():
        parameters.append("pm10")
    if pm25_var.get():
        parameters.append("pm25")

    if not city or not start_date_str or not end_date_str or not parameters:
        messagebox.showerror("Błąd", "Wprowadź wszystkie wymagane dane.")
        return

    url = f"https://api.openaq.org/v2/measurements?date_from={start_date_str}&date_to={end_date_str}&limit=10000&page=1&offset=0&sort=desc&radius=10000&country_id=PL&city={city}&order_by=datetime"

    response = requests.get(url)
    data = response.json()

    if 'results' in data:
        measurements = data['results']
        output_label.config(text=f"Aktualne zanieczyszczenie dla {city}: {len(measurements)} wyników")

        # Usunięcie poprzednich danych z tabelki
        treeview.delete(*treeview.get_children())

        # Dodanie danych do tabelki
        for measurement in measurements:
            parameter = measurement['parameter']
            value = measurement['value']
            date = measurement['date']['local']
            date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            location = measurement['location']

            if parameter in parameters:
                treeview.insert("", "end", values=(date, location, parameter, value))
    else:
        output_label.config(text="Brak danych dla podanego miasta")

def open_table_window():
    table_window = tk.Toplevel(window)
    table_window.title("Tabela z danymi")
    table_window.geometry("600x300")

    frame = tk.Frame(table_window)
    frame.pack(pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    table_treeview = ttk.Treeview(frame, columns=("Parametr", "Wartość"), show="headings", yscrollcommand=scrollbar.set)
    table_treeview.heading("Parametr", text="Parametr")
    table_treeview.heading("Wartość", text="Wartość")
    table_treeview.pack()

    scrollbar.config(command=table_treeview.yview)

    table_treeview.insert("", "end", values=("Dobra", "0-50", ""))
    table_treeview.insert("", "end", values=("Średnia", "50-100", ""))
    table_treeview.insert("", "end", values=("Niezdrowa dla osób wrażliwych", "100-150", ""))
    table_treeview.insert("", "end", values=("Niezdrowa", "150-200", ""))
    table_treeview.insert("", "end", values=("Bardzo niezdrowa", "200-300", ""))
    table_treeview.insert("", "end", values=("Zagrożenie dla życia", "300+", ""))


# Tworzenie okna głównego
window = tk.Tk()
window.title("Aplikacja zanieczyszczenia powietrza")
window.geometry("1000x800")

label = tk.Label(window, text="Wpisz nazwę miasta:")
label.pack(pady=10)

entry = tk.Entry(window)
entry.pack(pady=5)

start_date_label = tk.Label(window, text="Data początkowa:")
start_date_label.pack(pady=5)

start_date_entry = Calendar(window, date_pattern='yyyy-mm-dd')
start_date_entry.pack(pady=5)

end_date_label = tk.Label(window, text="Data końcowa:")
end_date_label.pack(pady=5)

end_date_entry = Calendar(window, date_pattern='yyyy-mm-dd')
end_date_entry.pack(pady=5)

pm10_var = tk.IntVar()
pm25_var = tk.IntVar()

pm10_checkbox = tk.Checkbutton(window, text="PM10", variable=pm10_var)
pm10_checkbox.pack(pady=5)

pm25_checkbox = tk.Checkbutton(window, text="PM2.5", variable=pm25_var)
pm25_checkbox.pack(pady=5)

submit_button = tk.Button(window, text="Sprawdź", command=get_air_quality_data)
submit_button.pack(pady=10)

output_label = tk.Label(window, text="")
output_label.pack(pady=10)

frame = tk.Frame(window)
frame.pack(pady=10)

table_button = tk.Button(window, text="Tabela z podziałem wartości", command=open_table_window)
table_button.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

treeview = ttk.Treeview(frame, columns=("Data", "Miejsce", "Parametr", "Wartość"), show="headings", yscrollcommand=scrollbar.set)
treeview.heading("Data", text="Data")
treeview.heading("Miejsce", text="Miejsce")
treeview.heading("Parametr", text="Parametr")
treeview.heading("Wartość", text="Wartość")
treeview.pack()

scrollbar.config(command=treeview.yview)

window.mainloop()