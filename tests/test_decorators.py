import functools


class TestDecorators:
    def test_hookup(self):
        assert 4 == 2+2

    def test_repeat_twice(self):
        def repeat(func):
            @functools.wraps(func)
            def rpt(*args, **kwargs):
                func(*args, **kwargs)
                func(*args, **kwargs)
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
                def wrapped(*args, **kwargs):
                    for i in range(times):
                        func(*args, **kwargs)
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

    def test_wrapping_class(self):
        # note that we do not actually wrap the class itself,
        # we just return the original. A more complex example
        # might do more.
        def report_creation(klass):
            if not hasattr(report_creation, "count"):
                report_creation.count = 0
            def wrapper_report():
                report_creation.count += 1
                return klass
            return wrapper_report

        @report_creation
        class Reported:
            def __init__(self):
                pass

        reported = Reported()
        r2 = Reported()
        assert report_creation.count == 2

        @report_creation
        class Another:
            pass

        another = Another()
        assert report_creation.count == 3

    def test_singleton(self):
        # lifted from RealPython
        def singleton(klass):
            def wrapper_singleton(*args, **kwargs):
                if not wrapper_singleton.instance:
                    wrapper_singleton.instance = klass(*args, **kwargs)
                return wrapper_singleton.instance
            wrapper_singleton.instance = None
            return wrapper_singleton

        @singleton
        class Something:
            def __init__(self, a, b):
                self.a = a
                self.b = b

        s1 = Something(1, 2)
        s2 = Something(3, 4)
        assert s1 is s2
        assert s2.a == 1
