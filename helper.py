import schedule
import smtplib   
import requests
from bs4 import BeautifulSoup
from models import connect_db, User
import geocoder
from decouple import Config, Csv
config = Config(Csv())
from flask import Flask
import logging  # Import the logging module

# Create a Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///weather'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# Push the application context
app.app_context().push()

# Connect to the database
connect_db(app)
# Load environment variables from .env to get email password
PASSWORD = config('MAIL_PASSWORD')

# Create a logger
logger = logging.getLogger(__name__)

# Function to fetch user locations within a Flask app context
def fetch_user_locations():
    # Fetch all users from the database
    users = User.query.all()
    print(set(map(lambda u: u.username, users)))
    # Use a lambda function with map to extract unique locations
    locations = set(map(lambda u: u.location, users))
    return locations

# Fetch user locations
locations = fetch_user_locations()

def weatherReminder():
    try:
        for location_town in locations:
            # getting latitude and longitude of location to use it in the url
            location = geocoder.osm(location_town)

            if location:
                print("Latitude:", location.latlng[0])
                print("Longitude:", location.latlng[1])
            else:
                print("Location not found")

            # sending request to the url with desired location lat and long
            url = f"https://forecast.weather.gov/MapClick.php?lat={location.latlng[0]}&lon={location.latlng[1]}"
            html = requests.get(url).content

            # webscraping using beautifulsoup
            weather_data = BeautifulSoup(html, 'html.parser')

            # retriving necessary data from scraped data includign current weather, temp and how it looks like later that day
            weather = weather_data.find(
                'p', attrs={'class': 'myforecast-current'}).text
            temperature= weather_data.find(
                'p', attrs={'class': 'myforecast-current-lrg'}).text
            nightly = weather_data.find(
                'div', attrs={'class': 'forecast-text'}).text
            print(weather, temperature, nightly)

            # checking if the weather has rain if so send the users reminder email
            if any(keyword in weather.lower() for keyword in ["thunderstorm", "heavy rain", "windy", "rainy", "showers", "haze", "light rain", "mist"]):
                # pulling all the users who live in the location which has rainy weather
                users = User.query.filter(User.location == location_town).all()
                # getting their email addresses
                user_emails = set(map(lambda u: u.email, users))
                print(user_emails)
                # initializing an SMTP (Simple Mail Transfer Protocol) object for sending emails via Gmail's SMTP server on port 587.
                smtp_object = smtplib.SMTP('smtp.gmail.com', 587)

                # start TLS for security
                smtp_object.starttls()

                # Authentication
                smtp_object.login("umbrellaremindererdem@gmail.com", PASSWORD)

                for email in user_emails:
                    # Email subject and body
                    subject = "Umbrella Reminder"
                    body = f"Take an umbrella before leaving the house. Weather condition for today is {weather} and temperature is {temperature} in {location_town}. Tonight's weather looks like: {nightly}"

                    # Construct and send the email
                    msg = f"Subject:{subject}\n\n{body}\n\nStay dry,\nUmbrellaReminderErdem".encode('utf-8')
                    smtp_object.sendmail("umbrellaremindererdem@gmail.com", email, msg)

                # Close the SMTP connection
                smtp_object.quit()
                print("Email Sent!")
            else:
                # pulling all the users who live in the location which has nice weather
                users = User.query.filter(User.location == location_town).all()
                # getting their email addresses
                user_emails = set(map(lambda u: u.email, users))
                print(user_emails)
                # initializing an SMTP (Simple Mail Transfer Protocol) object for sending emails via Gmail's SMTP server on port 587.
                smtp_object = smtplib.SMTP('smtp.gmail.com', 587)

                # start TLS for security
                smtp_object.starttls()

                # Authentication
                smtp_object.login("umbrellaremindererdem@gmail.com", PASSWORD)

                for email in user_emails:
                    # Email subject and body
                    subject = "Sunscreen Reminder"
                    body = f"Make sure to wear sunscreen half an hour before leaving the house. Weather condition for today is {weather} and temperature is {temperature} in {location_town}. Tonight's weather looks like: {nightly}"

                    # Construct and send the email
                    msg = f"Subject:{subject}\n\n{body}\n\nKeep your skin gorgeous,\nUmbrellaReminderErdem".encode('utf-8')
                    smtp_object.sendmail("umbrellaremindererdem@gmail.com", email, msg)

                # Close the SMTP connection
                smtp_object.quit()
                print("Email Sent!")

    except geocoder.GeocoderTimedOut:
        logger.error(f"Geocoder timed out for location: {location_town}")
        # Handle the timeout error here
    except requests.exceptions.RequestException as e:
        logger.error(f"RequestException occurred: {str(e)}")
        # Handle the request exception here
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        # Handle other unexpected exceptions here




# checking the weather every day at 7am and send emails if the location is rainy, this scheduler works while helper.py is running within venv
# schedule.every().day.at("07:00").do(weatherReminder)

# while True:
#     schedule.run_pending()
