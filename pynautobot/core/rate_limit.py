"""Parse the rate limiting headers returned by Nautobot 3.3+."""

from collections.abc import Mapping
from dataclasses import dataclass


def _to_number(value):
    """Convert a header value to an `int` or `float`, or `None` if it is not numeric."""
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return None


def _parse_structured_field(value):
    """Parse the first member of an IETF RateLimit structured field.

    Args:
        value (str): A header value such as `"rest-complexity-cost";r=996;t=60`.

    Returns:
        (tuple[str | None, dict[str, str]]): The policy name and its parameters.
    """
    if not value:
        return None, {}
    parts = [part.strip() for part in value.split(",", 1)[0].split(";")]
    name = parts[0].strip('"') or None
    params = {}
    for part in parts[1:]:
        key, sep, param_value = part.partition("=")
        if sep:
            params[key.strip()] = param_value.strip()
    return name, params


@dataclass(frozen=True)
class RateLimit:
    """Rate limit information reported by Nautobot 3.3+ in REST API response headers.

    Nautobot only sends these headers when rate limiting is set to `report` or `enforce` mode.
    Any value Nautobot did not send, or that could not be parsed, is `None`.

    Attributes:
        policy (str): Name of the rate limit policy, from `RateLimit` or `RateLimit-Policy`.
        quota (int | float): Total budget per window (`q` in `RateLimit-Policy`).
        window (int | float): Length of the budget window in seconds (`w` in `RateLimit-Policy`).
        remaining (int | float): Budget remaining in the current window (`r` in `RateLimit`).
        reset (int | float): Seconds until the current window resets (`t` in `RateLimit`).
        cost (int | float): Estimated cost of the request (`X-Nautobot-Cost`).
        retry_after (int): Seconds to wait before retrying a throttled request (`Retry-After`).

    Examples:
        >>> nb.dcim.devices.all()
        >>> nb.rate_limit.remaining
        996
        >>> try:
        ...     nb.dcim.devices.all()
        ... except pynautobot.RequestError as e:
        ...     if e.rate_limit and e.rate_limit.retry_after:
        ...         time.sleep(e.rate_limit.retry_after)
    """

    policy: str | None = None
    quota: float | None = None
    window: float | None = None
    remaining: float | None = None
    reset: float | None = None
    cost: float | None = None
    retry_after: int | None = None

    @classmethod
    def from_headers(cls, headers):
        """Build a `RateLimit` from HTTP response headers.

        Args:
            headers (Mapping): The response headers, such as `requests.Response.headers`.

        Returns:
            (RateLimit | None): The parsed rate limit information, or `None` when the response
                carries none of the `RateLimit`, `RateLimit-Policy`, `X-Nautobot-Cost` or `Retry-After`
                headers (Nautobot before 3.3, or rate limiting turned off).
        """
        if not isinstance(headers, Mapping):
            return None

        rate_limit = headers.get("RateLimit")
        policy = headers.get("RateLimit-Policy")
        cost = headers.get("X-Nautobot-Cost")
        retry_after = headers.get("Retry-After")
        if rate_limit is None and policy is None and cost is None and retry_after is None:
            return None

        state_name, state = _parse_structured_field(rate_limit)
        policy_name, policy_params = _parse_structured_field(policy)
        retry_after_seconds = _to_number(retry_after)

        return cls(
            policy=state_name or policy_name,
            quota=_to_number(policy_params.get("q")),
            window=_to_number(policy_params.get("w")),
            remaining=_to_number(state.get("r")),
            reset=_to_number(state.get("t")),
            cost=_to_number(cost),
            retry_after=retry_after_seconds if isinstance(retry_after_seconds, int) else None,
        )
