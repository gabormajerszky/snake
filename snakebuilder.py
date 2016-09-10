from tkinter import *
from snakelevels import *
from snaketext import *


class Snakebuild():
    """Class to help to build snake levels."""
    
    def __init__(self, columns, rows, gridsize):
        """Create main window and canvas."""
        
        self.columns = columns
        self.gridsize = gridsize
        
        self.root = Tk()
        #======================================================================
        # self.canvas = Canvas(self.root, width=columns * gridsize,
        #                           height=7 * gridsize + 5, bg="black",
        #                           highlightthickness=0)
        #======================================================================
        #======================================================================
        # self.canvas.create_rectangle(0, 7 * gridsize, columns * gridsize,
        #                                   7 * gridsize + 4,
        #                                   fill="SystemButtonFace",
        #                                   outline="SystemButtonFace")
        #======================================================================
        self.canvas = Canvas(self.root, width=columns * gridsize,
                             height=rows * gridsize, bg="black")
        self.canvas.pack(padx=5, pady=5)
        self.root.bind("<Button-1>", self.getdata)
        self.root.bind("<Button-2>", self.getdata2)
        self.root.bind("<Button-3>", self.deldata)
        self.root.bind("<r>", self.deldata2)
        
        self.drawlist = []
        
        self.root.mainloop()
        
        
    def draw(self, data, color):
        """Draw an arbitrary object, using the data paramater,
        
        which has to be an iterable consists of row and column coordinates."""
        
        for i in range(len(data)):
            self.canvas.create_oval((data[i][1] - 1) * self.gridsize,
                                    (data[i][0] - 1) * self.gridsize,
                                    data[i][1] * self.gridsize - 1,
                                    data[i][0] * self.gridsize - 1,
                                    fill=color, outline=color)
              
    
    def getdata(self, event):
        """Function that helps to draw easily on the canvas."""
        
        col = event.x // self.gridsize + 1
        row = event.y // self.gridsize + 1
        
        if (row, col) not in self.drawlist:
            self.drawlist.append((row, col))
            
        self.canvas.delete(ALL)
        self.draw(self.drawlist, "darkgrey")        
        print(self.drawlist)
        
        
    def getdata2(self, event):
        """Function to draw a 10x10 square."""
        
        col = event.x // self.gridsize + 1
        row = event.y // self.gridsize + 1
        
        for j in range(col, col + 10):
            for i in range(row, row + 10):
                if (i, j) not in self.drawlist:
                    self.drawlist.append((i, j))
                
        self.canvas.delete(ALL)
        self.draw(self.drawlist, "darkgrey")
        print(self.drawlist)
        
        
    def deldata(self, event):
        """Function that helps to remove things easily from the canvas."""
        
        col = event.x // self.gridsize + 1
        row = event.y // self.gridsize + 1
        
        if (row, col) in self.drawlist:
            self.drawlist.remove((row, col))
            
        self.canvas.delete(ALL)
        self.draw(self.drawlist, "darkgrey")        
        print(self.drawlist)
        
        
    def deldata2(self, event):
        """Function to remove a 10x10 square."""
        
        col = event.x // self.gridsize + 1
        row = event.y // self.gridsize + 1
        
        for j in range(col, col + 10):
            for i in range(row, row + 10):
                if (i, j) in self.drawlist:
                    self.drawlist.remove((i, j))
                
        self.canvas.delete(ALL)
        self.draw(self.drawlist, "darkgrey")
        print(self.drawlist)
        
        
builder = Snakebuild(80, 60, 10)
