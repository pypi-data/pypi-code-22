"""Compatibility utilities."""
import abc
import collections
import typing
from types import TracebackType
from typing import (
    Any, ContextManager, Dict, Generic, KT,
    MutableMapping, MutableSequence, Optional, T, T_co, Type, VT,
)
import _collections_abc

__all__ = [
    'AsyncContextManager',
    'ChainMap',
    'Counter',
    'Deque',
    'DummyContext',
]

if typing.TYPE_CHECKING:
    from typing import AsyncContextManager
else:
    try:
        from typing import AsyncContextManager  # noqa: F811
    except ImportError:
        @typing.no_type_check
        class AsyncContextManager(Generic[T_co]):  # noqa: F811
            __slots__ = ()

            async def __aenter__(self):
                return self

            @abc.abstractmethod
            async def __aexit__(self, exc_type, exc_value, traceback):
                return None

            @classmethod
            def __subclasshook__(cls, C):
                if cls is AsyncContextManager:
                    return _collections_abc._check_methods(
                        C, "__aenter__", "__aexit__")
                return NotImplemented


if typing.TYPE_CHECKING:
    from typing import ChainMap
else:
    try:
        from typing import ChainMap  # noqa: F811
    except ImportError:
        @typing.no_type_check
        class ChainMap(collections.ChainMap,  # noqa: F811
                       MutableMapping[KT, VT],
                       extra=collections.ChainMap):
            __slots__ = ()

            def __new__(cls, *args, **kwds):
                if typing._geqv(cls, ChainMap):
                    return collections.ChainMap(*args, **kwds)
                return typing._generic_new(
                    collections.ChainMap, cls, *args, **kwds)


if typing.TYPE_CHECKING:
    from typing import Counter
else:
    try:
        from typing import Counter  # noqa: F811
    except ImportError:
        @typing.no_type_check
        class Counter(collections.Counter,
                      Dict[T, int],
                      extra=collections.Counter):
            __slots__ = ()

            def __new__(cls, *args, **kwds):
                if typing._geqv(cls, Counter):
                    return collections.Counter(*args, **kwds)
                return typing._generic_new(
                    collections.Counter, cls, *args, **kwds)


if typing.TYPE_CHECKING:
    from typing import Deque
else:
    try:
        from typing import Deque  # noqa: F811
    except ImportError:
        @typing.no_type_check
        class Deque(collections.deque,  # noqa: F811
                    MutableSequence[T],
                    extra=collections.deque):
            __slots__ = ()

            def __new__(cls, *args, **kwds):
                if typing._geqv(cls, Deque):
                    return collections.deque(*args, **kwds)
                return typing._generic_new(
                    collections.deque, cls, *args, **kwds)


class DummyContext(ContextManager, AsyncContextManager):
    """Context for with-statement doing nothing."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...

    async def __aenter__(self) -> 'DummyContext':
        return self

    async def __aexit__(self,
                        exc_type: Type[BaseException] = None,
                        exc_val: BaseException = None,
                        exc_tb: TracebackType = None) -> Optional[bool]:
        ...

    def __enter__(self) -> 'DummyContext':
        return self

    def __exit__(self,
                 exc_type: Type[BaseException] = None,
                 exc_val: BaseException = None,
                 exc_tb: TracebackType = None) -> Optional[bool]:
        ...
