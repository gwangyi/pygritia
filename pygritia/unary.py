from .core import Lazy, LazyMixin
from .ops import lazy_operator


class UnaryMixin(LazyMixin):
    @lazy_operator
    def __neg__(self: Lazy) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __pos__(self: Lazy) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __abs__(self: Lazy) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __invert__(self: Lazy) -> Lazy:
        pass  # pragma: no cover
