import typing
from dataclasses import dataclass
from pytest import raises
from pygritia import symbol
from pygritia.util import copy_, getattr_, setattr_, update


def test_copy():
    @dataclass
    class Test:
        __slots__ = ['a', 'b', 'c', 'd']
        a: int
        b: int
        c: int
        d: int
    a = Test(1, 2, 3, 4)
    b = copy_(a)

    assert type(a) is type(b) and all(getattr(a, k) == getattr(b, k) for k in Test.__slots__)

def test_attr_():
    class Strange:
        a = 42

        def __getattribute__(self, k: str) -> typing.Any:
            raise AttributeError("FAIL!")

        def __setattr__(self, k: str, val: typing.Any) -> None:
            raise AttributeError("FAIL!")

    with raises(AttributeError):
        getattr(Strange(), 'a')

    with raises(AttributeError):
        setattr(Strange(), 'a', 512)

    strange = Strange()
    assert getattr_(strange, 'a') == 42
    setattr_(strange, 'a', 9)
    assert getattr_(strange, 'a') == 9

def test_update():
    this = symbol('this')
    that = symbol('that')
    test = [1]
    update(this[0], 9, this=test)
    assert test == [9]
    update(this[0], that, this=test, that=42)
    assert test == [42]

    with raises(AttributeError):
        update(this + [1], [1, 2], this=test)

    with raises(TypeError):
        update(this[0], that, this=test)

    with raises(AttributeError):
        update(1, 2, this=3)
