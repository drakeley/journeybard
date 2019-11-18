#!/usr/bin/env python

import json
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# FIXME: make this read from a json file
if __name__ == '__main__':
    reader = SimpleMFRC522()

    with open("keys.json") as f:
        keys = json.load(f)

    print(keys)

    for key in keys:
        try:
            print("Now place the tag for {} to write".format(key))
            reader.write(key)
            print("Wrote {} to tag.".format(key))
        finally:
            GPIO.cleanup()
