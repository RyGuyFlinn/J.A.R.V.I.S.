import pyaudio
import pyttsx3
import speech_recognition as sr
import time
import pvporcupine
import struct
import winsound
import os
import subprocess
import webbrowser
import tkinter as tk  # Importing tkinter for UI
from PIL import Image, ImageTk  # Importing PIL for GIF handling
from datetime import datetime
import random
import requests

USER = "sir"
TALKING = False

# Initialize tkinter for the UI
root = tk.Tk()
root.title("JARVIS UI")
root.geometry("200x200")  # Set a square size for the window
root.attributes('-topmost', True)  # Make the window always on top
root.configure(bg='black')  # Set background color to black

# Get screen width and height to position window in bottom-right corner with margin
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_size = 200  # Set the size of the square window
margin = 15  # Set the margin size
x_position = screen_width - window_size - margin  # Adjust for margin
y_position = screen_height - window_size - margin  # Adjust for margin

# Set the position of the window
root.geometry(f"{window_size}x{window_size}+{x_position}+{y_position}")

# Label to show JARVIS state
status_label = tk.Label(root, text="JARVIS is Idle", font=("Arial", 12), fg='white', bg='black')  # Text color white
status_label.pack(pady=10)

# Load the GIF
gif_path = "C:\\Users\\RyGuy\\Downloads\\2dabb694e9bfccef713863a4a6543c79_w200.gif"  # Update with your GIF path
gif_image = Image.open(gif_path)

# Function to update the GIF frames
def update_gif():
    try:
        # Get the next frame
        frame = gif_image.copy()
        frame.thumbnail((100, 100))  # Resize frame to fit the smaller window
        gif_frame = ImageTk.PhotoImage(frame)
        gif_label.config(image=gif_frame)
        gif_label.image = gif_frame  # Keep a reference

        # Tint the GIF if JARVIS is talking
        if TALKING:
            tinted_frame = apply_tint(frame, tint_color=(255, 255, 255), alpha=0.5)  # White tint
            tinted_gif_frame = ImageTk.PhotoImage(tinted_frame)
            gif_label.config(image=tinted_gif_frame)
            gif_label.image = tinted_gif_frame  # Keep a reference to the tinted image
            
        gif_image.seek(gif_image.tell() + 1)  # Move to the next frame
    except EOFError:
        gif_image.seek(0)  # Loop back to the first frame

def apply_tint(image, tint_color=(255, 255, 255), alpha=0.5):
    """Apply a tint to the given image, keeping the transparency intact."""
    # Convert the image to RGBA if it isn't already
    image = image.convert("RGBA")
    
    # Create an overlay with the tint color
    overlay = Image.new("RGBA", image.size, tint_color + (int(200 * alpha),))

    # Create a new image for the tinted output
    tinted_image = Image.new("RGBA", image.size)

    # Blend the overlay with the original image, respecting the alpha channel
    for x in range(image.width):
        for y in range(image.height):
            orig_pixel = image.getpixel((x, y))
            overlay_pixel = overlay.getpixel((x, y))

            # Calculate the new pixel value
            new_pixel = (
                int((orig_pixel[0] * (255 - overlay_pixel[3]) + overlay_pixel[0] * overlay_pixel[3]) / 255),
                int((orig_pixel[1] * (255 - overlay_pixel[3]) + overlay_pixel[1] * overlay_pixel[3]) / 255),
                int((orig_pixel[2] * (255 - overlay_pixel[3]) + overlay_pixel[2] * overlay_pixel[3]) / 255),
                orig_pixel[3]  # Keep original alpha
            )

            tinted_image.putpixel((x, y), new_pixel)

    return tinted_image

# Create a label for the GIF
gif_label = tk.Label(root, bg='black')  # Set background color of the GIF label to black
gif_label.pack(pady=5)  # Add some padding

# Update the GIF frames repeatedly
def animate_gif():
    update_gif()
    root.after(25, animate_gif)  # Update every 50 ms for faster playback

animate_gif()  # Start the GIF animation

# Speaks back to the user and updates UI
def speak(text):
    global TALKING
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    TALKING = True
    status_label.config(text="JARVIS is Speaking")  # Update UI
    print("J.A.R.V.I.S.: " + text + " \n")
    engine.say(text)
    engine.runAndWait()
    TALKING = False
    status_label.config(text="JARVIS is Idle")  # Reset UI after speaking

# Listens to the user and updates UI
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust for ambient noise to reduce background noise
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)  # Noise filtering with a 1-second duration
        
        # Ready to listen
        print("Listening...", end="")
        status_label.config(text="JARVIS is Listening")  # Update UI
        root.update()  # Refresh the window

        # Listen to the user's input
        audio = r.listen(source)
        query = ''
        
        try:
            print("Recognizing...", end="")
            query = r.recognize_google(audio, language='en-US')  # Recognize speech
            print(f"User said: {query}")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
        except Exception as e:
            print("Exception: " + str(e))

    status_label.config(text="JARVIS is Idle")  # Reset UI after listening
    return query.lower()

