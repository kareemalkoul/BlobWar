from enum import Enum


class Play(Enum):
    Max = 0
    Min = 1

    @classmethod
    def change(cls, play):
        return Play.Max if play == Play.Min else Play.Min
