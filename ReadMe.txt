Welcome to Kingdom Clash!

To play the game you must have the following files:
    - KingdomClash.py which you must run in order to play
    - KingdomClashClasses.py which stores classes and functions for certain 
      aspects of the game; this is imported to KingdomClash.py
    - highscore.txt which stores your highscore
    - cmu_112_graphics.py; this is also imported to KingdomClash.py

You must also have the following libraries installed:
    - Pil

List of Keyboard Shortcuts:
    - skip to next wave: press right arrow
    - initiate game over: press space bar

Kingdom Clash is a tower-defense game in which you must build towers and 
control soldiers to defend against the monsters trying to attack your kingdom! 
As the monsters enter along the path from the left, there are 4 different 
types of towers you can build: 
    1. Arrows, shoot arrows at enemies 
    2. Magic, which shoot defensive spells that injure monsters 
    3. Explosives, which launch bombs 
    4. Barracks, which places soldiers on the path to battle monsters
You are also given a Hero! This Hero has several special abilities:
    - the ability to move anywhere on path (not bounded by range)
    - the ability to battle two monsters at once
    - 3x the speed and health of a regular soldier
There are also several types of monsters you must defend your kingdom from: 
Goblins, Spiders, Ogres, Wolves, and Dark Knights. Each monster has a different 
size, speed, amount damage on soldiers, and health level. These monsters come 
in waves, and once you either kill all the monsters in a wave or they all exit 
the screen, a new wave immediately enters! 
This continues to ~infinity~ or until you have reached game over. You are given 
10 lives at the beginning of the game, and every time a monster reaches your 
kingdom (exits the right side of screen), you will lose 1 life. Once you reach 
0 lives, you have lost :(. Your score is determined by the number of waves you 
can survive with your 10 lives, and your highscore will be saved, even after 
closing the app! 
