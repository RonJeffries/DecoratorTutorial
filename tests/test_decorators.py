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
