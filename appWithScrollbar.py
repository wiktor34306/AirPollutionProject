import requests
import tkinter as tk
from datetime import datetime
from tkinter import ttk


class AirQualityApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Jakość powietrza w Polsce")
        self.result_tables = []

        # create a search label and entry box
        self.search_label = tk.Label(self.master, text="Podaj nazwę miejscowości:")
        self.search_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.search_entry = tk.Entry(self.master, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        # create a search button
        self.search_button = tk.Button(self.master, text="Szukaj", command=self.search)
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # create a result label to display location information
        self.result_label = tk.Label(self.master, text="")
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
        self.result_frame = tk.Frame(self.master)
        self.result_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)

        # create a scrollbar for the result frame
        self.scrollbar = tk.Scrollbar(self.result_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # create a canvas to hold the result frame and scrollbar
        canvas = tk.Canvas(self.result_frame, yscrollcommand=self.scrollbar.set)
        canvas.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))


        # configure scrollbar to work with the canvas
        self.scrollbar.config(command=canvas.yview)

        # create a frame to hold the result tables
        table_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=table_frame, anchor=tk.NE)

        # display location and measurement information for each location
        for location in data["results"]:
            # create a table to display measurement information
            tree = ttk.Treeview(table_frame, columns=("parameter", "value", "last_updated"), show="headings")
            tree.pack(side=tk.TOP, padx=5, pady=5)

            # extract and display location information
            result_location = location["location"]
            location_label = tk.Label(table_frame, text=f"Lokalizacja: {result_location}")
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


            
# create the GUI
root = tk.Tk()
app = AirQualityApp(root)
root.mainloop()