import pyttsx3 as p
import speech_recognition as sr

engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

r = sr.Recognizer()

speak("Hello there, I'm Voite, I'll be your voice assistant. How are you?")

with sr.Microphone() as source:
    r.energy_threshold = 10000
    r.adjust_for_ambient_noise(source, duration=1.2)
    print("Listening")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(text)
        if "what about you" in text:
            speak("I'm having a fantastic day, please, may I know your name?")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

speak("How may I help you?")
