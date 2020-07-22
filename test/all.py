from unittest import TestCase
from consumer.worker import DataManager, BettingManager
from web.server import app
from modules.e_sock import e_sock
from threading import Thread
from random import randint, sample
from producer.better import Emitter
import time
from faker import Faker


class Alltest(TestCase):

    def test_emmiter(self):
        pass
