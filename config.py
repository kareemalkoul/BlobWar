from __future__ import annotations
from multipledispatch import dispatch
from enums.color import Color
from enums.level import Level
from enums.turn import Turn
from enums.type_player import PlayerType


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    __instance__ = None

    @staticmethod
    def getInstance(**kargs) -> Config:
        """Static Access Method"""
        if not Config.__instance__:
            return Config(**kargs)
        return Config.__instance__

    '''
    @classmethod
    def fromuser(cls):
        player1_bcolor = input("player1_bcolor :")
        player2_bcolor = input("player2_bcolor :")
        size = input("size :")
        player1_type = input("player1_type :")
        player2_type = input("player2_type :")
        turn_first = input("turn_first")
        level = input("level ")
        return cls(player1_bcolor, player2_bcolor: Color,
                 size, turn_first, level,
                 player1_type, player2_type )
    '''

    def __init__(self, player1_bcolor: Color, player2_bcolor: Color,
                 size: int, turn_first: Turn, level: Level,
                 player1_type: PlayerType, player2_type: PlayerType) -> None:
        if not Config.__instance__:
            assert player1_bcolor != player2_bcolor, "must player1 and player2 dont have same color"
            self.player1_bcolor = player1_bcolor
            self.player2_bcolor = player2_bcolor
            self.size = size
            self.player1_type = player1_type
            self.player2_type = player2_type
            self.turn_first = turn_first
            self.level = level
            # print(self.__dict__)
            Config.__instance__ = self
            Config.__init_subclass__ = self.__dict__
        self = Config.__instance__

    @dispatch(Turn)
    def get_blobcolor(self, player_num: Turn) -> Color:
        """
        return color the player's blob
        """
        if player_num == Turn.Player1:
            return self.player1_bcolor
        else:
            return self.player2_bcolor

    @dispatch(str)
    def get_blobcolor(self, player_num: str) -> Color:
        """
        return color the player's blob
        """
        if player_num == "1":
            return self.player1_bcolor
        elif player_num == "2":
            return self.player2_bcolor
        else:
            return Color.Black

    def get_level(self):
        return self.level._value_+1
