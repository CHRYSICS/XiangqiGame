# Project: CS 162 Portfolio Project
# Author: Christopher Eckerson
# Date: 3/12/2020
# Description: This script is a Xiangqi Game, with supporting classes and functions.
#              It includes the main class, XiangqiGame, that manages and initializes the game,
#              starting with red player.  There is a super class of GamePiece, and additional
#              sub-classes game piece classes, represent their unique rules for moving.
#              The XiangqiGame class manages the board progress using a dictionary, where the
#              keys represent the location of pieces and the values are the particular GamePiece
#              class at that location.
#              Locations within the program are stored as tuples of index notation, representing
#              the horizontal and vertical (col, row) positions, starting from the red sides
#              left corner if the board were arranged (as seen from above the board) with the
#              red player as the top and black as the bottom.  Users by default are assumed to use
#              algebraic notation, but have the option with board methods to also use index notation.

#              The main function provides an interactive way to play the game or to test functionality
#              of the program.  This script introduces two exceptions class for handling algebraic
#              notation errors and a class for player name input errors.  The main function 'PLAY' option
#              is supported by some of the display methods found in the XiangqiGame class.


class XiangqiGame:
    """Represents Game of Xiangqi with players, board pieces, and a game state"""

    def __init__(self):
        """Initialize Xiangqi game parameters, set up the game piece"""
        self._game_state = "UNFINISHED"
        self._active_player = "RED"
        self._other_player = "BLACK"
        self._board_dictionary = {}
        self.board_piece_setup()
        self._generals = {"RED": self._board_dictionary[(4, 0)],
                          "BLACK": self._board_dictionary[(4, 9)]}

    def board_piece_setup(self):
        """Sets up board dictionary, where keys are starting locations and GamePieces are values"""
        # Place/initialize player's Cannon GamePieces at starting locations, by index notation (col, row)
        self._board_dictionary[(4, 9)] = General("BLACK", (4, 9))
        self._board_dictionary[(1, 2)] = Cannon("RED", (1, 2))
        self._board_dictionary[(1, 7)] = Cannon("BLACK", (1, 7))
        self._board_dictionary[(7, 2)] = Cannon("RED", (7, 2))
        self._board_dictionary[(7, 7)] = Cannon("BLACK", (7, 7))
        # Create list of GamePiece classes that are found in the back row of each player
        back_row = [Chariot, Horse, Elephant, Advisor, General, Advisor, Elephant, Horse, Chariot]
        # loop through each column on board
        for column in range(9):
            # index = column was added for readability, helps distinguish the different uses of the same value
            index = column
            # For each column, place/initialize the GamePiece class found in the back row for each player
            self._board_dictionary[(column, 0)] = back_row[index]("RED", (column, 0))
            self._board_dictionary[(column, 9)] = back_row[index]("BLACK", (column, 9))
            # for even column values, place/initialize the Solder GamePiece
            if column % 2 == 0:
                # Place/initialize player's Soldier GamePieces at starting locations, by index notation (col, row)
                self._board_dictionary[(column, 3)] = Soldier("RED", (column, 3))
                self._board_dictionary[(column, 6)] = Soldier("BLACK", (column, 6))

    def is_in_check(self, player):
        """takes as parameters 'red' or 'black' and returns True is that player is in check and False otherwise"""
        try:
            # make user input not case-sensitive
            player = player.upper()
            # check that user entered a player name found in Xiangqi Game
            if player == self._active_player or player == self._other_player:
                # get the general owned by the player
                player_general = self._generals[player]
                # get the location of that general
                generals_location = player_general.get_location()
                # look through all locations in current board dictionary
                for location in self._board_dictionary:
                    # get piece at current board location
                    piece = self._board_dictionary[location]
                    # check that piece is not owned by that player
                    if piece.get_player() != player:
                        # piece owned by other player, get the allowed moves for piece
                        piece_moves = piece.allowed_move(self)
                        # look through each move and remove any that would land on a piece of the same team
                        for move in piece_moves:
                            # check if location of move contains a piece
                            if move in self._board_dictionary:
                                # get other piece at that move location
                                other_piece = self._board_dictionary[move]
                                # check if that piece is the same player
                                if other_piece.get_player() == piece.get_player():
                                    # remove move from allowed moves
                                    piece_moves.remove(move)
                                else:
                                    # piece is other player, move allowed
                                    continue
                            else:
                                # move contains no piece, move allowed
                                continue
                        # after removing moves onto same player pieces, check if general location is in allowed moves
                        if generals_location in piece_moves:
                            # piece can capture general with available moves, return True
                            return True
                        else:
                            # piece can not capture general with available moves, go to next piece
                            continue
                    else:
                        # Piece is owned by the player, go to next piece
                        continue
                # no location puts player in check
                return False
            # incorrect player name entered
            else:
                raise InvalidPlayerError
        except InvalidPlayerError:
            print("Invalid Player Parameter: player parameter must be 'red' or 'black', not case-sensitive")

    def is_in_check_mate(self, player):
        """
        Takes in 'red' or 'black' and returns True if player has no more moves and is in checkmate, otherwise False
        """
        try:
            # make user input not case-sensitive
            player = player.upper()
            # check that user entered a player name found in Xiangqi Game
            if player == self._active_player or player == self._other_player:
                # look through all locations in current board dictionary
                for location in self._board_dictionary:
                    # get piece at current board location
                    piece = self._board_dictionary[location]
                    # get the allowed moves for piece
                    piece_moves = piece.allowed_move(self)
                    # check that piece is the players piece
                    if piece.get_player() == player:
                        for move in piece_moves:
                            # check if move in is a position occupied by another piece
                            if move in self._board_dictionary:
                                # location is occupied by another piece
                                other_piece = self._board_dictionary[move]
                                # check if other piece is not the same player
                                if other_piece.get_player() != player:
                                    # piece is other players, save return locations for both pieces
                                    return_location = piece.get_location()
                                    checked_location = other_piece.get_location()
                                    # update pieces and board as if piece is at location
                                    self._board_dictionary[move] = piece
                                    piece.set_location(move)
                                    other_piece.set_location(None)
                                    del self._board_dictionary[return_location]
                                    # check if new location may gets player out of check
                                    if not self.is_in_check(piece.get_player()):
                                        # move does not put player in check, not checkmate
                                        # reset pieces and board
                                        self._board_dictionary[return_location] = piece
                                        piece.set_location(return_location)
                                        self._board_dictionary[checked_location] = other_piece
                                        other_piece.set_location(checked_location)
                                        # There is a piece that can prevent check mate, return False
                                        return False
                                    else:
                                        # player is still in check, return pieces to old location
                                        self._board_dictionary[return_location] = piece
                                        piece.set_location(return_location)
                                        self._board_dictionary[move] = other_piece
                                        other_piece.set_location(move)
                                        # check another player piece
                                        continue
                                else:
                                    # move not allowed, other piece is same team, check another player piece
                                    continue
                            else:
                                # empty location, move piece to location and save return location
                                return_location = piece.get_location()
                                # update piece and board as if piece is at location
                                self._board_dictionary[move] = piece
                                piece.set_location(move)
                                del self._board_dictionary[return_location]
                                # check if new location puts player in check
                                if not self.is_in_check(piece.get_player()):
                                    # move does not put player in check, not checkmate
                                    # reset pieces and board
                                    self._board_dictionary[return_location] = piece
                                    piece.set_location(return_location)
                                    del self._board_dictionary[move]
                                    # There is a piece that can prevent check mate, return False
                                    return False
                                else:
                                    # move puts player in check, return piece to old location
                                    # reset pieces and board
                                    self._board_dictionary[return_location] = piece
                                    piece.set_location(return_location)
                                    del self._board_dictionary[move]
                                    # check another player piece
                                    continue
                # no player pieces has a possible move to escape checkmate
                return True

        except InvalidPlayerError:
            print("Invalid Player Parameter: player parameter must be 'red' or 'black', not case-sensitive")

    def make_move(self, currentPosition, nextPosition):
        """
        Takes the algebraic notation representing locations where piece is from and moving to.
        Checks if game is already over, validates algebraic notation, checks if move is possible,
        and if the moves puts the other player in check. Prints messages to inform the user of the
        action.
        Returns either True if move is allowed, otherwise False.
        """
        # before move, check if player is in check mate
        if self.is_in_check_mate(self._active_player):
            # update game state to other player has won
            self._game_state = self._other_player + "_WON"
            print(self._game_state)
            # move not allowed, return False
            return False

        # before move, check if other player is in check mate
        if self.is_in_check_mate(self._active_player):
            # update game state to other player has won
            self._game_state = self._other_player + "_WON"
            print(self._game_state)
            # move not allowed, return False
            return False

        # if game is already over
        if self._game_state != "UNFINISHED":
            print(self._game_state)
            return False

        # check that locations are in algebraic notation and are on the board
        if self.is_location_on_board(currentPosition) and self.is_location_on_board(nextPosition):
            currentPosition = ConvertAlgebraicNotation(currentPosition)
            nextPosition = ConvertAlgebraicNotation(nextPosition)
        else:
            return False
        # If no piece is at the current position, print message, return False
        if currentPosition not in self._board_dictionary:
            print("current position contains no pieces")
            return False

        # There is a piece at the given current location
        piece = self._board_dictionary[currentPosition]
        # If the piece at current location is not the active player's piece, print message, return False
        if piece.get_player() is not self._active_player:
            print("Incorrect Piece: Location contains a", piece.get_player(), piece.get_pieceName())
            return False
        else:
            print("Selected", piece.get_player(), piece.get_pieceName())

        # get piece's allowed moves
        piece_moves = piece.allowed_move(self)
        if nextPosition in piece_moves:
            # move allowed, check if location is already occupied
            if nextPosition in self._board_dictionary:
                # location is occupied by another piece
                other_piece = self._board_dictionary[nextPosition]
                # check if other piece is not the same player
                if self._active_player != other_piece.get_player():
                    # piece is other players, update pieces and board as if piece is at location
                    self._board_dictionary[nextPosition] = piece
                    piece.set_location(nextPosition)
                    other_piece.set_location(None)
                    del self._board_dictionary[currentPosition]
                    # check if new location puts player in check
                    if not self.is_in_check(self._active_player):
                        # move does not put player in check, update other piece as being captured
                        other_piece.captured()
                        # get name of captured piece for printing
                        captured_piece = other_piece.get_pieceName()
                        # end move, check if move checkmates other player
                        if self.is_in_check_mate(self._other_player):
                            # update game state to other player has won
                            self._game_state = self._active_player + "_WON"
                            print(self._game_state)
                            # move not allowed, return False
                            return True
                        else:
                            # exchange active player and other player
                            new_active_player = self._other_player
                            self._other_player = self._active_player
                            self._active_player = new_active_player
                            print(captured_piece, "was captured")
                            # move allowed, return True
                            return True
                    else:
                        # move puts player in check, return pieces back on board
                        self._board_dictionary[currentPosition] = piece
                        piece.set_location(currentPosition)
                        self._board_dictionary[nextPosition] = other_piece
                        other_piece.set_location(nextPosition)
                        # alert player their general is in check
                        players_general = self._generals[self._active_player]
                        print("Invalid Move:", players_general.get_pieceName(), "would be in check.")
                        # move not allowed, return False
                        return False
                else:
                    # move not allowed, other piece is same team
                    print("Move not allowed: same team")
                    return False
            else:
                # empty location, update pieces and board as if piece is at location
                self._board_dictionary[nextPosition] = piece
                piece.set_location(nextPosition)
                del self._board_dictionary[currentPosition]
                # check if new location puts player in check
                if not self.is_in_check(piece.get_player()):
                    # end move, check if move checkmates other player
                    if self.is_in_check_mate(self._other_player):
                        # update game state to other player has won
                        self._game_state = self._active_player + "_WON"
                        print(self._game_state)
                        # move not allowed, return False
                        return True
                    else:
                        # exchange active player and other player
                        new_active_player = self._other_player
                        self._other_player = self._active_player
                        self._active_player = new_active_player
                        print(piece.get_pieceName(), "was moved")
                        # move allowed, return True
                        return True
                else:
                    # move puts player in check, return piece to old location and delete new, and return False
                    self._board_dictionary[currentPosition] = piece
                    piece.set_location(currentPosition)
                    del self._board_dictionary[nextPosition]
                    # # check if player has any available moves or if they are in checkmate
                    if self.is_in_check_mate(self._active_player):
                        # update game state to other player has won
                        self._game_state = self._other_player + "_WON"
                        print(self._game_state)
                        # move not allowed, return False
                        return False
                    else:
                        # the player is only in check, the move is not allowed but there exists allowed moves
                        players_general = self._generals[self._active_player]
                        print("Invalid Move:", players_general.get_pieceName(), "is in check.")
                        # move not allowed, return False
                        return False
        else:
            # move is not allowed for piece, return False
            print(piece.get_pieceName(), "is not allowed to move there")
            return False

    def piece_at_location(self, location, indexNotation=False):
        """
        Returns GamePiece if at location, taken by default in algebraic notation, else returns None.
        IndexNotation: parameter as True allows user to input index notation tuple instead (col, row)
        """
        # If location given in algebraic notation
        if not indexNotation:
            # check if location is within board boundaries
            if self.is_location_on_board(location):
                # convert algebraic notation into index notation
                location = ConvertAlgebraicNotation(location)
                # check if location contains a board piece
                if location in self._board_dictionary:
                    # get piece at location and return the game piece object
                    piece = self._board_dictionary[location]
                    return piece
                else:
                    # location is not found in board dictionary, no piece found, return None
                    return None
            else:
                # location is not within board boundaries
                return None
        # location is given in index notation
        else:
            # check if location is within board boundaries
            if self.is_location_on_board(location, True):
                # check if location contains a piece in board dictionary
                if location in self._board_dictionary:
                    # get piece at location, return game piece object
                    piece = self._board_dictionary[location]
                    return piece
                else:
                    # location is not found in board dictionary, no piece found, return None
                    return None
            else:
                # location is not within board boundaries
                return None

    def is_location_on_board(self, location, indexNotation=False):
        """
        Returns True if location is within the boundary of the board [10 rows by 9 cols], otherwise False.
        Location by default is assumed to be in algebraic Notation.
        IndexNotation: parameter as True allows user to input index notation tuple instead (col, row)
        """
        # If location is given in index notation
        if indexNotation:
            # get the column and row values from the location
            col, row = location
            # check that the column and row values are within the board boundary
            if 0 <= col <= 8 and 0 <= row <= 9:
                # location is within the board, return True
                return True
            else:
                # location is outside of the board, Return False
                return False
        else:
            # Location is given in algebraic notation
            try:
                # Try to convert input from algebraic Notation into index notation (col, row)
                location = ConvertAlgebraicNotation(location)
                # get the column and row values from the location
                col, row = location
                # check that the column and row values are within the board boundary
                if 0 <= col <= 8 and 0 <= row <= 9:
                    # location is within the board, return True
                    return True
                else:
                    # location is outside of the board, Return False
                    return False
                # if user input is not in correct algebraic notation, raises Exception, print message, return False
            except AlgebraicNotationAlphabetError:
                print("first value of algebraic notation must be an alphabetical value")
                return False
            except AlgebraicNotationDigitError:
                print("second value of algebraic notation must be an integer value")
                return False

    def show_board(self):
        """Displays Xiangqi current instant of the board arrangement onto the console"""
        # print title of board and column values in algebraic notation
        print("Xiangqi board")
        print("     a    b    c    d    e    f    g    h    i")
        # for each row, go through each element and give piece objects a label
        for row in range(0, 10):
            # Start each row with an empty row list
            rowList = []
            for col in range(0, 9):
                # for each element in each row, set temp variable name to piece at location
                position = (col, row)
                if position in self._board_dictionary:
                    # append the symbol associated with each piece class
                    piece = self._board_dictionary[position]
                    symbol = piece.get_pieceSymbol()
                    rowList.append(symbol)
                # For the locations that contain no piece, append a space to rowList
                else:
                    rowList.append(" ")
            # print rowList to the console and move onto next row
            if row < 9:
                # to align board display for row 9 and below, add a space after row number
                print(str(row + 1) + " ", rowList)
            else:
                print(str(row + 1), rowList)

    def show_moves_on_board(self, targetLocation, indexNotation=False):
        """
        Displays current Xiangqi board arrangement and possible moves for piece at targetLocation,
        defaulted to algebraic notation.
        IndexNotation: parameter as True allows user to input index notation tuple instead (col, row)
        """
        # location is in algebraic notation
        if not indexNotation:
            # For locations not within the board boundaries, return without printing board
            if not self.is_location_on_board(targetLocation):
                return
            else:
                # convert algebraic notation to index notation
                targetLocation = ConvertAlgebraicNotation(targetLocation)
        # location is in index notation
        else:
            # For locations not within the board boundaries, return without printing board
            if not self.is_location_on_board(targetLocation, True):
                return

        # check if target location contains a piece
        if targetLocation not in self._board_dictionary:
            # not piece found at location, print error message and return without printing board
            print("no target at location")
            return
        # A piece was found at the location, display board and possible moves
        # print title of board and column values in algebraic notation
        print("Xiangqi board")
        print("     a    b    c    d    e    f    g    h    i")
        # get piece at target location and its allowed moves
        targetGamePiece = self._board_dictionary[targetLocation]
        targets_moves = targetGamePiece.allowed_move(self)
        # initialize a list that will contain any pieces that could be captured
        possible_captures = []
        # for each row, go through each element and give piece objects a label
        for row in range(0, 10):
            # Start each row with an empty row list
            rowList = []
            for col in range(0, 9):
                # for each element in each row, set temp variable name to piece at location
                position = (col, row)
                # if location contains a piece
                if position in self._board_dictionary:
                    # if the location is one of the target pieces allowed moves
                    if position in targets_moves:
                        # get the other piece at this allowed move
                        other_piece = self._board_dictionary[position]
                        # check if the piece is not the same team
                        if targetGamePiece.get_player() != other_piece.get_player():
                            # label a possible capture move with a 'X' symbol on board
                            rowList.append("X")
                            # add other piece to possible captures
                            possible_captures.append(other_piece.get_pieceName())
                        else:
                            # the piece is the same team, get pieces normal symbol
                            symbol = other_piece.get_pieceSymbol()
                            # add symbol to rowList
                            rowList.append(symbol)
                    else:
                        # position is not an allowed move, append the symbol associated with each piece class
                        piece = self._board_dictionary[position]
                        symbol = piece.get_pieceSymbol()
                        rowList.append(symbol)
                # For the locations that contain no piece, append a space to rowList
                else:
                    # if empty location is an allowed move for target, give it a '*' symbol
                    if position in targets_moves:
                        # add possible move symbol to rowList
                        rowList.append("*")
                    else:
                        # location is empty and not an allowed move
                        rowList.append(" ")
            # print rowList to the console and move onto next row
            if row < 9:
                # to align board display for row 9 and below, add a space after row number
                print(str(row + 1) + " ", rowList)
            else:
                print(str(row + 1), rowList)
        # print to console the target piece color, name, and location
        print(targetGamePiece.get_player(), targetGamePiece.get_pieceName(), targetGamePiece.get_location())
        # print possible capture list to console.
        print("Possible captures:", possible_captures)

    def play_game(self, continual_play=False):
        """
        Displays one round played by player, displaying baord, taking in location for making a move,
        and input options to see possible moves and exit method if continual play is set to True
        continual_play: By default, only plays one round, but set to True activates while loop
        """
        while continual_play:
            # print options instructions to console each round
            print("Type HELP anytime to see pieces possible moves or exit")
            # prints current player's turn
            print(self.get_active_player(), "player's turn:")
            # prints a prompt for the first from location in make a move method
            curLocation = input("from: ")
            # check if user instead input the string 'help'
            if curLocation.upper() == 'HELP':
                # for the help options, print exit instructions for play_game
                print("Type EXIT to exit active game")
                # else user is prompted to input the location they would like to display possible moves
                piece_location = input("Else, enter location of piece to see moves:")
                # check if user instead input the string 'exit'
                if piece_location.upper() == 'EXIT':
                    # set continual play to false, then bypass rest of code and jump out of while loop
                    continual_play = False
                    continue
                else:
                    # user input a target location to see possible moves, display moves
                    self.show_moves_on_board(piece_location)
                    # bypass rest of code, restart while loop
                    continue
            else:
                # user has input the from location, prompt user to input to location
                nexLocation = input("To: ")
                # check if input here was the string 'help'
                if nexLocation.upper() is 'HELP':
                    # for the help options, print exit instructions for play_game
                    print("Type EXIT to exit active game")
                    # else user is prompted to input the location they would like to display possible moves
                    piece_location = input("Else, enter location of piece to see moves:")
                    # check if user instead input the string 'exit'
                    if piece_location.upper() == 'EXIT':
                        # set continual play to false, then bypass rest of code and jump out of while loop
                        continual_play = False
                        continue
                    else:
                        # user input a target location to see possible moves, display moves
                        self.show_moves_on_board(piece_location)
                        # bypass rest of code, restart while loop
                        continue
                else:
                    # user input both from and to locations, execute make move method and show board
                    self.make_move(curLocation, nexLocation)
                    self.show_board()
                    # print the current check status of the two players
                    print("red checked:", self.is_in_check("red"))
                    print("black checked:", self.is_in_check("black"))
                    # print the current game state
                    print(self.get_game_state())

    def get_game_state(self):
        """Returns the game state.  It should be either 'UNFINSHED', 'RED_WON', or 'BLACK_WON'"""
        return self._game_state

    def get_active_player(self):
        """Returns the active player whose turn it is"""
        return self._active_player

    def get_other_player(self):
        """Returns the other player of the game"""
        return self._other_player

    def get_players_general(self, player):
        """Takes a player as 'red' or 'black' (not case-sensitive) and returns their General object"""
        try:
            # make user input not case-sensitive
            player = player.upper()
            # check that user entered a player name found in Xiangqi Game
            if player == self._active_player or player == self._other_player:
                # get that players general
                return self._generals[player.upper()]

        except InvalidPlayerError:
            print("Invalid Player Parameter: player parameter must be 'red' or 'black', not case-sensitive")

    def get_board_dictionary(self):
        """Returns the XiangqiGame board dictionary"""
        return self._board_dictionary


