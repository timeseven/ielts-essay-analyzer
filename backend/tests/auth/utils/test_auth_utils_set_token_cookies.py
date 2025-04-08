from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

from app.auth.utils import set_token_cookies


def test_set_token_cookies_sets_both_tokens():
    """
    Verify that set_token_cookies sets both access_token and refresh_token as HTTP only cookies
    with the correct values, path, domain, httponly, secure, samesite, and expires.
    """
    mock_response = MagicMock()
    access_token = "access123"
    refresh_token = "refresh456"
    access_expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    refresh_expires = datetime.now(timezone.utc) + timedelta(days=7)

    set_token_cookies(
        response=mock_response,
        access_token=access_token,
        access_expires_at=access_expires,
        refresh_token=refresh_token,
        refresh_expires_at=refresh_expires,
    )

    # Verify if access_token is set in cookie
    mock_response.set_cookie.assert_any_call(
        key="access_token",
        value=access_token,
        path="/",
        domain=None,
        httponly=True,
        secure=True,
        samesite="lax",
        expires=access_expires,
    )

    # Verify if refresh_token is set in cookie
    mock_response.set_cookie.assert_any_call(
        key="refresh_token",
        value=refresh_token,
        path="/",
        domain=None,
        httponly=True,
        secure=True,
        samesite="lax",
        expires=refresh_expires,
    )

    # Verify that set_cookie was called twice
    assert mock_response.set_cookie.call_count == 2


def test_set_token_cookies_skips_none_tokens():
    """
    Test that `set_token_cookies` does not set cookies when tokens are None.

    Verifies that when both access and refresh tokens and their expiration dates
    are None, the `set_cookie` method on the response object is not called.
    """
    mock_response = MagicMock()

    set_token_cookies(
        response=mock_response,
        access_token=None,
        access_expires_at=None,
        refresh_token=None,
        refresh_expires_at=None,
    )

    mock_response.set_cookie.assert_not_called()
