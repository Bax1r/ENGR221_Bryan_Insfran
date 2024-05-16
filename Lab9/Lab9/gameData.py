"""
Author: Prof. Alyssa
Represents the current state of the game.

Assignment adapted from HMC CS60

Last Updated: 5/16/24 3:03 AM
"""

from boardCell import BoardCell
from preferences import Preferences

import random
from enum import Enum, auto


class GameData:
    def __init__(self):
        # Dimensions of the board (in cells)
        self.__height = Preferences.NUM_CELLS_TALL
        self.__width = Preferences.NUM_CELLS_WIDE

        # Keep track of how many cells are empty and in the board
        self.__freeCells = self.__height * self.__width
        self.__totalCells = self.__height * self.__width

        # The current movement mode of the snake (i.e., the current
        # direction or in AI mode
        self.__currentMode = self.SnakeMode.GOING_EAST

        #A 2D array of cells in the board
        self.__board = self.createBoard()

        # A list of cells that currently contain food (from oldest to newest)
        self.__foodCells = [] 
        # A list of cells that contain the snake (from head to tail)
        self.__snakeCells = []

        # Whether or not the game is over
        self.__gameOver = False

    ##########################
    # Initialization methods #
    ##########################

    def createBoard(self):
        """ Populate the starting state of the board.
            Returns a 2D array of cells in the board. """
        
        # Fill in the board with empty cells
        board = [[BoardCell(row, col) for col in range(self.__width)] for row in range(self.__height)]
        # Change the left and right edges to walls
        for row in range(self.__height):
            board[row][0].becomeWall()
            board[row][self.__width-1].becomeWall() 
            # Make sure these cells are not counted as "free"
            self.__freeCells -= 2
        # Change the top and bottom edges to walls
        for col in range(1, self.__width-1):
            board[0][col].becomeWall()
            board[self.__height-1][col].becomeWall()
            # Make sure these cells are not counted as "free"
            self.__freeCells -= 2

        return board
        
    def placeSnakeAtStartLocation(self):
        """ Place the snake in the upper left corner, facing east """

        head = self.getCell(1, 2)
        body = self.getCell(1, 1)
        
        # Mark these cells as the head and body
        head.becomeHead()
        body.becomeBody()

        # Add these cells to the snake cells list
        self.__snakeCells.append(head)
        self.__snakeCells.append(body)

        # Set the starting direction of the snake as east
        self.__currentMode = self.SnakeMode.GOING_EAST

        # Make sure these cells are not counted as "free"
        self.__freeCells -= 2

    ###############################
    # Information about the board #
    ###############################

    def inAIMode(self):
        """ Returns a boolean indicating whether or not we are in AI mode """
        return self.__currentMode == self.SnakeMode.AI_MODE

    def getCell(self, row, col):
        """ Returns the cell at the given row and column.
            Inputs: row - The row to get (between 0 and height-1)
                    col - The column to get (between 0 and width-1)
            Returns: The cell in that location """
        if (row >= 0 and row < self.__height) and (col >= 0 and col < self.__width):
            return self.__board[row][col]
        else:
            raise Exception("getCell tried to access cell outside of board: ({}, {})".format(row, col))
        
    ########################
    # Food related methods #
    ########################

    def noFood(self):
        """ Returns a boolean indicating whether 
            or not there is food on the board """
        return len(self.__foodCells) == 0
    
    def addFood(self):
        """ Adds food to an open spont on the board """

        # Find a value between 1 and self.__height-1 (inclusive)
        row = random.randrange(1, self.__height)
        # Find a value between 1 and self.__width-1 (inclusive)
        col = random.randrange(1, self.__width)
        # Get the cell at that location
        cell = self.getCell(row, col)

        # If it is empty, add food
        if cell.isEmpty():
            cell.becomeFood()
            self.__foodCells.append(cell)
            self.__freeCells -= 1

        # Otherwise, only add food if over 30% of our cells are free
        elif self.__freeCells / self.__totalCells > 0.3:
            self.addFood()

        # Otherwise, there is too much food on the board already
        else:
            print("Not adding more food")

    ##########################
    # Snake movement methods #
    ##########################

    def updateHead(self, new_head):
        new_head.becomeHead()   # Change the cells' type to be "Head" 

        self.getSnakeHead().becomeBody()    # Update the current "head" to now be "body"

        self.__snakeCells.insert(0, new_head)   # Insert the new head at the front/top of the list

    def updateTail(self):
        self.getSnakeTail().becomeEmpty()   # Change the cells' type to be "Empty"

        self.__snakeCells.remove(self.getSnakeTail())   # I chose remove instead of pop because pop didn't work
                                                        # Removes the last element in the snakeCells list

    def removeFood(self, nextCell):
        self.__foodCells.remove(nextCell)   # Removes the given cell from the foodCells list

    ###############################
    # Methods to access neighbors #
    ###############################

    def getNorthNeighbor(self, cell): 
        """ Returns the cell to the north of the given cell """
        row = cell.getRow()     #Stores the "Y" coordinate of the cell
        col = cell.getCol()     #Stores the "X" coordinate of the cell

        if row == 0:        #Meant to prevent the method accessing "Out of Bound" Data
            return None

        cell_ID = self.getCell(row - 1, col)    #Stores the data of the cell to its "North"

        return cell_ID   #Returns the cell a row above the given cell
        
    def getSouthNeighbor(self, cell):
        """ Returns the cell to the south of the given cell """
        row = cell.getRow()     #Stores the "Y" coordinate of the cell
        col = cell.getCol()     #Stores the "X" coordinate of the cell

        if row == self.__height - 1:    #Meant to prevent the method accessing "Out of Bound" Data
            return None

        cell_ID = self.getCell(row + 1, col)    #Stores the data of the cell to its "South"

        return cell_ID   #Returns the cell a row below the given cell
    
    def getEastNeighbor(self, cell):
        """ Returns the cell to the east of the given cell """
        row = cell.getRow()     #Stores the "Y" coordinate of the cell
        col = cell.getCol()     #Stores the "X" coordinate of the cell

        if col == self.__width - 1: #Meant to prevent the method accessing "Out of Bound" Data
            return None

        cell_ID = self.getCell(row, col + 1)    #Stores the data of the cell to its "East"

        return cell_ID   #Returns the cell a column to the right the given cell
    
    def getWestNeighbor(self, cell):
        """ Returns the cell to the west of the given cell """
        row = cell.getRow()     #Stores the "Y" coordinate of the cell
        col = cell.getCol()     #Stores the "X" coordinate of the cell

        if col == 0:        #Meant to prevent the method accessing "Out of Bound" Data
            return None

        cell_ID = self.getCell(row, col - 1)    #Stores the data of the cell to its "West"

        return cell_ID   #Returns the cell a column to the left the given cell
    
    def getHeadNorthNeighbor(self):
        """ Returns the cell to the north of the snake's head """
        return self.getNorthNeighbor(self.getSnakeHead())
    
    def getHeadSouthNeighbor(self):
        """ Returns the cell to the south of the snake's head """
        return self.getSouthNeighbor(self.getSnakeHead())
    
    def getHeadEastNeighbor(self):
        """ Returns the cell to the east of the snake's head """
        return self.getEastNeighbor(self.getSnakeHead())
    
    def getHeadWestNeighbor(self):
        """ Returns the cell to the west of the snake's head """
        return self.getWestNeighbor(self.getSnakeHead())
    
    def getNextCellInDir(self):
        """ Returns the next cell in the snake's path based
            on its current direction (self.__currentMode) """
        if self.__currentMode == self.SnakeMode.GOING_NORTH:
            return self.getHeadNorthNeighbor()
        elif self.__currentMode == self.SnakeMode.GOING_SOUTH:
            return self.getHeadSouthNeighbor()
        elif self.__currentMode == self.SnakeMode.GOING_EAST:
            return self.getHeadEastNeighbor()
        elif self.__currentMode == self.SnakeMode.GOING_WEST:
            return self.getHeadWestNeighbor()

    def getNeighbors(self, center):
        """ Returns a set of the neighbors around the given cell """
        return {self.getNorthNeighbor(center),
                self.getSouthNeighbor(center),
                self.getEastNeighbor(center),
                self.getWestNeighbor(center)}
    
    def getRandomNeighbor(self, center):
        """ Returns a random empty neighbor of the given cell """
        neighbors = self.getNeighbors(center)
        for cell in neighbors:
            if cell.isEmpty():
                return cell 
        # If none of them are empty, just return the first one
        return random.choice(neighbors)
    
    ###################################
    # Methods to set the snake's mode #
    ###################################
    
    def setDirectionNorth(self):
        """ Set the direction as north """
        self.__currentMode = self.SnakeMode.GOING_NORTH

    def setDirectionSouth(self):
        """ Set the direction as south """
        self.__currentMode = self.SnakeMode.GOING_SOUTH 

    def setDirectionEast(self):
        """ Set the direction as east """
        self.__currentMode = self.SnakeMode.GOING_EAST

    def setDirectionWest(self):
        """ Set the direction as west """
        self.__currentMode = self.SnakeMode.GOING_WEST

    def setAIMode(self):
        """ Switch to AI mode """
        self.__currentMode = self.SnakeMode.AI_MODE

    ###############################
    # Methods to access the snake #
    ###############################

    def getSnakeHead(self):
        """ Return the cell containing the snake's head """
        return self.__snakeCells[0]
    
    def getSnakeTail(self):
        """ Return the cell containing the snake's tail """
        return self.__snakeCells[-1]
    
    def getSnakeNeck(self):
        """ Return the body cell adjacent to the snake's head """
        return self.__snakeCells[1]

    #################################
    # Helper method for the display #
    #################################
    
    def getCellColor(self, row, col):
        """ Returns the color of the cell at the given location.
            Inputs: row - The row of the cell to access
                    col - The column of the cell to access """
        return self.getCell(row, col).getCellColor()
    
    ################################
    # Helper method(s) for reverse #
    ################################
    
    def reverseSnake(self):
        """ Uses the built-in reverse list method to invert the order of the cells"""
        self.__snakeCells.reverse()

    def RelabelSnake(self):
        """ Changes the cell type of the first and last element in the snakeCells list
            Since the getSnakeHead method calls for the first element in the list rather
            than the cell of cell type head similarly for the getSnakeTail method calls
            for the last element in the list"""
        self.getSnakeHead().becomeHead()

        self.getSnakeTail().becomeBody()

    def DirectionChange(self, cell):
        """ Changes direction based on the current direction and
            if the next cell in that direction is of cell type body"""
        if self.__currentMode == self.SnakeMode.GOING_NORTH:
            if not cell.isBody():
                self.setDirectionSouth()
        elif self.__currentMode == self.SnakeMode.GOING_SOUTH:
            if not cell.isBody():
                self.setDirectionNorth()
        elif self.__currentMode == self.SnakeMode.GOING_WEST:
            if not cell.isBody():
                self.setDirectionEast()
        elif self.__currentMode == self.SnakeMode.GOING_EAST:
            if not cell.isBody():
                self.setDirectionWest()

    #################################
    # Methods for AI implementation #
    #################################

    def resetCellsForSearch(self):
        for row in self.__board:
            for col in self.__board:
                for cell in col:
                    cell.clearSearchInfo()
    
    #########################
    # Methods for Game over #
    #########################

    def setGameOver(self):
        """ Set the game over flag to True """
        self.__gameOver = True 

    def getGameOver(self):
        """ Check the game over value """
        return self.__gameOver
    
    ######################################
    # Helpers for printing and debugging #
    ######################################

    def __str__(self):
        """ Returns a string representation of the board """
        out = ""
        for row in self.__board:
            for cell in row:
                out += str(cell)
            out += "\n"
        return out
    
    def toStringParents(self):
        """ Returns a string representation of the parents of each cell """
        out = ""
        for row in self.__board:
            for cell in row:
                out += "{}\t".format(cell.parentString())
            out += "\n"
        return out

    class SnakeMode(Enum):
        """ An enumeration (or enum) to represent the valid
            SnakeModes, in order to ensure that we do not accidentally
            use an invalid mode. The auto() is used when the value of
            the objects does not matter.
        """
        GOING_NORTH = auto()
        GOING_SOUTH = auto()
        GOING_EAST = auto()
        GOING_WEST = auto()
        AI_MODE = auto()