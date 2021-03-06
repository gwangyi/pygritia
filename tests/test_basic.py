"""Tests for basic operation of lazy expressions"""
from pytest import raises  # type: ignore
from pygritia import *  # pylint: disable=unused-wildcard-import,wildcard-import


def test_dummy_eval_update():
    """Test evaluate and update with empty namespace"""
    obj = object()
    assert evaluate(obj, {}) is obj

    with raises(TypeError):
        update(obj, 5, {})

def test_symbol():
    """Test about symbol"""
    assert str(this) == 'this'
    assert repr(this) == '<LazyProp: this>'
    obj = object()
    assert evaluate(this, {this: obj}) is obj
    assert evaluate(this, {'this': obj}) is obj
    assert evaluate(this, {}) is this
    with raises(TypeError):
        update(this, this, {})
    with raises(AttributeError):
        update(this, 5, {})

def test_operator():
    """Test about operator"""
    assert str(this + 5) == 'this + 5'
    assert str(~this) == '~this'
    assert str(abs(this)) == 'abs(this)'
    assert str(divmod(this, 7)) == 'divmod(this, 7)'

    assert evaluate(this + 5, {this: 2}) == 7
    assert evaluate(9 // this, {this: 2}) == 4
    assert evaluate(this == 2, {this: 2})

    with raises(ZeroDivisionError):
        evaluate(this / 0, {this: 3})

def test_attr():
    """Test about attributes"""
    old = object()
    new = object()

    class Test:
        """Target class"""
        val = old

    test = Test()
    assert str(this.val) == 'this.val'

    assert evaluate(this.val, {this: test}) is old
    update(this.val, new, {this: test})
    assert test.val is new

    with raises(AttributeError):
        this.val = 5

def test_inner_attr():
    """Test nested attribute access"""
    old = object()
    new = object()

    class InnerTest:
        """Inner class"""
        val = old

    inner = InnerTest()

    class Test:
        """Target class"""
        val = inner

    test = Test()
    assert str(this.val.val) == 'this.val.val'

    assert evaluate(this.val.val, {this: test}) is old
    update(this.val.val, new, {this: test})
    assert inner.val is new

def test_item():
    """Tests for item access"""
    old = object()
    new = object()
    arr = [old]
    assert str(this[0]) == 'this[0]'
    assert str(this[:9]) == 'this[:9]'
    assert str(this[0:9:2]) == 'this[0:9:2]'
    assert evaluate(this[0], {this: arr}) is old
    update(this[0], new, {this: arr})
    assert arr[0] is new

def test_call():
    """Tests for function call"""
    assert str(this('42')) == "this('42')"
    assert evaluate(this('42'), {this: int}) == 42

def test_lazy_call():
    """Tests for function call with lazy exprs"""
    @lazy_call
    def my_func(obj: int) -> int:
        return obj * 2

    assert str(my_func(this)) == 'my_func(this)'
    assert my_func(42) == 84
    assert evaluate(my_func(this), {this: 42}) == 84

def test_lazy_callable():
    """Tests for calling callable with lazy exprs"""
    class MyCallable:
        """Target callable class"""
        def __call__(self, obj: int) -> int:
            return obj // 2

    my_callable = MyCallable()
    my_lazy_call = lazy_call(my_callable)
    non_callable = object()

    assert str(my_lazy_call(this)) == repr(my_callable) + '(this)'
    assert evaluate(my_lazy_call(this), {this: 42}) == 21

    with raises(TypeError):
        lazy_call(non_callable)

def test_this():
    """Tests this symbol"""
    class InnerTest:
        """Inner class"""
        val = 5

    class Test:
        """Target class"""
        this: 'Test'
        first = [1, 2, 3]
        second = InnerTest()
        third = this.first[2]
        fourth = this.second.val

    test = Test()
    assert str(Test.third) == 'this.first[2]'
    assert test.third == 3
    assert test.fourth == 5
    test.third = 9
    test.fourth = 10
    assert test.first == [1, 2, 9]
    assert test.second.val == 10
