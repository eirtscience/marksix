

from flask import Flask, request, session
import jsonify
from producer.better import Emitter
import threading
import json
from objects.response import JsonResponse

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
emmitter = Emitter()


@app.route('/bet/', methods=['POST'])
def set_bet():
    try:
        post_data = request.get_json(force=True)
        betting_number = post_data.get("number")
        emmitter.betting_number = betting_number
        # betting_number=
        emmitter.validate()
        emmitter.emmit_bet()
        draw_data = emmitter.getData()
        session["betting_number"] = betting_number
        # print(draw_data)
        # print(type(draw_data))
        return json.dumps(draw_data)
    except Exception as ex:
        return JsonResponse.error(str(ex))


@app.route('/ticket/', defaults={"token": None}, methods=['GET'])
@app.route('/ticket/<token>', methods=['GET'])
def get_ticket(token=None):
    if token:
        emmitter.token = token
    draw_data = emmitter.emmit_draw()
    return json.dumps(draw_data)


@app.route('/draw/', defaults={"token": None}, methods=['GET'])
@app.route('/draw/<token>', methods=['GET'])
def get_draw(token=None):
    emmitter = Emitter()
    if token:
        emmitter.token = token
    draw_data = emmitter.emmit_list_draw()
    return json.dumps(draw_data)
