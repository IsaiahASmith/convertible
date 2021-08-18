from convertible import ignore_self


@ignore_self
def decorator(func):
    def inner(*args, **kwargs):
        return {"args": args, "kwargs": kwargs}

    return inner


def test_function():
    def test(*args, **kwargs):
        pass

    test_func = decorator(test)
    res = test_func(1, 2, 3, test=4, bar=5)
    args, kwargs = res["args"], res["kwargs"]
    assert args[0] == 1
    assert args[1] == 2
    assert args[2] == 3
    assert kwargs["test"] == 4
    assert kwargs["bar"] == 5


def test_class():
    class Test:
        @decorator
        def test(self, *args, **kwargs):
            pass

    test_class = Test()
    res = test_class.test(1, 2, 3, test=4, bar=5)
    args, kwargs = res["args"], res["kwargs"]
    assert args[0] == 1
    assert args[1] == 2
    assert args[2] == 3
    assert kwargs["test"] == 4
    assert kwargs["bar"] == 5
