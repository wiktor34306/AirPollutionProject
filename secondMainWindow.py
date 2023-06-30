import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import requests
import datetime
import subprocess
import boxplotDiagram
import scatterplotDiagram
import histogramDiagram
import linearRegressionDiagram

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

        treeview.delete(*treeview.get_children())

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

    table_treeview = ttk.Treeview(frame, columns=("Parametr", "Wartość"), show="headings", 
                                  yscrollcommand=scrollbar.set)
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

def open_chart_1():
    city = entry.get()
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    parameters = []
    if pm10_var.get():
        parameters.append("pm10")
    if pm25_var.get():
        parameters.append("pm25")

    boxplotDiagram.generate_boxplot(city, start_date, end_date, parameters)

def open_chart_2():
    city = entry.get()
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    parameters = []
    if pm10_var.get():
        parameters.append("pm10")
    if pm25_var.get():
        parameters.append("pm25")

    scatterplotDiagram.generate_scatterplot(city, start_date, end_date, parameters)

def open_chart_3():
    city = entry.get()
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    parameters = []
    if pm10_var.get():
        parameters.append("pm10")
    if pm25_var.get():
        parameters.append("pm25")

    histogramDiagram.generate_histogram(city, start_date, end_date, parameters)

def open_chart_4():
    city = entry.get()
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    parameters = []
    if pm10_var.get():
        parameters.append("pm10")
    if pm25_var.get():
        parameters.append("pm25")

    linearRegressionDiagram.generate_linear_regression(city, start_date, end_date, parameters)

def go_back():
    window.destroy()
    subprocess.run(["python", "mainWindow.py"])

window = tk.Tk()
window.title("Aplikacja zanieczyszczenia powietrza")
window.configure(bg="#747474") 

back_button = ttk.Button(window, text="Powrót", command=go_back)
back_button.pack(pady=(30, 0))

label = ttk.Label(window, text="Wpisz nazwę miasta:", style="White.TLabel", background="#747474")
label.pack(pady=10)

entry = ttk.Entry(window)
entry.pack(pady=5)

date_frame = tk.Frame(window, bg="#747474")  
date_frame.pack(pady=10)

start_date_frame = tk.Frame(date_frame, bg="#747474")  
start_date_frame.pack(side=tk.LEFT, padx=10)

start_date_label = ttk.Label(start_date_frame, text="Data początkowa", style="White.TLabel", background="#747474")
start_date_label.pack(pady=5)

start_date_entry = Calendar(start_date_frame, date_pattern='yyyy-mm-dd', background="#747474")  
start_date_entry.pack(pady=5)

end_date_frame = tk.Frame(date_frame, bg="#747474")  
end_date_frame.pack(side=tk.LEFT, padx=10)

end_date_label = ttk.Label(end_date_frame, text="Data końcowa", style="White.TLabel", background="#747474")
end_date_label.pack(pady=5)

end_date_entry = Calendar(end_date_frame, date_pattern='yyyy-mm-dd', background="#747474") 
end_date_entry.pack(pady=5)

pm10_var = tk.IntVar()
pm25_var = tk.IntVar()

style = ttk.Style()
style.configure("Grey.TCheckbutton", background="#747474")
style.configure("White.TCheckbutton", background="#747474", foreground="white")
style.configure("White.TLabel", foreground="white")
style.configure("White.TCheckbutton", foreground="white")

pm10_checkbox = ttk.Checkbutton(window, text="PM10", variable=pm10_var, style="White.TCheckbutton")
pm10_checkbox.pack(pady=5)

pm25_checkbox = ttk.Checkbutton(window, text="PM2.5", variable=pm25_var, style="White.TCheckbutton")
pm25_checkbox.pack(pady=5)

submit_button = ttk.Button(window, text="Sprawdź", command=get_air_quality_data)
submit_button.pack(pady=10)

output_label = ttk.Label(window, text="", style="White.TLabel", background="#747474")
output_label.pack(pady=10)

frame = ttk.Frame(window)
frame.pack(pady=10)

table_button = ttk.Button(window, text="Tabela z podziałem wartości", command=open_table_window)
table_button.pack(pady=10)

charts_frame = ttk.Frame(window,  style="Grey.TCheckbutton")
charts_frame.pack(pady=10)

chart1_button = ttk.Button(charts_frame, text="Wykres pudełkowy", command=open_chart_1, width=31)
chart1_button.pack(side=tk.LEFT, padx=5)

chart2_button = ttk.Button(charts_frame, text="Wykres punktowy", command=open_chart_2, width=31)
chart2_button.pack(side=tk.LEFT, padx=5)

chart3_button = ttk.Button(charts_frame, text="Histogram", command=open_chart_3, width=31)
chart3_button.pack(side=tk.LEFT, padx=5)

chart4_button = ttk.Button(charts_frame, text="Regresja liniowa", command=open_chart_4, width=31)
chart4_button.pack(side=tk.LEFT, padx=5)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

treeview = ttk.Treeview(frame, columns=("Data", "Lokalizacja", "Parametr", "Wartość"), 
                        show="headings", yscrollcommand=scrollbar.set)
treeview.heading("Data", text="Data")
treeview.heading("Lokalizacja", text="Lokalizacja")
treeview.heading("Parametr", text="Parametr")
treeview.heading("Wartość", text="Wartość")
treeview.pack()

scrollbar.config(command=treeview.yview)

window.mainloop()
