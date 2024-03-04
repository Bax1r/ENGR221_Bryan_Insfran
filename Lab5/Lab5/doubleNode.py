"""
Title: Double Node Class
Author: Bryan Insfran
Date: 2/28/24
"""

class DoubleNode():

    def __init__(self, value, next=None, previous=None):
        self.__value = value
        self.__nextNode = next
        self.__previousNode = previous 

    #####
    # Methods
    #####
        
    #Checks if the node provided in the "self" argument has a None pointer as it's previousNode
    def isFirst(self) -> bool:
        if self.__previousNode == None:
            return True     #Returns True if provided node has a None pointer
        else:
            return None     #Returns None if the provided node's pointer is not None
        
    #Checks if the node provided in the "self" argument has a None pointer as it's nextNode
    def isLast(self) -> bool:
        if self.__nextNode == None:
            return True     #Returns True if provided node has a None pointer
        else:
            return None     #Returns None if the provided node's pointer is not None

    #####
    # Getters
    #####

    #Returns the value at node "self"
    def getValue(self):
        return self.__value
    
    #Returns the value of the node's "nextNode"
    def getNextNode(self):
        return self.__nextNode

    #Returns the value of the node's "previousNode"
    def getPreviousNode(self):
        return self.__previousNode

    #####
    # Setters
    #####

    #Sets the value of node "self" to "new_value"
    def setValue(self, new_value) -> None:
        self.__value = new_value
    
    #Sets the "next" pointer of current node to inputted node
    def setNextNode(self, new_next) -> None:
        # Confirm that the input is a valid node
        if self.__checkValidNode(new_next):
            self.__nextNode = new_next

    #Sets the "previous" pointer of current node to inputted node
    def setPreviousNode(self, new_previous) -> None:
        # Confirm that the input is a valid node
        if self.__checkValidNode(new_previous):
            self.__previousNode = new_previous

    #####
    # Helpers
    #####

    def __checkValidNode(self, node) -> bool:
        if type(node) != DoubleNode and node != None:
            raise Exception("Error: Input must be a valid DoubleNode or None")
        return True
    
    def __str__(self) -> str:
        return str(self.getValue())

if __name__ == "__main__":
    pass