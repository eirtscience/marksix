from modules.e_sock import e_sock
from modules.e_object import e_object
from modules.e_file import File
from modules.e_array import e_array
import logging
import os

import threading
import time


class User:
    def __init__(self):
        self.token = None

    def set_token(self, token):
        self.token = token


class Reciever(User):

    def __init__(self):
        User.__init__(self)


class Sender(User, e_object):

    reciever = Reciever()

    def __init__(self, betting_number=None, action=None):
        User.__init__(self)
        self.number = betting_number
        self.action = action
        self.token = e_object.gen_rand_str(11)

    def generate_transation_data(self):
        """Generate the transaction data"""
        # token =

        transaction_data = {
            "token": self.token,
            "action": self.action,
            "number": self.number
        }

        return transaction_data

    def transfer(self):
        return self.generate_transation_data()


class Emitter:

    def __init__(self, betting_number=None, token=None):
        self.betting_number = betting_number
        self.token = token
        self.clientsocket = None

    def emmit_bet(self):

        self.clientsocket = e_sock()

        is_connect = self.clientsocket.connect()

        sender = Sender(self.betting_number, "bet")

        self.token = sender.token

        transfer_data = sender.transfer()

        if(is_connect):

            self.clientsocket.set_data(transfer_data)

            self.clientsocket.sendall("json")

        # self.clientsocket.close()

        return self.token

    def emmit_draw(self):

        clientsocket = e_sock()

        is_connect = clientsocket.connect()

        sender = Sender(action="draw")

        sender.token = self.token

        transfer_data = sender.transfer()

        if(is_connect):

            clientsocket.set_data(transfer_data)

            clientsocket.sendall("json")
            # clientsocket.close()

        return clientsocket.getall(data_type="json")

    def getData(self):
        return self.clientsocket.getall(data_type="json")


# def start_transaction(transaction_delay):

#     try:
#         print("Start the stream client")

#         while True:
#             for card_holder in list_card_holder:
#                 name = card_holder["sender_name"]
#                 card_number = str(card_holder["card_number"])
#                 if len(card_number) == 0:
#                     card_number = e_object.gen_rand_int(16)
#                     card_holder["card_number"] = card_number
#                 emmitter = Emitter(card_number, name)
#                 trans_thread = threading.Thread(
#                     name=name, target=emmitter.emmit_trans)
#                 trans_thread.start()
#                 time.sleep(transaction_delay)
#             time.sleep(transaction_delay)
#     except KeyboardInterrupt as ex:
#         pass


# start_transaction(2)
