"""Main module for the sympath library"""

from collections.abc import Callable
from dataclasses import dataclass
from functools import reduce, singledispatchmethod
from typing import Any, Dict


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
class ForEach:
    """For Each entry at this point do the chain after this"""


@dataclass
class Select:
    """Select and rename values"""

    def __init__(self, **kwargs) -> None:
        self.mapper = kwargs

    def apply(self, data: Dict):
        """applies the select to the input data"""
        return {k: data.get(v) for k, v in self.mapper.items()}


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

    def map(self, func):
        """apply a function to every entry"""
        self.path.append(Map(func))
        return self

    def for_each(self):
        """apply a Sympath to every entry"""
        self.path.append(ForEach())
        return self

    def select(self, **kwargs):
        """Select/Rename keys"""
        self.path.append(Select(**kwargs))
        return self

    def __call__(self, data) -> Any:
        def reducer(carry, key):

            print(key, carry)

            if carry is not None:
                if isinstance(key, (str, int)):
                    if key in carry:
                        return carry[key]
                if isinstance(key, Map):
                    return key.apply(carry)
                if isinstance(key, Select):
                    return key.apply(carry)
                if isinstance(key, ForEach):
                    pass
            return None

        return reduce(reducer, self.path, data)
