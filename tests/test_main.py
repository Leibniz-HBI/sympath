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
    test_input = {
        "nested": [
            {"key1": "Captain", "key2": "Picard"},
            {"key1": "Captain", "key2": "Picard"},
        ]
    }

    sydestructure = Sympath().nested.for_each(
        Sympath().select(name="key1", last_name="key2")
    )

    print(sydestructure)

    assert sydestructure(test_input) == [
        {"name": "Captain", "last_name": "Picard"},
        {"name": "Captain", "last_name": "Picard"},
    ]


def test_sympath_2a():
    """layout and test the steps of sympath"""
    test_input = None

    sydestructure = Sympath().nested.for_each(
        Sympath().select(name="key1", last_name="key2")
    )

    assert sydestructure(test_input) is None


def test_sympath_2b():
    """layout and test the steps of sympath"""
    test_input = {}

    sydestructure = Sympath().select(name="key1", last_name="key2")

    assert sydestructure(test_input) == {"name": None, "last_name": None}


def test_sympath_3():
    """layout and test the steps of sympath"""
    test_input = {"nested": {"key1": "Captain", "key2": "Picard"}}

    sydestructure = Sympath().nested.select(name="key1", last_name="key2")

    assert sydestructure(test_input) == {"name": "Captain", "last_name": "Picard"}


def test_list_indexing():
    """Test whether list indexing with ints goes according to plan"""
    test_input = {"nested": [{"hello": "World"}]}

    sym = Sympath().nested[0].hello

    assert sym(test_input) == "World"
