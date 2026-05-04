# CS-3080-Semester-Project-Weather-App
This repository holds the code for a simple weather app for the CS 3080 Semester Project

===================== API KEY INFORMATION ==================== 

The application uses the OpenWeather API and requires a valid API key from OpenWeather to function.
To fullfil this requirement, visit https://openweathermap.org/api to sign up for a free account and
acquire a valid API key.

To add the API key, go to the .env file in main and add it to the "API_KEY=" field to add the key.
The program will return an "Invalid API key" error issued by OpenWeather upon request for the 
data.

================= ENVIRONMENT INFORMATION ===================

The .yml file included in the main branch holds all the required libraries and environment data to 
run the program, to install the environment access the anaconda prompt, navigate to the directory
where the environemt file is installed and enter the followingcommand:

conda env create -f WeatherAppEnv.yml

Once the environment is installed and activated, the program can be run from the conda command line

==================== APPLICATION FUNCTION ===================

This application has one main function: Access weather info through OpenWeatherMap API and display 
current conditions, current tempurature, and high/low temps. User can choose between imperial and
metric units for temperature data.
