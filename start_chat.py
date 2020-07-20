#!/usr/bin/python

from client.chat import TestCmd, Commander
from threading import Thread

if __name__ == '__main__':

    try:
        test_cmd = TestCmd()
        c = Commander('MarkSix', cmd_cb=test_cmd)

        # Test asynch output -  e.g. comming from different thread
        import time

        def run():
            while True:
                time.sleep(1)
                while test_cmd.body:
                    output = test_cmd.body.pop(0)
                    c.output(output)
        t = Thread(target=run)
        t.daemon = True
        t.start()

        # start main loop
        c.loop()
    except KeyboardInterrupt:
        pass
