from XiangqiGame import *
from tkinter import *
from PIL import Image, ImageTk

board_size = 500
piece_size = (board_size // 10, board_size // 10)
notation = ['a','b','c','d','e','f','g','h','i']
offset = 100
player1_color = '#ffaa2e'
player2_color = '#ffe0bd'

class Board(Canvas):

    def __init__(self):
        super().__init__(width=board_size + offset, height=board_size + offset)
        self.initgame()
        self.pack()

    def initgame(self):
        self.board_status = XiangqiGame()
        self.selected = False
        self.last_position = ''
        # bind left click from mouse as user input
        self.bind_all('<Button-1>', self.click)
        # bind right click from mouse as move options
        self.bind_all('<Button-3>', self.rightclick)
        
        self.board_setup()
        self.load_images()
        self.draw_pieces()
        
    def resetgame(self):
        self.initgame()

    def quitgame(self):
        exit(0)

    def undoMove(self):
        self.board_status.sync_to_last_log()
        self.board_setup()
        self.draw_pieces()

    def board_setup(self):
        # draw board
        self.create_rectangle(0, 0, board_size + offset, board_size + offset, fill='#be4d00')
        self.create_rectangle(offset / 2, offset / 2, board_size + offset / 2, board_size + offset / 2, fill='#ffbd33')
        # vertical lines on board
        for i in range(1, 8):
            self.create_line(i * board_size / 8 + offset / 2, offset / 2, i * board_size / 8 + offset / 2, 4 * board_size / 9 + offset / 2)
            self.create_line(i * board_size / 8 + offset / 2,  5 * board_size / 9 + offset / 2, i * board_size / 8 + offset / 2, board_size + offset / 2)
        # horizontal lines on board
        for i in range(1, 9):
            self.create_line(offset / 2, i * board_size / 9 + offset / 2, board_size + offset / 2, i * board_size / 9 + offset / 2)
        # palace diagonals
        self.create_line(3 * board_size / 8 + offset / 2, offset / 2, 5 * board_size / 8 + offset / 2, 2 * board_size / 9 + offset / 2)
        self.create_line(5 * board_size / 8 + offset / 2, offset / 2, 3 * board_size / 8 + offset / 2, 2 * board_size / 9 + offset / 2)
        self.create_line(3 * board_size / 8 + offset / 2, 7 * board_size / 9 + offset / 2, 5 * board_size / 8 + offset / 2, 9 * board_size / 9 + offset / 2)
        self.create_line(3 * board_size / 8 + offset / 2, 9 * board_size / 9 + offset / 2, 5 * board_size / 8 + offset / 2, 7 * board_size / 9 + offset / 2)
        self.create_text(board_size + offset - 2, board_size + offset - 2, text='possible moves [right click]', anchor=SE, fill='#f6e198')
        active_player = self.board_status.get_active_player()
        check = self.board_status.is_in_check(active_player)
        if active_player == 'RED':
            player_text = '1st Player'
            color = player1_color
        else:
            player_text = '2nd Player'
            color = player2_color
        if check:
            player_text += ' (IN CHECK)'

        color_bx_size = 15
        self.create_rectangle(4, board_size + offset - 4, 4 + color_bx_size, board_size + offset - 4 - color_bx_size, fill=color)
        self.create_text(4 + color_bx_size + 4, board_size + offset - 4 - color_bx_size, text=player_text, anchor=NW, fill='#f6e198')
        

    def load_images(self):
        piece_size = (board_size // 10, board_size // 10)
        try:
            # get horse image
            self.ihorse = Image.open('media/horse.png')
            horse = self.ihorse.resize(piece_size)
            self.horse = ImageTk.PhotoImage(horse)
            # get elephant image
            self.ielephant = Image.open('media/elephant.png')
            elephant = self.ielephant.resize(piece_size)
            self.elephant = ImageTk.PhotoImage(elephant)
            # get soldier image
            self.isoldier = Image.open('media/soldier.png')
            soldier = self.isoldier.resize(piece_size)
            self.soldier = ImageTk.PhotoImage(soldier)
            # get cannon image
            self.icannon = Image.open('media/cannon.png')
            cannon = self.icannon.resize(piece_size)
            self.cannon = ImageTk.PhotoImage(cannon)
            # get chariot image
            self.ichariot = Image.open('media/chariot.png')
            chariot = self.ichariot.resize(piece_size)
            self.chariot = ImageTk.PhotoImage(chariot)
            # get general image
            self.igeneral = Image.open('media/general.png')
            general = self.igeneral.resize(piece_size)
            self.general = ImageTk.PhotoImage(general)
            # get advisor image
            self.iadvisor = Image.open('media/advisor.png')
            advisor = self.iadvisor.resize(piece_size)
            self.advisor = ImageTk.PhotoImage(advisor)
        except IOError as e:
            print(e)
            sys.exit(1)

    def draw_pieces(self):
        pieces = self.board_status.get_board_dictionary()
        for location in pieces:
            pixel_location = (int(location[0] * board_size / 8) + offset / 4, int(location[1] * board_size / 9) + offset / 4)
            piece = pieces[location]
            # create player background
            self.create_oval(pixel_location[0], pixel_location[1], pixel_location[0] + piece_size[0], pixel_location[1] + piece_size[1], fill='#8e8e8e')
            if piece.get_player().upper() == 'RED':
                self.create_oval(pixel_location[0] + 2, pixel_location[1] + 2, pixel_location[0] + piece_size[0] - 2, pixel_location[1] + piece_size[1] - 2, fill=player1_color)
            else:
                self.create_oval(pixel_location[0] + 2, pixel_location[1] + 2, pixel_location[0] + piece_size[0] - 2, pixel_location[1] + piece_size[1] - 2, fill=player2_color)
            
            # create piece icon
            if piece.get_pieceName() == 'horse':
                self.create_image(int(location[0] * board_size / 8) + offset / 4, int(location[1] * board_size / 9) + offset / 4, image=self.horse, anchor=NW, tag="horse")
            elif piece.get_pieceName() == 'elephant':
                self.create_image(int(location[0] * board_size / 8) + offset / 4, int(location[1] * board_size / 9) + offset / 4, image=self.elephant, anchor=NW, tag="elephant")
            elif piece.get_pieceName() == 'soldier':
                self.create_image(int(location[0] * board_size / 8) + offset / 4, int(location[1] * board_size / 9) + offset / 4, image=self.soldier, anchor=NW, tag="soldier")
            elif piece.get_pieceName() == 'cannon':
                self.create_image(int(location[0] * board_size / 8) + offset / 4, int(location[1] * board_size / 9) + offset / 4, image=self.cannon, anchor=NW, tag="cannon")
            elif piece.get_pieceName() == 'chariot':
                self.create_image(int(location[0] * board_size / 8) + offset / 4, int(location[1] * board_size / 9) + offset / 4, image=self.chariot, anchor=NW, tag="chariot")
            elif piece.get_pieceName() == 'general':
                self.create_image(int(location[0] * board_size / 8) + offset / 4, int(location[1] * board_size / 9) + offset / 4, image=self.general, anchor=NW, tag="general")
            elif piece.get_pieceName() == 'advisor':
                self.create_image(int(location[0] * board_size / 8) + offset / 4, int(location[1] * board_size / 9) + offset / 4, image=self.advisor, anchor=NW, tag="advisor")
            else:
                print('no icon found')

    def click(self, event):
        print("click event")
        col = int((event.x - offset / 4) // (board_size / 8))
        row = int((event.y - offset / 4) // (board_size / 9)) + 1
        position = notation[col] + str(row)
        pixel_location = (int(col * board_size / 8) + offset / 4, int((row - 1) * board_size / 9) + offset / 4)
        if self.selected:
            print(" from:" + self.last_position + "to:" + position)
            madeMove = self.board_status.make_move(self.last_position, position)
            self.board_status.show_board()
            self.board_setup()
            self.draw_pieces()
            
            self.selected = False
        else:
            if self.board_status.piece_at_location(position) == None:
                return
            self.board_setup()
            self.draw_pieces()
            self.last_position = position
            self.selected = True
            print(pixel_location)
            self.create_oval(pixel_location[0], pixel_location[1], pixel_location[0] + piece_size[0], pixel_location[1] + piece_size[1], width=2, outline='#32dee1')

    def rightclick(self, event):
        print("right click event")
        self.board_setup()
        self.draw_pieces()
        col = int((event.x - offset / 4) // (board_size / 8))
        row = int((event.y - offset / 4) // (board_size / 9)) + 1
        pixel_location = (int(col * board_size / 8) + offset / 4, int((row - 1) * board_size / 9) + offset / 4)
        self.create_oval(pixel_location[0], pixel_location[1], pixel_location[0] + piece_size[0], pixel_location[1] + piece_size[1], width=2, outline='#32dee1')
        position = notation[col] + str(row)
        piece = self.board_status.piece_at_location(position)
        if piece != None:
            print('show moves')
            moves = piece.allowed_move(self.board_status)
            for move in moves:
                
                pixel_location = (int(move[0] * board_size / 8) + offset / 4, int((move[1]) * board_size / 9) + offset / 4)
                self.create_oval(pixel_location[0], pixel_location[1], pixel_location[0] + piece_size[0], pixel_location[1] + piece_size[1], width=2, outline='#32dee1')

                if move in self.board_status.get_board_dictionary():
                    self.create_line(pixel_location[0], pixel_location[1], pixel_location[0] + piece_size[0], pixel_location[1] + piece_size[1], width=2, fill='#32dee1')
        else:
            print('no piece selected')

class Xiangqi(Frame):

    def __init__(self):
        super().__init__()
        self.master.title('Xiangqi')
        self.board = Board()
        self.pack()


def main():
    root = Tk()
    game = Xiangqi()
    menubar = Menu(root)
    # file menu
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label='New Game', command=game.board.resetgame)
    filemenu.add_command(label='Close', command=game.board.quitgame)
    menubar.add_cascade(label='File', menu=filemenu)
    # edit menu
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label='Undo Last Move', command=game.board.undoMove)
    menubar.add_cascade(label='Edit', menu=editmenu)
    root.config(menu=menubar)
    root.mainloop()

if __name__ == '__main__':
    main()
