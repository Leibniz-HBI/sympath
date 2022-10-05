"""Main module for the sympath library"""

from collections.abc import Callable
from dataclasses import dataclass
from functools import reduce, singledispatchmethod
from typing import Any, Dict, List


@dataclass
class Map:
    """Map"""

    function: Callable

    @singledispatchmethod
    def apply(self, data):
        """applies the function to the input data"""
        raise NotImplementedError()

    @apply.register
    def _(self, data: dict):
        return {k: self.function(v) for k, v in data.items()}

    @apply.register
    def _(self, data: list):
        return [self.function(_) for _ in data]


@dataclass
class Reduce:
    """Reduce"""

    function: Callable

    def apply(self, data):
        """reduce adata item to a single item"""
        return reduce(self.function, data if isinstance(data, list) else data.values())


@dataclass
class ForEach:
    """For Each entry at this point do the chain after this"""

    sympath: "Sympath"

    def apply(self, data: List):
        """Apply the sub-Sympath to data"""
        return [self.sympath(_) for _ in data]


@dataclass
class Select:
    """Select and rename values"""

    def __init__(self, **kwargs) -> None:
        self.mapper = kwargs

    def apply(self, data: Dict):
        """applies the select to the input data"""
        return {k: data.get(v) for k, v in self.mapper.items()}

    def __repr__(self) -> str:
        return "select " + " ".join([f"{k}={v}" for k, v in self.mapper.items()])


class Sympath:
    """Sympathic indexing and destructuring"""

    def __init__(self) -> None:
        self.path = []

    def __getattr__(self, key):
        self.path.append(key)
        return self

    def __getitem__(self, key):
        self.path.append(key)
        return self

    def __call__(self, data) -> Any:
        def reducer(carry, key):

            if carry is not None:
                if isinstance(key, int):
                    return carry[key]
                if isinstance(key, str):
                    if key in carry:
                        return carry[key]
                if isinstance(key, (Map, Select, ForEach, Reduce)):
                    return key.apply(carry)
            return None

        return reduce(reducer, self.path, data)

    def __repr__(self) -> str:
        return f'<Sympath {" > ".join([str(_) for _ in self.path])}>'

    def map(self, func: Callable):
        """apply a function to every entry

        params:
          func: Callable
            Callback function that is passed each item

        returns:
          Whatever the data structure has or None
        """
        self.path.append(Map(func))
        return self

    def for_each(self, sympath):
        """apply a Sympath to every entry"""
        self.path.append(ForEach(sympath))
        return self

    def select(self, **kwargs):
        """Select/Rename keys"""
        self.path.append(Select(**kwargs))
        return self

    def reduce(self, func: Callable):
        """reduce the current items"""
        self.path.append(Reduce(func))
        return self
