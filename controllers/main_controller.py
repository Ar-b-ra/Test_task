from controllers.resource_controller import ResourceController
from controllers.resource_type_controller import ResourceTypeController
from db.default_data_base import DatabaseController


class Controller:
    def __init__(self, data_base: DatabaseController):
        self._routes = {"/resources": ResourceTypeController(),
                        "/resources/id": ResourceController()}
        self.data_base = data_base

    def register_controller(self, url, controller):
        self._routes[url] = controller

    def resolve(self, url, method):
        callback = self._routes.get(url)
        if callback:
            callback.data_base = self.data_base
            methods = {
                "POST": callback.post,
                "GET": callback.get,
                "UPDATE": callback.update,
                "DELETE": callback.delete
            }
            return methods.get(method, self.default_controller)
        return self.default_controller

    def default_controller(self, *args, **kwargs):
        status = '404 Not Found'
        body = {}
        return status, body
