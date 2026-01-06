import os

import pytest


@pytest.fixture(autouse=True)
def _no_database_url_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    # Backend settings require DATABASE_URL; tests that don't need DB should not.
    # Any DB-dependent tests must set DATABASE_URL explicitly.
    monkeypatch.setenv("DATABASE_URL", os.getenv("DATABASE_URL", "sqlite+pysqlite:///:memory:"))
