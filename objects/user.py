class User:

    def __init__(self):
        self.__token = None
        self.__betting_number = None
        self.__did_win = False

    def set_token(self, value):
        self.__token = value

    def getToken(self):
        return self.__token

    def set_betting_number(self, value):
        self.__betting_number = value

    def get_betting_number(self):
        return self.__betting_number

    def set_win(self, value):
        self.__did_win = value

    def did_win(self):
        return __did_win
