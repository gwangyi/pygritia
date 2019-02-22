from typing import Any
from dataclasses import dataclass
from .core import Lazy, LazyAction, LazyMixin, LazyNS, LazyType, evaluate, repr_


@dataclass
class Item(LazyAction):
    """Item accessor"""
    __slots__ = ['target', 'index']

    target: Any
    index: Any

    def __str__(self) -> str:
        target = repr_(self.target)
        index = repr_(self.index)
        return f'{target}[{index}]'

    def evaluate(self, ns: LazyNS) -> Any:
        return evaluate(self.target, ns)[evaluate(self.index, ns)]

    def update(self, val: Any, ns: LazyNS) -> None:
        obj = evaluate(self.target, ns)
        index = evaluate(self.index, ns)
        obj[index] = val


class ItemMixin(LazyMixin):
    def __getitem__(self: Lazy, idx: Any) -> Lazy:
        return self.__class__(action=Item(self, idx), origin=self)