class GamePiece:
    """Represents a game piece in Xiangqi with name, player, symbol, location, and capture status"""

    def __init__(self, player, pieceName, symbol, location):
        """Initialize player and location to none until assigned"""
        self._pieceName = pieceName
        self._player = player
        self._symbol = symbol
        self._location = location
        self._captured = False

    def get_pieceSymbol(self):
        """Returns the symbol given to the GamePiece"""
        return self._symbol

    def get_pieceName(self):
        """Returns the name of the GamePiece"""
        return self._pieceName

    def get_location(self):
        """Returns the location of the Gamepiece"""
        return self._location

    def set_location(self, location):
        """Sets location of GamePiece"""
        self._location = location

    def captured(self):
        """Game Piece has been captured, reset location to None and set captured status as True"""
        self._location = None
        self._captured = True

    def is_captured(self):
        """Return True if piece is captured, otherwise False."""
        return self._captured

    def get_player(self):
        """Get player who owns the piece"""
        return self._player

    def set_player(self, player):
        """Set the player who will own the piece"""
        self._player = player


class General(GamePiece):
    """Represents General in Xiangqi, subclass of GamePiece"""

    def __init__(self, player, location):
        """Initialize General as GamePiece with player, name, symbol, and location"""
        super().__init__(player, "general", "G", location)

    def allowed_move(self, GameInstance):
        """
        Takes in a XiangqiGame Instance and returns the index notation of the General's available moves.
        Includes move validation of board boundary and handles board piece collisions
        Parameter: XiangqiGame class instance
        Returns: List of location tuples (col, row) of General's allowed moves
        """
        # get the column and row values from General's location
        col, row = self._location
        # Initialize all the possible move increments the general can make
        moves = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        # Create list of possible moves tuples by adding the current location and move increments together
        possible_moves = [(move[0] + col, move[1] + row) for move in moves]
        # Initialize a list that will store the allowed moves after validating on board
        allowed_moves = []
        # Check if General can perform 'flying general' move
        if self.flying_general(GameInstance):
            # General can perform "flying general', which player is using the general
            if self.get_player() == "RED":
                # get the other general owned by the other player
                other_general = GameInstance.get_players_general("BLACK")
            else:
                # get the other general owned b the other player
                other_general = GameInstance.get_players_general("RED")
            # add the location of the other general to the list of allowed moves
            allowed_moves.append(other_general.get_location())
        # look through each move in possible moves
        for move in possible_moves:
            # check that move is in the palace
            if self.in_palace(move):
                # check if move contains another piece
                if move in GameInstance.get_board_dictionary():
                    # get piece from the move location
                    other_piece = GameInstance.piece_at_location(move, True)
                    # check if piece is not on the same team
                    if other_piece.get_player() != self.get_player():
                        # add the location to the allowed moves list
                        allowed_moves.append(move)
                    else:
                        # move is same team, continue to next move
                        continue
                else:
                    # move is empty, add move to allowed moves
                    allowed_moves.append(move)
            else:
                # move is not an allowed possible move or move is outside of palace
                continue
        # after looking at all moves, return the list of allowed moves as (col, row) values
        return allowed_moves

    def in_palace(self, location):
        """
        Takes in a location in index notation.
        Returns True if location is in the player's palace, otherwise False
        Restriction: does not handle algebraic notation
        """
        # get the column and row values of the location
        col, row = location
        # check if column is within the palace
        if 3 <= col <= 5:
            # check if player is red and row is within the red palace
            if self._player is "RED" and 0 <= row <= 2:
                # piece is in their palace
                return True
            # check if player is black and row is within the black palace
            elif self._player is "BLACK" and 7 <= row <= 9:
                # piece is in their palace
                return True
            else:
                # if not within the palace or not that player's palace
                return False
        else:
            # piece is not in palace
            return False

    def flying_general(self, GameInstance):
        """
        Takes in a XiangqiGame object instance, returns True if general can capture other general, otherwise False.
        """
        # check if General is owned by red player
        if self.get_player() == "RED":
            # gets black player's general
            other_general = GameInstance.get_players_general("BLACK")
        # Assumes General is owned by black player
        else:
            # gets red player's general
            other_general = GameInstance.get_players_general("RED")
        # get the column and row value of both of the generals
        checkCol, checkRow = other_general.get_location()
        curCol, curRow = self.get_location()
        # Checks which direction the check is being done by, in this case going from red side to black
        if curRow < checkRow:
            # initializes path variables for path from red general
            direction = 1
            start = curRow + direction
            end = checkRow + direction
        # check which direction the check is being done by, in this case going from black side to red
        else:
            # initializes path variables for path from black general
            direction = -1
            start = curRow + direction
            end = checkRow + direction
        # look along the path of the general to the other general
        for path in range(start, end, direction):
            # set a location along the path towards the other general as a tuple
            location = (curCol, path)
            # check if there is a piece between generals on the path
            if location in GameInstance.get_board_dictionary():
                # check if the location that contains a piece is the location of the other general
                if location != other_general.get_location():
                    # location is not the other general, path is blocked, return False
                    return False
                else:
                    # location is the other general, path is clear, return True
                    return True
            else:
                # location is empty, continue along path
                continue


