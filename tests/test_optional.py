from convertible import convert, Convertible
from convertible.Convertible.Optional import Optional
from convertible.Convert.ExceptionHandler.ConvertException import ConvertException
from convertible.Convert.ConvertHandler.ConvertHandler import ConvertHandler


class Test(Convertible):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def convert(self, argument: str) -> int:
        try:
            return int(argument)
        except ValueError:
            raise ConvertException(self, argument)


def test_class_arg():
    class Foo:
        @convert(ConvertHandler(Optional(Test())))
        def test(self, test=None) -> int:
            if test is None:
                return 5
            return test

    assert 1 == Foo().test("1")
    assert 5 == Foo().test()
    assert 5 == Foo().test("hi")


def test_class_args():
    class Foo:
        @convert(ConvertHandler(Optional(Test()), Optional(Test())))
        def test(self, test=None, test2=None) -> int:
            if test is None:
                return 5
            elif test2 is None:
                return 1 + test
            else:
                return test + test2

    assert 3 == Foo().test("1", "2")
    assert 2 == Foo().test("1")
    assert 2 == Foo().test("1", "hi")
    assert 5 == Foo().test("hi", "bye")
    assert 5 == Foo().test("hi")
    assert 5 == Foo().test()


def test_class_kwarg():
    class Foo:
        @convert(ConvertHandler(test=Optional(Test())))
        def test(self, test=None) -> int:
            if test is None:
                return 5
            return test

    assert 1 == Foo().test(test=1)
    assert 5 == Foo().test(test="hi")
    assert 5 == Foo().test()


def test_class_kwargs():
    class Foo:
        @convert(ConvertHandler(test=Optional(Test()), test2=Optional(Test())))
        def test(self, test=None, test2=None) -> int:
            if test is None:
                return 5
            elif test2 is None:
                return 1 + test
            return test + test2

    assert 3 == Foo().test(test="1", test2="2")
    assert 2 == Foo().test(test="1", test2="hi")
    assert 2 == Foo().test(test="1")
    assert 5 == Foo().test(test="hi", test2="bye")
    assert 5 == Foo().test(test="hi")
    assert 5 == Foo().test()


def test_class_both():
    class Foo:
        @convert(ConvertHandler(Optional(Test()), Optional(Test()), test=Optional(Test()), test2=Optional(Test())))
        def test(self, test=None, test2=None) -> int:
            if test is None:
                return 5
            elif test2 is None:
                return 1 + test
            return test + test2

    assert 3 == Foo().test("1", "2")
    assert 2 == Foo().test("1", test2="hi")
    assert 3 == Foo().test("2", test2="1")
    assert 5 == Foo().test()


def test_function_arg():
    @convert(ConvertHandler(Optional(Test())))
    def test(test=None) -> int:
        if test is None:
            return 5
        return test

    assert 1 == test("1")
    assert 5 == test()
    assert 5 == test("hi")


def test_function_args():
    @convert(ConvertHandler(Optional(Test()), Optional(Test())))
    def test(test=None, test2=None) -> int:
        if test is None:
            return 5
        elif test2 is None:
            return 1 + test
        else:
            return test + test2

    assert 3 == test("1", "2")
    assert 2 == test("1")
    assert 2 == test("1", "hi")
    assert 5 == test("hi", "bye")
    assert 5 == test("hi")
    assert 5 == test()


def test_function_kwarg():
    @convert(ConvertHandler(test=Optional(Test())))
    def test(test=None) -> int:
        if test is None:
            return 5
        return test

    assert 1 == test(test=1)
    assert 5 == test(test="hi")
    assert 5 == test()


def test_function_kwargs():
    @convert(ConvertHandler(test=Optional(Test()), test2=Optional(Test())))
    def test(test=None, test2=None) -> int:
        if test is None:
            return 5
        elif test2 is None:
            return 1 + test
        return test + test2

    assert 3 == test(test="1", test2="2")
    assert 2 == test(test="1", test2="hi")
    assert 2 == test(test="1")
    assert 5 == test(test="hi", test2="bye")
    assert 5 == test(test="hi")
    assert 5 == test()


def test_function_both():
    @convert(ConvertHandler(Optional(Test()), Optional(Test()), test=Optional(Test()), test2=Optional(Test())))
    def test(test=None, test2=None) -> int:
        if test is None:
            return 5
        elif test2 is None:
            return 1 + test
        return test + test2

    assert 3 == test("1", "2")
    assert 2 == test("1", test2="hi")
    assert 3 == test("2", test2="1")
    assert 5 == test()
