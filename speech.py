import pyttsx3  # For text-to-speech conversion
import speech_recognition as sr  # For voice recognition
import datetime  # For handling time-based tasks
import wikipedia  # For retrieving information from Wikipedia
import webbrowser  # For opening websites
import os  # For interacting with the operating system
import requests  # For interacting with APIs like weather and news

# Initialize the speech recognition and text-to-speech engines
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize voice commands
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1.2)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-US')
        print(f"User said: {command}\n")
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you say it again?")
        speak("Sorry, I didn't catch that. Could you say it again?")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        speak("Sorry, I couldn't connect to the recognition service.")
        return None
    return command.lower()

# Greeting based on time of day
def greet_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Voite, I'll be your assistant. How can I help you today?")

# Function to get weather information using OpenWeatherMap API
def get_weather(city):
    api_key = '5aa261f9b5512edd0a2028d394d3a3c8'  #OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    weather_data = response.json()
    if weather_data["cod"] != "404":
        main = weather_data["main"]
        temperature = main["temp"]
        weather_description = weather_data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {weather_description}.")
    else:
        speak("Sorry, I couldn't find the weather details for that location.")

# Function to get news headlines using NewsAPI
def get_news():
    api_key = 'e1d95f5811164fc994dc1ecdce0bbc87'  # NewsAPI key
    base_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(base_url)
    news_data = response.json()
    if news_data["status"] == "ok":
        articles = news_data["articles"]
        speak("Here are some top news headlines:")
        for i, article in enumerate(articles[:5]):
            speak(f"News {i + 1}: {article['title']}")
    else:
        speak("Sorry, I couldn't retrieve the news.")

# Main function to execute commands
def take_command():
    while True:
        command = listen()
        if command:
            if 'open youtube' in command:
                webbrowser.open("https://www.youtube.com")
                speak("Opening YouTube.")
            elif 'search wikipedia' in command:
                speak("What should I search on Wikipedia?")
                query = listen()
                if query:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
            elif 'play music' in command:
                music_dir = r'C:\Users\Davy\Desktop\music'  # music directory
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))
                speak("Playing music.")
            elif 'tell me the time' in command:
                current_time = datetime.datetime.now().strftime("%H:%M")
                speak(f"The time is {current_time}.")
            elif 'weather' in command:
                speak("Please tell me the city name.")
                city = listen()
                if city:
                    get_weather(city)
            elif 'news' in command:
                get_news()
            elif 'quit' in command or 'goodbye' in command:
                speak("Goodbye!")
                break
            else:
                speak("I am sorry, I don't know that command yet.")

# Main execution starts here
if __name__ == "__main__":
    greet_user()
    take_command()

