from typing import Any, Mapping, Optional, Sequence, Type, TypeVar, Union, cast
from .util import setattr_


LazyNamespace = Mapping[Union[str, 'LazyMixin'], Any]
LazyNS = LazyNamespace


class LazyAction:  # pylint: disable=too-few-public-methods
    """Lazy Expression Handler"""
    __slots__ = ('owner',)
    owner: 'LazyMixin'

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {str(self)}>"

    def evaluate(self, ns: LazyNamespace) -> Any:
        """Evaluate expression

        To substitute actual value for specific symbol, give value with keyword argument.
        """
        raise NotImplementedError

    def update(self, val: Any, ns: LazyNamespace) -> None:  # pylint: disable=no-self-use
        """Update value of expression

        If the expression is readonly, it raises AttributeError
        """
        raise AttributeError("expr cannot be updated")


class LazyMeta(type):
    _factory: 'LazyType'

    @classmethod
    def register_factory(cls, lazy_factory: 'LazyType') -> None:
        cls._factory = lazy_factory

    @classmethod
    def create(cls, action: LazyAction) -> 'LazyMixin':
        return cls._factory(action=action)


class LazyMixin(metaclass=LazyMeta):
    __slots__ = ['__action__', '__weakref__']
    __action__: LazyAction

    def __init_subclass__(cls) -> None:
        if '__hash__' not in cls.__dict__:
            def __hash__(self: LazyMixin) -> int:
                return hash(self.__action__)
            setattr(cls, '__hash__', __hash__)

    def __init__(self, action: LazyAction, origin: Optional['LazyMixin'] = None) -> None:
        setattr_(self, '__action__', action)
        action.owner = self

    def __str__(self) -> str:
        return str(self.__action__)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {str(self)}>"


Lazy = TypeVar('Lazy', bound=LazyMixin)
LazyType = Type[LazyMixin]
_T = TypeVar('_T')


def evaluate(expr: _T, ns: LazyNamespace) -> _T:
    """Evaluate expression
    """
    if isinstance(expr, LazyMixin):
        return cast(_T, expr.__action__.evaluate(ns))
    return expr


def update(expr: _T, val: _T, ns: LazyNamespace) -> None:
    """Update the value of expression
    """
    if not isinstance(expr, LazyMixin):
        raise TypeError("Expr must be a lazy expression")
    val = evaluate(val, ns)
    if isinstance(val, LazyMixin):
        raise TypeError("Val is not fully evaluated")
    expr.__action__.update(val, ns)


def repr_(expr: Any) -> str:
    if isinstance(expr, LazyMixin):
        return str(expr)
    return repr(expr)
