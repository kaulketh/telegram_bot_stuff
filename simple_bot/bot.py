#!/usr/bin/python3
# -*- coding: utf-8 -*-
import concurrent.futures
import json
import multiprocessing
import sys
from time import sleep

from secrets import THK
from .os_cmd import OsCmd, curl_updates, curl_send


class SimpleBot:

    def __init__(self, token, poll=5.0):
        self.__admin = THK
        sys.stdout.write(
            f"Initialize instance of {self.__class__.__name__}.\n")
        self.__token = token
        self.__update_poll = poll
        self.__result = None
        self.__msg_text = None
        self.__msg = None
        self.__from = None
        self.__from_id = None
        self.__msg_id = 0
        self.__msg_storage = 0
        self.__loop = None
        self.run()

    def __get_update(self):
        # helper
        def read(update, key):
            def found(_d: dict, _key: str):
                for _k, _v in _d.items():
                    if _k == _key:
                        yield _v
                    elif isinstance(_v, dict):
                        for _val in found(_v, _key):
                            yield _val

            for k in found(update, key):
                return k

        # cUrl
        response = OsCmd(curl_updates, self.__token).out()

        # decode all results from byte
        response = json.loads(
            response.decode('utf-8').replace("'", '"'))

        # get last of the returned results
        self.__result = read(response, "result")[-1]
        # extract text from last result
        self.__msg_text = read(self.__result, "text")
        # extract content parts
        self.__msg = read(self.__result, "message")
        self.__msg_id = read(self.__result, "message_id")
        self.__from = read(self.__msg, "from")
        self.__from_id = read(self.__from, "id")
        return self.__result, self.__msg_text, self.__msg, \
               self.__from, self.__from_id, self.__msg_id

    @property
    def __update(self):
        """
        Since Python >3.2, the stdlib- concurrent.futures module provides a
        higher-level API for threading, including passing return values or
        exceptions from a worker thread to the main thread:
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.submit(self.__get_update).result()
            return results

    @__update.setter
    def __update(self, results):
        # noinspection LongLine
        self.__result, self.__msg_text, self.__msg, self.__from, self.__from_id, self.__msg_id = results

    @property
    def result(self):
        return self.__update[0]

    @property
    def text(self):
        return self.__update[1]

    @property
    def message(self):
        return self.__update[2]

    @property
    def user(self):
        return dict(self.__update[3])

    @property
    def user_id(self):
        return self.__update[4]

    @property
    def message_id(self):
        return self.__update[5]

    def _loop(self):
        while True:
            # update
            self.__update = self.__update
            # if initial
            if self.__msg_storage == 0:
                self.__msg_storage = self.__msg_id
            # check for new message
            if self.__msg_id == self.__msg_storage:
                continue
            else:
                # store last msg id
                self.__msg_storage = self.__msg_id
                if self.__msg_text is not None:
                    sys.stdout.write(
                        f"Got new message: {self.__msg_storage} "
                        f"'{self.__msg_text}' from {self.__from_id}.\n")
                else:
                    # TODO: type exception!?
                    # ignore other then text
                    sys.stderr.write("Wrong content type!\n")
                    self.send(self.user_id, "WTF ????")
                    continue
            sleep(self.__update_poll)

    def stop(self):
        if self.__loop is not None:
            if self.__loop.is_alive():
                self.__loop.terminate()
        self.send(self.__admin, "Bot stopped.")
        del self
        sys.stdout.write("Bot stopped.")

    def run(self):
        self.__loop = multiprocessing.Process(target=self._loop, name="Loop")
        try:
            self.__loop.start()
            sys.stdout.write(
                f"Bot is running... "
                f"API polling every {self.__update_poll} second(s)\n")
        except KeyboardInterrupt:
            sys.stderr.write(f"Program interrupted\n")
            self.__loop.terminate()
            exit()
        except Exception as e:
            sys.stderr.write(f"An error occurred: {e}\n")
            self.__loop.terminate()
            exit()

    def send(self, chat_id, text):
        OsCmd(curl_send, self.__token, chat_id, text)
        sys.stdout.write(f"Sent '{text}' to {chat_id}\n")


if __name__ == '__main__':
    pass
