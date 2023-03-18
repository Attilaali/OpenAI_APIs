# clients
import unittest
from src.openai_client import Chat_Bot_Client


class TestDemo(unittest.TestCase):
    """
       Demo test to be replaced :)
    """

    client = Chat_Bot_Client(api_key="TEST")

    def test_demo(self):
        """
        Test demo
        """

        assert self.client != None