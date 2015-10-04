
import pytest

from pling.utils.defer import defer_properties

class DeferPropertyTest:
    @pytest.fixture
    def subject(self):
        """Sets up 2 objects, one of whom defers a property to the other"""
        class ChildClass:
            def __init__(self):
                self.foo = 123

            def bar(self, x):
                return x * 2

        @defer_properties("child", ["foo", "bar"])
        class Subject:
            def __init__(self):
                self.child = ChildClass()

        return Subject()

    def test_getting(self, subject):
        """Tests that getting works"""
        assert subject.foo == 123

    def test_setting(self, subject):
        """Tests that setting works"""
        subject.foo = 3.14

        assert subject.foo == 3.14

    def test_getattr(self, subject):
        """Tests that getattr also defers to the child property"""
        assert getattr(subject, "foo") == 123

    def test_setattr(self, subject):
        """Tests that setattr also defers to the child property"""
        setattr(subject, "foo", 1337)

        assert subject.child.foo == 1337

    def test_method_call(self, subject):
        """Tests that a method call will also be deferred to the child"""
        assert subject.bar(5) == 10
