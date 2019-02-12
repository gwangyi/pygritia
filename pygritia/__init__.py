"""Pygritia: Lazy evaluation"""
from .lazy import (lazy_call, lazy_delattr, lazy_delitem, lazy_getattr,
                   lazy_getitem, lazy_setattr, lazy_setitem, symbol)
from .core import evaluate, update
from .prop import this

__all__ = [
    'evaluate', 'lazy_call', 'lazy_delattr', 'lazy_delitem',
    'lazy_getattr', 'lazy_getitem', 'lazy_setattr',
    'lazy_setitem', 'symbol', 'update', 'this',
]
