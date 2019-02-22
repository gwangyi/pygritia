"""
Provides :py:class:`Lazy` class and :py:func:`symbol`
"""
from typing import Any, cast
import operator
from .core import LazyType
from .symbol import Symbol, SymbolMixin
from .attr import AttrMixin
from .item import ItemMixin
from .call import CallMixin, lazy_call
from .unary import UnaryMixin
from .binary import BinaryMixin
from .rbinary import ReversedBinaryMixin


# pylint: disable=too-many-ancestors,too-few-public-methods
class Lazy(SymbolMixin, AttrMixin, ItemMixin, CallMixin,
           UnaryMixin, BinaryMixin, ReversedBinaryMixin):
    """
    Minimal base class of lazy expressions

    To extend functionality of lazy expressions(i.e. property descriptor from expression),
    create a new class which is derived from this class.

    Each functionality of :py:class:`Lazy` is implemented in the base mixin classes.
    """


def symbol(name: str) -> Any:
    """
    Create symbol for lazy expression

    :return: Newly created symbol expression
    :rtype: Any
    """
    return cast(Any, Lazy.create(action=Symbol(name)))


# pylint: disable=invalid-name
lazy_getitem = lazy_call(operator.getitem)
lazy_setitem = lazy_call(operator.setitem)
lazy_delitem = lazy_call(operator.delitem)
lazy_getattr = lazy_call(getattr)
lazy_setattr = lazy_call(setattr)
lazy_delattr = lazy_call(delattr)
# pylint: enable=invalid-name
