import pytest

from src.size_parser import parse_size


def test_parse_size_plain_integer() -> None:
    assert parse_size("0") == 0
    assert parse_size("1024") == 1024


def test_parse_size_with_suffixes() -> None:
    assert parse_size("1KB") == 1024
    assert parse_size("2kb") == 2 * 1024
    assert parse_size("1MB") == 1024**2
    assert parse_size("1.5MB") == int(1.5 * 1024**2)
    assert parse_size("2 GB") == 2 * 1024**3


def test_parse_size_with_whitespace_and_case() -> None:
    assert parse_size(" 10 kb ") == 10 * 1024
    assert parse_size("3MB ") == 3 * 1024**2
    assert parse_size("4g") == 4 * 1024**3


def test_parse_size_invalid() -> None:
    with pytest.raises(ValueError):
        parse_size("")
    with pytest.raises(ValueError):
        parse_size("abc")
    with pytest.raises(ValueError):
        parse_size("10XB")
    with pytest.raises(ValueError):
        parse_size("   ")
    with pytest.raises(ValueError):
        parse_size("MB")