class Advisor(GamePiece):
    """Represents Advisor in Xiangqi, subclass of GamePiece"""

    def __init__(self, player, location):
        """Initialize Advisor as GamePiece with player, name, symbol, and location"""
        super().__init__(player, "advisor", "A", location)

    def allowed_move(self, GameInstance):
        """
        Takes in a XiangqiGame Instance and returns the index notation of the Advisor's available moves.
        Includes move validation of board boundary and handles board piece collisions
        Parameter: XiangqiGame class instance
        Returns: List of location tuples (col, row) of Advisor's allowed moves
        """
        # get the column and row values from advisor's location
        col, row = self._location
        # Initialize all the possible move increments the advisor can make
        moves = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
        # Create list of possible moves tuples by adding the current location and move increments together
        possible_moves = [(move[0] + col, move[1] + row) for move in moves]
        # Initialize a list that will store the allowed moves after validating on board
        allowed_moves = []
        # look through each move in possible moves
        for move in possible_moves:
            # check that move is in the palace
            if self.in_palace(move):
                # check if move contains another piece
                if move in GameInstance.get_board_dictionary():
                    # get the piece at the move location
                    other_piece = GameInstance.piece_at_location(move, True)
                    # check if piece is not on the same team
                    if other_piece.get_player() != self.get_player():
                        # add the location to the allowed moves list
                        allowed_moves.append(move)
                    else:
                        # move is same team, continue to next move
                        continue
                else:
                    # move is empty, add move to allowed moves
                    allowed_moves.append(move)
            else:
                # move is not an allowed possible move or move is outside of palace
                continue
        # after looking at all moves, return the list of allowed moves as (col, row) values
        return allowed_moves

    def in_palace(self, location):
        """
        Takes in a location in index notation.
        Returns True if location is in the player's palace, otherwise False
        Restriction: does not handle algebraic notation
        """
        # get the column and row values of the location
        col, row = location
        # check if column is within the palace
        if 3 <= col <= 5:
            # check if player is red and row is within the red palace
            if self._player is "RED" and 0 <= row <= 2:
                # piece is in their palace
                return True
            # check if player is black and row is within the black palace
            elif self._player is "BLACK" and 7 <= row <= 9:
                # piece is in their palace
                return True
            else:
                # if not within the palace or not that player's palace
                return False
        else:
            # piece is not in palace
            return False


