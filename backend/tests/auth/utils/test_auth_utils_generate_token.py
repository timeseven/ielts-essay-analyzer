from datetime import datetime, timezone

import jwt
import pytest

from app.auth.utils import generate_token


@pytest.mark.asyncio
async def test_auth_utils_generate_token():
    """
    Test that generate_token returns a valid JWT token.

    - Test that the token is a string
    - Test that the expires_at datetime is timezone-aware
    - Test that the contents of the decoded token match the input
    - Test that the expires_at datetime is close to the exp in the decoded token
    """
    token_type = "access_token"
    secret_key = "supersecret"
    algorithm = "HS256"
    expires_minutes = 10
    client_id = "test_client"
    user_id = "test_user"

    token, expires_at = await generate_token(token_type, secret_key, algorithm, expires_minutes, client_id, user_id)

    assert isinstance(token, str)
    assert isinstance(expires_at, datetime)
    assert expires_at.tzinfo is not None  # timezone-aware

    # decode to check contents
    decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
    assert decoded["client_id"] == client_id
    assert decoded["user_id"] == user_id
    assert decoded["type"] == token_type

    # check if expires_at is close to exp in decoded token
    exp_from_token = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    delta = abs((expires_at - exp_from_token).total_seconds())
    assert delta < 2  # allow minor delay difference
