from config import Config
from enums.level import Level
from enums.play import Play
from enums.turn import Turn
from enums.type_player import PlayerType
from game.state import State


class Game:
    def __init__(self, config: Config) -> None:
        self.config = config
        size = config.size
        turn_first = config.turn_first
        self.state = State(turn=turn_first, size=size)

    def playing(self):
        """
        start play
        """
        level = Config.getInstance().get_level()
        state = self.state
        player1 = self.config.player1_type
        player2 = self.config.player2_type
        state.print_info()
        while not state.is_finish():
            turn = state.turn
            player_type = player1 if turn == Turn.Player1 else player2
            if player_type == PlayerType.Human:
                cell1, cell2 = self.input(turn)
                try:
                    state.play(cell1, cell2)
                except:
                    print("error raise")
            else:
                # must by use min max
                v, state = self.max_min_alpha_beta(state, level, turn)
            state.print_info()

        print("player win {0}".format(self.state.turn._value_+1))

    def input(self, turn: Turn):
        # print("turn player : {0}".format(turn._value_+1))
        print("turn player : ", end="")
        self.state.print(Config.getInstance().get_blobcolor(
            turn), "{0}".format(turn._value_+1))
        print("blob you are want move it:", end=" ")
        x1 = int(input("column :"))
        y1 = int(input("row :"))
        cell1 = (x1, y1)
        print("to :", end=" ")
        x2 = int(input("column :"))
        y2 = int(input("row :"))
        cell2 = (x2, y2)
        return cell1, cell2

    def max_min_alpha_beta(self, state: State, level, turn: Turn, alpha=float('-inf'), beta=float('inf'), state_player: Play = Play.Max):
        state_win: State = None
        last_one_played = state.get_last_player_played()
        if state.win():
            if state_player == Play.Max:
                # this condition mean the player who is win is the Opponent
                # beacause the orginal player want play max
                value = -1000
                return value, state
            else:
                # this condition mean the player who is win is the orginal player
                # beacause the orginal player want this round play min
                value = +1000
                return value, state
        elif level == 0:
            return state.evolution(turn), state
        elif state.is_finish():
            return state.evolution(turn), state

        if state_player == Play.Min:
            value = float('inf')
            for temp in state.next_states():
                num, t = self.max_min_alpha_beta(
                    temp, level-1, turn, alpha, beta, Play.Max)
                if num < value:
                    value = num
                    state_win = temp

                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return value, state_win
        else:
            # Play.Max
            value = float('-inf')
            for temp in state.next_states():
                num, t = self.max_min_alpha_beta(
                    temp, level-1, turn, alpha, beta, Play.Min)
                if num > value:
                    value = num
                    state_win = temp
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        break
            beta = value
            return value, state_win
