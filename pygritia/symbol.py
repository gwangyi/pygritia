from typing import Any, MutableMapping, Optional
from weakref import WeakValueDictionary
from dataclasses import dataclass
from .core import LazyAction, LazyMixin, LazyNS, LazyType


@dataclass
class Symbol(LazyAction):
    """Attr accessor"""

    __slots__ = ['name']
    name: str

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return id(self)

    def evaluate(self, ns: LazyNS) -> Any:
        symbol_dict = getattr(type(self.owner), '_symbol_dict', {})
        if self not in symbol_dict:
            raise KeyError(f"Orphan symbol {self}")
        expr = symbol_dict[self]
        if expr in ns:
            return ns[expr]
        if self.name in ns:
            return ns[self.name]
        return expr


class SymbolMixin(LazyMixin):
    _symbol_dict: MutableMapping['Symbol', 'LazyMixin'] = WeakValueDictionary()

    def __init__(self, action: LazyAction, origin: Optional[LazyMixin] = None) -> None:
        super().__init__(action, origin)
        if isinstance(action, Symbol):
            type(self)._symbol_dict[action] = self
