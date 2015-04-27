# Helper for displaying wisdom

import random

def wisdom():
    return random.choice(
    (
       "The code was willing,\nIt considered your request,\nBut the chips were weak..",
       "Yesterday it worked,\nToday it is not working\nComputers are like that",
       "Three things are certain:\nDeath, taxes and computer errors.\nGuess which has occurred?",
    ) )
       

if __name__ == "__main__":
    for run in range(10):
        print wisdom()
        print