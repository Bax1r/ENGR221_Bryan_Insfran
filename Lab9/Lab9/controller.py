"""
Author: Prof. Alyssa
The Controller of the game, including handling key presses
(and AI in the next assignment). You will update this file.

Adapted from HMC CS60

Last Updated: 5/16/24 3:02 AM
"""

from preferences import Preferences
from gameData import GameData
from boardDisplay import BoardDisplay

import pygame
from enum import Enum
from queue import Queue

class Controller():
    def __init__(self):
        # The current state of the board
        self.__data = GameData()
        # The display
        self.__display = BoardDisplay()
        # How many frames have passed
        self.__numCycles = 0

        # Attempt to load any sounds and images
        try:
            pygame.mixer.init()
            self.__audioEat = pygame.mixer.Sound(Preferences.EAT_SOUND)
            self.__display.headImage = pygame.image.load(Preferences.HEAD_IMAGE)
        except:
            print("Problem error loading audio / images")
            self.__audioEat = None

        # Initialize the board for a new game
        self.startNewGame()
        
    def startNewGame(self):
        """ Initializes the board for a new game """

        # Place the snake on the board
        self.__data.placeSnakeAtStartLocation()

    def gameOver(self):
        """ Indicate that the player has lost """
        self.__data.setGameOver()

    def run(self):
        """ The main loop of the game """

        # Keep track of the time that's passed in the game 
        clock = pygame.time.Clock()

        # Loop until the game ends
        while not self.__data.getGameOver():
            # Run the main behavior
            self.cycle() 
            # Sleep
            clock.tick(Preferences.SLEEP_TIME)

    def cycle(self):
        """ The main behavior of each time step """

        # Check for user input
        self.checkKeypress()
        # Update the snake state
        self.updateSnake()
        # Update the food state
        self.updateFood()
        # Increment the number of cycles
        self.__numCycles += 1
        # Update the display based on the new state
        self.__display.updateGraphics(self.__data)

    def checkKeypress(self):
        """ Update the game based on user input """
        # Check for keyboard input
        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT:
                self.gameOver()
            # Change the snake's direction based on the keypress
            elif event.type == pygame.KEYDOWN:
                # Reverse direction of snake
                if event.key in self.Keypress.REVERSE.value:
                    self.reverseSnake()
                # Enter AI mode
                elif event.key in self.Keypress.AI.value:
                    self.__data.setAIMode()
                # Change Snake's Direction to North
                elif event.key in self.Keypress.UP.value:
                    if not self.__data.getHeadNorthNeighbor().isBody():
                        self.__data.setDirectionNorth()
                # Change Snake's Direction to South
                elif event.key in self.Keypress.DOWN.value:
                    if not self.__data.getHeadSouthNeighbor().isBody():
                        self.__data.setDirectionSouth()
                # Change Snake's Direction to East
                elif event.key in self.Keypress.RIGHT.value:
                    if not self.__data.getHeadEastNeighbor().isBody():
                        self.__data.setDirectionEast()
                # Change Snake's Direction to West
                elif event.key in self.Keypress.LEFT.value:
                    if not self.__data.getHeadWestNeighbor().isBody():
                        self.__data.setDirectionWest()

    def updateSnake(self):
        """ Move the snake forward one step, either in the current 
            direction, or as directed by the AI """

        # Move the snake once every REFRESH_RATE cycles
        if self.__numCycles % Preferences.REFRESH_RATE == 0:
            # Find the next place the snake should move
            if self.__data.inAIMode():
                nextCell = self.getNextCellFromBFS()
            else:
                nextCell = self.__data.getNextCellInDir()
            try:
                # Move the snake to the next cell
                self.advanceSnake(nextCell)
            except:
                print("Failed to advance snake")

    def advanceSnake(self, nextCell):
        """ Update the state of the world to move the snake's head to the given cell """

        # If we run into a wall or the snake, it's game over
        if nextCell.isWall() or nextCell.isBody():
            self.gameOver()
        
        # If we eat food, update the state of the board
        elif nextCell.isFood():
            self.playSound_eat()

            self.__data.updateHead(nextCell)

            self.__data.removeFood(nextCell)

        # If the next cell is empty, advance the snake without modifying its length
        elif nextCell.isEmpty():
            self.__data.updateHead(nextCell)

            self.__data.updateTail()

    def updateFood(self):
        """ Add food every FOOD_ADD_RATE cycles or if there is no food """
        if self.__data.noFood() or (self.__numCycles % Preferences.FOOD_ADD_RATE == 0):
            self.__data.addFood()

    def getNextCellFromBFS(self):
        """ Uses BFS to search for the food closest to the head of the snake.
            Returns the *next* step the snake should take along the shortest path
            to the closest food cell. """
        
        # Parepare all the tiles to search
        self.__data.resetCellsForSearch()

        # Initialize a queue to hold the tiles to search
        cellsToSearch = Queue()

        # Add the head to the queue and mark it as added
        head = self.__data.getSnakeHead()
        head.setAddedToSearchList()
        cellsToSearch.put(head)

        #Uses recursion to store the cells to add
        return self.BFS(cellsToSearch)
        
        # If the search failed, return a random neighbor
        return self.__data.getRandomNeighbor(head)
    
    def BFS(self, queue):
        Root = queue._get()
        
        Children = self.__data.getNeighbors(Root)       # Have seen as issue where the function will recurse nearly 1,000 
                                                        # times and end the game if the food is too far from the head
        
        for cell in Children:
            if cell == None:
                continue
            if cell.isBody():
                continue
            if cell.isWall():
                continue
            if cell.alreadyAddedToSearchList() == False:
                cell.setParent(Root)
                if cell.isFood():
                    return self.getFirstCellInPath(cell)
                cell.setAddedToSearchList()
                queue.put(cell)
            else:
                continue
        return self.BFS(queue)

    def getFirstCellInPath(self, foodCell):
        """ Recurses as many times as necessary to return the most optimal cell to move to"""

        if foodCell.getParent() == self.__data.getSnakeHead():
            return foodCell
        else:
            return self.getFirstCellInPath(foodCell.getParent())
    
    def reverseSnake(self):
        """ Inverts the order of the snake cells, then relabels the head and tail, then relies on some RNG to change direction """
        self.__data.reverseSnake()
        
        self.__data.RelabelSnake()

        cell = self.__data.getRandomNeighbor(self.__data.getSnakeHead())

        self.__data.DirectionChange(cell)

    def playSound_eat(self):
        """ Plays an eating sound """
        if self.__audioEat:
            pygame.mixer.Sound.play(self.__audioEat)
            pygame.mixer.music.stop()

    class Keypress(Enum):
        """ An enumeration (enum) defining the valid keyboard inputs 
            to ensure that we do not accidentally assign an invalid value.
        """
        UP = pygame.K_i, pygame.K_UP        # i and up arrow key
        DOWN = pygame.K_k, pygame.K_DOWN    # k and down arrow key
        LEFT = pygame.K_j, pygame.K_LEFT    # j and left arrow key
        RIGHT = pygame.K_l, pygame.K_RIGHT  # l and right arrow key
        REVERSE = pygame.K_r,               # r
        AI = pygame.K_a,                    # a


if __name__ == "__main__":
    Controller().run()