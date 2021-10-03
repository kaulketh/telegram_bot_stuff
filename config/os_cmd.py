#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

sudo_reboot = "sudo reboot"
curl_post = "curl -s -o /dev/nul/ -X  POST \"https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}\""
'''string format required: (bot token, chat id, message text)'''


class OsCmd:
    def __init__(self, cmd: str, *args):
        self.__cmd = cmd.format(*args) if args is not None else cmd
        os.system(self.__cmd)


if __name__ == '__main__':
    pass
