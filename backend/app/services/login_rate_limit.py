from collections import defaultdict, deque
from time import monotonic

from fastapi import HTTPException, Request, status

LOGIN_WINDOW_SECONDS = 5 * 60
MAX_LOGIN_ATTEMPTS = 5
_LOGIN_ATTEMPTS: dict[str, deque[float]] = defaultdict(deque)


def get_login_key(request: Request, email: str) -> str:
    client_host = request.client.host if request.client else "unknown"
    return f"{client_host}:{email.lower()}"


def _prune_attempts(attempts: deque[float], now: float) -> None:
    while attempts and now - attempts[0] > LOGIN_WINDOW_SECONDS:
        attempts.popleft()


def check_login_rate_limit(key: str) -> None:
    now = monotonic()
    attempts = _LOGIN_ATTEMPTS[key]
    _prune_attempts(attempts, now)
    if len(attempts) >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. Please try again later.",
        )


def record_failed_login(key: str) -> None:
    now = monotonic()
    attempts = _LOGIN_ATTEMPTS[key]
    _prune_attempts(attempts, now)
    attempts.append(now)


def clear_failed_logins(key: str) -> None:
    _LOGIN_ATTEMPTS.pop(key, None)
