from threading import Thread
from random import randint, sample
from producer.better import Emitter
import time
from subprocess import call
import os


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


def main():

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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
