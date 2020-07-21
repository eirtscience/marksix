import json


class JsonResponse:

    @staticmethod
    def send(data):
        return json.dumps(data).encode("utf-8")

    @staticmethod
    def recieve(data):
        return json.loads(data.decode("utf-8"))

    @staticmethod
    def error(message):
        return json.dumps({"message": message, "success": "false"})
