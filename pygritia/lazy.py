from typing import Any, TypeVar, cast
import operator
from .core import LazyType
from .symbol import Symbol, SymbolMixin
from .attr import AttrMixin
from .item import ItemMixin
from .call import CallMixin, lazy_call_with_factory
from .unary import UnaryMixin
from .binary import BinaryMixin
from .rbinary import ReversedBinaryMixin


class Lazy(SymbolMixin, AttrMixin, ItemMixin, CallMixin,
           UnaryMixin, BinaryMixin, ReversedBinaryMixin):
    pass


def symbol(name: str, factory: LazyType = Lazy) -> Any:
    return cast(Any, factory(action=Symbol(name)))


_T = TypeVar('_T')


def lazy_call(func: _T) -> _T:
    return lazy_call_with_factory(Lazy)(func)


# pylint: disable=invalid-name
lazy_getitem = lazy_call(operator.getitem)
lazy_setitem = lazy_call(operator.setitem)
lazy_delitem = lazy_call(operator.delitem)
lazy_getattr = lazy_call(getattr)
lazy_setattr = lazy_call(setattr)
lazy_delattr = lazy_call(delattr)
# pylint: enable=invalid-name
