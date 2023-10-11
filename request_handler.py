import json
from http.server import BaseHTTPRequestHandler

from logger import root_logger


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(b"Received get request")

    def do_POST(self):
        """Reads post request body"""
        self._set_headers()
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        root_logger.info(post_body.decode("UTF-8"))
        data = json.loads(str(post_body.decode("UTF-8")))
        self.wfile.write(f"Received post request:<br>{data}".encode("UTF-8"))

    def do_PUT(self):
        self.do_POST()

    def do_DELETE(self):
        root_logger.debug("DELETE")