class Elephant(GamePiece):
    """Represents Elephant in Xiangqi, subclass of GamePiece"""

    def __init__(self, player, location):
        """Initialize Elephant as GamePiece with player, name, symbol, and location"""
        super().__init__(player, "elephant", "E", location)

    def allowed_move(self, GameInstance):
        """
        Takes in a XiangqiGame Instance and returns the index notation of the Elephant's available moves.
        Includes move validation of board boundary and handles board piece collisions
        Parameter: XiangqiGame class instance
        Returns: List of location tuples (col, row) of Elephant's allowed moves
        """
        # get the column and row values from elephant's location
        col, row = self._location
        # Initialize all the possible move increments the elephant can make
        moves = [[2, 2], [2, -2], [-2, -2], [-2, 2]]
        # Initialize all blocker directions increments
        directions = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
        # Create list of possible moves tuples by adding the current location and move increments together
        possible_moves = [(move[0] + col, move[1] + row) for move in moves]
        # Create list of blocker location tuples by adding the current location and direction increments together
        blocker_locations = [(direction[0] + col, direction[1] + row) for direction in directions]
        # Initialize a list that will store the allowed moves after validating on board
        allowed_moves = []
        # look through each direction that the elephant can move and check if blocked
        for direction in range(4):
            # get move in that direction
            move = possible_moves[direction]
            # check if direction is not blocked by a piece at location in that direction
            if blocker_locations[direction] not in GameInstance.get_board_dictionary():
                # check if move contains another piece
                if GameInstance.is_location_on_board(move, True):
                    # check if the location contains a piece
                    if move in GameInstance.get_board_dictionary():
                        # get the piece at the move location
                        other_piece = GameInstance.piece_at_location(move, True)
                        # check if piece is not on the same team
                        if other_piece.get_player() != self.get_player():
                            # add the location to the allowed moves list
                            allowed_moves.append(possible_moves[direction])
                        else:
                            # location is the same team, continue to next move
                            continue
                    else:
                        # move is empty, add to allowed moves
                        allowed_moves.append(possible_moves[direction])
                else:
                    # move not within boundary, continue
                    continue

            else:
                # direction is blocked, continue to next move
                continue
        # after looking at all moves, return the list of allowed moves as (col, row) values
        return allowed_moves


