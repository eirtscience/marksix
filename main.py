#!/usr/bin/python

import sys
import os
import argparse
from consumer.worker import DataManager, BettingManager
from web.server import app
from modules.e_sock import e_sock
from threading import Thread
from random import randint, sample
from producer.better import Emitter
import time
from subprocess import call
from chat.chat import TestCmd, Commander


def consumer(port, draw):
    """Use as the main  start up of running the program.Just write anything here
    """
    try:
        """
        There is only one thing you can do to start the server
        you can call the class method server_thread on the class
        DataServer with argument or not.If no argument has been pass
        the server will use the current ipaddress with 8084 as the
        port number by default.
        """
        server_info = """
Running on 0.0.0.0:{} (Press CTRL+C to quit)
Draw Time Interval: {}
        """.format(port, draw)

        BettingManager.DRAW_SEC = int(draw)
        DataManager.server_thread(int(port), "")

        print(server_info)
        # raise Exception("Server stop intantly")
    except OSError as ex:
        print(ex)


def draw():
    betting_number = "-".join(map(str, sample(range(1, 50), 6)))
    emitter = Emitter(betting_number=betting_number)
    token = emitter.token
    emitter.emmit_bet()
    data = emitter.emmit_draw()
    # print(data)
    emitter.show_draw(data)
    while True:
        if emitter:
            data = emitter.emmit_draw()
            if data.get("draw_status") == "completed":
                break
        time.sleep(5)
    emitter.show_draw(data)


def clear():
    # check and make call for specific operating system
    _ = call('clear' if os.name == 'posix' else 'cls')


def automatic():

    while True:
        clear()
        number_of_client = randint(1, 5)

        info = """
                            SIMULATE {} USER(s)
        """.format(number_of_client)

        print(info)

        for index in range(number_of_client):

            try:
                client_bet_thread = Thread(target=draw)
                client_bet_thread.start()
            except KeyboardInterrupt:
                pass
            except Exception:
                pass
        time.sleep(30)


def chat():
    try:
        test_cmd = TestCmd()
        c = Commander('MarkSix', cmd_cb=test_cmd)
        import time

        def run():
            while True:
                time.sleep(1)
                while test_cmd.body:
                    output = test_cmd.body.pop(0)
                    c.output(output)

                while test_cmd.error:
                    output = test_cmd.error.pop(0)
                    c.output(output, "error")

        t = Thread(target=run)
        t.daemon = True
        t.start()

        # start main loop
        c.loop()
    except KeyboardInterrupt:
        pass


# check if the command line file called is the main file
if __name__ == "__main__":

    # waiting for the keyboardInterrupt action issue by the user
    try:
        # called to start the program
        parser = argparse.ArgumentParser()

        parser.add_argument('app', metavar='N', type=str,
                            help='an integer for the accumulator')

        list_argument = {
            '--port': 'Port to use for the server',
            '--draw': 'Time slot for drawing',
            '--bport': 'Port to use for the betting server',
            '--bhost': 'Hostname to use for the betting server'
        }

        for key, value in list_argument.items():
            parser.add_argument(key, nargs='?', help=value)

        # parser.add_argument('--port', nargs='?',
        #                     help='Port to use for the server')

        # parser.add_argument('--draw', nargs='?',
        #                     help='Time slot for drawing')

        # parser.add_argument('--bport', nargs='?',
        #                     help='Port to use for the betting server')

        # parser.add_argument('--bhost', nargs='?',
        #                     help='Hostname to use for the betting server')

        args = parser.parse_args()

        if args.app == "consumer":
            consumer(args.port or 8089, args.draw or 30)
        elif args.app == "web":
            e_sock.HOSTNAME = args.bhost
            e_sock.PORT = args.bport
            app.run(host='0.0.0.0', port=args.port or 5000, debug=True)
        elif args.app == "auto":
            automatic()
        elif args.app == "chat":
            chat()

    except KeyboardInterrupt:
        """if the program catch any key that request an interrupt
           immediate of the program.Print this message to the user.
        """
        print("\nOperation cancel by the user")
        try:
            sys.exit(0)
        except SystemExit as ex:
            print(ex)
            os._exit(0)
