import pygame
import random
import sys

# Font
pygame.font.init()
FONT_1 = pygame.font.SysFont("comicsans", 30)
FONT_2 = pygame.font.SysFont("comicsans", 20)

# Colours
BLACK   = (0, 0, 0, 128)
WHITE   = (255, 255, 255, 128)
RED     = (255, 0, 0, 128)
GREEN   = (0, 255, 0, 128)
BLUE    = (0, 0, 255, 128)
ORANGE  = (255, 165, 0, 128)
YELLOW  = (225, 225, 0, 128)
PINK    = (255, 192, 203, 128)
SKY     = (191, 255, 244, 128)
CYAN    = (0, 255, 255, 128)

colours = [RED, GREEN, BLUE, ORANGE, YELLOW, PINK, SKY, CYAN]

# Window size
W_WIDTH  = 1000 
W_HEIGHT = 650

# Quadtree area
Q_WIDTH  = W_WIDTH - 350
Q_HEIGHT = W_HEIGHT

# Text area
T_WIDTH  = W_WIDTH - Q_WIDTH
T_HEIGHT = W_HEIGHT

# Square min and max size
SQUARE_MIN = 20
SQUARE_MAX = 50

# Timer
DELAY_MS = 15

# Screen
SCREEN = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
pygame.display.set_caption("Quadtree collision")

'''
Quad tree implementation
Each instance is a tree node
Not perfect
'''
class Quadtree():
    # Quadtree quadrant indexes
    QUAD_PARENT       = -1 # Parent node
    QUAD_TOP_LEFT     = 0  # X, Y
    QUAD_TOP_RIGHT    = 1  # X + (W / 2), Y
    QUAD_BOTTOM_RIGHT = 2  # X + (W / 2), Y + (H / 2)
    QUAD_BOTTOM_LEFT  = 3  # X, Y + (H / 2)
    
    # Quadtree constants
    QUADTREE_MAX_OBJECTS = 5
    QUADTREE_MAX_LEVELS  = 5

    def __init__(self, level, bounds):
        self.__level = level
        self.__bound = bounds
        self.__nodes = [None] * 4
        self.__items = []

    '''
    Return node bound
    '''
    def GetBound(self):
        return self.__bound

    '''
    Remove items and clear nodes
    '''
    def Clear(self):
        self.__items.clear()

        for node in self.__nodes:
            if node is not None:
                node.Clear()

        self.__nodes.clear()
        self.__nodes = [None] * 4
    
    '''
    Split node into 4 children nodes
    '''
    def Split(self):
        sub_w = self.__bound.width // 2
        sub_h = self.__bound.height // 2
        x = self.__bound.left
        y = self.__bound.top

        self.__nodes[self.QUAD_TOP_LEFT]     = Quadtree(self.__level + 1, pygame.Rect(x           , y         , sub_w, sub_h))
        self.__nodes[self.QUAD_TOP_RIGHT]    = Quadtree(self.__level + 1, pygame.Rect(x + sub_w   , y         , sub_w, sub_h))
        self.__nodes[self.QUAD_BOTTOM_RIGHT] = Quadtree(self.__level + 1, pygame.Rect(x + sub_w   , y + sub_h , sub_w, sub_h))
        self.__nodes[self.QUAD_BOTTOM_LEFT]  = Quadtree(self.__level + 1, pygame.Rect(x           , y + sub_h , sub_w, sub_h))

    '''
    Return the index of the node which contains the desired object
    '''
    def GetContainingNodeIndex(self, square):
        index = self.QUAD_PARENT

        is_top_quadrants    = square.y < self.__bound.centery and square.y + square.size < self.__bound.centery
        is_bottom_quadrants = not is_top_quadrants and square.y > self.__bound.centery
        is_left_quadrants   = square.x < self.__bound.centerx and square.x + square.size < self.__bound.centerx
        is_right_quadrants  = not is_left_quadrants and square.x > self.__bound.centerx

        if is_left_quadrants:
            if is_top_quadrants:
                index = self.QUAD_TOP_LEFT
            elif is_bottom_quadrants:
                index = self.QUAD_BOTTOM_LEFT

        if is_right_quadrants:
            if is_top_quadrants:
                index = self.QUAD_TOP_RIGHT
            elif is_bottom_quadrants:
                index = self.QUAD_BOTTOM_RIGHT
        
        return index
    
    '''
    Check the element count in the node and, if necessary, split into 4 children nodes
    '''
    def __MaybeSplit(self):
        if len(self.__items) > self.QUADTREE_MAX_OBJECTS and self.__level < self.QUADTREE_MAX_LEVELS:
            new_list     = []
            top_left     = []
            top_right    = []
            bottom_right = []
            bottom_left  = []

            for item in self.__items:
                index = self.GetContainingNodeIndex(item)
                if index == self.QUAD_PARENT:
                    new_list.append(item)
                elif index == self.QUAD_TOP_LEFT:
                    top_left.append(item)
                elif index == self.QUAD_TOP_RIGHT:
                    top_right.append(item)
                elif index == self.QUAD_BOTTOM_RIGHT:
                    bottom_right.append(item)
                elif index == self.QUAD_BOTTOM_LEFT:
                    bottom_left.append(item)

                self.__items = new_list
            
            if self.__nodes[0] is None:
                self.Split()

            self.__nodes[self.QUAD_TOP_LEFT].Insert(top_left)
            self.__nodes[self.QUAD_TOP_RIGHT].Insert(top_right)
            self.__nodes[self.QUAD_BOTTOM_RIGHT].Insert(bottom_right)
            self.__nodes[self.QUAD_BOTTOM_LEFT].Insert(bottom_left)

    '''
    Add items into the item list
    '''
    def Insert(self, squares):
        for square in squares:
            self.__items.append(square)
        self.__MaybeSplit()

    '''
    Remove last element from the item list
    '''
    def Remove(self):
        self.__items.remove(self.__items[len(self.__items) - 1])

    '''
    Return the list of rectangles which make up the nodes
    '''
    def GetQuadRectangles(self, rectangles):
        if self.__nodes[0] is not None:
            for i in range(0, len(self.__nodes)):
                self.__nodes[i].GetQuadRectangles(rectangles)

        rectangles.append(self.__bound)

    '''
    Check for any collisions within the node (and children nodes)
    '''
    def CheckCollisions(self, collisions, parent_items = []):
        num_comparisons = 0

        if self.__nodes[0] is not None:
            num_comparisons += self.__nodes[self.QUAD_TOP_LEFT].CheckCollisions(collisions, self.__items)
            num_comparisons += self.__nodes[self.QUAD_TOP_RIGHT].CheckCollisions(collisions, self.__items)
            num_comparisons += self.__nodes[self.QUAD_BOTTOM_RIGHT].CheckCollisions(collisions, self.__items)
            num_comparisons += self.__nodes[self.QUAD_BOTTOM_LEFT].CheckCollisions(collisions, self.__items)
        
        else:
            joined = self.__items + parent_items
            for i in range(0, len(joined)):
                for ii in range(i + 1, len(joined)):
                    num_comparisons += 1
                    x_overlaps = joined[i].x < joined[ii].x + joined[ii].size and joined[i].x + joined[i].size > joined[ii].x
                    y_overlaps = joined[i].y < joined[ii].y + joined[ii].size and joined[i].y + joined[i].size > joined[ii].y
                    if x_overlaps and y_overlaps:
                        collisions.append((joined[i], joined[ii]))

        return num_comparisons

