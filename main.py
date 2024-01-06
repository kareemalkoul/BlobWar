from config import Config
from enums.color import Color
from enums.level import Level
from enums.turn import Turn
from enums.type_player import PlayerType
from game.game import Game


def main():
    c = Config(Color.Red, Color.Blue, 6, Turn.Player1,
               Level.Normal, PlayerType.Human, PlayerType.Computer)
    game = Game(c)
    game.playing()

    # game.state.play((0, 0), (1, 1))
    # game.state.print_info()

    # for i in game.state.next_states():
    #     i.print_info()


if __name__ == "__main__":
    main()
