from tkinter import *
from snaketext import *
from snakelevels import *
import random
import pickle


class Snake():

    """Class for the snake game."""

    @classmethod
    def center(cls, win):
        """Center the main window on the screen."""

        resx = win.winfo_screenwidth()
        resy = win.winfo_screenheight()
        rootx = win.winfo_width()
        rooty = win.winfo_height()

        leftmargin = (resx - rootx) // 2
        topmargin = (resy - rooty) // 2
        win.minsize(rootx, rooty)
        win.maxsize(rootx, rooty)
        win.geometry("{}x{}+{}+{}".format(rootx, rooty, leftmargin, topmargin))

    def __init__(self, columns, rows, gridsize):
        """Initialize the game."""

        try:
            f = open("ts.data", "rb")
            self.record = pickle.load(f)
        except FileNotFoundError:
            f = open("ts.data", "wb")
            pickle.dump(0, f)
            self.record = 0
        f.close()

        self.columns = columns
        self.rows = rows
        self.gridsize = gridsize

        self.levelnum = 0
        self.sublevel = 0
        self.eaten = 0
        self.totalscore = 0
        self.basescore = 100
        self.foodscore = 100
        self.leveltexts = (lvl0, lvl1, lvl2)
        self.levels = (level0, level1, level2)

        self.root = Tk()
        self.root.title("Snake")
        self.canvas = Canvas(self.root, width=columns * gridsize,
                             height=rows * gridsize, bg="black",
                             highlightthickness=0)
        self.canvas.pack(padx=5, pady=5)
        self.scorecanvas = Canvas(self.root, width=columns * gridsize,
                                  height=7 * gridsize + 5, bg="black",
                                  highlightthickness=0)
        self.scorecanvas.create_rectangle(0, 7 * gridsize, columns * gridsize,
                                          7 * gridsize + 4,
                                          fill="SystemButtonFace",
                                          outline="SystemButtonFace")

        self.scorecanvas.pack()
        self.root.update()
        Snake.center(self.root)
        self.drawmenu("event")
        self.root.mainloop()

    def draw(self, widget, data, color):
        """Draw an arbitrary object, using the data paramater,

        which has to be an iterable consists of row and column coordinates."""

        for i in range(len(data)):
            widget.create_oval((data[i][1] - 1) * self.gridsize,
                               (data[i][0] - 1) * self.gridsize,
                               data[i][1] * self.gridsize - 1,
                               data[i][0] * self.gridsize - 1,
                               fill=color, outline=color)

    def drawchar(self, char):
        """Draw a pixelated character on the canvas."""

        # top right pixel
        tr = (2, self.columns - 1 - self.charctr * 4)

        if char == "0":
            chartup = (tr, (tr[0] + 1, tr[1]), (tr[0] + 2, tr[1]),
                       (tr[0] + 3, tr[1]), (tr[0] + 4, tr[1]),
                       (tr[0], tr[1] - 1), (tr[0] + 4, tr[1] - 1),
                       (tr[0], tr[1] - 2), (tr[0] + 1, tr[1] - 2),
                       (tr[0] + 2, tr[1] - 2), (tr[0] + 3, tr[1] - 2),
                       (tr[0] + 4, tr[1] - 2))
        if char == "1":
            chartup = (tr, (tr[0] + 1, tr[1]), (tr[0] + 2, tr[1]),
                       (tr[0] + 3, tr[1]), (tr[0] + 4, tr[1]))
        if char == "2":
            chartup = (tr, (tr[0] + 1, tr[1]), (tr[0] + 2, tr[1]),
                       (tr[0] + 4, tr[1]), (tr[0], tr[1] - 1),
                       (tr[0] + 2, tr[1] - 1), (tr[0] + 4, tr[1] - 1),
                       (tr[0], tr[1] - 2), (tr[0] + 2, tr[1] - 2),
                       (tr[0] + 3, tr[1] - 2), (tr[0] + 4, tr[1] - 2))
        if char == "3":
            chartup = (tr, (tr[0] + 1, tr[1]), (tr[0] + 2, tr[1]),
                       (tr[0] + 4, tr[1]), (tr[0], tr[1] - 1),
                       (tr[0] + 2, tr[1] - 1), (tr[0] + 4, tr[1] - 1),
                       (tr[0], tr[1] - 2), (tr[0] + 2, tr[1] - 2),
                       (tr[0] + 3, tr[1]), (tr[0] + 4, tr[1] - 2))
        if char == "4":
            chartup = (tr, (tr[0] + 1, tr[1]), (tr[0] + 2, tr[1]),
                       (tr[0] + 3, tr[1]), (tr[0] + 4, tr[1]),
                       (tr[0] + 2, tr[1] - 1), (tr[0] + 3, tr[1]),
                       (tr[0], tr[1] - 2), (tr[0] + 1, tr[1] - 2),
                       (tr[0] + 2, tr[1] - 2))
        if char == "5":
            chartup = (tr, (tr[0] + 2, tr[1]), (tr[0] + 4, tr[1]),
                       (tr[0], tr[1] - 1), (tr[0] + 2, tr[1] - 1),
                       (tr[0] + 4, tr[1] - 1), (tr[0], tr[1] - 2),
                       (tr[0] + 2, tr[1] - 2), (tr[0] + 4, tr[1] - 2),
                       (tr[0] + 1, tr[1] - 2), (tr[0] + 3, tr[1]))
        if char == "6":
            chartup = (tr, (tr[0] + 2, tr[1]), (tr[0] + 4, tr[1]),
                       (tr[0], tr[1] - 1), (tr[0] + 2, tr[1] - 1),
                       (tr[0] + 4, tr[1] - 1), (tr[0], tr[1] - 2),
                       (tr[0] + 2, tr[1] - 2), (tr[0] + 4, tr[1] - 2),
                       (tr[0] + 1, tr[1] - 2), (tr[0] + 3, tr[1]),
                       (tr[0] + 3, tr[1] - 2))
        if char == "7":
            chartup = (tr, (tr[0] + 1, tr[1]), (tr[0] + 2, tr[1]),
                       (tr[0] + 3, tr[1]), (tr[0] + 4, tr[1]),
                       (tr[0], tr[1] - 1), (tr[0], tr[1] - 2))
        if char == "8":
            chartup = (tr, (tr[0] + 2, tr[1]), (tr[0] + 4, tr[1]),
                       (tr[0], tr[1] - 1), (tr[0] + 2, tr[1] - 1),
                       (tr[0] + 4, tr[1] - 1), (tr[0], tr[1] - 2),
                       (tr[0] + 2, tr[1] - 2), (tr[0] + 4, tr[1] - 2),
                       (tr[0] + 1, tr[1] - 2), (tr[0] + 3, tr[1]),
                       (tr[0] + 3, tr[1] - 2), (tr[0] + 1, tr[1]))
        if char == "9":
            chartup = (tr, (tr[0] + 2, tr[1]), (tr[0] + 4, tr[1]),
                       (tr[0], tr[1] - 1), (tr[0] + 2, tr[1] - 1),
                       (tr[0] + 4, tr[1] - 1), (tr[0], tr[1] - 2),
                       (tr[0] + 2, tr[1] - 2), (tr[0] + 4, tr[1] - 2),
                       (tr[0] + 1, tr[1] - 2), (tr[0] + 3, tr[1]),
                       (tr[0] + 1, tr[1]))

        self.draw(self.scorecanvas, chartup, "darkgrey")
        self.charctr += 1

    def drawscore(self, score, record=False):
        """Draw the score on the bottom canvas."""

        self.charctr = 0
        self.scorecanvas.delete(ALL)
        if not record:
            self.draw(self.scorecanvas, self.leveltexts[self.levelnum],
                      "darkgrey")
        for char in str(score)[::-1]:
            self.drawchar(char)
        self.scorecanvas.create_rectangle(0, 7 * self.gridsize,
                                          self.columns * self.gridsize,
                                          7 * self.gridsize + 4,
                                          fill="SystemButtonFace",
                                          outline="SystemButtonFace")

    def drawsnake(self):
        """Draw the snake on the canvas using a list of coordinates."""

        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []
        for i in range(len(self.snake)):
            id = self.canvas.create_oval(
                (self.snake[i][1] - 1) * self.gridsize,
                (self.snake[i][
                 0] - 1) * self.gridsize,
                (self.snake[i][
                 1] * self.gridsize) - 1,
                (self.snake[i][
                 0] * self.gridsize) - 1,
                fill="green", outline="green")
            self.ids.append(id)

    def drawmenu(self, event):
        """Draw the main menu."""

        self.canvas.delete(ALL)
        self.root.unbind("<Return>")
        self.root.unbind("<Esc>")
        self.root.bind("<Up>", self.changemenu)
        self.root.bind("<Down>", self.changemenu)
        self.root.bind("<Return>", self.entermenu)
        self.draw(self.canvas, play, "white")
        self.draw(self.canvas, record, "darkgrey")
        self.draw(self.canvas, quit, "darkgrey")
        self.selected = "play"

    def changemenu(self, event):
        """Change the active menu."""

        if self.selected == "play":
            self.draw(self.canvas, play, "darkgrey")
            if event.keysym == "Down":
                self.selected = "record"
                self.draw(self.canvas, record, "white")
                return
            else:
                self.selected = "quit"
                self.draw(self.canvas, quit, "white")
                return

        if self.selected == "record":
            self.draw(self.canvas, record, "darkgrey")
            if event.keysym == "Down":
                self.selected = "quit"
                self.draw(self.canvas, quit, "white")
                return
            else:
                self.selected = "play"
                self.draw(self.canvas, play, "white")
                return

        if self.selected == "quit":
            self.draw(self.canvas, quit, "darkgrey")
            if event.keysym == "Down":
                self.selected = "play"
                self.draw(self.canvas, play, "white")
                return
            else:
                self.selected = "record"
                self.draw(self.canvas, record, "white")
                return

    def entermenu(self, event):
        """Enter the selected menu."""

        if self.selected == "play":
            self.start()
        if self.selected == "record":
            f = open("ts.data", "rb")
            self.record = pickle.load(f)
            f.close()
            self.drawscore(self.record, record=True)
        if self.selected == "quit":
            self.root.destroy()

    def start(self):
        """"A list to store the snake's coordinates.

        Rows' and columns' numbering starts with one in the top left corner."""

        self.foodid = None
        self.dir = "Right"
        self.sublevel = 0
        self.speeds = (79, 69, 59, 49, 39)
        self.ids = []
        self.snake = [(self.rows // 2, self.columns // 2 + 1),
                      (self.rows // 2, self.columns // 2),
                      (self.rows // 2 + 1, self.columns // 2),
                      (self.rows // 2 + 1, self.columns // 2 + 1)]

        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.root.unbind("<Return>")
        self.root.bind("<Escape>", self.pause)

        self.canvas.delete(ALL)
        self.draw(self.canvas, self.levels[self.levelnum], "darkgrey")
        self.drawscore(self.totalscore)
        self.drawsnake()
        self.placefood()
        self.move()

    def move(self):
        """Move the snake in the given direction."""

        lastpart = self.snake[len(self.snake) - 1]

        if self.dir == "Left":
            self.root.bind("<Up>", self.changedir)
            self.root.bind("<Down>", self.changedir)
            for i in range(len(self.snake) - 1, 0, -1):
                self.snake[i] = self.snake[i - 1]
            self.snake[0] = (self.snake[0][0], self.snake[0][1] - 1)

        if self.dir == "Right":
            self.root.bind("<Up>", self.changedir)
            self.root.bind("<Down>", self.changedir)
            for i in range(len(self.snake) - 1, 0, -1):
                self.snake[i] = self.snake[i - 1]
            self.snake[0] = (self.snake[0][0], self.snake[0][1] + 1)

        if self.dir == "Up":
            self.root.bind("<Left>", self.changedir)
            self.root.bind("<Right>", self.changedir)
            for i in range(len(self.snake) - 1, 0, -1):
                self.snake[i] = self.snake[i - 1]
            self.snake[0] = (self.snake[0][0] - 1, self.snake[0][1])

        if self.dir == "Down":
            self.root.bind("<Left>", self.changedir)
            self.root.bind("<Right>", self.changedir)
            for i in range(len(self.snake) - 1, 0, -1):
                self.snake[i] = self.snake[i - 1]
            self.snake[0] = (self.snake[0][0] + 1, self.snake[0][1])

        # Check if the snake is going to hit a wall.
        if self.snake[0][0] < 1 or self.snake[0][0] > self.rows \
                or self.snake[0][1] < 1 or self.snake[0][1] > self.columns:
            self.gameover()
            return

        # Check if the snake is going to hit an object on the level.
        if self.snake[0] in self.levels[self.levelnum]:
            self.gameover()
            return

        # Check if the snake is going to hit itself.
        snakebody = self.snake.copy()
        snakebody.pop(0)
        for part in snakebody:
            if self.snake[0] == part:
                self.gameover()
                return

        # Check if the snake has picked up a piece of food.
        if self.snake[0] == self.foodplace:
            self.eaten += 1
            self.basescore = 100 * (self.levelnum + 1)
            self.foodscore = self.basescore * (self.sublevel + 1)
            self.totalscore += self.foodscore
            self.drawscore(self.totalscore)
            self.snake.append(lastpart)
            self.placefood()

            if self.eaten > 24:
                self.levelup()
                return
            elif self.eaten > 19:
                self.sublevel = 4
            elif self.eaten > 14:
                self.sublevel = 3
            elif self.eaten > 9:
                self.sublevel = 2
            elif self.eaten > 4:
                self.sublevel = 1
            else:
                self.sublevel = 0

        self.drawsnake()
        self.repeat = self.root.after(self.speeds[self.sublevel], self.move)

    def changedir(self, event):
        """Change the direction of the movement."""

        if event.keysym == "Left":
            self.root.unbind("<Left>")
            self.root.unbind("<Right>")
            self.dir = "Left"

        if event.keysym == "Right":
            self.root.unbind("<Left>")
            self.root.unbind("<Right>")
            self.dir = "Right"

        if event.keysym == "Up":
            self.root.unbind("<Up>")
            self.root.unbind("<Down>")
            self.dir = "Up"

        if event.keysym == "Down":
            self.root.unbind("<Up>")
            self.root.unbind("<Down>")
            self.dir = "Down"

    def placefood(self):
        """Place the food on the canvas."""

        grids = []

        for i in range(1, self.rows + 1):
            for j in range(1, self.columns + 1):
                if (i, j) not in self.levels[self.levelnum]:
                    grids.append((i, j))

        emptygrids = grids.copy()

        for part in self.snake:
            emptygrids.remove(part)

        self.foodplace = random.choice(emptygrids)

        # self.foodid is initally None,
        # so, if and only if food has been placed before we delete it.
        if self.foodid:
            self.canvas.delete(self.foodid)

        self.foodid = self.canvas.create_oval(
            (self.foodplace[1] - 1) * self.gridsize,
            (self.foodplace[0] - 1) * self.gridsize,
            (self.foodplace[1] * self.gridsize) - 1,
            (self.foodplace[0] * self.gridsize) - 1,
            fill="yellow", outline="yellow")

    def levelup(self):
        """Get to the next level."""

        self.root.after_cancel(self.repeat)
        self.canvas.delete(ALL)
        self.scorecanvas.delete(ALL)
        self.scorecanvas.create_rectangle(0, 7 * self.gridsize,
                                          self.columns * self.gridsize,
                                          7 * self.gridsize + 4,
                                          fill="SystemButtonFace",
                                          outline="SystemButtonFace")
        self.levelnum += 1
        self.eaten = 0
        if self.levelnum == len(self.levels):
            self.win()
        else:
            self.start()

    def pause(self, event):
        self.root.after_cancel(self.repeat)
        self.root.unbind("<Escape>")
        self.root.bind("<Escape>", self.resume)

    def resume(self, event):
        self.move()
        self.root.bind("<Escape>", self.pause)

    def gameover(self):
        """End the game."""

        if self.totalscore > self.record:
            f = open("ts.data", "wb")
            pickle.dump(self.totalscore, f)
            f.close()
        self.levelnum = 0
        self.sublevel = 0
        self.eaten = 0
        self.totalscore = 0
        self.basescore = 100
        self.foodscore = 100

        self.root.after_cancel(self.repeat)
        self.canvas.delete(ALL)
        self.scorecanvas.delete(ALL)
        self.scorecanvas.create_rectangle(0, 7 * self.gridsize,
                                          self.columns * self.gridsize,
                                          7 * self.gridsize + 4,
                                          fill="SystemButtonFace",
                                          outline="SystemButtonFace")
        self.drawmenu("event")
        self.draw(self.canvas, gameover, "darkgrey")

    def win(self):
        """The user beat the game."""

        f = open("ts.data", "wb")
        pickle.dump(1000000, f)
        f.close()
        self.draw(self.canvas, youwin, "darkgrey")
        self.root.bind("<Return>", self.drawmenu)
        self.root.unbind("<Escape>")
        self.root.bind("<Escape>", self.drawmenu)
        self.levelnum = 0
        self.sublevel = 0
        self.eaten = 0
        self.totalscore = 0
        self.basescore = 100
        self.foodscore = 100


myGame = Snake(80, 60, 10)
