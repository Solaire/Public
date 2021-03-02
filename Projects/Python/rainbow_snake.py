from pygame import *
import sys
from os.path import abspath, dirname
from random import *

BASE_PATH = abspath(dirname(__file__))

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen and game area
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 700

GAME_AREA_WIDTH = 500
GAME_AREA_HEIGHT = 500
GAME_AREA_X_POS = 100
GAME_AREA_Y_POS = 100

# Game states
MENU_STATE = 0
PLAY_STATE = 1
GAME_OVER_STATE = 2
END_STATE = 3

# Font and font size
FONT = BASE_PATH + '/common/font.ttf'
FONT_SIZE_TITLE = 50
FONT_SIZE_PROMPT = 25
FONT_SIZE_SCORE = 20

# Test location
TITLE_TEXT_POS_X = 164
TITLE_TEXT_POS_Y = 155
GAME_OVER_TEXT_POS_X = 210
GAME_OVER_TEXT_POS_Y = 225
PLAY_PROMPT_TEXT_POS_X = 201
PLAY_PROMPT_TEXT_POS_Y = 270
SCORE_TEXT_POS_X = 5
SCORE_TEXT_POS_Y = 5

# Snake directions
DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4

# Snake and food size
FOOD_SIZE = 10

'''
Calculate and return the closest divisible of n / m
'''
def FindClosestDivisible(n, m):
    # Find the quotient
    q = int(n / m)

    # 1st possible closeset number
    n1 = int(m * q)

    # 2nd possible closest number
    n2 = 0

    if m * m > 0:
        n2 = int(m * (q + 1))
    else:
        n2 = int(m * (q - 1))

    # If true, this is the closest number
    if abs(n - n1) < abs(n - n2):
        return n1

    # else this is the closest number
    return n2

