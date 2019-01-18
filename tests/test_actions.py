from pygritia import symbol, evaluate, update, lazy_function

def test_attr():
    class Test:
        obj: 'Test'
        value = 5

    this = symbol('this')
    test = Test()
    test.obj = Test()
    test.obj.value = 27
    assert repr(this.obj.value) == 'this.obj.value'
    assert evaluate(this.value, this=test) == test.value
    assert evaluate(this.obj.value, this=test) == test.obj.value

    update(this.value, 42, this=test)
    assert test.value == 42

    update(this.obj.value, 7, this=test)
    assert test.obj.value == 7

def test_item():
    this = symbol('this')
    that = symbol('that')
    test = {'hello': 'world'}
    assert repr(this['hello']) == f'this[{repr("hello")}]'
    assert repr(this[that]) == f'this[that]'

    assert evaluate(this['hello'], this=test) == 'world'
    assert evaluate(this[that], this=test, that='hello') == 'world'
    assert repr(evaluate(this[that], that='hello')) == repr(this['hello'])

    update(this[that], 'egg', this=test, that='hello')
    assert test['hello'] == 'egg'

def test_call():
    this = symbol('this')
    that = symbol('that')
    test = {'answer': 9}
    assert repr(this.update(answer=42)) == 'this.update(answer=42)'
    assert repr(this.update(answer=that)) == 'this.update(answer=that)'
    assert evaluate(this.pop('answer'), this=test) == 9
    assert not test
    evaluate(this.update(answer=42), this=test)
    assert test['answer'] == 42
    assert repr(evaluate(this.update(answer=that), that=7)) == 'this.update(answer=7)'
    evaluate(this.update(answer=that), this=test, that=7)
    assert test['answer'] == 7

def test_call_repr():
    from pygritia.actions import Call

    this = symbol('this')
    len_ = lazy_function(len)
    assert repr(len_(this)) == 'len(this)'
    assert evaluate(len_(this), this=[1, 2, 3]) == 3

    assert repr(Call("", (), {})) == '()'
