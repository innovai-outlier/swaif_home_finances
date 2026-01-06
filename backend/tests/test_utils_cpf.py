import pytest

from app.utils import normalize_cpf


@pytest.mark.parametrize(
    "cpf,expected",
    [
        ("12345678901", "12345678901"),
        ("123.456.789-01", "12345678901"),
    ],
)
def test_normalize_cpf_accepts_formats(cpf: str, expected: str) -> None:
    assert normalize_cpf(cpf) == expected


@pytest.mark.parametrize(
    "cpf",
    [
        "",
        "123",
        "123.456.789-0",
        "123.456.789-012",
        "1234567890A",
        "123-456-789-01",
    ],
)
def test_normalize_cpf_rejects_other_formats(cpf: str) -> None:
    with pytest.raises(ValueError):
        normalize_cpf(cpf)
