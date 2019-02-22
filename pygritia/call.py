from typing import Any, Callable, Mapping, Tuple, TypeVar, cast
from functools import wraps
from dataclasses import dataclass
from .core import Lazy, LazyAction, LazyMixin, LazyNS, LazyType, evaluate, repr_


@dataclass
class Call(LazyAction):
    """Function call"""
    __slots__ = ['target', 'args', 'kwargs']

    target: Any
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]

    def __str__(self) -> str:
        if isinstance(self.target, LazyMixin):
            name = str(self.target)
        elif hasattr(self.target, '__name__'):
            name = self.target.__name__
        else:
            name = repr(self.target)
        return '{}({})'.format(
            name,
            ', '.join(
                item
                for items in (
                    (repr_(arg) for arg in self.args),
                    (key + '=' + repr_(value) for key, value in self.kwargs.items())
                )
                for item in items
            )
        )

    def evaluate(self, ns: LazyNS) -> Any:
        callable_ = evaluate(self.target, ns)
        args_ = (evaluate(arg, ns) for arg in self.args)
        kwargs_ = {key: evaluate(value, ns) for key, value in self.kwargs.items()}
        return callable_(*args_, **kwargs_)


class CallMixin(LazyMixin):
    def __call__(self: Lazy, *args: Any, **kwargs: Any) -> Lazy:
        return self.__class__(action=Call(self, args, kwargs), origin=self)


_T = TypeVar('_T')

def lazy_call(func: _T) -> _T:
    if callable(func):
        func_ = func

        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            lazy = any(
                isinstance(arg, LazyMixin)
                for arglist in (args, kwargs.values())
                for arg in arglist
            )
            if lazy:
                return LazyMixin.create(action=Call(func_, args, kwargs))
            return func_(*args, **kwargs)
        return cast(_T, wrapped)
    raise TypeError("lazy_call must be applied to callable")
