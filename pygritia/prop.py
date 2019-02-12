from typing import Any, Type, Optional
from .core import LazyAction, LazyMixin, evaluate, update
from .lazy import Lazy, symbol
from .util import setattr_


class LazyProp(Lazy):
    def __init__(self, action: LazyAction, origin: Optional[LazyMixin] = None) -> None:
        super().__init__(action, origin)
        setattr_(self, '__doc__', str(self))

    def __get__(self, inst: Any, owner: Type[Any]) -> Any:
        if inst is None:
            return self
        return evaluate(self, {this: inst})

    def __set__(self, inst: Any, value: Any) -> None:
        update(self, value, {this: inst})

this = symbol('this', factory=LazyProp)
