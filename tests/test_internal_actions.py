from pytest import raises
from pygritia._actions import LazyAction
from pygritia.lazy import Lazy
from pygritia.util import setattr_
from pygritia import evaluate, update


def test_abstract_action():
    lazy = Lazy('hi')
    setattr_(lazy, '__action__', LazyAction())

    with raises(NotImplementedError):
        evaluate(lazy, hi=42)

    with raises(AttributeError):
        update(lazy, 9, hi=42)