class Horse(GamePiece):
    """Represents Horse in Xiangqi, subclass of GamePiece"""

    def __init__(self, player, location):
        """Initialize Horse as GamePiece with player, name, symbol, and location"""
        super().__init__(player, "horse", "H", location)

    def allowed_move(self, GameInstance):
        """
        Takes in a XiangqiGame Instance and returns the index notation of the Horse's available moves.
        Includes move validation of board boundary and handles board piece collisions
        Parameter: XiangqiGame class instance
        Returns: List of location tuples (col, row) of Horse's allowed moves
        """
        # get the column and row values from horse's location
        col, row = self._location
        # Initialize all the possible move increments the horse can make
        moves = [[-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1]]
        # Initialize all blocker directions increments
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        # Create list of possible moves tuples by adding the current location and move increments together
        possible_moves = [(move[0] + col, move[1] + row) for move in moves]
        # Create list of blocker location tuples by adding the current location and direction increments together
        blocker_locations = [(direction[0] + col, direction[1] + row) for direction in directions]
        # Initialize a list that will store the allowed moves after validating on board
        allowed_moves = []
        # look through each direction that the horse can move and check if blocked
        for direction in range(4):
            # get the two moves in that direction that the horse can make
            moves_in_direction = possible_moves[:2]
            # check if direction is not blocked by a piece at location in that direction
            if blocker_locations[direction] not in GameInstance.get_board_dictionary():
                # For each move in that direction, check if move contains a piece
                for move in moves_in_direction:
                    # check if move on the board
                    if GameInstance.is_location_on_board(move, True):
                        # check if the location contains a piece
                        if move in GameInstance.get_board_dictionary():
                            # get the piece at the move location
                            other_piece = GameInstance.piece_at_location(move, True)
                            # check if piece is not on the same team
                            if other_piece.get_player() != self.get_player():
                                # add the location to the allowed moves list
                                allowed_moves.append(move)
                            else:
                                # piece is same team, continue to next move
                                continue
                        else:
                            # move is empty, add to allowed moves
                            allowed_moves.append(move)
                    else:
                        # move not within board boundary
                        continue
                    # Once the move in a direction have been checked, remove them from the possible moves
                    possible_moves = possible_moves[2:]
            else:
                # Moves are blocked in direction, remove them from the possible moves
                possible_moves = possible_moves[2:]
        # after looking at all moves, return the list of allowed moves as (col, row) values
        return allowed_moves