'''
Text drawing class
'''
class Text(object):
    def __init__(self, textFont, size, message, color, xpos, ypos):
        self.font = font.Font(textFont, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    '''
    Draw text to screen
    '''
    def Draw(self, surface):
        surface.blit(self.surface, self.rect)

'''
Snake food class
'''
class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = FOOD_SIZE
        self.colour = WHITE
        self.SetRandomPosition()

    '''
    Return current food position
    '''
    def GetPosition(self):
        return Vector2(self.x, self.y)

    '''
    Set radnom position, snapping it to the invisible "grid"
    This function does not check if the position is occupied by snake parts
    '''
    def SetRandomPosition(self):
        x = uniform(GAME_AREA_X_POS, GAME_AREA_X_POS + GAME_AREA_WIDTH - 20)
        y = uniform(GAME_AREA_Y_POS, GAME_AREA_Y_POS + GAME_AREA_HEIGHT - 20)
        self.x = FindClosestDivisible(x, FOOD_SIZE)
        self.y = FindClosestDivisible(y, FOOD_SIZE)

    '''
    Draw food to screen
    '''
    def Draw(self, screen):
        draw.rect(screen, self.colour, Rect(self.x, self.y, self.size, self.size))

'''
Represents snake's invidicual cells
'''
class SnakePart:
    def __init__(self, x, y, size, colour):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour

    '''
    Return position of the cell
    '''
    def GetPosition(self):
        return Vector2(self.x, self.y)

    '''
    Set position of the cell
    '''
    def SetPosition(self, vec2Pos):
        self.x = vec2Pos.x
        self.y = vec2Pos.y

    '''
    If the cell's position is outside of game area, set the position to the opposite size of the axis
    This allows the snake to "wrap around the game area"
    '''
    def MaybeWrapAround(self):
        if self.x < GAME_AREA_X_POS:
            self.x = GAME_AREA_X_POS + GAME_AREA_WIDTH - 20
        elif self.x > GAME_AREA_X_POS + GAME_AREA_WIDTH - 20:
            self.x = GAME_AREA_X_POS

        if self.y < GAME_AREA_Y_POS:
            self.y = GAME_AREA_Y_POS + GAME_AREA_HEIGHT - 20
        elif self.y > GAME_AREA_Y_POS + GAME_AREA_HEIGHT - 20:
            self.y = GAME_AREA_Y_POS

        self.x = FindClosestDivisible(self.x, FOOD_SIZE)
        self.y = FindClosestDivisible(self.y, FOOD_SIZE)

    '''
    Move the cell's position by x and y
    '''
    def Move(self, x, y):
        self.x += x
        self.y += y

    '''
    Set cell's colour
    '''
    def SetColour(self, colour):
        self.colour = colour

    ''' 
    Draw cell to screen
    '''
    def Draw(self, screen):
        draw.rect(screen, self.colour, Rect(self.x, self.y, self.size, self.size))

'''
Snake class
Contains array of snake parts
'''
class Snake:
    def __init__(self):
        self.parts = []
        self.direction  = DIRECTION_UP
        self.directionChanged = False
        self.Reset()

    '''
    Reset snake's state to default
    '''
    def Reset(self):
        self.parts = []
        almostRed = (255, 10, 0)

        initX = int(SCREEN_WIDTH / 2)
        initY = int(SCREEN_WIDTH / 2)
        self.parts.append(SnakePart(FindClosestDivisible(initX, FOOD_SIZE), FindClosestDivisible(initY, FOOD_SIZE), FOOD_SIZE, almostRed))

    '''
    Get snake's movement vector
    '''
    def __GetMovement(self):
        dir = self.__GetDirection()
        offset = Vector2(dir.x * FOOD_SIZE, dir.y * FOOD_SIZE)
        return offset

    '''
    Get snake's direction of travel
    '''
    def __GetDirection(self):
        dir = Vector2(0, 0)

        if self.direction == DIRECTION_LEFT:
            dir.x = -1

        elif self.direction == DIRECTION_RIGHT:
            dir.x = 1

        elif self.direction == DIRECTION_UP:
            dir.y = -1

        elif self.direction == DIRECTION_DOWN:
            dir.y = 1

        self.directionChanged = False
        return dir

    '''
    Set colour of a specified cell
    Colour is a rainbow gradient
    '''
    def __SetColour(self, cell):
        r = 0
        g = 0
        b = 0

        colourPicker = int(((len(self.parts) - 1 ) % 150) / 25)
        snakePartCountMod25 = (len(self.parts) - 1) % 25

        if colourPicker == 0:
            r = 255
            g = 10 * snakePartCountMod25
            b = 0

        elif colourPicker == 1:
            r = 255 - 10 * snakePartCountMod25
            g = 255
            b = 0

        elif colourPicker == 2:
            r = 0
            g = 255
            b = 10 * snakePartCountMod25

        elif colourPicker == 3:
            r = 0
            g = 255 - 10 * snakePartCountMod25
            b = 255

        elif colourPicker == 4:
            r = 10 * snakePartCountMod25
            g = 0
            b = 255

        elif colourPicker == 5:
            r = 255
            g = 0
            b = 255 - 10 * snakePartCountMod25

        colour = (r, g, b)
        cell.SetColour(colour)

    '''
    Move the snake along its direction of travel
    '''
    def Move(self):
        previousPos = self.parts[0].GetPosition()
        movement = self.__GetMovement()

        self.parts[0].Move(movement.x, movement.y)
        self.parts[0].MaybeWrapAround()

        # Due to each cell having a different colour, we need to move each cell
        # Otherwise a solution would be to move the last cell (tail) to the head
        for i in range(1, len(self.parts)):
            tmp = self.parts[i].GetPosition()
            self.parts[i].SetPosition(previousPos)
            previousPos = tmp

    '''
    Change snake's direction of travel
    '''
    def ChangeDirection(self, newDirection):
        if abs(newDirection - self.direction) > 1 and self.directionChanged == False:
            self.direction = newDirection
            self.directionChanged = True

    '''
    Add a cell to snake's tail
    '''
    def AddBodyPart(self):
        bodyPart = SnakePart(-16, -16, FOOD_SIZE, WHITE)
        self.__SetColour(bodyPart)
        self.parts.append(bodyPart)

    '''
    Return true if snake's head overlaps with other body part
    Otherwise false
    '''
    def IsBitingSelf(self):
        headPos = self.GetHeadPosition()
        for i in range(1, len(self.parts)):
            partPos = self.parts[i].GetPosition()
            if headPos == partPos:
                return True

        return False

    '''
    Get position of snake's head
    '''
    def GetHeadPosition(self):
        return self.parts[0].GetPosition()

    '''
    Draw snake to the screen
    '''
    def Draw(self, game):
        for part in self.parts:
            part.Draw(game)

'''
Main game class
'''
class Game:
    screen = None
    snake = None
    food = None
    gameOver = False

    def __init__(self):
        init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = time.Clock()
        self.timer = time.get_ticks()
        self.score = 0

        self.gameOverText = Text(FONT, FONT_SIZE_TITLE, "Game Over", WHITE, GAME_OVER_TEXT_POS_X, GAME_OVER_TEXT_POS_Y)
        self.scoreText = Text(FONT, FONT_SIZE_SCORE, "Score", WHITE, SCORE_TEXT_POS_X, SCORE_TEXT_POS_Y)
        
        done = False
        self._snake = Snake()
        self._food = Food()

        while True:
            self.clock.tick(15)
            display.flip()

            if not done:
                for evt in event.get():
                    if evt.type == QUIT:
                        done = True
                    if evt.type == KEYDOWN and evt.key == K_LEFT:
                        self._snake.ChangeDirection(DIRECTION_LEFT)
                    elif evt.type == KEYDOWN and evt.key == K_RIGHT:
                        self._snake.ChangeDirection(DIRECTION_RIGHT)
                    elif evt.type == KEYDOWN and evt.key == K_UP:
                        self._snake.ChangeDirection(DIRECTION_UP)
                    elif evt.type == KEYDOWN and evt.key == K_DOWN:
                        self._snake.ChangeDirection(DIRECTION_DOWN)
                    elif evt.type == KEYDOWN and evt.key == K_ESCAPE:
                        sys.exit(0)

                self.Update()

                self.screen.fill((0, 0, 0))
                self.DrawGameArea()
                self._snake.Draw(self.screen)
                self._food.Draw(self.screen)

                self.acutalScore = Text(FONT, 20, str(self.score), WHITE, 86, 5)
                self.scoreText.Draw(self.screen)
                self.acutalScore.Draw(self.screen)

                if self.IsFailure():
                    gameOver = True
                    done = True

            else:
                currentTime = time.get_ticks()
                self.ShowGameOverScreen(currentTime)

    '''
    Reset game state
    '''
    def Reset(self):
        self._snake.Reset()
        self._food = Food()
        self.keys = key.get_pressed()
        self.timer = time.get_ticks()
        self.noteTimer = time.get_ticks()
        self.snakeAlive = True

    '''
    Update game logic
    '''
    def Update(self):        
        self._snake.Move()

        if self._snake.GetHeadPosition() == self._food.GetPosition():
            self._food.SetRandomPosition()
            self._snake.AddBodyPart()
            self.score += 1

    '''
    Check if failure condition has been reached
    '''
    def IsFailure(self):
        if self._snake.IsBitingSelf():
            return True

        vec2SnakePos = self._snake.GetHeadPosition()
        if (vec2SnakePos.x < 0 or vec2SnakePos.x > SCREEN_WIDTH) and ((vec2SnakePos.y < 0 or vec2SnakePos.y > SCREEN_HEIGHT)):
            return True

        return False
    
    '''
    Display game over screen
    '''
    def ShowGameOverScreen(self, currentTime):
        self.screen.fill((0, 0, 0))
        passed = currentTime - self.timer
        self.gameOverText.Draw(self.screen)
        
        for e in event.get():
            if self.IsExit(e):
                sys.exit(0)

    '''
    Check if exit condition has been met
    '''
    def IsExit(self, event):
        return event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE)

    '''
    Draw game region
    '''
    def DrawGameArea(self):
        draw.rect(self.screen, WHITE, Rect(GAME_AREA_X_POS - 5, GAME_AREA_Y_POS - 5, GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        draw.rect(self.screen, BLACK, Rect(GAME_AREA_X_POS, GAME_AREA_Y_POS, GAME_AREA_WIDTH - 10, GAME_AREA_HEIGHT - 10))

if __name__ == '__main__':
    game = Game()
