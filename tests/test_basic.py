from pygritia import *
from pytest import fixture, raises

@fixture
def this():
    return symbol('this')

def test_dummy_eval_update():
    obj = object()
    assert evaluate(obj, {}) is obj

    with raises(TypeError):
        update(obj, 5, {})

def test_symbol(this):
    assert str(this) == 'this'
    assert repr(this) == '<Lazy: this>'
    obj = object()
    assert evaluate(this, {this: obj}) is obj
    assert evaluate(this, {'this': obj}) is obj
    assert evaluate(this, {}) is this
    with raises(TypeError):
        update(this, this, {})
    with raises(AttributeError):
        update(this, 5, {})

def test_operator(this):
    assert str(this + 5) == 'this + 5'
    assert str(~this) == '~this'
    assert str(abs(this)) == 'abs(this)'
    assert str(divmod(this, 7)) == 'divmod(this, 7)'

    assert evaluate(this + 5, {this: 2}) == 7
    assert evaluate(9 // this, {this: 2}) == 4
    assert evaluate(this == 2, {this: 2})

    with raises(ZeroDivisionError):
        evaluate(this / 0, {this: 3})

def test_attr(this):
    old = object()
    new = object()

    class Test:
        val = old

    test = Test()
    assert str(this.val) == 'this.val'

    assert evaluate(this.val, {this: test}) is old
    update(this.val, new, {this: test})
    assert test.val is new

    with raises(AttributeError):
        this.val = 5

def test_inner_attr(this):
    old = object()
    new = object()

    class InnerTest:
        val = old

    inner = InnerTest()

    class Test:
        val = inner

    test = Test()
    assert str(this.val.val) == 'this.val.val'

    assert evaluate(this.val.val, {this: test}) is old
    update(this.val.val, new, {this: test})
    assert inner.val is new

def test_item(this):
    old = object()
    new = object()
    arr = [old]
    assert str(this[0]) == 'this[0]'
    assert evaluate(this[0], {this: arr}) is old
    update(this[0], new, {this: arr})
    assert arr[0] is new

def test_call(this):
    assert str(this('42')) == "this('42')"
    assert evaluate(this('42'), {this: int}) == 42

def test_lazy_call(this):
    @lazy_call
    def my_func(obj: int) -> int:
        return obj * 2

    assert str(my_func(this)) == 'my_func(this)'
    assert my_func(42) == 84
    assert evaluate(my_func(this), {this: 42}) == 84

def test_lazy_callable(this):
    class MyCallable:
        def __call__(self, obj: int) -> int:
            return obj // 2

    my_callable = MyCallable()
    my_lazy_call = lazy_call(my_callable)
    non_callable = object()

    assert str(my_lazy_call(this)) == repr(my_callable) + '(this)'
    assert evaluate(my_lazy_call(this), {this: 42}) == 21

    with raises(TypeError):
        lazy_call(non_callable)
