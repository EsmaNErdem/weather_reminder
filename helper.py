import schedule
import smtplib   
import requests
from bs4 import BeautifulSoup
import re
import geocoder
from decouple import config

# Load environment variables from .env
PASSWORD = config('MAIL_PASSWORD')

location_town = "Roswell, NM"
location = geocoder.osm(location_town)

if location:
    print("Latitude:", location.latlng[0])
    print("Longitude:", location.latlng[1])
else:
    print("Location not found")

url = f"https://forecast.weather.gov/MapClick.php?lat={location.latlng[0]}&lon={location.latlng[1]}"
html = requests.get(url).content
weather_data = BeautifulSoup(html, 'html.parser')

weather = weather_data.find(
  'p', attrs={'class': 'myforecast-current'}).text
temperature= weather_data.find(
  'p', attrs={'class': 'myforecast-current-lrg'}).text
nightly = weather_data.find(
  'div', attrs={'class': 'forecast-text'}).text
print(weather, temperature, nightly)

if "Thunderstorm" in weather or "Heavy Rain" in weather or "Windy" in weather or "Windy" in weather or "Rainy" in weather or "Showers" in weather or "Haze" in weather:
    print("Weather is Thunderstorm Heavy Rain and Windy")
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    smtp_object.starttls()

    # Authentication
    smtp_object.login("umbrellaremindererdem@gmail.com", PASSWORD)

    # Email subject and body
    subject = "Umbrella Reminder"
    body = f"Take an umbrella before leaving the house. Weather condition for today is {weather} and temperature is {temperature} in {location_town}. Tonight's weather looks like: {nightly}"

    # Construct and send the email
    msg = f"Subject:{subject}\n\n{body}\n\nRegards,\nUmbrellaReminderErdem".encode('utf-8')
    smtp_object.sendmail("umbrellaremindererdem@gmail.com", "esmaerdem94@gmail.com", msg)

    # Close the SMTP connection
    smtp_object.quit()
    print("Email Sent!")