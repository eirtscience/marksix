import socketserver
import time
import datetime
import threading
import sys
import os
import json
import uuid
from decimal import *
from modules.e_object import e_object
from modules.e_datetime import Timer
from modules.e_file import File
from modules.e_sock import e_sock
from modules.e_datetime import Timer
import struct
from random import sample
from objects.marksix import MarkSix
from objects.user import User

# initialize this global variable to handle the client data
data_queue = {
    "draw": {},
    "user": {},
    "draw_history": {}
}


class DataHandler(socketserver.BaseRequestHandler, e_object):
    """This class has been declare to handle the request send by the client
    """

    def client_data_send(self, to_object=False):
        # recieve all the byte data send by the client and save it into
        # the data variable object
        self.data = self.recvall(self.request, 1024)
        # Trasform the send data into requestData object
        if self.data != None:

            try:
                if to_object:
                    return requestData(**(json.loads(self.data.decode("utf-8"))))

                return json.loads(self.data.decode("utf-8"))

            except json.decoder.JSONDecodeError as ex:
                data = {"action": "None", "data": self.data.decode("utf-8")}
                return data

    def get_current_time(self):
        time_stamp = time.time()
        return datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

    def get_env(self, env_name):
        """Get the environment variable"""
        return os.environ[env_name]

    def handle_transaction_data(self, recieve_data):
        pass

    def __get_user_bet(self, betting_number, token):
        return {
            "betting_number": betting_number,
            "draw_status": "In progress",
            "token": token,
            "draw_id": BettingManager.CURRENT_DRAW_ID,
            "time_before_draw": data_queue["draw"][BettingManager.CURRENT_DRAW_ID]["time_elaspsed_before_draw"]
        }

    def handler_requester(self, request_data):

        is_save = False

        request_action = request_data.action

        token = request_data.token

        try:
            if request_data.action == "bet":
                betting_number = request_data.number
                #
                data_queue["user"][str(token)] = self.__get_user_bet(
                    betting_number, token)

                data_queue["draw"][BettingManager.CURRENT_DRAW_ID]["users"].append(
                    token)

                self.request.sendall(
                    (json.dumps(data_queue["user"][str(token)]).encode("utf-8")))

            if request_data.action == "draw":
                #
                user_data = data_queue["user"].get(str(token))

                if user_data["draw_status"] != "completed":
                    user_data["time_before_draw"] = data_queue["draw"][BettingManager.CURRENT_DRAW_ID]["time_elaspsed_before_draw"]
                else:
                    if user_data.get("time_before_draw"):
                        del user_data["time_before_draw"]
                # print(user_data)
                # print(data_queue["draw"])
                self.request.sendall((json.dumps(user_data)).encode("utf-8"))

            if request_data.action == "list_draw":
                if token:
                    data = {}
                    if data_queue["draw_history"].get(token):
                        data = data_queue["draw_history"].get(token)

                    return self.request.sendall((json.dumps(data)).encode("utf-8"))
                else:
                    return self.request.sendall((json.dumps(list(data_queue["draw_history"].values()))).encode("utf-8"))

            # self.request.sendall(
            #     (json.dumps({"message": "Recive the request", "status": "success"}).encode("utf-8")))

        except Exception as ex:
            print(ex)
            self.request.sendall(
                (json.dumps({"message": str(ex), "status": "failed"}).encode("utf-8")))
            # self.request.sendall((json.dumps({"Error_message":"There is an error proccesssing your request","status":"failed"}).encode("utf-8")))
        except KeyboardInterrupt:
            pass

    def handle(self):
        """The handle function get call every time a new client connect into
           the server socket
        """
        recieve_data = self.client_data_send(True)

        # print(data_queue["draw"])

        is_action_requested = False

        # print(recieve_data)

        if hasattr(recieve_data, "action"):
            is_action_requested = True

        if (is_action_requested):
            self.handler_requester(recieve_data)
        else:
            """In case the request number is invalid send
               an error message to the client.
            """
            self.request.sendall((json.dumps(
                {"Error_message": "An error has occured", "status": "failed"}).encode("utf-8")))

    def recvall(self, request, recv_byte):
        """This method help to wait and get all the send data from the connected
           client
        """
        # initialize the buffer object to a binary
        buf = b''

        # wait untill all the data send by the client was retrieve
        while recv_byte:
            # start getting the data send by the client
            data_recv = request.recv(recv_byte)

            # if case there is no data send by the client return none
            if not data_recv:
                return None

            # keep appending the recieve data into buf object
            buf += data_recv

            """remove the length of byte currently recieve from the
               total length of byte sent
            """
            recv_byte -= len(data_recv)

            # return the recieve data
            return buf
        return None


