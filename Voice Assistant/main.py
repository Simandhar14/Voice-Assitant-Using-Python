import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import requests
from bs4 import BeautifulSoup

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def get_weather(city):
    api_key = "45e4b5eac79649eb4657572631eac689"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    weather_data = response.json()

    if weather_data["cod"] == "404":
        raise Exception("City not found")

    temperature = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]

    return f"The temperature in {city} is {temperature}°C with {description}. Humidity: {humidity}%. Wind speed: {wind_speed} m/s"


def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com','your-password')
    server.sendmail('youremail@gmail.com',to,content)
    server.close()



def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Jarvis Sir. Please tell me how may i help you")

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:  # Use the constructor here
        print("Listening...")
        r.pause_threshold = 1  # It gives the user a time of 1 sec to take a break while speaking
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query


if __name__=="__main__":
    wishMe()
    if 1:
        query=takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query,sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'the time' in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir,The time is{strTime}")
        elif 'open code' in query:
            codepath="C:\\Users\\baids\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codepath)
        elif 'email to simandhar' in query:
            try:
                speak("What should i write?")
                content=takeCommand()
                to="youremail@gmail.com"
                sendEmail(to,content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Sorry, i am not able to send this email")
        elif 'weather' in query:
            try:
                speak("Tell me the name of the city")
                city = takeCommand().lower()  # Get the city name from user's speech
                weather_info = get_weather(city)
                print(weather_info)
                speak(weather_info)
            except Exception as e:
                print(e)
                speak("Sorry, I was not able to get the weather information")

