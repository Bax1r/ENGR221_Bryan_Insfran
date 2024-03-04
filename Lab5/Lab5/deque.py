"""
Title: Double Ended Queue
Author: Bryan Insfran
Date: 2/28/24
"""

from .doublyLinkedList import DoublyLinkedList

class Deque():
    def __init__(self):
        self.__values = DoublyLinkedList()

    #Checks if the deque is empty and returns a boolean value
    def isEmpty(self):
        return self.__values.isEmpty()
    
    #Returns the length of the deque
    def __len__(self):
        return len(self.__values)
    
    #Outputs string values by iterating down the deque
    def __str__(self):
        return str(self.__values)

    #Checks if list is empty, and if not empty returns the first value
    def peekLeft(self):
        return self.__values.first()
    
    #Returns the value at the end of the deque
    def peekRight(self):
        return self.__values.getLastNode().getValue()

    #Checks if the deque is empty and adds value to the "front" of the deque
    def insertLeft(self, value):
        self.__values.insertFront(value)
        
    #Checks if the deque is empty and adds value to the "back" of the deque
    def insertRight(self, value): 
        self.__values.insertBack(value)

    #Checks if the deque is empty, and if not empty dequeues from the "front"
    def removeLeft(self): 
        return self.__values.deleteFirstNode()

    #Checks if the deque is empty, and if not empty dequeues from the "backs"
    def removeRight(self):
        return self.__values.deleteLastNode()
    
if __name__ == "__main__":
    pass