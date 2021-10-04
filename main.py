#!/usr/bin/python3
# -*- coding: utf-8 -*-

from secrets import *
from simple_bot import SimpleBot

if __name__ == '__main__':
    b = SimpleBot(RING_BOT_TOKEN, poll=0.5)
