import functools

import pytest


class TestDecorators:
    def test_hookup(self):
        assert 4 == 2+2

    def test_repeat_twice(self):
        def repeat(f):
            def rpt():
                f()
                f()
            return rpt
        count = 0

        @repeat
        def increment():
            nonlocal count
            count += 1
        assert count == 0
        increment()
        assert count == 2

        s = ""

        @repeat
        def add_a():
            nonlocal s
            s += "a"
        add_a()
        assert s == "aa"

    def test_repeat_with_parameter(self):
        def repeat(times):
            def rpt(func):
                @functools.wraps(func)
                def wrapped():
                    for i in range(times):
                        func()
                return wrapped
            return rpt

        count = 0

        @repeat(3)
        def increment():
            nonlocal count
            count += 1
        print("increment", increment)
        count = 0
        increment()
        assert count == 3

    def test_repeat_with_function_parameters(self):
        def repeat(times):
            def rpt(func):
                @functools.wraps(func)
                def wrapped(*args, **kwargs):
                    for i in range(times):
                        func(*args, **kwargs)
                return wrapped
            return rpt
        count = 0
        @repeat(3)
        def increment(by, multiplier=1):
            nonlocal count
            count += by*multiplier
        increment(2)
        assert count == 6
        count = 0
        increment(2, multiplier=2)
        assert count == 12
