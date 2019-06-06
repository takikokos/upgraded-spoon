# Conway's Game of Life.
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
