import functools


def ignores(exc_type, returns, when=None):
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

    Examples
    --------

    Ignore all `ValueError`s:

    >>> @ignores(ValueError, returns=1)
    ... def foo(e):
    ...     raise e

    >>> foo(ValueError)
    1

    >>> foo(TypeError)
    Traceback (most recent call last):
        ...
    TypeError

    Ignore `ValueError`s with a specific message:

    >>> @ignores(ValueError, returns=1, when=lambda e: str(e) == "Not so bad.")
    ... def bar(e):
    ...     raise e

    >>> bar(ValueError("Bad!"))
    Traceback (most recent call last):
        ...
    ValueError: Bad!

    >>> bar(ValueError("Not so bad."))
    1
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
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


def reraises(from_exc, to_exc, when=None, make_message=None):
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

    Examples
    --------

    Reraise ValueError as TypeError with a new message:

    >>> @reraises(
    ...     from_exc=ValueError,
    ...     to_exc=TypeError,
    ...     make_message=lambda m: m + " (I used to be a ValueError)"
    ... )
    ... def foo(e):
    ...     raise(e)

    >>> foo(ValueError("Error!"))
    Traceback (most recent call last):
        ...
    TypeError: Error! (I used to be a ValueError)

    Other exceptions are unaffected!

    >>> foo(RuntimeError("Error!"))
    Traceback (most recent call last):
        ...
    RuntimeError: Error!
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
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
