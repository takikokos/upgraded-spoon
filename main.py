'''
    This is my variation of Conway's Game of Life.
    https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

    Used only numpy and opencv, didn't want to achieve
    very high perfomance but decided to make the best i can

    Was made in one evening so cant say it's very beautiful,
    though i can't stop watching the result. Actually there 
    are 2 ways of updating the cells in these functions,
    used only one of them, the fastest in my opinion.

    It's probably better to run main loop in second thread
    to decrease the FREEZE_TIME

    After execution press SPACE to start/stop the game.
    You can zoom with your mouse wheel

    There are some bugs if you continue placing alive 
    cells after stoping the game and with corners.
'''

import numpy as np
import cv2
from time import sleep, time


FREEZE_TIME = 20 # time in ms of "sleeping" after each generation, actually controlls fps
WINDOW_NAME = "Conway's Game of Life"
BOTTOM_PANEL_WIDTH = 60 # additional parametres for text on the bottom
BOTTOM_PANEL_HEIGHT = 50 # additional parametres for text on the bottom
 
WIDTH, HEIGHT = 800, 800 # size of playing area
RECT_SIZE = (5, 5) # size of one cell
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

X_CELLS_AMOUNT = (WIDTH - RECT_SIZE[0]) // RECT_SIZE[0] + 1 
Y_CELLS_AMOUNT = (HEIGHT - RECT_SIZE[1]) // RECT_SIZE[1] + 1

ALIVE_CELLS = [] # array with coords of alive cells
ALIVE_CELLS_INIT = False # determines whether ALIVE_CELLS was inited
ALL_CELLS = [] # array with all cells in playing area, 0 - dead, 1 - alive


def get_alive_neib(arr, x, y):
    '''
        return list with coords of 
        all alive neighbors
    '''
    res = []
    for i in range(x-1, x+2, 1):
        for j in range(y-1, y+2, 1):
            if i == x and j == y:
                continue
            if arr[i][j] == 1:
                res += [[i, j]]
    return res, len(res)

def get_all_neib(arr, x, y):
    '''
        return list with coords of 
        all neighbors
    '''
    res = []
    for i in range(x-1, x+2, 1):
        for j in range(y-1, y+2, 1):
            if i == x and j == y:
                continue
            res += [[i, j]]
    return res

def life(arr, x, y):
    '''
        arr : np.array
        x, y : int
        return bool, should this cell live or die
    '''
    nieb, amount = get_alive_neib(arr, x, y)
    if arr[x, y] == 0 and amount == 3: 
        return True
    elif amount < 2: # arr[x, y] == 1 and 
        return False
    elif arr[x, y] == 1 and (amount == 2 or amount == 3): 
        return True
    elif arr[x, y] == 1 and amount > 3:
        return False
    else:
        return False

def update_grid(use_slow=False):
    '''
        use_slow is used fro debug only

        counts new generation on all cells
        this func removes and redraws dead cells by default
        returns new array of ALL_CELLS
    '''

    global ALL_CELLS
    new_cells = np.copy(ALL_CELLS)
    global ALIVE_CELLS
    saved_alive_cells = np.copy(ALIVE_CELLS)

    if use_slow:
        for i in range(1, X_CELLS_AMOUNT + 1):
            for j in range(1, Y_CELLS_AMOUNT + 1):
                if life(ALL_CELLS, i, j):
                    new_cells[i, j] = 1
                    if ALL_CELLS[i, j] != 1:
                        ALIVE_CELLS = np.append(ALIVE_CELLS, np.array([i-1, j-1], ndmin=2), axis=0)
                else:
                    new_cells[i, j] = 0
                    if ALL_CELLS[i, j] == 1:
                        index = ALIVE_CELLS.tolist().index([i-1, j-1])
                        ALIVE_CELLS = np.delete(ALIVE_CELLS, index, axis=0)

                    # testing inplace deleting, for only updating cells (draw_alive_cells)
                    x = (i-1) * RECT_SIZE[0]
                    y = (j-1) * RECT_SIZE[1]
                    cv2.rectangle(img, (x, y), (x + RECT_SIZE[0], y + RECT_SIZE[1]), COLOR_WHITE, -1)
                    cv2.rectangle(img, (x, y), (x + RECT_SIZE[0], y + RECT_SIZE[1]), COLOR_BLACK, 1)
        return new_cells

    # second idea
    for c in range(saved_alive_cells.shape[0]):
        x = saved_alive_cells[c][0]
        y = saved_alive_cells[c][1]
        neib = get_all_neib(ALL_CELLS, x+1, y+1)
        neib += [[x+1, y+1]]
        for i, j in neib:
            if i == 0 or j == 0 or i == X_CELLS_AMOUNT + 1 or j == Y_CELLS_AMOUNT + 1:
                continue
            if life(ALL_CELLS, i, j):
                if new_cells[i, j] != 1:
                    ALIVE_CELLS = np.append(ALIVE_CELLS, np.array([i-1, j-1], ndmin=2), axis=0)
                    new_cells[i, j] = 1
            else:
                if new_cells[i, j] == 1: 
                    index = ALIVE_CELLS.tolist().index([i-1, j-1])
                    ALIVE_CELLS = np.delete(ALIVE_CELLS, index, axis=0)
                    new_cells[i, j] = 0

                # testing inplace deleting, for only updating cells (draw_alive_cells)
                cv2.rectangle(img, ((i-1) * RECT_SIZE[0], (j-1) * RECT_SIZE[1]), ((i-1) * RECT_SIZE[0] + RECT_SIZE[0], (j-1) * RECT_SIZE[1] + RECT_SIZE[1]), COLOR_WHITE, -1)
                cv2.rectangle(img, ((i-1) * RECT_SIZE[0], (j-1) * RECT_SIZE[1]), ((i-1) * RECT_SIZE[0] + RECT_SIZE[0], (j-1) * RECT_SIZE[1] + RECT_SIZE[1]), COLOR_BLACK, 1)

    return new_cells
      
