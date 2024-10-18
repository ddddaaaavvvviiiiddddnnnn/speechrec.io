import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests
from flask import Flask, render, jsonify, request

app = Flask(__name__)

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    api_key = '5aa261f9b5512edd0a2028d394d3a3c8'
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    weather_data = response.json()
    if weather_data["cod"] != "404":
        main = weather_data["main"]
        temperature = main["temp"]
        weather_description = weather_data["weather"][0]["description"]
        return f"The temperature in {city} is {temperature} degrees Celsius with {weather_description}."
    else:
        return "Sorry, I couldn't find the weather details for that location."

@app.route('/')
def index():
    return render('index.html')

@app.route('/process-command')
def process_command():
    command = request.args.get('command')
    response = ""

    if 'open youtube' in command.lower():
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube."
    elif 'search wikipedia' in command.lower():
        response = "What should I search on Wikipedia?"
        results = wikipedia.summary(command.replace('search wikipedia', ''), sentences=2)
        response += f" According to Wikipedia: {results}"
    elif 'play music' in command.lower():
        music_dir = 'C:\\Users\\Davy\\Desktop\\music'
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
        response = "Playing music."
    elif 'tell me the time' in command.lower():
        current_time = datetime.datetime.now().strftime("%H:%M")
        response = f"The time is {current_time}."
    elif 'weather' in command.lower():
        response = "Please tell me the city name."
        city = command.replace('weather', '').strip()
        if city:
            response = get_weather(city)
    else:
        response = "I am sorry, I don't know that command yet."

    speak(response)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