'''
Square class
The object used to test collisions
'''
class Square():
    def __init__(self, x, y, size, colour):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.is_colliding = False
        velX = random.randrange(2, 4)
        velY = random.randrange(2, 4)
        self.velocity = [velX, velY]
        self.surface = pygame.Surface((size, size), pygame.SRCALPHA)

    '''
    Draw to screen
    '''
    def Draw(self):
        if self.is_colliding:
            self.surface.fill((self.colour[0], self.colour[1], self.colour[2], 255))
        else:
            self.surface.fill(self.colour)
        SCREEN.blit(self.surface, (self.x, self.y))

    '''
    Update square's positon
    '''
    def Update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        if self.x + self.velocity[0] < 0 or self.x + self.velocity[0] > Q_WIDTH - self.size:
            self.velocity[0] *= -1
        if self.y + self.velocity[1] < 0 or self.y + self.velocity[1] > Q_HEIGHT - self.size:
            self.velocity[1] *= -1

        self.Draw()
        self.is_colliding = False

# Global variables
squares             = []
qt                  = Quadtree(1, pygame.Rect(0, 0, Q_WIDTH, Q_HEIGHT))
is_using_quadtree   = False

'''
Brute force collision test
Check each square against all other squares
'''
def CheckCollisions(items, collisions):
    num_comparisons = 0

    if len(items) < 2:
        return num_comparisons

    for i in range(0, len(items)):
        for ii in range(i + 1, len(items)):
            num_comparisons += 1
            x_overlaps = items[i].x < items[ii].x + items[ii].size and items[i].x + items[i].size > items[ii].x
            y_overlaps = items[i].y < items[ii].y + items[ii].size and items[i].y + items[i].size > items[ii].y
            if x_overlaps and y_overlaps:
                collisions.append((items[i], items[ii]))

    return num_comparisons

