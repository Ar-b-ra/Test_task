import unittest
from io import BytesIO

from request_handler import HTTPRequestHandler


class SimpleHTTPRequestHandlerTests(unittest.TestCase):
    def setUp(self):
        self.handler = HTTPRequestHandler()
        self.handler.requestline = "GET / HTTP/1.1\r\n"
        self.handler.client_address = ("127.0.0.1", 12345)
        self.handler.headers = {}

    def test_do_GET_positive(self):
        response = self.handler.do_GET()
        self.assertEqual(response, b"Received get request")

    def test_do_POST_positive(self):
        post_data = b'{"key": "value"}'
        self.handler.headers["Content-length"] = len(post_data)
        self.handler.rfile = BytesIO(post_data)
        response = self.handler.do_POST()
        self.assertEqual(response, b"Received post request:<br>{'key': 'value'}")

    def test_do_POST_negative(self):
        post_data = b'{"key": "value"'  # Invalid JSON
        self.handler.headers["Content-length"] = len(post_data)
        self.handler.rfile = BytesIO(post_data)
        response = self.handler.do_POST()
        self.assertEqual(response, b"")  # Expecting an empty response

    def test_do_PUT(self):
        self.handler.do_POST = lambda: b"PUT request handled"  # Mocking do_POST method
        response = self.handler.do_PUT()
        self.assertEqual(response, b"PUT request handled")


if __name__ == "__main__":
    unittest.main()
