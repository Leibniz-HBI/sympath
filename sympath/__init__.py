"""Sympath

Processing nested data structure with ease

## Usage

```python
a = {
        "nested": {
            "key1": "Captain",
            "key2": "Picard"
        }
    }

b = {
    "nested": {
        "key1": "Venetian",
        "key2": "Trobones",
        "key3": "Really"
    }
}

sydestructure = Sympath().nested.select(name="key1", last_name="key2")

sydestructure(a)
>>> {"name": "Captain", "last_name": "Picard"}

sydestructure(b)
>>> {"name": "Venetian", "last_name": "Trombone"}
```


## Developer Installation

1. Install `poetry` if you don't have it: `pipx install poetry`.
2. Clone this repo, go into the repo's folder.
3. Install the dependencies with `poetry install` and
   spawn a shell in your new virtual environment with `poetry shell`.
4. To run tests type `pytest`.

---

[Philipp Kessling](mailto:p.kessling@leibniz-hbi.de) under the MIT license, 2022.

"""

from .main import Sympath
