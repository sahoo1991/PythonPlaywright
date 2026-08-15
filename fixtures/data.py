import pytest


@pytest.fixture(scope="session")
def test_username(env_vars: dict) -> str:
    username = env_vars["TEST_USERNAME"]
    return username

@pytest.fixture(scope="session")
def test_password(env_vars: dict) -> str:
    password = env_vars["TEST_PASSWORD"]
    return password