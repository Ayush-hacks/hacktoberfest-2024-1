import speech_recognition as sr
import webbrowser
import requests
import pyttsx3

recognize = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

apikey = "" #put your api here

def playsong(userinput):
    words = userinput.split() #converted to list
    
    playindex = words.index('play') if 'play' in words else -1

    if playindex != -1:
        platformindex = words.index('on') if 'on' in words else -1

        if platformindex != -1:
            songname = ' '.join(words[playindex + 1:platformindex]).strip() #string strip between on and play.  
            platform = ' '.join(words[platformindex + 1:]).strip()
        else:
            songname = ' '.join(words[playindex + 1:]).strip()
            platform = 'youtube'

        speak(f"Opening {songname} on {platform}. Enjoy!")

        if platform.lower() == 'spotify': 
            url = f"https://open.spotify.com/search/{songname.replace(' ', '%20')}"
        elif platform.lower() == 'youtube music':
            url = f"https://music.youtube.com/search?q={songname.replace(' ', '%20')}"
        else:
            url = f"https://www.youtube.com/results?search_query={songname.replace(' ', '+')}"
        
        webbrowser.open(url)
    else:
        speak("I couldn't understand the request. Please try again.")


def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open insta" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open yt" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={apikey}")
        if r.status_code == 200:
            data = r.json()
            if 'articles' in data and data['articles']:
                for article in data['articles']:
                    speak(article['title'])
    else:
        # Check for song requests
        if 'play' in c.lower():
            playsong(c)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        r = sr.Recognizer()
        print("Hi recognizing....")

        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes?")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processcommand(command)
        except Exception as e:
            print(f"Error: {e}")
