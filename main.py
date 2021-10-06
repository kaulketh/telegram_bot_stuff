#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import RPi.GPIO as GPIO
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from fritzconnection import FritzConnection

from secrets import *
from simple_bot import SimpleBot

IDS = ANNIB, THK
ADMIN = THK
GROUP = DING_DONG_GROUP


# PIN = BELL_PIN
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(PIN, GPIO.IN)
#
#
# def __bell_is_ringing():
#     return False if GPIO.input(PIN) == 0 else True


def __trigger_call(number, wait):
    fc = FritzConnection(
        address=BOX_IP,
        user=BOX_USER,
        password=BOX_PASS,
    )

    sys.stdout.write(f"<< Call '{number}' via {fc.modelname}.\n")
    fc.call_action("X_VoIP1", "X_AVM-DE_DialNumber",
                   arguments={
                       "NewX_AVM-DE_PhoneNumber ": number})
    time.sleep(wait)
    fc.call_action("X_VoIP", "X_AVM-DE_DialHangup")


def __ding_dong(bot):
    """
    all actions to be performed should go in here
    """
    with ThreadPoolExecutor() as executor:
        executor.submit(bot.send, GROUP, DING_DONG)
        executor.submit(__trigger_call, FRITZ_APP_K, WAIT_TO_HANGUP)


def handle(bot):
    user = bot.user_id
    command = bot.text

    # check user
    if user not in IDS:
        bot.send(user, "Your ID is blocked!")
        bot.send(ADMIN, f"User '{user}' blocked.")
        return
    else:
        # TODO: commands and triggers
        if command == "ding dong":  # TODO: if __bell_is_ringing():
            __ding_dong(bot)
        else:
            bot.send(user, "Unknown or command not allowed!")
        return


if __name__ == '__main__':
    my_bot = SimpleBot(token=RING_BOT_TOKEN,
                       chat_id=THK,
                       handle_function=handle,
                       poll=.5)
