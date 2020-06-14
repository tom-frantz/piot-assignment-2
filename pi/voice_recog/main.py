"""
Main program of Admin voice recognition.

- External USB microphone required.
- Google service account credentials required.

`export GOOGLE_APPLICATION_CREDENTIALS = {KEY_FILE.json}`
"""

from voice_recog.menu import Menu
from voice_recog.voice import VoiceRecog
import sys

menu = Menu()
voice = VoiceRecog()
is_valid = menu.login()


if is_valid:
    while(voice.search_str==""):
        voice.recog()
    car_number = voice.search_str
    car_number = car_number.upper()
    menu.search(car_number)
    sys.exit(0)
    
    