from Game import Game

THREE_MINUTES = 3 * 60


def words_list(file):
    """This function returns a list of the words that appear in the given
    file"""
    words = []
    with open(file, "r") as file:
        for line in file.readlines():
            words.append(line[:-1])
    return words


if __name__ == '__main__':
    words1 = words_list("boggle_dict.txt")
    game = Game(words1, THREE_MINUTES)
    game.init_opening_window()
