#!/usr/bin/python3
# -*- coding: utf-8 -*-

from secrets import *
from simple_bot import SimpleBot

USERS = ANNIB, THK
ADMIN = THK
GROUP = RING_RING_GROUP


class RingBot:

    def __init__(self, token=RING_BOT_TOKEN, admin=THK, clients=USERS, chat_group=RING_RING_GROUP):
        self.__token = token
        self.__admin = admin
        self.__ids = clients
        self.__group = chat_group
        self.__bot = SimpleBot(self.__token, self.__admin, poll=0.5)

        self.__commands = ("/start", "/stop", "/reboot")
        while True:
            self.handle()

    def trigger(self):
        # GPIO read stuff here
        return "ding dong"

    def handle(self):
        user = self.__bot.user_id
        command = self.__bot.text
        # check user
        if user not in self.__ids:
            self.__bot.send(user, "You are blocked!")
            return
        if command == "ding dong":
            self.__bot.send(self.__group, "hat jeklingelt")
            return
        elif any(c for c in self.__commands if (command == c)):
            # start
            if command == self.__commands[0]:
                pass
            # stop
            elif command == self.__commands[1]:
                pass
            # reboot
            elif command == self.__commands[0]:
                pass
            else:
                self.__bot.send(user, "Wrong command!")
                return
        else:
            return


if __name__ == '__main__':
    RingBot()
