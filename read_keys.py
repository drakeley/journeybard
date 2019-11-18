#!/usr/bin/env python

import json
import RPi.GPIO as GPIO
import random
import subprocess
import time
from mfrc522 import SimpleMFRC522

def random_welcome(bg_pid):
    with open("messages.json") as m:
        messages = json.load(m)
    rand_welcome = random.randint(0, len(messages["welcome"]) - 1)
    print("\n~=~=~=~=~=~=~=\n{}\n".format(messages["welcome"][rand_welcome]))
    bg_pid.kill()
    return subprocess.Popen(["mpg123", "audio/messages/welcome{}.mp3".format(rand_welcome)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def play_background():
    with open("background_music.json") as b:
        bg_music = json.load(b)

    filename = random.choice(bg_music.keys())
    # Call out to OS to play the audio in a new process
    return subprocess.Popen(["mpg123", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    reader = SimpleMFRC522()

    welcomed = False

    # Fixme: do this in a separate thread
    bg_pid = play_background()

    while True:
        if not welcomed:
            rw_pid = random_welcome(bg_pid)
            welcomed = True
        try:
            id, text = reader.read()
            print(id)
            print("Ah, the {} has returned. Do tell us of your journey.".format(text.strip()))
            welcomed = False
        except KeyboardInterrupt:
            print("Goodbye!")
            GPIO.cleanup()
            exit()
        except Exception as e:
            print("Unfortunately, we cannot hear the tale of {} at the moment".format(text.strip()))
            welcomed = False
        time.sleep(3)
