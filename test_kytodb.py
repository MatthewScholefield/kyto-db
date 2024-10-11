import pytest
import tempfile
import uuid
from kytodb import KytoDbClient, IdModel


class MyModel(IdModel):
    name: str


@pytest.fixture
def temp_db():
    with tempfile.TemporaryDirectory() as temp_dir:
        client = KytoDbClient(temp_dir)
        yield client
        client.close()


@pytest.fixture
def collection(temp_db):
    return temp_db.collection(MyModel, 'test_collection')


def test_add_generates_id_and_stores(collection):
    obj = MyModel(name='Test Object')
    new_id = collection.add(obj)
    retrieved = collection.get(new_id)
    assert obj.id == new_id
    assert retrieved == obj


def test_add_raises_if_id_not_empty(collection):
    obj = MyModel(id='123', name='Test Object')
    with pytest.raises(ValueError):
        collection.add(obj)


def test_get_returns_object_if_found(collection):
    obj = MyModel(name='Test Object')
    new_id = collection.add(obj)
    retrieved = collection.get(new_id)
    assert retrieved == obj


def test_get_returns_none_if_not_found(collection):
    result = collection.get(str(uuid.uuid4()))
    assert result is None
