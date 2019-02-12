from pygritia import evaluate, symbol
from pygritia.symbol import Symbol
from pygritia.lazy import Lazy
from pygritia.call import lazy_call_with_factory
from pygritia.core import LazyAction
from pygritia.ops import lazy_operator, lazy_roperator
from pytest import raises


def test_lazy_action():
    class DumbAction(LazyAction):
        def __str__(self) -> str:
            return "NOP"

    expr = Lazy(action=DumbAction())

    with raises(NotImplementedError):
        evaluate(expr, {})

    assert repr(expr.__action__) == '<DumbAction: NOP>'

def test_call_internal():
    class DerivedLazy(Lazy):
        pass

    str_ = lazy_call_with_factory(DerivedLazy)(str)
    this = symbol('this')
    assert isinstance(str_(this), DerivedLazy)

def test_lazy_operator():
    with raises(TypeError):
        lazy_operator(42)

    with raises(TypeError):
        lazy_roperator(42)

def test_symbol_internal():
    class DerivedLazy(Lazy):
        _symbol_dict = {}

    this = symbol('this')
    with raises(KeyError):
        evaluate(this, {this: 5}, DerivedLazy)
    that = symbol('that', DerivedLazy)
    assert evaluate(that, {that: 9}, DerivedLazy) == 9
