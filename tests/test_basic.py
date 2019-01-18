from pygritia import *
from pytest import raises

def test_symbol():
    this = symbol('this')
    assert repr(this) == 'this'

def test_symbol_without_name():
    with raises(ValueError):
        symbol('')

def test_symbol_evaluate():
    this = symbol('this')
    assert evaluate(this, this=42) == 42

def test_symbol_evaluate_leave_lazy():
    this = symbol('this')
    res = evaluate(this, that=42)
    assert repr(res) == 'this' and evaluate(res, this=42) == 42
