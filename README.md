# Flask Weather Reminder App

The Flask Weather Reminder App is a simple web application that allows users to sign up for weather-related email reminders. It checks the weather conditions for user-specified locations and sends email reminders based on the weather forecast.

## Motivation

The motivation behind creating this app was to embark on a weekend project for learning and practicing various Python libraries. During the course of this short project, I aimed to gain hands-on experience with libraries such as BeautifulSoup, Schedule, and others. 

This project served as a valuable opportunity to explore and apply web scraping techniques, scheduling tasks, and working with geolocation data, all within a limited timeframe.

Keep in mind that this app was developed as a weekend project, highlighting the dedication to learning and practical application of Python libraries in a short span and setting myself up for challenges coming ahead.

- Learn how to webscrape using BeautifulSoup.
- Utilize features like Geocoder for location-based data.
- Implement SMTP (Simple Mail Transfer Protocol) for sending email notifications.
- Explore different scheduling methods, including Python's `schedule` library and Windows Task Scheduler. Intructions on how to implement these feature is explained below.

## Features

- **User Signup:** Users can register by providing their username, email address, and the desired location for weather reminders. This feature is implemented to save users' information to send scheuled reminder emails. 
- **Weather Reminders:** The app sends emails to users based on the current weather conditions in their specified location upon signup (using `current.py`). While the `helper.py` script is set to send reminder emails every morning at 07:00 am, this feature is not implemented in the app since the app is educational purposes.
- **Email Notifications:** Users receive emails with weather information and reminders to take appropriate actions, such as carrying an umbrella or wearing sunscreen.

## Technologies Used

- Python(Python 3.10.6), 
- Flask as Backend, 
- PostgreSQL for designing database.
- SQLAlchemy for modeling SQL tables
- BeautifulSoup: A Python library for web scraping HTML.
- Geocoder: A Python library for working with geolocation data.
- Requests: A Python library for making HTTP requests.
- Flask-WTF for creating web forms.
- SMTP (Simple Mail Transfer Protocol) for sending email notifications.

## Installation and Setup

1. Clone this repository to your local machine.

```shell
https://github.com/EsmaNErdem/weather_reminder.git
```

2. Create a virtual environment using Python 3.10.6:
```shell
    python3 -m venv venv
```

3. Activate the virtual environment:
```shell
    source venv/bin/activate
```

4. Install the required packages using pip:
```shell
    (venv) $ pip3 install -r requirements.txt
```

5. Create a PostgreSQL database for the app:
```shell
    (venv) $ createdb weather
```

6. Create database tables for the app:
```shell
    (venv) $ python3 seed.py
```

7. Create a `.env` file and add your Gmail email and password for sending email notifications.

8. Create a PostgreSQL database for the test:
```shell
    (venv) $ createdb weather_test
```


## Scheduling Weather Reminders

The Flask Weather Reminder App provides two methods for scheduling weather reminders:


### 1. Python `schedule` Library

The Python `schedule` library allows your Python script to perform tasks at specific times while the script is running. To set up scheduled weather reminders using this method, follow these steps:

1. Open the `helper.py` file in your project directory.

2. Locate the `weatherReminder` function within the script. This function is responsible for checking the weather conditions and sending email reminders.

3. Within the `weatherReminder` function, you'll find a comment indicating the scheduled time: `# checking the weather every day at 7 am and send emails if the location is rainy`. You can modify this time to your desired schedule using military time (24-hour clock). For example, to schedule reminders at 3:30 PM, set it to `"15:30"`.

4. Save the `helper.py` file after making your changes.

5. Run the `helper.py` to activate the scheduler:


### 2. Windows Task Scheduler (Windows Users)

While building this app, I practiced using Windows Task Scheduler and Windows Services to keep `helper.py` running. Although this feature is not implemented in the app itself, you can manually set up the task scheduler to automate the script. Here's how to do it:

1. Create a Batch Script:

First, create a batch script (a .bat file) that activates your virtual environment and then runs your Python script. Open a text editor and create a file named run_script.bat with the following content:

```t
@echo off
call C:\path\to\your\virtualenv\Scripts\activate
python "C:\path\to\your\script\helper.py"
```

2. Open Windows Task Scheduler on your computer.

3. Create a new task and configure it to run your Python script, `helper.py`, at the desired schedule (e.g., daily at 7 AM).

4. Set up triggers, actions, and conditions as needed for your specific use case.

5. Save and activate the task.

Now, Windows Task Scheduler will execute your `helper.py` script according to the defined schedule, even if the Flask app is not running. This method allows for more automated weather reminders.

Please note that these instructions are provided for educational purposes, and the app itself does not implement this functionality. Feel free to use either method based on your preference and requirements.

For more instruction on how to implement Windows Task Scheduler:
- Implementing Task Scheduler:
https://www.youtube.com/watch?v=4n2fC97MNac&t=334s
- Starting your virtual enviroment within task scheduler:
https://stackoverflow.com/questions/34622514/run-a-python-script-in-virtual-environment-from-windows-task-scheduler

### Further Study

## Further Study

This Flask Weather Reminder App is an educational project designed for learning and practicing various Python libraries and concepts. While the app is functional and demonstrates key features, there are several areas for further study and enhancement:

### Writing Tests

Testing is a crucial part of any software development process. I will be writing unit tests and integration tests to ensure the reliability and robustness of the application. The app includes a test database (`weather_test`) for this purpose.

### Error Handling and Logging

Strengthening the app's error handling and logging mechanisms is important. I will ensure that the app gracefully handles unexpected errors and provides clear error messages to users. Comprehensive logging will be implemented to track application activities and errors effectively.

### Advanced Scheduling

Explore advanced scheduling options to optimize the timing of weather reminders. Implement features such as user-specific reminder schedules, multiple reminder times per day, or user-configurable reminder preferences.

### User Opt-Out From Email List Requests

I will be developing a feature that allows users to opt-out from the reminder email list. This feature respects users' preferences. 


Remember that continuous learning and improvement are essential in software development. I use this project as a foundation to explore more advanced topics and technologies in web development and application deployment.
