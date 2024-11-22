import enum
from collections.abc import Sequence
from typing import Generic, TypeVar, List, Type
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, Indexed, init_beanie
from pymongo import MongoClient
from inrastructure.settings import database as database_settings
from bson.objectid import ObjectId

T = TypeVar("T")

class SavingType(enum.Enum):
    PLAIN = 1
    OBJECTS = 2


class BeanieAPI:

    def __init__(self):
        self.client = AsyncIOMotorClient(
            f"mongodb://{database_settings.MONGO_DB_USER}:"
            f"{database_settings.MONGO_DB_PASSWORD}@"
            f"{database_settings.MONGO_DB_DATABASE}:"
            f"{database_settings.MONGO_DB_PORT}")

    async def initialization(self, models: Sequence[Type[Document]]):
        await init_beanie(
            database=self.client.db_name,
            document_models=models
        )

    async def save(self, obj: Document)-> Document:
        await obj.insert()
        return obj

class RawMongoAPI:
    client = None
    db = None
    collection = None

    def __init__(self):
        self.client = MongoClient(
            f"mongodb://{database_settings.MONGO_DB_USER}:"
            f"{database_settings.MONGO_DB_PASSWORD}@"
            f"{database_settings.MONGO_DB_DATABASE}:"
            f"{database_settings.MONGO_DB_PORT}")

    def get_database(self, database_name: str):
        self.db = self.client[database_name]

    def get_collection(self, collection: str):
        self.collection = self.db[collection]

    def save(self, data: dict) -> ObjectId:
        return self.collection.insert_one(data).inserted_id

class MongoDbAPI:
    def __init__(
            self,
            doc_for_initialize: Sequence[Type[Document]] = None,
            database_name: str = None
    ):
        if doc_for_initialize is None and database_name is None:
            raise ValueError(
                "Set one of te parameters doc_for_initialize for beanie "
                "or database name for pymongo"
            )

        self.raw_pymongo_api = RawMongoAPI()
        self.raw_pymongo_api.get_database(database_name)
        self.beanie_api = BeanieAPI()
        self.beanie_api.initialization(doc_for_initialize)

    def _discover_saving_type(self, data) -> int:
        if isinstance(data, dict):
            return SavingType.PLAIN.value
        return SavingType.OBJECTS.value

    def _saving_raw_data(self, collection: str, data: Generic[T]) -> ObjectId:
        self.raw_pymongo_api.get_collection(collection)
        return self.raw_pymongo_api.save(data)

    def _saving_objects(self, data: Generic[T]) -> Generic[T]:
        return self.beanie_api.save(data)

    def save(self, data: Generic[T]):
        return {
            1: self._saving_raw_data,
            2: self._saving_objects
        }[self._discover_saving_type(data)](data)
