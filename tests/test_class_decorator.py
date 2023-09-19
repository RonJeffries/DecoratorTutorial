import pytest


class TestClassDecorator:
    def test_get_info(self):
        class MyDeco:
            def __init__(self, *args, **kwargs):
                print("init", args, kwargs)

        @MyDeco
        def my_func(a, b):
            pass

        # assert False

    def test_func_get_info(self):
        class MyDeco:
            def __init__(self, func):
                self.func = func

        @MyDeco
        def my_func(a, b):
            return a+b
        with pytest.raises(TypeError): # not callable
            my_func(3,5)

    def test_func_call(self):
        class MyDeco:
            def __init__(self, func):
                self.func = func

            def __call__(self, *args, **kwargs):
                return self.func(*args, **kwargs)

        @MyDeco
        def my_func(a, b):
            return a+b

        result = my_func(1, 3)
        assert result == 4

    def test_deco_with_parameters(self):
        class MyDeco:
            def __init__(self, a, *, bird):
                self.a = a
                self.bird = bird

            def __call__(self, func):
                def call_me(*args, **kwargs):
                    return func(*args, *kwargs)
                return call_me

        @MyDeco(3, bird=5)
        def my_func(a, b):
            return a+b

        result = my_func(1, 3)
        assert result == 4
