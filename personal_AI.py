# Developed by Mohammed Ali Ansar
# Used python 3.8.5
# Mac OS Cataline version 10.15.7

import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
import requests, json
import pyttsx3
import smtplib, ssl
import wikipedia
import subprocess
import config

#pyttsx3 is a python text to speech libary

try:
    engine = pyttsx3.init()
except ImportError:
    print("libary not found or imported wrong")
except RuntimeError:
    print("libary not working due to driver error")

# Test the python text to speech and define the engine
# set fail safes for troublshooting

converter = pyttsx3.init()
# converter for a voice changer
# change the volume, pace etc 

# to get the available voices uncomment this
voices = engine.getProperty("voices")
for voice in voices:
#    print("Voice:") 
 #   print("ID: %s" %voice.id) 
  #  print("Name: %s" %voice.name) 
   # print("Age: %s" %voice.age) 
    #print("Gender: %s" %voice.gender)   
    #print("Languages Known: %s" %voice.languages)

    voice_id = "com.apple.speech.synthesis.voice.Victoria"
# from the list provided copy and paste the voice id

converter.setProperty('voice', voice_id)
converter.runAndWait
# setting the converter to use the voice id 
# wait untill the function is called 

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        audio = r.listen(source) # sets the script to listen for a voice
    data = "" # what you say in the mic 
    try:
        data = r.recognize_google(audio) # translates using google tts
        print("You said: " + data)
    except sr.UnknownValueError:        
        print("Google Speech Recognition did not understand audio")
        engine.say('I did not understand what you said')
        engine.runAndWait() # instead of printing. it can speak
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
    return data

# listen using the laptop mic as input
# set failsafe for it 

def respond(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')

# define the respond function
# setting the script to respond

def digital_assistant(data):
    if "how's life" in data:
        listening = True
        respond('I am okay')
        engine.say('I am well')
        engine.runAndWait()
# it listens for whatever is in the if statement
# it using this script to respond back

    if "time" in data:
        listening = True
        respond(ctime())
        engine.say(ctime())
        engine.runAndWait()
# using the libary time check the time on your device
# respond prints in the command line and engine speaks
        
    if "message me" in data:
        listening = True
        data = data.split(' ')
        def send_email(subject, msg):
            try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login(config.EMAIL_ADDRESS, config.PASSWORD)
                message = 'Subject: #{}\n\n{}'.format(subject, msg)
                server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, message)
                server. quit()
                print("Sucessfully quit")
            except:
                print("Email failed to send")

        subject = "Test Subject"
        msg = data
    
        send_email(subject, msg)


    if "where is" in data:
        listening = True
        data = data.split(" ")
        location_url = "https://www.google.com/maps/place/" + str(data[2])
        respond("Hold on Ali, I will show you where " + data[2] + " is.")
        maps_arg = '/usr/bin/open -a "/Applications/Google Chrome.app" ' + location_url
        os.system(maps_arg)

# search google maps for what you say

    if "wikipedia" in data:
        listening = True
        data = data.split(' ')
        wiki = '/usr/bin/open -a "/Applications/Google Chrome.app"'

# search wikipedia for what you say    

    if 'quiz time' in data:
        listening = True
        data = data.split(' ')
        quiz = '/usr/bin/open -a "/Applications/Discord.app" '
        os.system(quiz)

# open discord and open the last server
        
    if "stop listening" in data:
        listening = False
        print('Listening stopped')
        return listening
    return listening

# if you say stop listening it turns off  

time.sleep(2)
respond("Hi Ali what can I do for you ?")
engine.say('Hi Ali what can I do for you ?')
engine.runAndWait()
listening = True
while listening == True:
    data = listen()
    listening = digital_assistant(data)

# listens to the data and responds with the required output
