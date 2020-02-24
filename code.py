import time

import displayio
from adafruit_pybadger import pybadger

from states import StateManager, DefaultMenuItemState, MainMenu, State
from util import ALL_COLORS, generate_qr_code_display_group, set_splash_screen
from collections import namedtuple


# These are constants, try changing them and saving the file!
NAME = "Pythonista"
NAME_BADGE_COLORS = ALL_COLORS
URL = "https://aka.ms/pycon2020"
LED_BRIGHTNESS = 0.1
pybadger.pixels.brightness = LED_BRIGHTNESS


class PressStart(State):

    label = "Main Screen"

    def display(self):
        set_splash_screen(image="images/initial.bmp", text="press start to begin")

    def handle_event(self):
        if pybadger.button.start:
            state_manager.state = MainMenu
        elif pybadger.button.a and pybadger.button.b:
            state_manager.state = EasterEgg


class Credits(DefaultMenuItemState):

    label = "Credits"

    def display(self):
        set_splash_screen(image="images/credits.bmp")


class NameBadge(DefaultMenuItemState):

    label = "Name Badge"

    led_on = True

    def display(self):
        self.led_color = NAME_BADGE_COLORS[self.current_index % len(NAME_BADGE_COLORS)]
        pybadger.show_badge(
            name_string=NAME,
            background_color=self.led_color,
            hello_scale=2,
            my_name_is_scale=2,
            name_scale=2,
        )


class QrCode(DefaultMenuItemState):

    label = "Learn More"

    def __init__(self):
        self.qr_group = generate_qr_code_display_group(URL)
        super().__init__()

    def display(self):
        pybadger.display.show(self.qr_group)


class SocialBattery(DefaultMenuItemState):

    label = "Social Battery Status"

    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)

    SocialState = namedtuple("SocialState", ["color", "image"])
    states = [
        SocialState(color=RED, image="images/social_battery/empty.bmp"),
        SocialState(color=YELLOW, image="images/social_battery/low.bmp"),
        SocialState(color=GREEN, image="images/social_battery/full.bmp"),
    ]

    led_on = True

    def display(self):
        social_state = self.states[self.current_index % len(self.states)]
        set_splash_screen(image=social_state.image)
        self.led_color = social_state.color


class EasterEgg(State):

    label = "Easter Egg"

    def display(self):
        set_splash_screen(image="images/easter_egg/easter_egg.bmp")
        time.sleep(4.0)  # Wait 4 seconds, then return to main state_manager.
        state_manager.previous_state()


main_menu = MainMenu(NameBadge, SocialBattery, QrCode, Credits, PressStart)

state_manager = StateManager()
state_manager.add(
    main_menu,
    PressStart(),
    Credits(),
    NameBadge(),
    QrCode(),
    SocialBattery(),
    EasterEgg(),
)
state_manager.state = PressStart

while True:
    state_manager.check_for_event()
    time.sleep(0.15)  # Debounce
