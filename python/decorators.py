import functools
from typing import Any, Callable, Optional, Type, TypeVar

T = TypeVar("T")
E = TypeVar("E", bound=Exception)
E1 = TypeVar("E1", bound=Exception)
E2 = TypeVar("E2", bound=Exception)


def ignores(
    exc_type: Type[E], returns: T, when: Optional[Callable[[E], bool]] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Ignores exception thrown by decorated function.

    When the specified exception is raised by the decorated function,
    the value 'returns' is returned instead.

    The exceptions to catch can further be limited by providing a predicate
    which should return 'True' for exceptions that should be ignored.

    Parameters
    ----------
    exc_type : type
        The exception type that should be ignored.
    returns : T
        The value that is returned when an exception is ignored.
    when : callable, optional
        A predicate that can be used to further refine
        the exceptions to be ignored.
    """

    def decorator(f: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return f(*args, **kwargs)
            except exc_type as e:
                if when is None or when(e):
                    pass
                else:
                    raise e
            return returns

        return wrapper

    return decorator


def reraises(
    from_exc: Type[E1],
    to_exc: Type[E2],
    when: Optional[Callable[[E1], bool]] = None,
    make_message: Optional[Callable[[str], str]] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Reraises exception thrown by decorated function.

    This decorator catches the specified exception 'from_exc' in the decorated function
    and reraises it as a different exception 'to_exc'.

    The exceptions to catch can further be limited by providing a predicate
    which should return 'True' for exceptions that should be reraised.

    It allows to optionally adjust the exception's message.

    Parameters
    ----------
    from_exc : type
        The original exception type
    to_exc : type
        The target exception type
    when : callable, optional
        A predicate that can be used to further refine
        the exceptions to be reraised.
    make_message : callable, optional
        Modify the original exception message.
    """

    def decorator(f: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return f(*args, **kwargs)
            except from_exc as e:
                if when is None or when(e):
                    msg = str(e) if make_message is None else make_message(str(e))
                    raise to_exc(msg) from e
                else:
                    raise e

        return wrapper

    return decorator
