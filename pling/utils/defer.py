
def defer_property(recipent_name, property_name):
    """Returns a property that defers to a child

    Example:

    >>> class MyClass
    >>>     foo = defer_property("member", "foo")
    >>>
    >>> x = MyClass()

    Now the following two lines are functionally identical:

    >>> x.member.foo = 3.14
    >>> x.foo = 3.14
    """
    def getter(self):
        recipent = getattr(self, recipent_name)
        return getattr(recipent, property_name)

    def setter(self, value):
        recipent = getattr(self, recipent_name)
        setattr(recipent, property_name, value)

    return property(getter, setter)

def defer_properties(recipent_name, property_names):
    """Shortcut for defering multiple properties to the same object

    Unlike defer_property, this function should be used as a class decorator:

    >>> @defer_properties("member", ["foo", "bar"])
    >>> class MyClass
    >>>     pass
    """
    def decorator(cls):
        for property_name in property_names:
            prop = defer_property(recipent_name, property_name)

            setattr(cls, property_name, prop)

        return cls

    return decorator
