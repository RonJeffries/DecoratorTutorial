import pytest


class TestForArticle:

    def test_property(self):
        class Mumble:
            def __init__(self, foo):
                self._secret_foo = foo

            @property
            def foo(self):
                return self._secret_foo

        mumble = Mumble(42)
        assert mumble.foo == 42
        with pytest.raises(AttributeError):
            mumble.foo = 37

    def test_wrapper(self):
        def walking():
            return "walking"

        def running():
            return "running"

        def mumbling():
            return "mumbling"

        def wrapper(func):
            return "you are " + func() + ", sir!"

        assert wrapper(walking) == "you are walking, sir!"
        assert wrapper(running) == "you are running, sir!"
        assert wrapper(mumbling) == "you are mumbling, sir!"

