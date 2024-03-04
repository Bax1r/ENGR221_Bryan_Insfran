"""
Title: Doubly Linked List
Author: Bryan Insfran
Date: 2/28/24
"""

from .doubleNode import DoubleNode 

class DoublyLinkedList():

    def __init__(self):
        self.__firstNode = None
        self.__lastNode = None 

    def isEmpty(self):
        if self.__firstNode == None and self.__lastNode == None:
            return 1
        else:
            return 0

    def first(self):
        # Raise an exception if the list is empty
        if self.isEmpty():
            raise Exception("Error: List is empty, cannot return first  value")
        return self.getFirstNode().getValue()
    
    def getFirstNode(self):
        return self.__firstNode

    def getLastNode(self):
        return self.__lastNode
    
    def setFirstNode(self, node):
        # Raise an exception if the input is not a valid node
        if node != None and type(node) != DoubleNode:
            raise Exception("Error: Input must be valid Node or None")
        else:
            self.__firstNode = node

    def setLastNode(self, node):
        # Raise an exception if the input is not a valid node
        if node != None and type(node) != DoubleNode:
            raise Exception("Error: Input must be valid Node or None")
        else:
            self.__lastNode = node
    
    def find(self, value):
        # Traverse down the list, starting with the first node
        node = self.getFirstNode()
        while node != None:
            # If this node has the given value, return it
            if node.getValue() == value:
                return node 
            # Otherwise, grab the next node to check
            node = node.getNextNode()
        # If the value was not found, return None
        return None

    def insertFront(self, value):
        # Create a new node that points to the first node in the list
        node = DoubleNode(value, self.getFirstNode(), None)
        # Update the "previous" pointer of the old first, now second, node in the list if the list is not empty
        if self.isEmpty():
            self.setFirstNode(node)
            self.setLastNode(node)
        else:
            old = self.getFirstNode()
            old.setPreviousNode(node)
            self.setFirstNode(node)


    def insertBack(self, value):
        # Create a new node that points to the last node in the list
        node = DoubleNode(value, None, self.getLastNode())
        # Update the "previous" pointer of the old last, now second to last, node in the list if the list is not empty
        if self.isEmpty():
            self.setFirstNode(node)
            self.setLastNode(node)
        else:
            old = self.getLastNode()
            old.setNextNode(node)
            self.setLastNode(node)

    def insertAfter(self, value_to_add, after_value) -> None:
        # Create a new node that points to the X node in the list
        node = DoubleNode(value_to_add, self.find(after_value), self.find(after_value))
        # Update the "Next" and "Previous" pointers
        if self.isEmpty():
            self.setFirstNode(node)
            self.setLastNode(node)
        else:
            old = self.getFirstNode()
            old.setPreviousNode(node)
            self.setFirstNode(node)
            
    def deleteFirstNode(self):
        # If we try to delete from an empty list, raise an exception
        if self.isEmpty():
            raise Exception("Error: List is empty")
        # Otherwise, grab the first node of the list and store its value
        first = self.getFirstNode()
        Removed = self.first
        # Set the first node of the list to the second node
        if first.getNextNode == None:
            self.setFirstNode(None)
            self.setLastNode(None)
            return Removed
        else:
            self.setFirstNode(first.getNextNode())
            self.getFirstNode().setPreviousNode(None)
        # Return the value of the deleted node
        return Removed
    
    def deleteLastNode(self):
        # If we try to delete from an empty list, raise an exception
        if self.isEmpty():
            raise Exception("Error: List is empty")
        # Otherwise, grab the last node of the list
        last = self.getLastNode()
        #Set the second to last node to be the last node
        self.setLastNode(last.getPreviousNode())
        last.setNextNode(None)
        # Return the value of the deleted node
        return last.getValue()
    
    def deleteValue(self, value):
        # If we try to delete from an empty list, raise an exception
        if self.isEmpty():
            raise Exception("Error: Cannot delete from empty list")
        # Otherwise, traverse down the list starting with the first node
        if self.find(value) == self.getFirstNode:
            self.deleteFirstNode
        elif self.find(value) == self.getLastNode:
            self.deleteLastNode
        else:
            next = self.find(value).getNextNode()
            prev = self.find(value).getPreviousNode()
            self.find(value).setPreviousNode(prev)
            self.find(value).setNextNode(next)
        # If the value was not found, raise an exception
        raise Exception("Error: Cannot find value {} in list".format(value))
    
    def forwardTraverse(self):
        # Traverse starting from the first node
        node = self.getFirstNode()
        # Stop when we reach the end of the list
        while node != None:
            # Print the value of this node
            print(node.getValue())
            # Update node to be the next node
            node = node.getNextNode()

    def reverseTraverse(self):
        # Traverse starting from the last node
        node = self.getLastNode()
        # Stop when we reach the 'end' of the list
        while node != None:
            # Print the value of this node
            print(node.getValue())
            # Update node to be the previous node
            node = node.getPreviousNode()

    def __len__(self):
        # A counter starting at 0
        l = 0
        # Traverse down the list starting with the first node
        node = self.getFirstNode() 
        # Stop when we reach the end of the list
        while node != None:
            # Increment the counter for each node we find
            l += 1
            # Update node to be the next node
            node = node.getNextNode()
        # Return the counter
        return l
    
    def __str__(self):
        # Begin the string with the left bracket
        out = "["
        # Traverse down the list starting with the first node
        node = self.getFirstNode() 
        # Stop when we reach the end of the list
        while node != None:
            # Only add the arrow if there's more than one value in the list
            if len(out) > 1:
                out += " <-> "
            # Add the value of the current node to the string
            out += str(node)
            # Update node to be the next node
            node = node.getNextNode()
        # Add the closing bracket and return the string
        return out + "]"
    
if __name__ == "__main__":
    pass