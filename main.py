# a program to send a text message to person with 12 hour forcast
import requests
import os
from datetime import datetime
from twilio.rest import Client 

api_key = os.environ.get("API_KEY")
account_sid = os.environ.get("ACCT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
my_phone_number = "YOUR_PHONE_NUMBER"

class Weather:
    """Get Weather forcast"""
    
    def __init__(self):

        self.parameters = {"lat": 40.678177,
                           "lon": -73.944160,
                           "appid": api_key,
                           "units": "imperial",
                           "exclude": "minutely"}
        self.res = requests.get(
            "https://api.openweathermap.org/data/2.5/onecall", params=self.parameters)
        self.data = self.res.json()
        self.current_data = self.data["current"]
        self.date = self.current_data["dt"]
        self.date = self.data
        self.current_temp = round(self.current_data["temp"])
        self.weather_id = self.current_data["weather"][0]["id"]

    def weekly_forcast(self):
        """
        Return formated forcast for each day of the week, providing min/max
        temp and weather conditions 
        """
        self.weekly_data = self.data["daily"]
        week_dict = {}
        for day in self.weekly_data:
            # set each dict key with day of the week using UNIX timestamp
            timestamp = day["dt"]
            weekday = datetime.utcfromtimestamp(timestamp).strftime('%A')
            week_dict[weekday] = day
            self.week_forcast = ""
        for day in week_dict:
            # extract and format min/max temp and weather conditions for 7 day
            min_temp = week_dict[day]["temp"]["min"]
            max_temp = week_dict[day]["temp"]["max"]
            weather_conditions = week_dict[day]["weather"][0]["description"]
            daily_forcast_text = f"Day: {day}\n\tMIN: {min_temp}, MAX: {max_temp},\n\tforcast: {weather_conditions}\n"
            self.week_forcast += daily_forcast_text
        return self.week_forcast

    def hourly_forcast(self):
        """Get the weather conditions for the next day from 5am-8pm """
        self.hourly_data = self.data["hourly"][6:22]
        self.forcast_text = ""
        for hour in self.hourly_data:
            timestamp = hour["dt"]
            formatted_hour = datetime.utcfromtimestamp(
                timestamp).strftime('%A, %H:%M')
            main_condition = hour["weather"][0]["main"]
            description = hour["weather"][0]["description"]
            forcast = (
                f"Time: {formatted_hour}\n\tMain: {main_condition},\n\tDescription: {description}\n")
            self.forcast_text += forcast
        return self.forcast_text


# get forcast for week and hours
weather = Weather()
hourly_forcast = weather.hourly_forcast()
weekly_forcast = weather.weekly_forcast()

# text hourly forcast via Twilio

client = Client(account_sid, auth_token)

message = client.messages.create(
                     body=f"Here is your hourly weather forcast for the day:\n{hourly_forcast}.",
                     from_='+17738302382',
                     to=my_phone_number
                 )

# text hourly forcast via Twilio

message = client.messages.create(
                     body=f"Here is your weekly weather forcast:\n{weekly_forcast}.",
                     from_='+17738302382',
                     to=my_phone_number
                 )
