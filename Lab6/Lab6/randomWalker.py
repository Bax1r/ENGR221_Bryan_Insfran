"""
Title: Random Walking program
Date: 3/6/24
Assignment adapted from HMC CS5
"""

import random  
import time

def rs():
    """rs chooses a random step and returns it.
       Note that a call to rs() requires parentheses.
       Arguments: none at all!
    """
    return random.choice([-1, 1])

def rwpos(start, nsteps):
    """ rwpos models a random walker that
        * starts at the int argument, start
        * takes the int # of steps, nsteps

        rwpos returns the final position of the walker.
    """
    time.sleep(0.1)
    print('location is', start)
    if nsteps == 0:
        return start
    else:
        newpos = start + rs()  # take one step
        return rwpos(newpos, nsteps - 1)

def rwsteps(start, low, hi):
    """ rwsteps models a random walker which
        * is currently at start 
        * is in a walkway from low (usually 0) to hi (max location) 
          
        rwsteps returns the # of steps taken 
        when the walker reaches an edge
    """
    walkway = "_"*(hi-low)    # create a walkway of underscores
    S = (start-low)           # this is our sleepwalker's location, start-low

    walkway = walkway[:S] + "S" + walkway[S:]  # put our sleepwalker, "S", there

    walkway = " " + walkway + " "              # surround with spaces, for now...

    print(walkway, "    ", start, low, hi)     # print everything to keep track...
    time.sleep(0.05)

    if start <= low or start >= hi:            # base case: no steps if we're at an endpt
        return 0
    
    else:
        newstart = start + rs()                # takes one step, from start to newstart
        return 1 + rwsteps(newstart, low, hi)  # counts one step, recurses for the rest!

def rwstepsLoop(start, low, hi):
    """ rwsteps models a random walker which
        * is currently at start 
        * is in a walkway from low (usually 0) to hi (max location) 
          
        rwsteps returns the # of steps taken 
        when the walker reaches an edge
    """
    if start <= low or start >= hi:     #Checks if the start is within bounds
        return 0
    else:
        steps = 0   #Initialised a counter to keep track of the steps taken
        while start != low or start != hi:
            if start < low or start > hi:
                return steps
            walkway = "_"*(hi-low)    # create a walkway of underscores
            S = (start-low)           # this is our sleepwalker's location, start-low

            walkway = walkway[:S] + "S" + walkway[S:]  # put our sleepwalker, "S", there

            walkway = " " + walkway + " "              # surround with spaces, for now...

            print(walkway, "    ", start, low, hi)     # print everything to keep track...
            time.sleep(0.05)
            start = start + rs()    #Updates the start value for the following loop
            steps = steps + 1       #Updates the amount of steps taken

if __name__ == '__main__':
    print(rwstepsLoop(1,1,10))