from pytest import raises
from pygritia import evaluate, symbol, lazy_function, lazy_getitem, lazy_setitem, symbols


def test_clone():
    from pygritia.lazy import Lazy

    res = [0]
    class MyLazy(Lazy):
        def __clone__(self) -> None:
            res[0] += 1

    this = MyLazy('this')

    expr = this.hello
    assert repr(expr) == 'this.hello' and type(expr) is MyLazy
    assert res[0] == 1

    expr = this[1]
    assert repr(expr) == 'this[1]' and type(expr) is MyLazy
    assert res[0] == 2

    expr = this(1)
    assert repr(expr) == 'this(1)' and type(expr) is MyLazy
    assert res[0] == 3

def test_lazy_func():
    this = symbol('this')
    len_ = lazy_function(len)

    assert repr(len_(this)) == 'len(this)'
    assert len_([1, 2, 3]) == 3
    assert evaluate(len_(this), this=[1, 2, 3]) == 3

    with raises(TypeError):
        lazy_function(1)

def test_getitem():
    this = symbol('this')
    expr = lazy_getitem([1, 2, 3], this)
    assert evaluate(expr, this=2) == 3
    assert lazy_getitem([1, 2, 3], 2) == 3

def test_setitem():
    this = symbol('this')
    arr = [1, 2, 3]
    expr = lazy_setitem(arr, 2, this)
    evaluate(expr, this=9)
    assert arr == [1, 2, 9]
    expr = lazy_setitem(arr, this, 1)
    evaluate(expr, this=2)

def test_symbols():
    this = symbol('this')
    that = symbol('that')
    assert symbols(this) == {'this'}
    assert symbols(this + that) == {'this', 'that'}
    assert symbols(evaluate(this + that, this=1)) == {'that'}
    assert symbols(42) is None
