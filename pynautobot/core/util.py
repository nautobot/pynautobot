"""
This file has been modified by NetworktoCode, LLC.
"""


class Hashabledict(dict):
    def __hash__(self):
        return hash(frozenset(self))
