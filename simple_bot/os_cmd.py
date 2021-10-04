#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess
import sys

sudo_reboot = "sudo reboot"
curl_send = "curl -s -o /dev/nul/ -X  POST \"https://api.telegram.org/bot{}/" \
            "sendMessage?chat_id={}&text={}\""
'''string format required: (bot token, chat id, message text)'''

curl_updates = "curl -s -X POST \"https://api.telegram.org/bot{}/getUpdates\""
'''string format required: bot token'''


class OsCmd:
    def __init__(self, cmd: str, *args):
        try:
            self.__cmd = cmd.format(*args) if args is not None else cmd
            proc = subprocess.Popen(self.__cmd, stdout=subprocess.PIPE)
            self.__out = proc.communicate()[0]
        except Exception as e:
            sys.stderr.write(f"An error occurred: {e}\n")
            exit()

    def out(self):
        return self.__out


if __name__ == '__main__':
    pass
