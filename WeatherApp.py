import requests
import os
import json
import tkinter as tk
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

class WeatherApp:

    def __init__(self):
        self.mainwindow = tk.Tk()
        self.mainwindow.title("CS 3080 Open Weather API - City Weather App")  # give the application a title label
        self.mainwindow.geometry("856x482")

        load_dotenv()
        self.api_key = os.getenv("API_KEY")

        self.create_elements()

    @staticmethod
    def get_weather(city, api_key, units):
        response = requests.get("https://api.openweathermap.org/data/2.5/weather",params={"q": city, "appid": api_key, "units": units})
        return response.json()

    def submit_and_process(self):
        input_units = self.temp_unit.get()
        input_city = self.input_field.get()

        self.input_field.delete(0, tk.END)

        if input_units == "imperial":
            display_unit = "F"
        elif input_units == "metric":
            display_unit = "C"

        date_and_time = datetime.now()
        current_time = date_and_time.strftime("%I:%M %p")
        current_date = date_and_time.strftime("%m-%d-%y")

        data = self.get_weather(input_city, self.api_key, input_units)

        if data.get("cod") != 200:
            self.result_label.config(text=f"Error: {data.get('message')}")

        with open('weather_data.json', 'w') as f:
            json.dump(data, f, indent=4)

        city = data["name"]
        conditions = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        temp_max = data["main"]["temp_max"]
        temp_min = data["main"]["temp_min"]

        self.result_label.config(
            text=f"City: {city}\nDate: {current_date}\nTime of Query: {current_time}\n\nCurrent Weather Conditions: {conditions}\nCurrent Temperature ({display_unit}): {temp}"
                 f"\nLow ({display_unit}): {temp_min}\nHigh ({display_unit}): {temp_max}")


    def create_elements(self):

        userframe = tk.Frame(self.mainwindow)  # frame allows for the usage of the expand feature, which will allow all on screen
        userframe.pack(expand=True)  # widgets to move and adjust to changes in window size while remaining grouped together

        title_label = tk.Label(userframe, text="OpenWeather API City Weather App")
        title_label.pack()

        input_label = tk.Label(userframe, text="Enter a City to display current weather:")
        input_label.pack()

        self.input_field = tk.Entry(userframe)  # add input box to frame
        self.input_field.pack(pady=5)

        submit = tk.Button(userframe, text="Enter", command=self.submit_and_process)  # add button to frame
        submit.pack(pady=5)

        self.temp_unit = tk.StringVar(value="imperial")  # default value is imperial
        temp_set_label = tk.Label(userframe, text="Select Units")
        temp_set_label.pack()

        # radio buttons to act settings for unit preference
        tk.Radiobutton(userframe, text="Imperial (F)", variable=self.temp_unit, value="imperial").pack()
        tk.Radiobutton(userframe, text="Metric (C)", variable=self.temp_unit, value="metric").pack()

        # create and print results to mainwindow frame
        self.result_label = tk.Label(userframe, text="", justify="left")
        self.result_label.pack(pady=15)

        tk.Button(userframe, text="Exit", command=self.quit_program).pack(pady=30)

    def run_program(self):
        self.mainwindow.mainloop()

    @staticmethod
    def quit_program():
        exit(0)

if __name__ == '__main__':
    app = WeatherApp()
    app.run_program()