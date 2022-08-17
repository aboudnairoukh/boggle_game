import datetime
import tkinter as tk
from ex12_utils import is_valid_path


SCORE_POWER = 2
BG_COLOR = 'bisque'


class Board:
    """This class represent a round in the game"""
    def __init__(self, board_lst, words, game_time):
        self.board_lst = board_lst
        self.height = len(board_lst)
        self.width = len(board_lst[0])
        self.words = words
        self.root = None
        self.main_frame = None
        self.button_dict = {}
        self.build = False
        self.temp_word_label = None
        self.temp_word = {}
        self.entered_words_frame = None
        self.score_label = None
        self.score = 0
        self.entered_words = []
        self.timer = game_time

    def get_timer(self):
        """This function returns the timer of the current round"""
        return self.timer

    def clicked(self, i, j):
        """This function runs the clicking of a letter button and the building
        of a word, if the user was not building a word before, it starts a
        build, else it checks if the built word is valid"""
        if not self.build:
            for button in self.temp_word:
                button.configure(bg='old lace')
            self.temp_word = {}
            self.first_click(i, j)
            self.temp_word_label.configure(text="current word:\n", fg='black')
        else:
            self.build = False
            path = []
            self.build_path(path)
            self.valid_word(path)

    def first_click(self, i, j):
        """This function represent the first click of a button"""
        self.button_dict[(i, j)][0].configure(bg='khaki1')
        self.temp_word[self.button_dict[(i, j)][0]] = self.board_lst[i][j]
        self.button_dict[(i, j)][1] = True
        self.temp_word_label.configure(text="current word:\n" +
                                            self.board_lst[i][j])
        self.build = True

    def build_path(self, path):
        """This function builds a coordinates path based on the word that was
        built"""
        for button in self.temp_word:
            for button_cords in self.button_dict:
                if button == self.button_dict[button_cords][0]:
                    path.append(button_cords)
                    self.button_dict[button_cords][1] = False

    def valid_word(self, path):
        """This function checks if the given path represent a valid path or
        not, if yes it updates the score and the chosen words, else it updates
        the color of the buttons and the temp_word_label"""
        entered_word = "".join(self.temp_word.values())
        if is_valid_path(self.board_lst, path, self.words) and \
                entered_word not in self.entered_words:
            self.score += len(path) ** SCORE_POWER
            self.score_label.configure(text="Score: " + str(self.score))
            valid_word = tk.Label(self.entered_words_frame,
                                  text="".join(self.temp_word.values()),
                                  bg='seagreen3')
            valid_word.pack(fill=tk.X)
            self.entered_words.append(entered_word)
            for button in self.temp_word:
                button.configure(bg='seagreen3')
        else:
            for button in self.temp_word:
                button.configure(bg='tomato2')
            self.temp_word_label.configure(text="current word:\n INVALID WORD",
                                           fg='red')

    def hoovered(self, i, j):
        """This function runs the hoover method of the buttons, if the user is
        currently building a word it updates the button and the temp word"""
        if self.build:
            self.hoover_back(i, j)
            self.button_dict[(i, j)][0].configure(bg='khaki1')
            self.temp_word[self.button_dict[(i, j)][0]] = self.board_lst[i][j]
            self.button_dict[(i, j)][1] = True
            self.temp_word_label.configure(text="current word:\n" +
                                                "".join(
                                                    self.temp_word.values()))

    def hoover_back(self, i, j):
        """This function updates the buttons and the temp word depending on the
        users mouse key"""
        after = False
        if self.button_dict[(i, j)][1]:
            buttons_to_change = []
            for button in self.temp_word:
                if not after and button == self.button_dict[(i, j)][0]:
                    after = True
                    continue
                if after:
                    button.configure(bg='old lace')
                    self.button_dict[(i, j)][1] = False
                    buttons_to_change.append(button)
            for button in buttons_to_change:
                self.temp_word.pop(button)

    def init_body(self):
        """This function builds the body frame of the root"""
        body = tk.Frame(self.main_frame, background=BG_COLOR)
        body.pack(expand=True, fill=tk.BOTH)
        left = tk.Frame(body, background=BG_COLOR)
        left.place(relwidth=0.6, relheight=1.0)
        right = tk.Frame(body, background=BG_COLOR)
        right.place(relwidth=0.4, relx=0.6, relheight=1.0)
        timer = tk.Label(left, text='Time: ' + str(datetime.timedelta
                                                   (seconds=self.timer))[2:],
                         background=BG_COLOR, font='italic 12')
        self.root.after(500, lambda: self.update_time(timer))
        timer.pack()
        self.score_label = tk.Label(right, text='Score: ' + str(self.score),
                                    background=BG_COLOR)
        self.score_label.pack(fill=tk.X)
        self.temp_word_label = tk.Label(right, text="current word:\n",
                                        background=BG_COLOR)
        self.temp_word_label.pack(fill=tk.X)
        self.entered_words_frame = tk.Frame(right, background=BG_COLOR)
        self.entered_words_frame.pack(fill=tk.BOTH, expand=True)
        self.init_buttons(left)

    def update_time(self, timer):
        """This function updates the timer each second"""
        self.timer -= 1
        timer.configure(text='Time: ' + str(datetime.timedelta
                                            (seconds=self.timer))[2:])
        if self.timer == 0:
            self.main_frame.pack_forget()
        else:
            self.root.after(1000, lambda: self.update_time(timer))

    def init_buttons(self, left):
        """This function build the letters buttons"""
        buttons_frame = tk.Frame(left, background=BG_COLOR)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        for i in range(self.height):
            for j in range(self.width):
                button = tk.Button(buttons_frame, text=self.board_lst[i][j],
                                   command=lambda row=i, col=j:
                                   self.clicked(row, col), bg="old lace")
                button.bind("<Enter>", lambda event, row=i, col=j: self.
                            hoovered(row, col))
                self.button_dict[(i, j)] = [button, False]
                button.grid(row=i, column=j, sticky=tk.NSEW, padx=(7, 7),
                            pady=(7, 7))
                buttons_frame.grid_rowconfigure(i, weight=1)
                buttons_frame.grid_columnconfigure(j, weight=1)

    def init_GUI(self):
        """this function builds all the frame of the board"""
        self.main_frame = tk.Frame(self.root, background=BG_COLOR)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        header = tk.Frame(self.main_frame, background=BG_COLOR)
        header.pack()
        header_label = tk.Label(header, text='BOGGLE', font='italic 20 bold',
                                background=BG_COLOR)
        header_label.pack()
        self.init_body()

    def draw_main_board(self, root):
        """this function draws all the board"""
        self.root = root
        self.init_GUI()
        self.root.mainloop()
