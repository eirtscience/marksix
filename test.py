import unittest
from consumer.worker import DataManager, BettingManager
from web.server import app
from threading import Thread
from random import randint, sample
from producer.better import Emitter
import time
from faker import Faker


class Alltest(unittest.TestCase):

    def test_emmiter(self):

        betting_number = " ".join(map(str, sample(range(1, 49), 6)))

        emitter = Emitter(betting_number)

        self.assertEqual(betting_number, emitter.betting_number)


if __name__ == '__main__':
    unittest.main()
