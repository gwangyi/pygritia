from typing import Any
import operator
from dataclasses import dataclass
from .core import Lazy, LazyAction, LazyMixin, LazyNS, LazyType, evaluate
from .util import OPERATORS, getattr_


@dataclass
class Attr(LazyAction):
    """Attr accessor"""

    __slots__ = ['target', 'attr']
    target: LazyMixin
    attr: str

    def __str__(self) -> str:
        return f'{str(self.target)}.{self.attr}'

    def evaluate(self, ns: LazyNS) -> Any:
        return operator.attrgetter(self.attr)(evaluate(self.target, ns))

    def update(self, val: Any, ns: LazyNS) -> None:
        if '.' in self.attr:
            prior, attr = self.attr.rsplit('.', 1)
            obj = operator.attrgetter(prior)(evaluate(self.target, ns))
        else:
            attr = self.attr
            obj = evaluate(self.target, ns)
        setattr(obj, attr, val)


class AttrMixin(LazyMixin):
    def __getattribute__(self: Lazy, name: str) -> Lazy:
        if (name.startswith('__') and
                name.endswith('__') and
                name not in OPERATORS):
            return getattr_(self, name)  # type: ignore

        act = self.__action__
        if isinstance(act, Attr):
            return self.__class__(action=Attr(act.target, act.attr + '.' + name), origin=self)
        return self.__class__(action=Attr(self, name), origin=self)

    def __setattr__(self, name: str, val: Any) -> None:
        raise AttributeError(f"{name} can't be set")
