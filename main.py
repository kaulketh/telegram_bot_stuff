#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bot import SimpleBot
from config import *

if __name__ == '__main__':
    b = SimpleBot(RING_BOT_TOKEN, poll=.5)
    b.send(THK, "Test")
