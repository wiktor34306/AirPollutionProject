import requests
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from ttkthemes import ThemedTk


class AirQualityApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Jakość powietrza w Polsce")
        self.result_tables = []

        # create a switch app button
        self.switch_app_button = ttk.Button(self.master, text="Dane indeksu powietrza w przedziale czasowym", command=self.switch_app, style="Switch.TButton")
        self.switch_app_button.pack(padx=5, pady=5)

        # create a search label and entry box
        self.search_label = ttk.Label(self.master, text="Podaj nazwę miejscowości:", style="TGray.TLabel")
        self.search_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_entry = ttk.Entry(self.master, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # create a search button
        self.search_button = ttk.Button(self.master, text="Szukaj", command=self.search, style="Search.TButton")
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

        # create a result label to display location information
        self.result_label = ttk.Label(self.master, text="", style="TGray.TLabel")
        self.result_label.pack(side=tk.TOP, padx=5, pady=5)

    def search(self):
        # clear existing tables and labels
        for table in self.result_tables:
            table.destroy()
        self.result_tables.clear()

        # destroy result frame and scrollbar
        if hasattr(self, "result_frame"):
            self.result_frame.destroy()
        if hasattr(self, "scrollbar"):
            self.scrollbar.destroy()

        # get city name from search entry
        nameCity = self.search_entry.get().title()

        # make API request
        url = f"https://api.openaq.org/v2/latest?city={nameCity}&country=PL"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        data = response.json()

        # create a frame to hold all result tables and scrollbar
        self.result_frame = ttk.Frame(self.master)
        self.result_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)

        # create a scrollbar for the result frame
        self.scrollbar = ttk.Scrollbar(self.result_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # create a canvas to hold the result frame and scrollbar
        canvas = tk.Canvas(self.result_frame, yscrollcommand=self.scrollbar.set)
        canvas.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # configure scrollbar to work with the canvas
        self.scrollbar.config(command=canvas.yview)

        # create a frame to hold the result tables
        table_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=table_frame, anchor=tk.NE)

        # display location and measurement information for each location
        for location in data["results"]:
            # create a table to display measurement information
            tree = ttk.Treeview(table_frame, columns=("parameter", "value", "last_updated"), show="headings")
            tree.pack(side=tk.TOP, padx=5, pady=5)

            # extract and display location information
            result_location = location["location"]
            location_label = ttk.Label(table_frame, text=f"Lokalizacja: {result_location}")
            location_label.pack(side=tk.TOP, padx=5, pady=5)

            # add headings to the table
            tree.heading("parameter", text="Parametr")
            tree.heading("value", text="Wartość")
            tree.heading("last_updated", text="Ostatnia aktualizacja")

            # extract and display measurement information
            for measurement in location["measurements"]:
                parameter = measurement["parameter"]
                value = measurement["value"]
                last_updated = measurement["lastUpdated"]
                last_updated = datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S")

                # insert a row into the table
                tree.insert("", "end", values=(parameter, value, last_updated))

            # add the table to the result table frame
            tree.pack(in_=table_frame, side=tk.TOP)

            # add the table to the list of result tables
            self.result_tables.append(tree)

        # update the canvas after adding all the tables
        table_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def switch_app(self):
        self.master.destroy()  # Zamknięcie okna aplikacji appWIthScrollbar.py
        import secondMainWindow  # Importowanie aplikacji newAppWithOldApi.py


# create the GUI
root = ThemedTk(theme="")
root.configure(background="#747474")

# define styles
style = ttk.Style()
style.configure("TButton", background="white")
style.configure("Switch.TButton", background="white")
style.configure("Search.TButton", background="white")
style.configure("TGray.TLabel", background="#747474", foreground="white")

app = AirQualityApp(root)
root.geometry("1200x500")
root.mainloop()
