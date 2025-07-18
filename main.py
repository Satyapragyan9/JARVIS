import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import google.generativeai as genai
from apikey import api_data

# Configure Gemini API
GENAI_API_KEY = api_data
genai.configure(api_key=GENAI_API_KEY)

# Initialize speech recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def generate_response(query):
    """Generate a response for the given query using Gemini."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # use "gemini-1.5-pro" if available in your API
        response = model.generate_content(
            query,
            generation_config=genai.GenerationConfig(
                max_output_tokens=100,
                temperature=0.2
            )
        )
        return response.text if response and hasattr(response, 'text') else "I couldn't process that."
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, there was an error with the AI response."

def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
        speak("Opening Google.")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook.")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn.")
    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak("Song not found in your music library.")
    else:
        response = generate_response(c)
        speak(response)

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        print("\nSay Jarvis for activate 'Jarvis'...")

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if word.lower() == "jarvis":
                speak("Yes boss.")

                with sr.Microphone() as source:
                    print("Jarvis is active, waiting for your command...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print("Command:", command)

                    if command.lower() in ["quit", "exit", "shutdown", "stop"]:
                        speak("Shutting down. Goodbye boss.")
                        break
                    else:
                        processCommand(command)

        except sr.WaitTimeoutError:
            print("Listening timed out, waiting again...")
        except sr.UnknownValueError:
            print("Sorry, I did not catch that.")
        except Exception as e:
            print(f"Error: {e}")
