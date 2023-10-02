import smtplib
import requests
from bs4 import BeautifulSoup
import geocoder
from decouple import config
import logging  # Import the logging module

# Create a logger
logger = logging.getLogger(__name__)

# Load environment variables from .env to get email password
PASSWORD = config('MAIL_PASSWORD')

def currentWeather(user):
    try:
        # getting latitude and longitude of location to use it in the URL
        location = geocoder.osm(user.location)

        if location:
            print("Latitude:", location.latlng[0])
            print("Longitude:", location.latlng[1])
        else:
            print("Location not found")

        # sending request to the URL with desired location lat and long
        url = f"https://forecast.weather.gov/MapClick.php?lat={location.latlng[0]}&lon={location.latlng[1]}"
        html = requests.get(url).content

        # webscraping using BeautifulSoup
        weather_data = BeautifulSoup(html, 'html.parser')

        # retrieving necessary data from scraped data including current weather, temp, and how it looks like later that day
        weather = weather_data.find(
            'p', attrs={'class': 'myforecast-current'}).text
        temperature = weather_data.find(
            'p', attrs={'class': 'myforecast-current-lrg'}).text
        nightly = weather_data.find(
            'div', attrs={'class': 'forecast-text'}).text
        print(weather, temperature, nightly)

        # checking if the weather has rain if so send the user's reminder email
        if any(keyword in weather.lower() for keyword in ["thunderstorm", "heavy rain", "windy", "rainy", "showers", "haze", "light rain", "mist"]):
            # initializing an SMTP (Simple Mail Transfer Protocol) object for sending emails via Gmail's SMTP server on port 587.
            smtp_object = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
            smtp_object.starttls()

            # Authentication
            smtp_object.login("umbrellaremindererdem@gmail.com", PASSWORD)

            # Email subject and body
            subject = "Umbrella Reminder"
            body = f"Dear {user.username}, Take an umbrella before leaving the house. Weather condition for today is {weather} and temperature is {temperature} in {user.location}. Tonight's weather looks like: {nightly}"

            # Construct and send the email
            msg = f"Subject:{subject}\n\n{body}\n\nStay dry,\nUmbrellaReminderErdem".encode('utf-8')
            smtp_object.sendmail("umbrellaremindererdem@gmail.com", user.email, msg)

            # Close the SMTP connection
            smtp_object.quit()
            print("Email Sent!")
        else:
            # initializing an SMTP (Simple Mail Transfer Protocol) object for sending emails via Gmail's SMTP server on port 587.
            smtp_object = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
            smtp_object.starttls()

            # Authentication
            smtp_object.login("umbrellaremindererdem@gmail.com", PASSWORD)

            # Email subject and body
            subject = "Sunscreen Reminder"
            body = f"Dear {user.username}, Make sure to wear sunscreen half an hour before leaving the house. Weather condition for today is {weather} and temperature is {temperature} in {user.location}. Tonight's weather looks like: {nightly}"

            # Construct and send the email
            msg = f"Subject:{subject}\n\n{body}\n\nKeep your skin gorgeous,\nUmbrellaReminderErdem".encode('utf-8')
            smtp_object.sendmail("umbrellaremindererdem@gmail.com", user.email, msg)

            # Close the SMTP connection
            smtp_object.quit()
            print("Email Sent!")

    except geocoder.GeocoderTimedOut:
        logger.error(f"Geocoder timed out for location: {user.location}")
        # Handle the timeout error here
    except requests.exceptions.RequestException as e:
        logger.error(f"RequestException occurred: {str(e)}")
        # Handle the request exception here
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        # Handle other unexpected exceptions here
