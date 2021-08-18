from convertible import convert, Convertible


class Test(Convertible):
    def convert(self, argument: int) -> str:
        return str(argument)


def test_class_arg():
    class Foo:
        @convert(Test())
        def test(self, test: str) -> str:
            return test

    assert str(1) == Foo().test(1)


def test_class_args():
    class Foo:
        @convert(Test(), Test())
        def test(self, test: str, test2: str) -> str:
            return test + test2

    assert str(1) + str(2) == Foo().test(1, 2)


def test_class_kwarg():
    class Foo:
        @convert(test=Test())
        def test(self, test: str) -> str:
            return test

    assert str(1) == Foo().test(test=1)


def test_class_kwargs():
    class Foo:
        @convert(test=Test(), test2=Test())
        def test(self, test: str, test2: str) -> str:
            return test + test2

    assert str(1) + str(2) == Foo().test(test=1, test2=2)


def test_class_both():
    class Foo:
        @convert(Test(), Test(), Test(), test=Test(), test2=Test(), test3=Test())
        def test(self, test: str, test2: str, test3: str) -> str:
            return test + test2 + test3

    res = str(1) + str(2) + str(3)

    assert res == Foo().test(1, 2, 3)
    assert res == Foo().test(1, 2, test3=3)
    assert res == Foo().test(1, test2=2, test3=3)
    assert res == Foo().test(test=1, test2=2, test3=3)


def test_function_arg():
    @convert(Test())
    def test(test: str) -> str:
        return test

    assert str(1) == test(1)


def test_function_args():
    @convert(Test(), Test())
    def test(test: str, test2: str) -> str:
        return test + test2

    assert str(1) + str(2) == test(1, 2)


def test_function_kwarg():
    @convert(test=Test())
    def test(test: str) -> str:
        return test

    assert str(1) == test(test=1)


def test_function_kwargs():
    @convert(test=Test(), test2=Test())
    def test(test: str, test2: str) -> str:
        return test + test2

    assert str(1) + str(2) == test(test=1, test2=2)


def test_function_both():
    @convert(Test(), Test(), Test(), test=Test(), test2=Test(), test3=Test())
    def test(test: str, test2: str, test3: str) -> str:
        return test + test2 + test3

    res = str(1) + str(2) + str(3)

    assert res == test(1, 2, 3)
    assert res == test(1, 2, test3=3)
    assert res == test(1, test2=2, test3=3)
    assert res == test(test=1, test2=2, test3=3)
