import copy

MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def is_valid_path(board, path, words):
    """this function checks if the path given is a valid word, by checking the
    gaps between the steps of the path and the path got out of the borders of
    the board"""
    if not path or not is_in_bound(path[0], board):
        return
    word = board[path[0][0]][path[0][1]]
    for i in range(len(path) - 1):
        if not is_in_bound(path[i + 1], board):
            return
        if abs(path[i][0] - path[i+1][0]) > 1 or \
                abs(path[i][1] - path[i+1][1]) > 1:
            return
        word += board[path[i + 1][0]][path[i + 1][1]]
    if word in words:
        return word


def is_in_bound(coordinate, board):
    """this function checks if the coordinates given are out of the
    board bounds"""
    if (coordinate[0] < 0 or coordinate[0] > len(board) - 1 or
            coordinate[1] > len(board[0]) - 1 or coordinate[1] < 0):
        return False
    return True


def find_length_n_helper(n, board, words, temp_word, path, paths,
                         n_is_word_len, cur_coord):
    """this function returns a list of all the possible n length paths or
    n length words on the board that matches with one the words in a
    words list"""
    path.append(cur_coord)
    temp_word += board[cur_coord[0]][cur_coord[1]]
    if not n_is_word_len:
        if len(path) == n:
            if binary_search(words, 0, len(words)-1, temp_word, False) != -1:
                paths.append(copy.deepcopy(path))
            return
    else:
        if len(temp_word) == n:
            if binary_search(words, 0, len(words)-1, temp_word, False) != -1:
                paths.append(copy.deepcopy(path))
            return
    for move in MOVES:
        temp_coord = (cur_coord[0] + move[0], cur_coord[1] + move[1])
        if temp_coord in path or not is_in_bound(temp_coord, board) or \
                binary_search(words, 0, len(words)-1, temp_word, True) == -1:
            continue
        find_length_n_helper(n, board, words, temp_word, path, paths,
                             n_is_word_len, temp_coord)
        if not path:
            return
        path.pop()


def binary_search(lst, low, high, x, is_sliced_path):
    """binary search function for searching for a word in a words list"""
    if high >= low:
        mid = (high + low) // 2
        if is_sliced_path and len(x) <= len(lst[mid]) and \
                lst[mid][:len(x)] == x:
            return mid
        elif not is_sliced_path and lst[mid] == x:
            return mid
        elif lst[mid] > x:
            return binary_search(lst, low, mid - 1, x, is_sliced_path)
        else:
            return binary_search(lst, mid + 1, high, x, is_sliced_path)
    else:
        return -1


def coords_to_word(board, path):
    """this function converts coordinates to the word on the board"""
    word = ""
    for coord in path:
        word += board[coord[0]][coord[1]]
    return word


def find_length_n_paths(n, board, words):
    """This function  returns all n length valid paths"""
    return all_cords_find_len(n, board, words, False, len(board),
                              len(board[0]))


def find_length_n_words(n, board, words):
    """This function returns all valid paths that contain a word with the
    length of n"""
    return all_cords_find_len(n, board, words, True, len(board), len(board[0]))


def all_cords_find_len(n, board, words, n_is_word_len, height, width):
    """This function returns the n length paths that starts in every
    coordinate on the board using 'find_length_n_helper' function"""
    paths = []
    if 0 < n and words:
        for i in range(height):
            for j in range(width):
                find_length_n_helper(n, board, sorted(words), '', [], paths,
                                     n_is_word_len, (i, j))
    return paths


def max_score_paths(board, words):
    """This function returns all the valid paths in the board """
    filtered_paths = []
    filtered_words = []
    paths = []
    for num in range(len(board)*len(board[0]), 0, -1):
        paths += find_length_n_paths(num, board, words)
    for path in paths:
        temp_word = coords_to_word(board, path)
        if temp_word not in filtered_words:
            filtered_paths.append(path)
            filtered_words.append(temp_word)
    return filtered_paths