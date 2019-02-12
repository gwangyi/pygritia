from typing import Any
from .core import Lazy, LazyMixin
from .ops import lazy_roperator


class ReversedBinaryMixin(LazyMixin):
    @lazy_roperator
    def __radd__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rsub__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rmul__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rmatmul__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rdiv__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rtruediv__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rfloordiv__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rmod__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rdivmod__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rpow__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rlshift__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rrshift__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rand__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rxor__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __ror__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover
