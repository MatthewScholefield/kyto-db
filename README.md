# KytoDB

[![PyPI - Downloads](https://img.shields.io/pypi/dd/kytodb)](https://pypi.org/project/kytodb/)
[![PyPI - Version](https://img.shields.io/pypi/v/kytodb)](https://pypi.org/project/kytodb/)
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye.astral.sh)

*A simple, easy-to-use Pydantic embedded database library*

KytoDB is designed to provide a simple and easy-to-use persistence layer for Pydantic models. KytoDB leverages RocksDB as the underlying storage engine.

```python
from kytodb import KytoDbClient, IdModel

class User(IdModel):
    name: str
    email: str

client = KytoDbClient(db_path="app-database")
users = client.collection(User, "users")

new_user = User(name="John Doe", email="john.doe@example.com")
user_id = users.add(new_user)

retrieved_user = users.get(user_id)
print(retrieved_user)
```

## Installation

Install the library using pip:

```
pip install kytodb
```

## Development

KytoDB uses Rye for dependency management and the development workflow. To get started with development, ensure you have [Rye](https://github.com/astral-sh/rye) installed and then clone the repository and set up the environment:

```sh
git clone https://github.com/MatthewScholefield/fastapi-sse.git
cd fastapi-sse
rye sync
rye run pre-commit install

# Run tests
rye test
```
