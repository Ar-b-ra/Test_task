import json
from http.server import BaseHTTPRequestHandler

from db.db_resources import ResourcesDataBaseManager
from logger import root_logger


class HTTPRequestHandler(BaseHTTPRequestHandler):
    db: ResourcesDataBaseManager = None

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        raw_json = post_body.decode("UTF-8")
        root_logger.info(raw_json)
        if raw_json:
            data = json.loads(raw_json)
            if self.path in ("/resources/id", "/resources/id/"):
                resource = str(self.db.get_resources(resource_name=data["name"]))
                self.wfile.write(resource.encode("UTF-8"))
            elif self.path in ("/resources/type", "/resources/type/"):
                resources = str(self.db.get_resources_by_type(resource_type=data["type"]))
                self.wfile.write(resources.encode("UTF-8"))
        if self.path in ("/resources", "/resources/"):
            resources = str(self.db.get_resources())
            self.wfile.write(resources.encode("UTF-8"))
        elif self.path in ("/resource_types", "/resource_types/"):
            resources_types = str(self.db.get_resource_types())
            self.wfile.write(resources_types.encode("UTF-8"))



    def do_POST(self):
        """Reads post request body"""
        self._set_headers()
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        raw_json = post_body.decode("UTF-8")
        root_logger.info(raw_json)
        if self.path in ("/resources", "/resources/"):
            if raw_json:
                data = json.loads(raw_json)
                self.db.create_resource_type(resource_name=data["type"], max_speed=data["max_speed"])
                self.wfile.write("Done!".encode("UTF-8"))
        elif self.path in ("/resources/id", "/resources/id/"):
            if raw_json:
                data = json.loads(raw_json)
                self.db.create_resource(resource_name=data["name"], resource_type=data["type"],
                                        current_speed=data["speed"])

    def do_PUT(self):
        self.do_POST()

    def do_DELETE(self):
        root_logger.debug("DELETE")
