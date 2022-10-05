""" Test suite for sympath.main
"""

from sympath import Sympath


def test_sympath_1():
    """layout and test the steps of sympath"""
    test_input = {"nested": [1, 2, 3, 4]}

    symath = Sympath().nested.map(lambda x: x + 1)

    assert symath(test_input) == [2, 3, 4, 5]


def test_sympath_2():
    """layout and test the steps of sympath"""
    test_input = {"nested": [{"key1": "Captain", "key2": "Picard"}]}

    sydestructure = Sympath().nested.for_each().select(name="key1", last_name="key2")

    assert sydestructure(test_input) == [{"name": "Captain", "last_name": "Picard"}]


def test_sympath_3():
    """layout and test the steps of sympath"""
    test_input = {"nested": {"key1": "Captain", "key2": "Picard"}}

    sydestructure = Sympath().nested.select(name="key1", last_name="key2")

    assert sydestructure(test_input) == {"name": "Captain", "last_name": "Picard"}