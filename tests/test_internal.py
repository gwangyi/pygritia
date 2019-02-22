"""Tests for internal operation of lazy expressions"""
from pytest import raises  # type: ignore
from pygritia import evaluate, symbol
from pygritia.lazy import Lazy
from pygritia.call import lazy_call
from pygritia.core import LazyAction
from pygritia.ops import lazy_operator, lazy_roperator


def test_lazy_action():
    """Test about abstract lazy action"""
    class DumbAction(LazyAction):  # pylint: disable=abstract-method
        """Evaluation method is not implemented"""
        def __str__(self) -> str:
            return "NOP"

    expr = Lazy(action=DumbAction())

    with raises(NotImplementedError):
        evaluate(expr, {})

    assert repr(expr.__action__) == '<DumbAction: NOP>'

def test_lazy_operator():
    """Test about lazy_operator decorator with non-callable"""
    with raises(TypeError):
        lazy_operator(42)

    with raises(TypeError):
        lazy_roperator(42)

def test_lazy_factory():
    """Test about lazy factory"""
    class DerivedLazy(Lazy):
        """Target lazy class"""

    Lazy.register_factory(DerivedLazy)
    str_ = lazy_call(str)
    this = symbol('this')
    assert isinstance(str_(this), DerivedLazy)
