"""Tests for `lazy_cast`"""
from pygritia import lazy_cast, symbol, evaluate, update


def test_casting():
    """Test basic operation of `lazy_cast`"""
    sym = symbol('sym')
    target = lazy_cast(float, sym[0], int)
    arr = [1]
    assert str(target) == 'float(sym[0])'
    assert isinstance(evaluate(target, {sym: arr}), float)
    update(target, 2.0, {sym: arr})
    assert isinstance(arr[0], int)

def test_implicit_casting():
    """Test operation of `lazy_cast` when expr type is omitted"""
    sym = symbol('sym')
    target = lazy_cast(float, sym[0])
    arr = [1]
    assert str(target) == 'float(sym[0])'
    assert isinstance(evaluate(target, {sym: arr}), float)
    update(target, 2.0, {sym: arr})
    assert isinstance(arr[0], int)
