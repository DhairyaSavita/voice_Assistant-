import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import datetime
import os
import wikipedia
import wolframalpha
from googletrans import Translator

engine = pyttsx3.init()


wolfram_client = wolframalpha.Client('YOUR_WOLFRAM_API_KEY') 

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat, please?")
        return "None"
    return query.lower()


def get_weather(city=None):
    api_key = ""  
    if not city:
        city = "your city"  
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        main = weather_data["main"]
        temperature = main["temp"]
        weather_description = weather_data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {weather_description}.")
    else:
        speak("Sorry, I couldn't find the weather information.")

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}.")

def answer_question(question):
    try:
       
        res = wolfram_client.query(question)
        answer = next(res.results).text
        speak(answer)
    except Exception:
     
        try:
            answer = wikipedia.summary(question, sentences=2)
            speak(answer)
        except wikipedia.exceptions.DisambiguationError:
            speak("I found multiple results. Can you be more specific?")
        except Exception as e:
            speak("Sorry, I couldn't find the answer to that question.")
            print(e)


def translate_text(text, target_language="en"):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        speak(f"The translation is: {translation.text}")
    except Exception as e:
        speak("Sorry, I couldn't translate the text.")
        print(e)


def search_web(query):
    speak(f"Searching for {query} on the web.")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def open_application(app_name):
    try:
        if "notepad" in app_name:
            os.system("notepad.exe")  # Example for Windows
        else:
            speak("Application not supported.")
    except Exception as e:
        speak("Sorry, I couldn't open the application.")
        print(e)

# Main command execution
def execute_command(command):
    if "weather" in command:
        speak("Which city?")
        city = listen()
        get_weather(city)

    elif "time" in command:
        tell_time()

    elif "question" in command:
        speak("What question would you like me to answer?")
        question = listen()
        answer_question(question)

    elif "translate" in command:
        speak("What would you like to translate?")
        text_to_translate = listen()
        speak("Which language should I translate to?")
        target_language = listen()
        translate_text(text_to_translate, target_language)

    elif "search" in command or "look up" in command:
        speak("What should I search for?")
        query = listen()
        search_web(query)

    elif "open" in command:
        speak("Which application would you like to open?")
        app_name = listen()
        open_application(app_name)

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("Sorry, I didn't understand the command.")


def start_assistant():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if command != "None":
            execute_command(command)

if __name__ == "__main__":
    start_assistant()