'''
Add square to the global square list
'''
def AddSquare():
    size = random.randrange(SQUARE_MIN, SQUARE_MAX)
    x    = random.randrange(0, Q_WIDTH - size)
    y    = random.randrange(0, Q_HEIGHT - size)
    rand_col = random.randrange(0, len(colours) - 1)
    squares.append(Square(x, y, size, colours[rand_col]))

'''
Remove last square from the global square list
'''
def RemoveSquare():
    if len(squares) == 1:
        squares.remove(squares[0])
    elif len(squares) > 1:
        rand = random.randrange(0, len(squares) - 1)
        squares.remove(squares[rand])

'''
Program main logic loop
Handle input
Update logic
Render to screen
'''
def MainLoop():
    global qt
    global is_using_quadtree
    SCREEN.fill(WHITE)

    # Draw the collision area
    pygame.draw.rect(SCREEN, BLACK, (0, 0, Q_WIDTH, Q_HEIGHT))

    # Check collisions using brute force
    collisions     = []
    quadtree_rects = []
    compare_count  = 0

    '''
    If using quadtree, clear the quadtree list and add all squares
    This is definately not the most efficient method of doing this, but it's the easiest for visualisation purposes

    If not using quadtree, perform brute-force collision test
    '''
    if is_using_quadtree:
        qt.Clear()
        qt.Insert(squares)
        compare_count = qt.CheckCollisions(collisions)
    else:
        compare_count = CheckCollisions(squares, collisions)

    for i in range(0, len(collisions)):
        collisions[i][0].is_colliding = True
        collisions[i][1].is_colliding = True

    # Draw each square
    for square in squares:
        square.Update()

    # render text
    txt_collision_mode  = ["brute force", "quadtree"]
    txt_square_count    = FONT_1.render("Square count: "         + str(len(squares))    , 1, BLACK)
    txt_compare_count   = FONT_1.render("Number of comparions: " + str(compare_count)   , 1, BLACK)
    txt_collision_count = FONT_1.render("Number of collisions: " + str(len(collisions)) , 1, BLACK)
    txt_arr_up          = FONT_1.render("'UP' - add a square"      , 1, BLACK)
    txt_arr_down        = FONT_1.render("'DOWN'- remove a square" , 1, BLACK)
    txt_arr_space       = FONT_1.render("'SPACE' - toggle collision mode", 1, BLACK)
    txt_collision_mode  = FONT_1.render("Collision mode: " + txt_collision_mode[is_using_quadtree] , 1, BLACK)

    SCREEN.blit(txt_square_count    , (Q_WIDTH + 20, 60))
    SCREEN.blit(txt_compare_count   , (Q_WIDTH + 20, 80))
    SCREEN.blit(txt_collision_count , (Q_WIDTH + 20, 100))
    SCREEN.blit(txt_arr_up          , (Q_WIDTH + 20, 140))
    SCREEN.blit(txt_arr_down        , (Q_WIDTH + 20, 160))
    SCREEN.blit(txt_arr_space       , (Q_WIDTH + 20, 180))
    SCREEN.blit(txt_collision_mode  , (Q_WIDTH + 20, 200))

    # Draw quadtree node bounds
    if is_using_quadtree:
        qt.GetQuadRectangles(quadtree_rects)
        for rect in quadtree_rects:
            pygame.draw.line(SCREEN, RED, (rect.left, rect.top)         , (rect.right - 2, rect.top)        , 2)
            pygame.draw.line(SCREEN, RED, (rect.left, rect.bottom - 2)  , (rect.right - 2, rect.bottom - 2) , 2)
            pygame.draw.line(SCREEN, RED, (rect.left, rect.top)         , (rect.left, rect.bottom - 2)      , 2)
            pygame.draw.line(SCREEN, RED, (rect.right - 2, rect.top)    , (rect.right - 2, rect.bottom - 2) , 2)

    pygame.display.update()
    pygame.time.delay(DELAY_MS)

    # Handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
            elif event.key == pygame.K_UP:
                AddSquare()
            elif event.key == pygame.K_DOWN:
                RemoveSquare()
            elif event.key == pygame.K_SPACE:
                is_using_quadtree = not is_using_quadtree

if __name__ == '__main__':
    while True:
        MainLoop()
    pygame.quit()
