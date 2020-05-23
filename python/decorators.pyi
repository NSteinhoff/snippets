from typing import Any, Callable, Optional, Type, TypeVar

T = TypeVar("T")
E = TypeVar("E", bound=Exception)
E1 = TypeVar("E1", bound=Exception)
E2 = TypeVar("E2", bound=Exception)


def ignores(
    exc_type: Type[E], returns: T, when: Optional[Callable[[E], bool]] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]: ...


def reraises(
    from_exc: Type[E1],
    to_exc: Type[E2],
    when: Optional[Callable[[E1], bool]] = None,
    make_message: Optional[Callable[[str], str]] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]: ...
