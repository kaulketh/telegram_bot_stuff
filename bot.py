#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
import time
from multiprocessing import Process

from config import OsCmd, curl_updates, curl_send


class SimpleBot:

    def __init__(self, token, poll=5.0):
        sys.stdout.write(
            f"Initialize instance of {self.__class__.__name__}.\n")

        self.__token = token
        self.__update_poll = poll

        self.__update = None
        self.__msg_text = None
        self.__last_result = None
        self.__msg_text = None
        self.__last_message = None
        self.__from = None
        self.__from_id = None
        self.__last_msg_id = 0
        self.__msg_storage = 0

        self.__run()

    def _get_updates(self):
        while True:
            self.__update = OsCmd(curl_updates, self.__token).out()
            # decode all results from byte
            self.__update = json.loads(
                self.__update.decode('utf-8').replace("'", '"'))
            # get last of the returned results
            self.__last_result = self.__read(self.__update, "result")[-1]
            # extract content parts
            self.__last_message = self.__read(self.__last_result, "message")
            self.__last_msg_id = self.__read(self.__last_result, "message_id")
            if self.__msg_storage == 0:
                self.__msg_storage = self.__last_msg_id
            self.__last_from = self.__read(self.__last_message, "from")
            self.__from_id = self.__read(self.__last_from, "id")
            # check for new message
            if self.__last_msg_id == self.__msg_storage:
                continue
            else:
                self.__msg_storage = self.__last_msg_id
                # extract text from last result
                read = self.__read(self.__last_result, "text")
                if read is not None:
                    self.__msg_text = read
                    sys.stdout.write(
                        f"Got new message {self.__msg_storage} "
                        f"'{self.__msg_text}' from {self.__from_id}.\n")
                else:
                    # ignore other then text
                    self.send(self.__from_id, "????")
                    sys.stderr.write("Wrong content type!\n")
                    # TODO: type exception!?
                    continue
            time.sleep(self.__update_poll)

    @staticmethod
    def __read(update, key):

        def found(_d: dict, _key: str):
            for _k, _v in _d.items():
                if _k == _key:
                    yield _v
                elif isinstance(_v, dict):
                    for _val in found(_v, _key):
                        yield _val

        for k in found(update, key):
            return k

    def __run(self):
        try:
            self.__checker = Process(target=self._get_updates)
            self.__checker.start()
            sys.stdout.write(
                f"Bot is running... "
                f"API polling every {self.__update_poll} second(s)\n")
        except KeyboardInterrupt:
            sys.stderr.write(f"Program interrupted\n")
            self.__checker.terminate()
            exit()
        except Exception as e:
            sys.stderr.write(f"An error occurred: {e}\n")
            self.__checker.terminate()
            exit()

    def send(self, chat_id, text):
        OsCmd(curl_send, self.__token, chat_id, text)
        sys.stdout.write(f"Sent '{text}' to {chat_id}\n")

    @property
    def text(self):
        return self.__msg_text

    @property
    def update(self):
        return self.__update

    @update.setter
    def update(self, u):
        self.__update = u


if __name__ == '__main__':
    pass