def get_weather_info():
    API_KEY = 'e01d6f57ccd88b49acb29affd1ed88df'  # Replace with your OpenWeatherMap API key
    CITY = 'Vancouver'  # Replace with your city name
    URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=imperial'

    try:
        response = requests.get(URL)
        data = response.json()
        if response.status_code == 200:  # Check if the request was successful
            temp = data['main']['temp']
            weather_desc = data['weather'][0]['description']
            return f"The temperature is {temp}°F with {weather_desc}."
        else:
            return f"Error {data['cod']}: {data['message']}"  # Return specific error messages
    except Exception as e:
        return f"There was an error retrieving weather information: {str(e)}"

    
def tell_joke():
    jokes = [
        "Why don’t scientists trust atoms?: Because they make up everything!",
        "Why did the scarecrow win an award?: Because he was outstanding in his field!",
        "What do you call fake spaghetti?: An impasta!",
        "Why don’t skeletons fight each other?: They don’t have the guts!",
        "Why did the math book look sad?: Because it had too many problems.",
        "What do you call cheese that isn't yours?: Nacho cheese!",
        "Why was the broom late?: It swept in!",
        "Why did the computer go to therapy?: Because it had too many bytes!",
        "What do you call a bear with no teeth?: A gummy bear!",
        "Why can’t you give Elsa a balloon?: Because she will let it go!",
        "What did one wall say to the other wall?: I'll meet you at the corner!",
        "Why don't eggs tell jokes?: Because they might crack up!",
        "What do you get when you cross a snowman and a vampire?: Frostbite!",
        "Why did the bicycle fall over?: Because it was two-tired!",
        "What did the ocean say to the beach?: Nothing, it just waved!",
        "Why don’t oysters donate to charity?: Because they are shellfish!",
        "What do you call a fish wearing a bowtie?: Sofishticated!",
        "Why did the golfer bring two pairs of pants?: In case he got a hole in one!",
        "How do you organize a space party?: You planet!",
        "Why did the cookie go to the hospital?: Because it felt crummy!"
    ]
    return random.choice(jokes)

def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
    current_date = now.strftime("%Y-%m-%d")
    return f"The current date is {current_date} and the time is {current_time}."

def ReadyChirp1():
    winsound.Beep(600, 300)

def ReadyChirp2():
    winsound.Beep(500, 300)

def Website(url):
    webbrowser.get().open(url)

def web_search(query):
    """Search the web for a given query."""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def Daily():
    speak("Good Morning " + USER)
    os.startfile('C:\\Users\\RyGuy\\Downloads\\videoplayback.m4a')
    
def ConversationFlow():
    while True:
        userSaid = takeCommand()
        if "hello" in userSaid or "hi" in userSaid or "hey" in userSaid:
            speak("hello " + USER)
        if "stop" in userSaid or "thank" in userSaid or "bye" in userSaid or "exit" in userSaid:
            speak("Shutting down program " + USER)
            break
        if "email" in userSaid:
            speak("Opening your email " + USER)
            Website('https://mail.google.com/mail/u/0/#inbox')
        if "calculator" in userSaid:
            try:
                subprocess.Popen("calc")
                speak("Calculator opening " + USER)
            except:
                speak("Calculator not opening " + USER)
                pass
        if "wake up" in userSaid or "i'm home" in userSaid:
            Daily()
            break
        if "weather" in userSaid or "tempature" in userSaid or "how hot is it" in userSaid:
            weather_info = get_weather_info()
            speak(weather_info)
        if "joke" in userSaid:
            joke = tell_joke()
            speak(joke)
        if "time" in userSaid or "date" in userSaid or "day" in userSaid:
            current_time = get_current_time()
            speak(current_time)
        if "search" in userSaid or "look up" in userSaid:
            query = userSaid.replace("search for ", "").replace("look up ", "")
            speak(f"Searching the web for {query}")
            web_search(query)


def Jmain():
    porcupine = None
    pa = None
    audio_stream = None

    print("J.A.R.V.I.S. version 1.2 - Online and Ready!")
    print("********************************************************")
    status_label.config(text="JARVIS is Awaiting Call")  # Update UI
    root.update()

    try:
        porcupine = pvporcupine.create(keywords=["jarvis", "computer"])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length)

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Hotword Detected.. ", end="")
                status_label.config(text="Hotword Detected")  # Update UI
                root.update()  # Refresh the window
                speak("yes " + USER)
                ConversationFlow()
                time.sleep(1)
                status_label.config(text="JARVIS is Awaiting Call")  # Reset UI after the conversation
                root.update()

    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
            pa.terminate()

# Run the main assistant loop in a separate thread
import threading
threading.Thread(target=Jmain, daemon=True).start()

# Start the Tkinter event loop
root.mainloop()
