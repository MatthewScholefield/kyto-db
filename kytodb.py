from os import PathLike
from pydantic import BaseModel, Field
import uuid
from typing import Type, TypeVar, Generic, Optional
import rocksdbpy


class IdModel(BaseModel):
    id: str = Field(default='')


T = TypeVar('T', bound=IdModel)


class KytoDbCollection(Generic[T]):
    def __init__(self, db: rocksdbpy.RocksDB, model: Type[T], collection_name: str):
        self.db = db
        self.model = model
        self.collection_name = collection_name

    def add(self, obj: T) -> str:
        if not obj.id:
            obj.id = str(uuid.uuid4())
        key = self._construct_key(obj.id)
        value = obj.model_dump_json().encode('utf-8')
        self.db.set(key, value)
        return obj.id

    def get(self, obj_id: str) -> Optional[T]:
        key = self._construct_key(obj_id)
        value = self.db.get(key)
        if value is not None:
            return self.model.model_validate_json(value)
        return None

    def update(self, obj: T):
        if obj.id == '':
            raise ValueError('ID must not be empty during update')
        key = self._construct_key(obj.id)
        value = obj.model_dump_json().encode('utf-8')
        self.db.set(key, value)

    def _construct_key(self, obj_id: str) -> bytes:
        return f'{self.collection_name}:{self.model.__name__}:{obj_id}'.encode('utf-8')


class KytoDbClient:
    def __init__(self, db_path: str | PathLike[str]):
        opts = rocksdbpy.Option()
        opts.create_if_missing(True)

        self.db = rocksdbpy.open(str(db_path), opts)

    def collection(self, model: Type[T], collection_name: str) -> KytoDbCollection[T]:
        return KytoDbCollection(self.db, model, collection_name)

    def close(self):
        self.db.close()