class Chariot(GamePiece):
    """Represents Chariot in Xiangqi, subclass of GamePiece"""

    def __init__(self, player, location):
        """Initialize Chariot as GamePiece with player, name, symbol, and location"""
        super().__init__(player, "chariot", "C", location)

    def allowed_move(self, GameInstance):
        """
        Takes in a XiangqiGame Instance and returns the index notation of the Chariot's available moves.
        Includes move validation of board boundary and handles board piece collisions
        Parameter: XiangqiGame class instance
        Returns: List of location tuples (col, row) of Chariot's allowed moves
        """
        # get the column and row values from chariot's location
        col, row = self._location
        # Initialize all the possible move increments the chariot can make
        moves = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        # Create list of possible moves tuples by adding the current location and move increments together
        possible_moves = [(move[0] + col, move[1] + row) for move in moves]
        # Initialize a list that will store the allowed moves after validating on board
        allowed_moves = []
        # look through each direction that the chariot can move
        for direction in range(4):
            # get move and the next move increment in that direction
            move = possible_moves[direction]
            motion_vector = moves[direction]
            # Initialize continue moving variable for checking moves in a given direction
            continue_moving = True
            # For a given direction, check if move is allowed
            # increment to next location in that direction until Chariot has a collision
            while continue_moving:
                # check if location is within the boundary of the board
                if GameInstance.is_location_on_board(move, True):
                    # check if the location contains a piece
                    if move in GameInstance.get_board_dictionary():
                        # get piece at that location
                        other_piece = GameInstance.piece_at_location(move, True)
                        # check if piece is not on the same team
                        if other_piece.get_player() != self.get_player():
                            # include opponents location to allowed moves list
                            allowed_moves.append(move)
                            # Chariot can't go any further, set continue moving to False
                            continue_moving = False
                        else:
                            # The piece is the same team, Chariot can't go any further, set continue moving to False
                            continue_moving = False
                    else:
                        # location is empty, add location to allowed moves
                        allowed_moves.append(move)
                        # update move to next location in that direction by using the increment move
                        curCol, curRow = move
                        move = (curCol + motion_vector[0], curRow + motion_vector[1])
                else:
                    # The move has reach the end of the board, Chariot can't go further, set continue mocing to False
                    continue_moving = False
        # after looking at all moves, return the list of allowed moves as (col, row) values
        return allowed_moves


