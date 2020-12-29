import pygame
import math
from queue import PriorityQueue

WIDTH = 600 #defining the width of the window in pixels
WIN = pygame.display.set_mode((WIDTH,WIDTH)) #setting the window with it's dimensions
pygame.display.set_caption("BFS Path Finding Algorithm")#name (caption) of the window

RED = (255, 0, 0)         #already visited squares
GREEN = (0, 255, 0)       #nodes in queue
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)   #not visited
BLACK = (0, 0, 0)         #barrier
PURPLE = (128, 0, 128)    #path
ORANGE = (255, 165, 0)    #starting node
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)#end node

class Spot:#basically cubes,and its neigbors, keep track of its location and color
    def __init__(self,row,col,width, total_rows):#width is how wide is the spot
        self.row=row 
        self.col=col 
        self.x=row*width #what is the position of that cube
        self.y=col*width #to keep track of x and y, actual coordinate postion on screen
        self.neighbors=[]
        self.color=WHITE #initial color of grid
        self.width=width
        self.total_rows=total_rows
    def get_pos(self): #method to get the mouse cursor position get_pos() -> (x, y)
        return self.row, self.col
        # Returns the X and Y position of the mouse cursor. The position is relative the the top-left corner of the display. The cursor position can be located outside of the display window, but is always constrained to the screen.
    
    
    #These functions are just gonna tell the state of a node so we can decide their fate
    def is_closed(self): #visited node
        return self.color== RED 
    def is_open(self):#in the queue
        return self.color==GREEN
    def is_barrier(self):# is a barrier
        return self.color==BLACK
    def is_start(self): #start color
        return self.color==ORANGE
    def is_end(self): #end color
        return self.color==TURQUOISE

    def reset(self):#change the color back to white on pressing c
        self.color=WHITE

    def make_closed(self): 
        self.color=RED #mark the node as VISITED
    def make_open(self): 
        self.color=GREEN #mark the node inside QUEUE
    def make_barrier(self):
        self.color=BLACK #mark the node as BARRIER
    def make_start(self):  
        self.color=ORANGE #mark the node as START 
    def make_end(self):  
        self.color=TURQUOISE #mark the node as END 
    def make_path(self): 
        self.color=PURPLE #mark the nodes as PATH
    
    def draw(self,win): #where do we wanna draw this ?? #draw a rectangle in window
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
                    #window ,color     ,x coord ,y coor,length right   ,height down
    def update_neighbors(self,grid):
        self.neighbors=[]
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():#DOWN
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():#UP
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():#LEFT
            self.neighbors.append(grid[self.row][self.col-1])

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():#RIGHT
            self.neighbors.append(grid[self.row][self.col+1])
        
        if self.col < self.total_rows-1 and self.row > 0 and not grid[self.row-1][self.col+1].is_barrier():#North East
            self.neighbors.append(grid[self.row-1][self.col+1])

        if self.col >0 and self.row > 0 and not grid[self.row-1][self.col-1].is_barrier():#North West
            self.neighbors.append(grid[self.row-1][self.col-1])

        if self.col < self.total_rows-1 and self.row < self.total_rows-1 and not grid[self.row+1][self.col+1].is_barrier():#South East
            self.neighbors.append(grid[self.row+1][self.col+1])

        if self.col >0 and self.row < self.total_rows-1 and not grid[self.row+1][self.col-1].is_barrier():#South West
            self.neighbors.append(grid[self.row+1][self.col-1])

    def __lt__(self,other):
        return False

def h(p1,p2): #this is the heuristic function (manhattan distance)
    # x1,y1=p1
    # x2,y2=p2
    return 0
    # return abs(x1-x2)+abs(y1-y2)
    # return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start]=0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start]=h(start.get_pos(),end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1

            if temp_g_score<g_score[neighbor]:
                came_from[neighbor]=current
                g_score[neighbor]=temp_g_score
                f_score[neighbor]=temp_g_score+h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current!= start:
            current.make_closed()
    
    return False

def make_grid(rows,width):
    grid=[] #make a grid which will have spot objects in them
    gap=width//rows #WIDTH it is intgeger division giving the width of these cubes
    for i in range(rows): 
        grid.append([]) #each grid will have a array of spot objects
        for j in range(rows):
            spot = Spot(i,j,gap,rows) #defining a new spot
            #to make a spot we are passing it (row,column,width,total pixels)
            grid[i].append(spot) #appnding the spot in array
    return grid #return the grid

def draw_grid(win,rows,width): #draws the black lines making them look like grid in the window
    gap=width//rows
    
    for i in range(rows):
        pygame.draw.line(win,GREY, (0,i*gap),(width,i*gap)) #draws a horizontal line (from start to end ______________)
    for j in range(rows):
        pygame.draw.line(win,GREEN, (j*gap,0),(j*gap,width)) #draws a horizontal line (from top  to bottom | | | | |)
    # pygame.draw.line(win,RED, (0*gap,0),(0*gap,width))

def draw(win,grid,rows,width):
    win.fill(WHITE)#fills the entire frame with white
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked_pos(pos,rows,width):
    gap=width//rows
    y,x=pos
    row=y//gap
    col=x//gap
    return row,col

def main(win,width):
    ROWS=50
    grid=make_grid(ROWS,width)

    start=None
    end=None
    
    run = True
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: #0 represents LEFT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot!=end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot!=end and spot!=start:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]: #2 represents RIGHT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start=None
                elif spot == end:
                    end=None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda : draw(win,grid,ROWS,width),grid,start,end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)
    pygame.quit()

main(WIN,WIDTH)
