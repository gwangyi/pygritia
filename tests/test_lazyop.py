from pytest import raises  # type: ignore
from pygritia import symbol, evaluate, update
from pygritia.lazyop import _generate_operator_method


def test_forward_op():
    this = symbol('this')
    expr = this + [42]
    assert repr(expr) == 'this + [42]'
    assert evaluate(expr, this=[9]) == [9, 42]
    with raises(AttributeError):
        update(expr, 5, this=[9])

def test_reverse_op():
    this = symbol('this')
    expr = [42] + this
    assert repr(expr) == '[42] + this'
    assert evaluate(expr, this=[9]) == [42, 9]
    with raises(AttributeError):
        update(expr, 5, this=[9])

def test_repr_op():
    this: int = symbol('this')
    assert repr(~this) == '~this'
    assert repr(divmod(this, 5)) == 'divmod(this, 5)'

def test_wrong_op_gen():
    with raises(ValueError):
        _generate_operator_method('__wow__')
