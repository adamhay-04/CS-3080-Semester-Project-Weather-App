import requests
import os
import json
import tkinter as tk
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

class WeatherApp:

    def __init__(self):
        self.mainwindow = tk.Tk()                                              # create application window
        self.mainwindow.title("CS 3080 Open Weather API - City Weather App")   # application window title
        self.mainwindow.geometry("856x482")                                    # dimensions of the window (in pixels)

        load_dotenv()                          # load env file data
        self.api_key = os.getenv("API_KEY")    # retrieve API key

        self.create_elements()                 # create all ui elements and widgets

    # get_weather sends request to OpenWeather and returns response data in json format
    
    @staticmethod
    def get_weather(city, api_key, units):
        response = requests.get("https://api.openweathermap.org/data/2.5/weather",params={"q": city, "appid": api_key, "units": units})
        return response.json()

    # submit_and_process takes user input and provides requested data based on those inputs

    def submit_and_process(self):
        input_units = self.temp_unit.get()    # set input units to user selection
        input_city = self.input_field.get()   # set city to user input city

        self.input_field.delete(0, tk.END)    # clear input box upon hitting enter and after saving input data

        # determine unit type based on user input
        
        if input_units == "imperial":
            display_unit = "F"
        elif input_units == "metric":
            display_unit = "C"

        # retrieve data for current date and time

        date_and_time = datetime.now()
        current_time = date_and_time.strftime("%I:%M %p")
        current_date = date_and_time.strftime("%m-%d-%y")

        data = self.get_weather(input_city, self.api_key, input_units)    # naje request to OpenWeather with user input and store in data as json

        if data.get("cod") != 200:
            self.result_label.config(text=f"Error: {data.get('message')}")    # check for errors with getting the data from OpenWeather (ex: "Invalid API Key")

        with open('weather_data.json', 'w') as f:    # save all retrieved data to json file for further analysis and review
            json.dump(data, f, indent=4)             # this will overwrite previous data every execution 

        # store relevant data for program into variables
        
        city = data["name"]
        conditions = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        temp_max = data["main"]["temp_max"]
        temp_min = data["main"]["temp_min"]

        # display data in result label
        
        self.result_label.config(
            text=f"City: {city}\nDate: {current_date}\nTime of Query: {current_time}\n\nCurrent Weather Conditions: {conditions}\nCurrent Temperature ({display_unit}): {temp}"
                 f"\nLow ({display_unit}): {temp_min}\nHigh ({display_unit}): {temp_max}"
        )


    def create_elements(self):


        # create frame to manage placement and movement of widgets
        userframe = tk.Frame(self.mainwindow) 
        userframe.pack(expand=True)  
        
        title_label = tk.Label(userframe, text="OpenWeather API City Weather App")    # application title label over text box
        title_label.pack()

        input_label = tk.Label(userframe, text="Enter a City to display current weather:")    # prompt label
        input_label.pack()    

        self.input_field = tk.Entry(userframe)     # create and place input box
        self.input_field.pack(pady=5)

        submit = tk.Button(userframe, text="Enter", command=self.submit_and_process)    # create button that processes input when clicked
        submit.pack(pady=5)

        self.temp_unit = tk.StringVar(value="imperial")              # create varaible for unit selection buttons, set default value to imperial
        temp_set_label = tk.Label(userframe, text="Select Units")
        temp_set_label.pack()

        tk.Radiobutton(userframe, text="Imperial (F)", variable=self.temp_unit, value="imperial").pack()    # simple buttons to toggle units choice
        tk.Radiobutton(userframe, text="Metric (C)", variable=self.temp_unit, value="metric").pack()

        self.result_label = tk.Label(userframe, text="", justify="left")    # create blank label with a left-sided alignment for result data
        self.result_label.pack(pady=15)

        tk.Button(userframe, text="Exit", command=self.quit_program).pack(pady=30)    # button to exit and terminate program

    # function to start mainwindow loop
    def run_program(self):
        self.mainwindow.mainloop()

    # function to quit program when called
    @staticmethod
    def quit_program():
        exit(0)

if __name__ == '__main__':
    app = WeatherApp()    # create weather application object
    app.run_program()     # run application
