import tkinter as tk
from tkinter import ttk, scrolledtext
import requests

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
    url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if 'data' in data:
        air_quality = data['data']['aqi']
        parameters = data['data']['iaqi']
        city_name = data["data"]["city"]["name"]

        quality_text = get_quality_text(air_quality)

        output_label.config(text=f"Aktualne zanieczyszczenie dla {city_name}: {air_quality} ({quality_text})")

        # Usunięcie poprzednich danych z tabelki
        treeview.delete(*treeview.get_children())

        # Dodanie danych do tabelki
        for param, value in parameters.items():
            treeview.insert("", "end", values=(param, value['v']))
    else:
        output_label.config(text="Brak danych dla podanego miasta")

def open_table_window():
    table_window = tk.Toplevel(window)
    table_window.title("Tabela z danymi")
    table_window.geometry("400x300")

    frame = tk.Frame(table_window)
    frame.pack(pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    table_treeview = ttk.Treeview(frame, columns=("Parametr", "Wartość"), show="headings", yscrollcommand=scrollbar.set)
    table_treeview.heading("Parametr", text="Parametr")
    table_treeview.heading("Wartość", text="Wartość")
    table_treeview.pack()

    scrollbar.config(command=table_treeview.yview)

    table_treeview.insert("", "end", values=("Dobra", "0-50: Dobra - Jakość powietrza jest uznawana za zadowalającą, a zanieczyszczenie powietrza stanowi niewielkie ryzyko lub jego brak."))
    table_treeview.insert("", "end", values=("Średnia", "50-100: Średnia - Jakość powietrza jest dopuszczalna; jednak niektóre zanieczyszczenia mogą być umiarkowanie szkodliwe dla bardzo małej liczby osób, które są niezwykle wrażliwe na zanieczyszczenie powietrza."))
    table_treeview.insert("", "end", values=("Niezdrowa dla osób wrażliwych", "100-150: Niezdrowe dla wrażliwych osób - u osób wrażliwych mogą wystąpić negatywne skutki dla zdrowia. Większość populacji może nie odczuwać negatywnych objawów."))
    table_treeview.insert("", "end", values=("Niezdrowa", "150-200: Niezdrowe - Każdy może zacząć doświadczać negatywnych skutków zdrowotnych; U osób wrażliwych mogą wystąpić poważniejsze skutki zdrowotne."))
    table_treeview.insert("", "end", values=("Bardzo niezdrowa", "200-300: Bardzo niezdrowe - Ostrzeżenie zdrowotne, poziom alarmowy. Bardzo prawdopodobny negatywny wpływ na całą populację."))
    table_treeview.insert("", "end", values=("Zagrożenie dla życia", "300+: Niebezpieczny - Alarm Zdrowotny: każdy może doświadczyć poważniejszych skutków zdrowotnych."))

    # Tworzenie widżetu ScrolledText
    scrolled_text = scrolledtext.ScrolledText(table_window)
    scrolled_text.pack(pady=10, fill=tk.BOTH, expand=True)

    # Przypisanie zawartości tabeli do widżetu ScrolledText
    table_text = "\n".join([f"{item['values'][0]}: {item['values'][1]}" for item in table_treeview.get_children()])
    scrolled_text.insert(tk.END, table_text)

# Tworzenie okna głównego
window = tk.Tk()
window.title("Aplikacja zanieczyszczenia powietrza")
window.geometry("600x400")

label = tk.Label(window, text="Wpisz nazwę miasta:")
label.pack(pady=10)

entry = tk.Entry(window)
entry.pack(pady=5)

button = tk.Button(window, text="Sprawdź", command=get_air_quality_data)
button.pack(pady=5)

output_label = tk.Label(window, text="")
output_label.pack(pady=10)

frame = tk.Frame(window)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

treeview = ttk.Treeview(frame, columns=("Parametr", "Wartość"), show="headings", yscrollcommand=scrollbar.set)
treeview.heading("Parametr", text="Parametr")
treeview.heading("Wartość", text="Wartość")
treeview.pack()

scrollbar.config(command=treeview.yview)

open_table_button = tk.Button(window, text="Otwórz tabelę", command=open_table_window)
open_table_button.pack(pady=5)

window.mainloop()