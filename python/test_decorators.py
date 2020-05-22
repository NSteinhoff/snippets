import pytest

from decorators import ignores, reraises


class OldError(Exception):
    pass


class NewError(Exception):
    pass


class IgnoredError(Exception):
    pass


class OtherError(Exception):
    pass


def i_throw_exceptions(e):
    raise e("This is bad!")


def throw(e):
    raise e


def test_reraises__keep_message():
    wrapped = reraises(OldError, NewError)(i_throw_exceptions)

    with pytest.raises(NewError, match="This is bad!"):
        wrapped(OldError)

    with pytest.raises(ValueError, match="This is bad!"):
        wrapped(ValueError)


def test_reraises__with_new_message():
    wrapped = reraises(OldError, NewError, make_message=lambda m: m + " Really bad!")(
        i_throw_exceptions
    )

    with pytest.raises(NewError, match="This is bad! Really bad!"):
        wrapped(OldError)

    with pytest.raises(ValueError, match="This is bad!"):
        wrapped(ValueError)


def test_reraises__can_filter():
    wrapped = reraises(OldError, NewError, when=lambda e: "bad" in str(e))(throw)

    with pytest.raises(NewError, match="This is bad!"):
        wrapped(OldError("This is bad!"))

    with pytest.raises(OldError, match="This is fine!"):
        wrapped(OldError("This is fine!"))


def test_ignores__ingnores_based_on_type_alone():
    wrapped = ignores(IgnoredError, None)(i_throw_exceptions)

    assert wrapped(IgnoredError) is None
    with pytest.raises(OtherError):
        assert wrapped(OtherError)


def test_ignores__returns_fallback_value():
    wrapped = ignores(IgnoredError, "fine, take this")(i_throw_exceptions)

    assert wrapped(IgnoredError) == "fine, take this"

    with pytest.raises(OtherError):
        assert wrapped(OtherError)


def test_ignores__ingnores_based_and_predicate():
    wrapped = ignores(IgnoredError, None, lambda e: str(e) == "This is bad!")(
        i_throw_exceptions
    )
    assert wrapped(IgnoredError) is None

    wrapped = ignores(IgnoredError, None, lambda e: str(e) == "This is even worse!")(
        i_throw_exceptions
    )
    with pytest.raises(IgnoredError):
        wrapped(IgnoredError)