class Cannon(GamePiece):
    """Represents Cannon in Xiangqi, subclass of GamePiece"""

    def __init__(self, player, location):
        """Initialize Cannon as GamePiece with player, name, symbol, and location"""
        super().__init__(player, "cannon", "O", location)

    def allowed_move(self, GameInstance):
        """
        Takes in a XiangqiGame Instance and returns the index notation of the Cannon's available moves.
        Includes move validation of board boundary and handles board piece collisions
        Parameter: XiangqiGame class instance
        Returns: List of location tuples (col, row) of Cannon's allowed moves
        """
        # get the column and row values from cannon's location
        col, row = self._location
        # Initialize all the possible move increments the cannon can make
        moves = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        # Create list of possible moves tuples by adding the current location and move increments together
        possible_moves = [(move[0] + col, move[1] + row) for move in moves]
        # Initialize a list that will store the allowed moves after validating on board
        allowed_moves = []
        # look through each direction that the cannon can move
        for direction in range(4):
            # get move and the next move increment in that direction
            move = possible_moves[direction]
            motion_vector = moves[direction]
            # Initialize continue moving variable for checking moves in a given direction
            continue_moving = True
            # Initialize the jump variable for setting state of capturing
            has_jumped = False
            # For a given direction, check if move is allowed
            # increment to next location in that direction until cannon has a collision, then find capture, if any
            while continue_moving:
                # check if location is within the boundary of the board
                if GameInstance.is_location_on_board(move, True):
                    # check if cannon has jumped over another piece yet
                    if has_jumped:
                        # check if the location contains a piece
                        if move in GameInstance.get_board_dictionary():
                            # get piece at that location
                            other_piece = GameInstance.piece_at_location(move, True)
                            # check if piece is not on the same team
                            if self.get_player() != other_piece.get_player():
                                # include opponents location to allowed moves list
                                allowed_moves.append(move)
                                # Cannon can't go any further, set continue moving to False
                                continue_moving = False
                            else:
                                # The piece is the same team, Cannon can't go any further, set continue moving to False
                                continue_moving = False
                        else:
                            # increment move, continue to look if the cannon has a capture location
                            move = (move[0] + motion_vector[0], move[1] + motion_vector[1])
                    else:
                        # Cannon has not jumped, check if move contains a piece
                        if move in GameInstance.get_board_dictionary():
                            # piece to jump off, set to True
                            has_jumped = True
                            # increment move, continue now to look if the cannon has capture location
                            move = (move[0] + motion_vector[0], move[1] + motion_vector[1])
                        else:
                            # the space is empty, add to allowed moves
                            allowed_moves.append(move)
                            # increment move in that direction
                            move = (move[0] + motion_vector[0], move[1] + motion_vector[1])
                else:
                    # cannon has reached end of board, set continue moving to False
                    continue_moving = False
        # after looking at all moves, return the list of allowed moves as (col, row) values
        return allowed_moves