class requestData():
    """This class is use to store the data send by the client
       as class object data, a small reminder is the data has been send as a json
       format.Every json key represent the object key
    """

    def __init__(self, **entities):
        self.__dict__.update(entities)


class ThreadTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    """A void class that only inherite the ThreadingMixIn and socketserv.TCPServer
       class.
    """
    allow_reuse_address = True


class BettingManager:

    DRAW_SEC = 30
    COUNT_DRAW = 0
    CURRENT_DRAW_ID = None

    def __init__(self):
        self.timer = Timer()
        self.draw_id = None

    def check_draw_result(self):
        current_draw_id = BettingManager.CURRENT_DRAW_ID
        if current_draw_id:
            # print("Checking previous winner")
            # print(data_queue["draw"].get(current_draw_id))
            is_win = False
            if data_queue["draw"].get(current_draw_id) is not None:
                list_user = data_queue["draw"][current_draw_id].get(
                    "users")
                if list_user:
                    for user_token in list_user:
                        user = data_queue["user"][user_token]
                        if user:
                            if not is_win:
                                is_win = (
                                    user.get("betting_number") == data_queue["draw"][current_draw_id].get("mark_six"))
                                data_queue["user"][user_token]["win"] = is_win

                            data_queue["user"][user_token]["draw_status"] = "completed"

                for draw_id, draw_data in data_queue.get("draw").items():
                    draw_history = {}
                    if draw_data.get("mark_six"):
                        list_number = (
                            list(map(str, draw_data.get("mark_six"))))
                        draw_history["id"] = draw_id
                        draw_history["draw_number"] = "-".join(list_number)
                        draw_history["special_number"] = draw_data.get(
                            "special_number")
                        draw_history["date"] = draw_data.get(
                            "date")
                        draw_history["prize"] = "No winner"
                        if is_win:
                            draw_history["prize"] = "One winner"

                        data_queue["draw_history"][draw_id] = draw_history

                # print(data_queue["user"])

    def start(self):
        try:
            self.draw_id = e_object.gen_rand_str(15)
            print("Start new drawing with ID {}".format(self.draw_id))

            data_queue["draw"][self.draw_id] = {"users": []}

            result_thread = threading.Thread(target=self.check_draw_result)
            result_thread.start()

            BettingManager.CURRENT_DRAW_ID = self.draw_id
            self.timer.start_time()
            self.draw()
        except KeyboardInterrupt:
            pass
        except Exception:
            pass

    def draw(self):

        try:
            while True:
                time_in_sec = int(self.timer.diff_btwn_date_in_sec())
                time_elapse = BettingManager.DRAW_SEC - time_in_sec
                if time_elapse < 0:
                    break
                data_queue["draw"][self.draw_id]["time_elaspsed_before_draw"] = time_elapse
                if time_in_sec == BettingManager.DRAW_SEC:
                    draw_number = sample(range(1, 50), 7)
                    mark_six = draw_number[:6]
                    special_number = draw_number[6]
                    BettingManager.COUNT_DRAW += 1
                    data_queue["draw"][self.draw_id].update({
                        "mark_six": mark_six,
                        "special_number": special_number,
                        "date": Timer.str_now("%Y/%m/%d %H:%M")
                    })
                    break
                time.sleep(2)
            self.start()
        except KeyboardInterrupt:
            pass
        except Exception:
            pass


class DataManager(object):
    """Declare to run the current server.
    """
    @staticmethod
    def write_server_post(port):
        with open("modules/.port", "w") as f:
            f.writelines("{}".format(port))

    @staticmethod
    def server_thread(port=8089, host=""):
        try:
            """Static method use for starting the server thread.When called this
            method by the default the server will run on port 8084, but can be
            change to any port.And if the host leave empty it will use the current
            machine ip address to recieve a connection.
            """
            """Start the server ThreadTCPServer with the handler class
            This way the server will handle each client request
                in the separate thread process
            """
            DataManager.write_server_post(port)
            server = ThreadTCPServer((host, int(port)), DataHandler)

            # let us initialize the thread method with the THreadTCPServer
            # object
            server_thread = threading.Thread(target=server.serve_forever)
            # allow_reuse_address=True
            # here we go start the thread
            server_thread.start()

            betting_manager = BettingManager()
            betting_thread = threading.Thread(target=betting_manager.start)
            betting_thread.daemon = True
            betting_thread.start()

        except KeyboardInterrupt as ex:
            pass
        # except Exception as ex:
        #     print(ex)
