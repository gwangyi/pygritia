"""Test for `pygritia.cases`"""
from pytest import raises  # type: ignore
from pygritia import *  # pylint: disable=wildcard-import,unused-wildcard-import


def test_if():
    """Test for If"""
    cond = symbol('cond')
    sym = symbol('sym')
    arr = [1, 2, 3]
    expr = If(cond, sym[0])
    assert str(expr) == 'If(cond, sym[0])'
    assert evaluate(expr, {cond: True, sym: arr}) == arr[0]
    assert evaluate(expr, {cond: False, sym: arr}) is None
    update(expr, 9, {cond: True, sym: arr})
    assert arr[0] == 9
    with raises(TypeError):
        update(expr, 12, {cond: False, sym: arr})

def test_if_then_else():
    """Test for IfThenElse"""
    cond = symbol('cond')
    cond = symbol('cond')
    sym = symbol('sym')
    arr = [1, 2, 3]
    expr = IfThenElse(cond, sym[0], sym[1])
    assert str(expr) == 'IfThenElse(cond, sym[0], sym[1])'
    assert evaluate(expr, {cond: True, sym: arr}) == arr[0]
    assert evaluate(expr, {cond: False, sym: arr}) == arr[1]
    update(expr, 9, {cond: True, sym: arr})
    assert arr[0] == 9 and arr[1] == 2
    update(expr, 12, {cond: False, sym: arr})
    assert arr[0] == 9 and arr[1] == 12

def test_case():
    """Test for Case"""
    cond = symbol('cond')
    sym = symbol('sym')
    arr = [1, 2, 3]
    expr = Case(cond, {'first': sym[0], 'second': sym[1]}, sym[2])
    assert str(expr) == "Case(cond, {'first': sym[0], 'second': sym[1]}, sym[2])"
    assert evaluate(expr, {cond: 'first', sym: arr}) == arr[0]
    assert evaluate(expr, {cond: 'second', sym: arr}) == arr[1]
    assert evaluate(expr, {cond: 'third', sym: arr}) == arr[2]
    update(expr, 9, {cond: 'first', sym: arr})
    assert arr == [9, 2, 3]
    update(expr, 12, {cond: 'second', sym: arr})
    assert arr == [9, 12, 3]
    update(expr, 15, {cond: 'third', sym: arr})
    assert arr == [9, 12, 15]
    expr = Case(cond, {'first': sym[0]}, None)
    assert str(expr) == "If(cond == 'first', sym[0])"

def test_ensure():
    """Test for Ensure"""
    obj = symbol('obj')
    expr = Ensure(obj, 'none')
    assert str(expr) == 'Ensure(obj)'
    assert evaluate(expr, {obj: None}) == 'none'
    assert evaluate(expr, {obj: 'hello'}) == 'hello'
