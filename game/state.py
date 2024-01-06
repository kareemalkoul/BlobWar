from __future__ import annotations
from typing import List, Tuple
from config import Config
from enums.color import Color
from enums.turn import Turn
from enums.type_player import PlayerType
from copy import deepcopy


class State:
    """
    A class for define state of game

    ...

    Attributes
    ----------
    - turn -> Turn :
        the current turn for which one of players
    - size -> int :
        size of the board
    - fill -> int :
        number of cells which fill it for initlaiz state is 4 (2 piece for each player)
    - board -> list :
        content of board
    - player_blobs -> int :
        num of blob in initlaiz
    """

    def __init__(self, **kwargs) -> None:
        default_values = {
            "turn": Turn.Player1,
            "size": 8,
            "fill": 4,
            "player2_blobs": 4,
            "player1_blobs": 4,
            "board": None
        }
        self.__dict__.update(default_values)
        self.__dict__.update(kwargs)
        self.son = None
        if not self.board:
            self.__create_board__()

    def __create_board__(self):
        """
        create board depaned on self.size
        """
        size = self.size
        self.board = [["#"]*size for _ in range(size)]
        self.fill = self.player1_blobs+self.player2_blobs
        self.__initilaz_blobs_on_board__()

    def __initilaz_blobs_on_board__(self):
        for i in range(self.fill):
            if i % 2 == 0:
                # player1
                # num blob for player1
                num_blobs = (i/2) .__floor__()
                x = (num_blobs/2).__floor__()
                y = 0 if num_blobs % 2 == 0 else -1
                cell = (x, y)
                self.put_blob(cell, Turn.Player1)
            else:
                # player2
                # num blob for player2
                num_blobs = (i/2).__floor__()
                x = -(num_blobs/2).__floor__()-1
                y = 0 if num_blobs % 2 == 0 else -1
                cell = (x, y)
                self.put_blob(cell, Turn.Player2)

    def __print_board__(self):
        board = self.board
        size = self.size
        width_board = 4*size+1
        print(width_board*"-")
        for row in board:
            self.__print_row__(row)
            print(width_board*"-")

    def print_info(self):
        """
        print the board with informaion (cells fill it ,player1_blobs,player2_blobs,the board)
        """
        player1_color = Config.getInstance().get_blobcolor(Turn.Player1)
        player2_color = Config.getInstance().get_blobcolor(Turn.Player2)
        self.print(player1_color, "player 1 blobs : {0}".format(
            self.player1_blobs))
        self.print(player2_color, "player 2 blobs : {0}".format(
            self.player2_blobs))
        self.print(Color.Green, self.evolution(self.get_last_player_played()).__str__() + " player" +
                   self.get_num_player().__str__())
        self.__print_board__()

    def put_blob(self, cell: tuple, player: Turn):
        """
        cell must by (x,y) whereas x=column , y=row and start from up left corner
        """
        column = cell[0]
        row = cell[1]
        num = 1 if player == Turn.Player1 else 2
        # board[row][column]
        self.board[row][column] = f"{num}"

    def next_states(self) -> List[State]:
        """
        return next states available for all blobs
        """
        next_states = []
        blob_cells = self.blobs_on_board()
        for blob_cell in blob_cells:
            next_states_for_one_blob = self.next_states_for_one_blob(blob_cell)
            for state in next_states_for_one_blob:
                next_states.append(state)
        return next_states

    def play(self, bolb_cell: tuple, to_cell: tuple):
        """
        This function move the blob to anthor cell :
        1. if this cell far away a one step  create a blob for this player.
        2. if this cell far away a two step  move the blob for this player.

        then controll in around of this cell
        and change the turn to the other player
        """
        steps = self.length(bolb_cell, to_cell)
        if steps == 2:
            self.move_blob(bolb_cell, to_cell)
        elif steps == 1:
            self.create_blob(to_cell)
        elif steps == 0:
            raise Exception(
                "this step invalid is it the same cell actually no movement")
        self.controll(to_cell)
        self.change_turn()

    def controll(self, cell):
        """
        this function to controll blobs in around
        """
        column = cell[0]
        row = cell[1]
        turn = self.turn
        blobs_contolled = 0
        board = self.board
        blob_num = "1" if self.turn == Turn.Player1 else "2"
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.is_vaild_step(row+i, column+j) and blob_num != board[row+i][column+j] and board[row+i][column+j] != "#":
                    blobs_contolled += 1
                    board[row+i][column+j] = blob_num
        if blob_num == "1":
            self.player1_blobs += blobs_contolled
            self.player2_blobs -= blobs_contolled
        else:
            self.player2_blobs += blobs_contolled
            self.player1_blobs -= blobs_contolled

    def create_blob(self, cell: tuple):
        """
        this function for create blob for current player
        """
        turn = self.turn
        if turn == Turn.Player1:
            self.player1_blobs += 1
        else:
            self.player2_blobs += 1
        self.put_blob(cell, turn)

    def move_blob(self, from_cell: tuple, to_cell: tuple):
        """
        this fnction for move blob from cell to another
        """
        column = from_cell[0]
        row = from_cell[1]
        num = self.board[row][column]
        self.board[row][column] = "#"
        turn = Turn.Player1 if num == "1" else Turn.Player2 if num == "2" else Exception(
            "This is a empty cell")
        if not self.check_turn(turn):
            raise Exception("this blob not for player {0}".format(turn))
        self.put_blob(to_cell, turn)

    def is_vaild(self, cell: tuple):
        """
        check if the cell is empty or not and in board
        """
        column = cell[0]
        row = cell[1]
        if self.is_vaild_step(row, column) and self.board[row][column] == '#':
            return True
        return False

    def print(self, color: Color, char, **kwarg):
        color_code = Color.get_code(color)
        end_color = "\033[0m"
        print(color_code+char+end_color, **kwarg)

    def __print_row__(self, row):
        print(end='| ')
        for i in row:
            # color = Config.getInstance().get_blobcolor(Turn.Player1) if i == "1" else Config.getInstance().get_blobcolor(
            #     Turn.Player2) if i == "2" else Color.Black
            color = Config.getInstance().get_blobcolor(i)
            self.print(color=color, char=(
                i if i != "#" else ' '), end=' | ')
        print()

    def is_filled(self):
        """
        this function for check if board filled or not
        """
        player1_blobs = self.player1_blobs
        player2_blobs = self.player2_blobs
        size = self.size
        if size**2 == (player1_blobs+player2_blobs):
            return True
        return False

    def is_finish(self) -> bool:
        """
        This function check if the players are finished by
            win one of them or filled the board
        """
        finish = True if self.win() else False
        return finish

    def win(self):
        """
        This function return who's win
        and return false is no win
        """
        player1_blobs = self.player1_blobs
        player2_blobs = self.player2_blobs
        if player1_blobs == 0:
            return Turn.Player2
        elif player2_blobs == 0:
            return Turn.Player1
        elif self.is_filled():
            return Turn.Player1 if player1_blobs > player2_blobs else Turn.Player2 if player1_blobs < player2_blobs else None
        return None

    def length(self, t1: tuple, t2: tuple):
        x = abs(t1[0]-t2[0])
        y = abs(t1[1]-t2[1])
        if x == 0 and y == 0:
            return 0
        elif x <= 1 and y <= 1:
            return 1
        elif x <= 2 and y <= 2:
            return 2
        else:
            raise Exception("this step invalid is bigger than 2 ")

    def change_turn(self):
        """
        change turn to the other player
        """
        if self.turn == Turn.Player1:
            self.turn = Turn.Player2
        else:
            self.turn = Turn.Player1

    def check_turn(self, turn: Turn) -> bool:
        """
        this function to check if this turn for this player or not
        """
        return turn == self.turn

    def check_blob(self, blob: str) -> bool:
        """
        check if this blob for current player or not
        """
        turn = self.get_num_player()
        return blob == turn

    def is_vaild_step(self, i, j) -> bool:
        """
        This finction check if the step inside board
        """
        size = self.size
        if size > i and 0 <= i and size > j and 0 <= j:
            return True
        return False

    def blobs_on_board(self) -> List[Tuple]:
        """
        this function return all blobs' cells for current player on the board
        """
        cells = []
        board = self.board
        size = self.size
        blob_num = self.get_num_player()
        for row in range(size):
            for column in range(size):
                if blob_num == board[row][column]:
                    # the tuple must by (x,y)=(column, row)
                    cells.append((column, row))
        return cells

    def get_num_player(self):
        """
        return the current player's number
        """
        return "1" if self.turn == Turn.Player1 else "2"

    def next_states_for_one_blob(self, blob_cell: tuple) -> List[State]:
        """
        return next state of a certain blob
        """
        next_states = []
        column = blob_cell[0]
        row = blob_cell[1]
        for i in range(-2, 3):
            for j in range(-2, 3):
                x = i+column
                y = j+row
                if self.is_vaild((x, y)):
                    to_cell = (x, y)
                    clone = self.__colne__()
                    clone.play(blob_cell, to_cell)
                    next_states.append(clone)
        return next_states

    def __colne__(self) -> State:
        obj = State(turn=self.turn, size=self.size, board=deepcopy(self.board),
                    player2_blobs=self.player2_blobs, player1_blobs=self.player1_blobs, fill=self.fill)
        return obj

    def get_last_player_played(self) -> Turn:
        """
        get the player who played in last round
        """
        cur_turn = self.turn
        return Turn.Player1 if cur_turn == Turn.Player2 else Turn.Player2

    def get_player_turn(self):
        """
        get the player who must play now
        """
        cur_turn = self.turn
        return cur_turn

    def evolution(self, player: Turn) -> int:
        blob1 = self.player1_blobs
        blob2 = self.player2_blobs
        if Turn.Player1 == player:
            return blob1-blob2
        else:
            return blob2-blob1
