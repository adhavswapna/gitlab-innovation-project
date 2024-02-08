import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from ship_weather_script import get_weather
from PIL import Image, ImageTk
import requests

class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Ship Weather App")
        self.create_interface()

    def create_interface(self):
        self.create_menu()
        self.create_main_frame()

    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.master.destroy)

        options_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Change Background", command=self.change_background_color)
        options_menu.add_command(label="Temperature Unit", command=self.convert_temperature_unit_dialog)

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack()

        self.create_entry("Enter ship's latitude:", 0)
        self.create_entry("Enter ship's longitude:", 1)
        self.create_entry("Enter city name:", 2)

        ttk.Button(self.main_frame, text="Fetch Weather", command=self.fetch_weather).grid(column=0, row=3, columnspan=2, pady=10)

        self.weather_icon_label = ttk.Label(self.main_frame)
        self.weather_icon_label.grid(column=0, row=4, columnspan=2)

    def create_entry(self, label_text, row):
        ttk.Label(self.main_frame, text=label_text).grid(column=0, row=row, padx=5, pady=5, sticky="W")
        ttk.Entry(self.main_frame).grid(column=1, row=row, padx=5, pady=5, sticky="W")

    def fetch_weather(self):
        try:
            latitude, longitude = map(float, [self.get_entry_value(0), self.get_entry_value(1)])
            city_name = self.get_entry_value(2)
            weather_data = get_weather("e886d0c1e85cb295f25c28e68e2ca573", latitude, longitude, city_name)

            if weather_data:
                self.display_weather_details(weather_data)
                self.display_weather_icon(weather_data)
            else:
                messagebox.showerror("Error", "Unable to retrieve weather data.")
        except ValueError:
            messagebox.showerror("Error", "Invalid latitude, longitude, or city name. Please enter valid values.")

    def display_weather_details(self, weather_data):
        details_window = self.create_toplevel("Weather Details", "white")

        details_frame = ttk.Frame(details_window, padding="10", style='Background.TFrame')
        details_frame.pack()

        temperature = self.convert_temperature_unit(weather_data['main']['temp'])
        labels_data = [
            (f"Temperature: {temperature}°C", 0),
            (f"Condition: {weather_data['weather'][0]['description']}", 1),
            (f"Wind Speed: {weather_data['wind']['speed']} m/s", 2),
            (f"Wind Direction: {weather_data['wind']['deg']}°", 3),
        ]

        for label_text, row in labels_data:
            ttk.Label(details_frame, text=label_text).grid(column=0, row=row, padx=5, pady=5, sticky="W")

    def create_toplevel(self, title, bg_color):
        window = tk.Toplevel(self.master)
        window.title(title)
        window.configure(bg=bg_color)
        return window

    def change_background_color(self):
        color = colorchooser.askcolor(title="Select Background Color")[1]
        if color:
            for widget in [self.master, self.create_toplevel("Weather Details", color)]:
                widget.configure(bg=color)
            ttk.Style().configure('Background.TFrame', background=color)

    def get_entry_value(self, row):
        return self.main_frame.grid_slaves(row=row, column=1)[0].get()

    def display_weather_icon(self, weather_data):
        icon_url = f"http://openweathermap.org/img/w/{weather_data['weather'][0]['icon']}.png"
        image = Image.open(requests.get(icon_url, stream=True).raw)
        image = ImageTk.PhotoImage(image)

        self.weather_icon_label.configure(image=image)
        self.weather_icon_label.image = image

    def convert_temperature_unit(self, temperature):
        # Add logic to convert temperature to Fahrenheit if needed
        return temperature

    def convert_temperature_unit_dialog(self):
        # Implement a dialog to let the user choose the temperature unit (Celsius/Fahrenheit)
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
