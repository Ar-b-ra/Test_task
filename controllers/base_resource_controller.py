from abc import ABC, abstractmethod

from db.resource_database_manager import ResourcesDataBaseManager


class BaseResourceController(ABC):
    data_base: ResourcesDataBaseManager

    @abstractmethod
    def post(cls, prepared_json):
        return 400, "error"

    @abstractmethod
    def get(self, prepared_json):
        return 400, "error"

    @abstractmethod
    def update(self, prepared_json):
        return 400, "error"

    @abstractmethod
    def delete(self, prepared_json):
        return 400, "error"
