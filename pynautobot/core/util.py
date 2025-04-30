"""This file has been modified by NetworktoCode, LLC."""


class Hashabledict(dict):
    """A dictionary subclass that is hashable."""

    def __hash__(self):
        """Hash the dictionary."""
        return hash(frozenset(self))
