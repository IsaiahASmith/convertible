from typing import List

from convertible import convert, Convertible
from convertible.Convertible.Greedy import Greedy
from convertible.Convert.ConvertHandler.ConvertHandler import ConvertHandler


class Test(Convertible):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def convert(self, argument: int) -> str:
        return str(argument)


def test_class_arg():
    class Foo:
        @convert(ConvertHandler(Greedy(Test())))
        def test(self, args: List[str]) -> list[str]:
            return args

    assert [str(1)] == Foo().test(1)


def test_class_args():
    class Foo:
        @convert(ConvertHandler(Greedy(Test())))
        def test(self, args: List[str]) -> List[str]:
            return args

    assert [str(1), str(2)] == Foo().test(1, 2)


def test_class_both():
    class Foo:
        @convert(ConvertHandler(Greedy(Test()), test=Test()))
        def test(self, args: List[str], test: str) -> List[str]:
            return [test] + args

    assert [str(1), str(2), str(3)] == Foo().test(2, 3, test=1)


def test_function_arg():
    @convert(ConvertHandler(Greedy(Test())))
    def test(args: List[str]) -> List[str]:
        return args

    assert [str(1)] == test(1)


def test_function_args():
    @convert(ConvertHandler(Greedy(Test())))
    def test(args: List[str]) -> List[str]:
        return args

    assert [str(1), str(2)] == test(1, 2)


def test_function_both():
    @convert(ConvertHandler(Greedy(Test()), test=Test()))
    def test(args: List[str], test: str) -> List[str]:
        return [test] + args

    assert [str(1), str(2), str(3)] == test(2, 3, test=1)
