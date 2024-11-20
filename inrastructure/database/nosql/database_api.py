import enum
from collections.abc import Sequence
from typing import Generic, TypeVar, List, Type
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, Indexed, init_beanie
from pymongo import MongoClient


T = TypeVar("T")

class SavingType(enum.Enum):
    PLAIN = 1
    OBJECTS = 2


class BeanieAPI:

    def __init__(self):
        self.client = AsyncIOMotorClient(f"mongodb://user:pass@host:27017")

    async def initialization(self, models: Sequence[Type[Document]]):
        await init_beanie(
            database=self.client.db_name,
            document_models=models
        )

    async def save(self, obj: Document):
        await obj.insert()


class RawMongoAPI:
    client = None
    db = None
    collection = None

    def __init__(self):
        self.client = MongoClient(f"mongodb://user:pass@host:27017")

    def get_database(self, database_name: str):
        self.db = self.client[database_name]

    def get_collection(self, collection: str):
        self.collection = self.db[collection]

class MongoDbAPI:

    def __init__(self):
        pass

    def _discover_saving_type(self, data) -> int:
        if isinstance(data, dict):
            return SavingType.PLAIN.value
        return SavingType.OBJECTS.value


    def _saving_raw_data(self, data: Generic[T]):
        pass


    def _saving_objects(self, data: Generic[T]):
        pass

    def save(self, data: Generic[T]):
        {
            1: self._saving_raw_data,
            2: self._saving_objects
        }[self._discover_saving_type(data)](data)
