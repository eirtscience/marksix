

class Draw:

    def __init__(self):
        self.__status = None
        self.__id = None
        self.__number = []
        self.__special_number = None

    def set_status(self, value):
        self.__status = value

    def get_status(self):
        return self.__status

    def set_id(self, value):
        self.__id = value

    def get_id(self):
        return self.__id

    def set_draw_number(self, value):
        self.__number = value

    def get_draw_number(self):
        return self.__number


class MarkSix(Draw):

    def __init__(self):
        pass
