def test_main():
    from convertible import (
        convert,
        Convertible,
        ignore_self,
        Convert,
        NextArgumentException,
        ConvertHandler,
        ExceptionHandler,
        ConvertException,
    )

    assert callable(convert)
    assert isinstance(Convertible, type)
    assert callable(ignore_self)
    assert isinstance(Convert, type)
    assert isinstance(NextArgumentException, type)
    assert isinstance(ConvertHandler, type)
    assert isinstance(ExceptionHandler, type)
    assert isinstance(ConvertException, type)


def test_convert():
    from convertible.Convert import Convert, NextArgumentException

    assert isinstance(Convert, type)
    assert isinstance(NextArgumentException, type)


def test_convert_handler():
    from convertible.Convert.ConvertHandler import ConvertHandler

    assert isinstance(ConvertHandler, type)


def test_exception_handler():
    from convertible.Convert.ExceptionHandler import ExceptionHandler, ConvertException

    assert isinstance(ExceptionHandler, type)
    assert isinstance(ConvertException, type)
