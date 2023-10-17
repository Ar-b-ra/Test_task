from controllers.resource_controller import ResourceController
from controllers.resource_type_controller import ResourceTypeController


class Router:
    def __init__(self):
        self._routs = {"/resources": ResourceTypeController,
                       "/resources/id": ResourceController}

    def register_controller(self, url, controller):
        self._routs[url] = controller

    def resolve(self, url, method):
        callback = self._routs.get(url)
        if callback:
            return callback
        return self.default_controller

    def default_controller(self, *args, **kwargs):
        status = '404 Not Found'
        body = b''
        return status, body