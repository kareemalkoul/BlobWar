from __future__ import annotations
from enum import Enum


class Color(Enum):
    Red = 0
    Blue = 1
    Black = 2
    Yellow = 3
    Pink = 4
    Bold = 5
    UnderLine = 6
    Green = 7
    Cyan = 8

    def get_code(color: Color) -> str:
        if color == Color.Red:
            return '\033[91m'
        elif color == Color.Blue:
            return '\033[94m'
        elif color == Color.Black:
            return '\033[30m'
        elif color == Color.Yellow:
            return
        elif color == Color.Pink:
            return
        elif color == Color.UnderLine:
            return '\033[4m'
        elif color == Color.Green:
            return '\033[92m'
        elif color == Color.Cyan:
            return '\033[96m'
