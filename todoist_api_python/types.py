from __future__ import annotations

from typing import Annotated

from annotated_types import Predicate

LanguageCode = Annotated[str, Predicate(lambda value: len(value) == 2)]  # noqa: PLR2004

_SUPPORTED_PROJECT_COLORS = (
    "berry_red",
    "red",
    "orange",
    "yellow",
    "olive_green",
    "lime_green",
    "green",
    "mint_green",
    "teal",
    "sky_blue",
    "light_blue",
    "blue",
    "grape",
    "violet",
    "lavender",
    "magenta",
    "salmon",
    "charcoal",
    "grey",
    "taupe",
)

ColorString = Annotated[
    str,
    Predicate(lambda value: value in _SUPPORTED_PROJECT_COLORS),
]
ViewStyle = Annotated[
    str,
    Predicate(lambda value: value in ("list", "board", "calendar")),
]

__all__ = ["ColorString", "LanguageCode", "ViewStyle"]