class Soldier(GamePiece):
    """Represents Soldier in Xiangqi, subclass of GamePiece"""

    def __init__(self, player, location):
        """Initialize Soldier as GamePiece with player, name, symbol, and location"""
        super().__init__(player, "soldier", "S", location)

    def allowed_move(self, GameInstance):
        """
        Takes in a XiangqiGame Instance and returns the index notation of the Soldier's available moves.
        Includes move validation of board boundary and handles board piece collisions
        Parameter: XiangqiGame class instance
        Returns: List of location tuples (col, row) of Soldier's allowed moves
        """
        # get the column and row values from Soldier's location
        curCol, curRow = self.get_location()
        # Initialize all the possible move increments the soldier can make
        moves = [[0, 1], [1, 0], [-1, 0], [0, -1]]
        # Initialize a list that will store the allowed moves after validating on board
        allowed_moves = []
        # check who owns the piece
        if self.get_player() is "RED":
            # if soldier has passed the river, give more moves
            if curRow > 4:
                moves = moves[:3]
            else:
                # else soldier can only move in one direction
                moves = [moves[0]]
        if self.get_player() is "BLACK":
            # if soldier has passed the river, give move moves
            if curRow < 5:
                moves = moves[1:]
            else:
                # else soldier can only moves in one direction
                moves = [moves[3]]
        # Create list of possible moves tuples by adding the current location and move increments together
        possible_moves = [(move[0] + curCol, move[1] + curRow) for move in moves]
        # look through each move to see if allowed
        for move in possible_moves:
            # check if move is on the board
            if GameInstance.is_location_on_board(move, True):
                # check if move contains another piece
                if move in GameInstance.get_board_dictionary():
                    # get piece at location
                    other_piece = GameInstance.piece_at_location(move, True)
                    # check that other piece is not on the same team
                    if self.get_player() != other_piece.get_player():
                        # add move to allowed moves
                        allowed_moves.append(move)
                    else:
                        # other piece is on same team, go to next move
                        continue
                else:
                    # location is empty, add to allowed moves
                    allowed_moves.append(move)
            else:
                # lcoation is not within the board boudaries, go to next move
                continue
        return allowed_moves


def ConvertAlgebraicNotation(location):
    """
    Takes simple algebraic notation (letter/number string only) and Returns column and row index values as a tuple.
    Algebraic Notation example: 'a1' would return (0, 0)"
    """
    # verify input is converted into string
    location = str(location)
    # Set first value as variable storing alphabet coordinate
    letter_coord = location[0]
    # Set rest of values as variable storing number corrdinate
    number_coord = location[1:]
    # check that the letter coordinate is indeed a letter
    if letter_coord.isalpha():
        # convert letter coordinate to column index representation, starting with 'a' = 0, 'b' = 1, ect
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        column = alphabet.index(letter_coord.lower())
    else:
        raise AlgebraicNotationAlphabetError
    # check that the number coordinate only contains digits
    if location[1:].isdigit():
        # convert number coordinate to row index representation, starting with "1" = 0, "2" = 1, ect.
        row = int(number_coord) - 1
    else:
        raise AlgebraicNotationDigitError
    # Return algebraic notation values as a tuple: (column, row)
    return column, row


class AlgebraicNotationAlphabetError(Exception):
    """Raised when first value of algebraic notation for a location is not a alphabet letter"""
    pass


class AlgebraicNotationDigitError(Exception):
    """Raised when number value of algebraic notation for a location is not only digit values"""
    pass


class InvalidPlayerError(Exception):
    """Raised when player parameter is incorrect, must be 'red' or 'black'"""
    pass


def main():
    """Testing functionality"""
    game = XiangqiGame()
    game.show_board()
    print("Type PLAY to see Xiangqi Game")
    make_play = input()
    # not typing play bypasses play option, goes to test code instead
    if make_play.upper() == 'PLAY':
        game.play_game(True)
    # insert other testing code here

    # Designer's temporary test code:
    # removed soldiers temporarily to test in check method
    # game.make_move("d1", "e2")
    # game.make_move("a10", "a9")
    # game.make_move("a1", "a2")
    # game.make_move("a9", "e9")
    # game.make_move("a2", "a3")
    # game.make_move("e9", "e2")
    # says red general is not allowed to move (0, 3)
    # game.make_move("e1", "d1") # make_move also shows location updated before is_in_check when print() inserted
    # print(game.is_in_check("red"))
    # print(game.get_board_dictionary()) # general location is correct in dictionary
    # # says move is not in allowed moves of general, check general attributes
    # general = game.piece_at_location("e1") # match dictionary location
    # print(general.get_location()) # general location matches game board dictionary
    # same_general = game.get_players_general("red") # check program is referring to same object
    # print(general is same_general) # same general object referred to within in_check method
    # print(general.allowed_move(game))  # check allowed moves of general
    # # location "d1" aka (3, 0) is in allowed moves
    # # Note: When make_move happens, it updated board to new location before checking is_in_check,
    # #       if is_in_check with updated is true, method resets locations to original locations.
    # #       General is already at "d1" when checking for "in-check", so should not be returning True.
    # #       Check 'is_in_check' method.
    # general.set_location((3, 0))
    # boardPieces = game.get_board_dictionary()
    # boardPieces[(3, 0)] = general
    # del boardPieces[(4, 0)]
    # print(boardPieces)
    # game.show_board()
    # # insert print(piece) in is_in_check just before returning True, to get the piece checking the general
    # game.make_move("a3", "a4")
    # # checking piece: <__main__.General object at 0x033329B0> "memory address matches black general"
    # # check black generals allowed moves
    # blk_general = boardPieces[(4, 9)]
    # print(blk_general.allowed_move(game)) # FIXED: is_in_check did not check if move of piece contained same team
    # game.show_board()

    # remove all black pieces except general, test is_in_check_mate
    # game.make_move("b3", "e3")
    # print(game.is_in_check_mate("black"))
    # game.make_move("e10", "d10")
    # print(game.is_in_check_mate("black"))
    # game.make_move("a1", "a2")
    # print(game.is_in_check_mate("black"))
    # game.make_move("d10", "d9")
    # print(game.is_in_check_mate("black"))
    # game.make_move("a2", "d2")
    # print(game.is_in_check_mate("black"))
    # game.make_move("d9", "e9") # FIXED: Seems to work!


if __name__ == "__main__":
    main()