def draw_alive_cells(img, use_slow=False):
    '''
        use_slow is used for debug only

        redraws all necessary cells
    '''

    global ALIVE_CELLS
    global ALIVE_CELLS_INIT
    global ALL_CELLS
    if not ALIVE_CELLS_INIT: 
        return

    # brute force
    if use_slow:
        for i in range(1, X_CELLS_AMOUNT + 1):
            for j in range(1, Y_CELLS_AMOUNT + 1):
                x = (i-1) * RECT_SIZE[0]
                y = (j-1) * RECT_SIZE[1]
                if ALL_CELLS[i, j] == 1:
                    cv2.rectangle(img, (x, y), (x + RECT_SIZE[0], y + RECT_SIZE[1]), COLOR_BLACK, -1)
                else:
                    cv2.rectangle(img, (x, y), (x + RECT_SIZE[0], y + RECT_SIZE[1]), COLOR_WHITE, -1)
                    cv2.rectangle(img, (x, y), (x + RECT_SIZE[0], y + RECT_SIZE[1]), COLOR_BLACK, 1)
        return

    for i in range(ALIVE_CELLS.shape[0]):
        x = ALIVE_CELLS[i][0] * RECT_SIZE[0]
        y = ALIVE_CELLS[i][1] * RECT_SIZE[1]
        cv2.rectangle(img, (x, y), (x + RECT_SIZE[0], y + RECT_SIZE[1]), COLOR_BLACK, -1)

def init_grid(img):
    '''
        inits and draws the grid
    '''
    global ALL_CELLS
    global Y_CELLS_AMOUNT
    global X_CELLS_AMOUNT
    ALL_CELLS = np.zeros((X_CELLS_AMOUNT + 2, Y_CELLS_AMOUNT + 2, 1), np.uint8) # init with boundaries
    for i in range(0, WIDTH - RECT_SIZE[0], RECT_SIZE[0]):
        for j in range(0, HEIGHT - RECT_SIZE[1], RECT_SIZE[1]):
            img = cv2.rectangle(img, (i, j), (i + RECT_SIZE[0], j + RECT_SIZE[1]), COLOR_BLACK, 1)

def mouse_event_handler(event, x, y, flags, param):
    global ALIVE_CELLS
    global ALIVE_CELLS_INIT
    global ALL_CELLS
    if event == cv2.EVENT_LBUTTONDOWN:
        x = x // RECT_SIZE[0]
        y = y // RECT_SIZE[1]
        if x >= X_CELLS_AMOUNT or y >= Y_CELLS_AMOUNT: # wanna check if (x, y) is not outside the grid
            return
        if ALIVE_CELLS_INIT:
            ALIVE_CELLS = np.append(ALIVE_CELLS, np.array([x, y], ndmin=2), axis=0)
        else:
            ALIVE_CELLS = np.array([x, y], ndmin=2, dtype=np.uint8)
            ALIVE_CELLS_INIT = True
        ALL_CELLS[x+1, y+1] = 1

def main_loop(window_name, img):
    global ALL_CELLS
    gen_count = 0
    init_grid(img)
    start_game = False
    while(1):

        eval_time = time()
        if start_game:
            ALL_CELLS = update_grid()
            gen_count += 1
        draw_alive_cells(img)
        cv2.imshow(window_name, img)
        eval_time = time() - eval_time

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(img, (0,  HEIGHT + BOTTOM_PANEL_HEIGHT), (WIDTH + BOTTOM_PANEL_WIDTH, HEIGHT), COLOR_WHITE, -1)
        cv2.putText(img, f"Last generation evaled in {eval_time:.4f} sec, total {gen_count} gens", (10, HEIGHT + 30), font, 1, COLOR_BLACK, 1, cv2.LINE_AA)

        key = cv2.waitKey(FREEZE_TIME) & 0xFF
        if (key == 27) or (cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1):
            break
        elif key == 32:
            if not start_game:
                print("Game started")
            else:
                print("Game stopped")
            start_game = not start_game

    cv2.destroyAllWindows()


if __name__ == "__main__":
    img = np.zeros((HEIGHT + BOTTOM_PANEL_HEIGHT, WIDTH + BOTTOM_PANEL_WIDTH, 3), np.uint8)
    img.fill(255)
    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, mouse_event_handler)
    main_loop(WINDOW_NAME, img)
