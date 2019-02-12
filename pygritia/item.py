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

    def evaluate(self, ns: LazyNS, factory: LazyType) -> Any:
        return evaluate(self.target, ns, factory)[evaluate(self.index, ns, factory)]

    def update(self, val: Any, ns: LazyNS, factory: LazyType) -> None:
        obj = evaluate(self.target, ns, factory)
        index = evaluate(self.index, ns, factory)
        obj[index] = val


class ItemMixin(LazyMixin):
    def __getitem__(self: Lazy, idx: Any) -> Lazy:
        return self.__class__(action=Item(self, idx), origin=self)
