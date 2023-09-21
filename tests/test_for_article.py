import functools

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

    def test_do_twice(self):
        def do_twice(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = "do_twice begin\n"
                result += func(*args, **kwargs)
                result += func(*args, **kwargs)
                result += "end do_twice\n"
                return result
            return wrapper

        @do_twice
        def hello(name):
            return "hello, " + name + "!\n"

        said_twice = hello("Avery")
        assert (said_twice ==
"""do_twice begin
hello, Avery!
hello, Avery!
end do_twice
""")

    def test_repeat_parameterized(self):
        def do_n_times(number_of_times):
            def get_function(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    result = "do_n_times begin\n"
                    for _ in range(number_of_times):
                        result += func(*args, **kwargs)
                    result += "end do_n_times\n"
                    return result
                return wrapper
            return get_function

        @do_n_times(3)
        def hello(name):
            return "hello, " + name + "!\n"

        said_twice = hello("Parker")
        assert (said_twice ==
"""do_n_times begin
hello, Parker!
hello, Parker!
hello, Parker!
end do_n_times
""")

    def test_do_twice_class(self):
        class do_twice:
            def __init__(self, func):
                self.func = func

            def __call__(self, *args, **kwargs):
                result = "do_twice begin\n"
                result += self.func(*args, **kwargs)
                result += self.func(*args, **kwargs)
                result += "end do_twice\n"
                return result

        @do_twice
        def hello(name):
            return "hello, " + name + "!\n"

        said_twice = hello("Avery")
        assert (said_twice ==
"""do_twice begin
hello, Avery!
hello, Avery!
end do_twice
""")

    def test_do_n_times_class(self):
        class do_n_times:
            def __init__(self, number_of_times):
                self.number_of_times = number_of_times

            def __call__(self, func):
                self.func = func
                return self.perform_behavior

            def perform_behavior(self, *args, **kwargs):
                result = "do_n_times begin\n"
                for _ in range(self.number_of_times):
                    result += self.func(*args, **kwargs)
                result += "end do_n_times\n"
                return result

        @do_n_times(3)
        def hello(name):
            return "hello, " + name + "!\n"

        said_twice = hello("Parker")
        assert (said_twice ==
"""do_n_times begin
hello, Parker!
hello, Parker!
hello, Parker!
end do_n_times
""")

