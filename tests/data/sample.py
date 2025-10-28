#!/usr/bin/env python3
"""Sample Python file for testing show-paths."""


def outer_function():
    """Outer function."""
    x = 1

    def inner_function():
        """Inner function."""
        y = 2

        def deeply_nested():
            """Deeply nested function."""
            z = 3
            target_line = "find_me"
            return z

        return deeply_nested()

    return inner_function()


class MyClass:
    """A sample class."""

    def method_one(self):
        """First method."""
        if True:
            for i in range(10):
                important_var = i
                pass

    def method_two(self):
        """Second method."""
        data = {
            "key1": "value1",
            "key2": {
                "nested_key": "nested_value",
            },
        }
        return data
