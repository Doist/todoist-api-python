from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, TypeAlias, cast
from urllib.parse import urlsplit, urlunsplit

import httpx

JSONValue = dict[str, object] | list[object] | str | int | float | bool | None
Matcher: TypeAlias = Callable[[httpx.Request], object]

_UNSET = object()


@dataclass
class _Expectation:
    method: str
    url: str
    status: int
    json: JSONValue
    has_json: bool
    matchers: list[Matcher]
    calls: int = 0


class RequestsMock:
    """responses-like matcher built on top of respx routing."""

    def __init__(self, router: object) -> None:
        """Initialize the request mock and install a catch-all HTTP handler."""
        self._router = cast("Any", router)
        self._expectations: list[_Expectation] = []
        self.calls: list[httpx.Request] = []
        self._router.route().mock(side_effect=self._handle_request)

    def add(
        self,
        method: str,
        url: str,
        *,
        json: JSONValue | object = _UNSET,
        status: int = 200,
        match: list[Matcher] | None = None,
    ) -> None:
        response_json: JSONValue = None if json is _UNSET else cast("JSONValue", json)

        self._expectations.append(
            _Expectation(
                method=method,
                url=url,
                status=status,
                json=response_json,
                has_json=json is not _UNSET,
                matchers=match or [],
            )
        )

    def assert_all_called(self) -> None:
        pending = [
            f"{expectation.method} {expectation.url}"
            for expectation in self._expectations
            if expectation.calls == 0
        ]
        if len(pending) > 0:
            raise AssertionError(
                f"Not all expected requests were made. Pending expectations: {pending}"
            )

    def _handle_request(self, request: httpx.Request) -> httpx.Response:
        request_url = _strip_query(str(request.url))

        for expectation in self._expectations:
            if request.method != expectation.method or request_url != expectation.url:
                continue

            if _match_request(expectation.matchers, request) is False:
                continue

            expectation.calls += 1
            self.calls.append(request)

            if expectation.has_json:
                return httpx.Response(
                    status_code=expectation.status,
                    json=expectation.json,
                    request=request,
                )

            return httpx.Response(status_code=expectation.status, request=request)

        raise AssertionError(f"Unexpected request: {request.method} {request.url}")


def _match_request(matchers: list[Matcher], request: httpx.Request) -> bool:
    try:
        for matcher in matchers:
            matcher(request)
    except AssertionError:
        return False

    return True


def _strip_query(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
