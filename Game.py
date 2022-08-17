import tkinter as tk
from boggle_board_randomizer import randomize_board
from Board import Board

ROOT_WIDTH = 600
ROOT_HEIGHT = 400
BG_COLOR = 'bisque'
INSTRUCTIONS = ("Press 'PLAY' to start the game.\n"
                "In game, click one time on a letter, \n"
                "hover the mouse over the letters you want to choose,\n"
                "and click again to confirm the marked letters \n"
                "(click again on instructions button to close the "
                "instructions)")


def center_window(root, width, height):
    """This function places the root in the center of the window"""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


class Game:
    """This class represents a boggle game"""

    def __init__(self, words, game_time):
        self.root = tk.Tk()
        center_window(self.root, ROOT_WIDTH, ROOT_HEIGHT)
        self.root.configure(bg=BG_COLOR)
        self.root.configure()
        self.board = Board(randomize_board(), words, game_time)
        self.words = words
        self.timer = game_time
        self.opening_window = tk.Frame(bg=BG_COLOR)
        self.closing_window = tk.Frame(bg=BG_COLOR)
        self.timer = game_time

    def init_round(self):
        """This function closes the opening window and initiates the main
        board"""
        self.opening_window.pack_forget()
        self.closing_window.pack_forget()
        self.root.after(1000, lambda: self.check_time())
        self.board.draw_main_board(self.root)

    def check_time(self):
        """This function checks the timer of the game, if timer is zero it
        initiates the ending of a round"""
        if self.board.get_timer() == 0:
            self.round_ended()
        else:
            self.root.after(200, lambda: self.check_time())

    def round_ended(self):
        """This function show the closing window on the screen"""
        self.closing_window.pack(expand=True, fill=tk.BOTH)

    def init_opening_window(self):
        """This function builds the opening window"""
        self.init_closing_window()
        self.opening_window.pack()
        header = tk.Frame(self.opening_window)
        header.pack()
        header_label = tk.Label(header, text='MENU', font='italic 20 bold',
                                bg=BG_COLOR)
        header_label.pack(expand=True, fill=tk.BOTH)
        body = tk.Frame(self.opening_window, bg=BG_COLOR)
        body.pack(expand=True, fill=tk.BOTH)
        empty_frame = tk.Frame(body, height=50, width=10, background=BG_COLOR)
        empty_frame.pack(expand=True, fill=tk.BOTH)
        self.init_body_buttons(body)
        self.root.mainloop()

    def init_body_buttons(self, body):
        """This function builds the play and instruction buttons, and the
        instructions label"""
        play_button = tk.Button(body, text='PLAY',
                                font='italic 15',
                                command=self.init_round,
                                height=3, width=15,
                                bg='tan1')
        inst_label = [tk.Label(body,
                               text=INSTRUCTIONS,
                               font='italic 10', height=8, width=45,
                               bg=BG_COLOR),
                      False]
        play_button.pack()
        inst_button = tk.Button(body, text='instructions',
                                font='italic 15', command=lambda: self.
                                draw_inst_label(inst_label, inst_button),
                                height=3, width=15, fg='black', bg='tan1')
        inst_button.pack()

    def draw_inst_label(self, instructions_label, instruction_button):
        """This function draws the instruction_label and updates the
        instruction button"""
        if not instructions_label[1]:
            instructions_label[0].pack()
            instructions_label[1] = True
            instruction_button.configure(fg='grey')
        else:
            instructions_label[0].pack_forget()
            instructions_label[1] = False
            instruction_button.configure(fg='black')

    def init_closing_window(self):
        """This function builds the closing window"""
        header = tk.Frame(self.closing_window, background=BG_COLOR)
        header.pack()
        header_label = tk.Label(header, text='GAME OVER',
                                font='italic 20 bold', background=BG_COLOR)
        header_label.pack()
        body = tk.Frame(self.closing_window, background=BG_COLOR)
        body.pack(expand=True, fill=tk.BOTH)
        empty_frame = tk.Frame(body, height=70, width=10, background=BG_COLOR)
        empty_frame.pack()
        play_again_button = tk.Button(body, text='PLAY AGAIN',
                                      font='italic 15',
                                      command=self.play_again,
                                      height=2, width=20, bg='tan1')
        play_again_button.pack()
        back_to_menu_button = tk.Button(body, text='go back to main menu',
                                        font='italic 15',
                                        command=self.back_to_menu,
                                        height=2, width=20, bg='tan1')
        back_to_menu_button.pack()

    def play_again(self):
        """This function initiates a round with a new board"""
        self.new_board()
        self.init_round()

    def new_board(self):
        """This function builds a new board"""
        self.board = Board(randomize_board(), self.words, self.timer)

    def back_to_menu(self):
        """This function closes the closing window and opens the opening
        window with a ndw board"""
        self.closing_window.pack_forget()
        self.opening_window.pack()
        self.new_board()
