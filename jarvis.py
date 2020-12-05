import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import sys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
# select jarvis's voice'
engine.setProperty('voice', voices[0].id)

# creating dictionary of email ids
email_id = {"hp": "harry.potter@hogwarts.com"}

chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening")

    speak("Hi I am Jarvis! How may I help you?")


def takeCommand():
    """
    Takes command as an audio input from user and returns string output
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # removing background noise just to hear user's voice'
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)
        print(audio)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User said: ", query)

    except Exception as e:
        print(e)
        print("Please say that again...")
        return "None"

    return query


def sendEmail(to, content):
    # Enable less secure apps option for your gmail as step one before running this function
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('fn.ln@gmail.com', 'your-password-here')
    server.sendmail('fn.ln@gmail.com', to, content)
    server.close()


if __name__ == '__main__':
    wishMe()  # run only once, hence written out of while loop

    while True:
        query = takeCommand().lower()

        # Logic for executing tasks on user input
        if 'wikipedia' in query or 'who is' in query:
            try:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                query = query.replace("who is", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak("Sorry I couldn't search wikipedia. Please ask me again clearly.")

        elif 'open youtube' in query:
            speak("Opening Youtube")
            webbrowser.get(chrome_path).open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.get(chrome_path).open("google.com")
            # webbrowser.open("google.com")

        elif 'play music' in query:
            speak("Playing music from your playlist")
            music_dir = "C:\\Users\\aksha\\Music"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[1]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'open notepad' in query:
            speak("Opening Notepad")
            notepad_path = "C:\\WINDOWS\\system32\\notepad.exe"
            os.startfile(notepad_path)

        elif 'how are you' in query:
            speak("I am fine, thank you! Hope you are doing well too")

        elif 'repeat' in query:
            query = query.replace("say", "")
            query = query.replace("se", "")
            query = query.replace("repeat", "")
            speak(query)

        elif 'send email to' in query:
            recipient = query.replace("send email to", "")
            print(recipient)
            try:
                speak("What should I say?")
                content = takeCommand()
                to = recipient
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email at the moment")

        elif 'quit' in query or 'bye' in query or 'tata' in query:
            speak("Thanks for your time. Bye Bye! Tata")
            sys.exit(0)

