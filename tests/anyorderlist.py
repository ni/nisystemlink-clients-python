class AnyOrderList:
    """Sequence that compares to a list, but allows any order.

    This is only intended for comparison purposes, not as an actual list replacement.
    """

    def __init__(self, list_):
        self._list = list_
        self._list.sort()

    def __eq__(self, other):
        assert isinstance(other, list)
        return self._list == sorted(other)

    def __str__(self):
        return str(self._list)

    def __repr__(self):
        return "AnyOrderList({})".format(repr(self._list))
