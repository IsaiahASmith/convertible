def test_main():
    from convertible import convert, Convertible, ignore_self

    assert callable(convert)
    assert isinstance(Convertible, type)
    assert callable(ignore_self)
