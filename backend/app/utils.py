import re


_CPF_ACCEPTED = re.compile(r"^(\d{11}|\d{3}\.\d{3}\.\d{3}-\d{2})$")


def normalize_cpf(cpf: str) -> str:
    cpf = cpf.strip()
    if not _CPF_ACCEPTED.match(cpf):
        raise ValueError("invalid_cpf_format")
    digits = re.sub(r"\D", "", cpf)
    if len(digits) != 11:
        raise ValueError("invalid_cpf_format")
    return digits
