#File for my custom Classes
import math, copy

########## helper functions ########################
#get distance between 2 points
def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

#get midpoint between 2 points
def midpoint(x1, y1, x2, y2):
    x = (x1+x2)/2
    y = (y1+y2)/2
    return (x,y)

#functions that define paths 
def path1(x, height):
    y = 100*math.cos(1/100*x) + height
    return y

def path2(x, height):
    y = 3/4*x - 5 - height
    return y

def path3(x, height):
    y = 1/400*(x-600)**2+height
    return y

#get slope of line between 2 points
def slope(x1, y1, x2, y2):
    m = (y2 - y1)/(x2 - x1)
    return m
####################################################

# Weapons #
class Weapon(object):
    def __init__(self, position, tower, isMoving=False, target=None):
        self.position = position
        self.isMoving = isMoving
        self.tower = tower
        self.target = target
        self.originalPosition = position[0], position[1]
    
    #launches weapon towards target (some bugs)
    def launch(self):
        targetX = self.target[0]
        targetY = self.target[1]
        currX = self.position[0]
        currY = self.position[1]
        if(0 < distance(currX, currY, targetX, targetY) <= self.size + self.speed):
            self.position[0] = targetX
            self.position[1] = targetY
        elif((currX, currY) == (targetX, targetY)):
            self.land()
        elif(self.size > abs(currX - targetX)):
            if(targetY > self.originalPosition[1]):
                self.position[1] += 10
            elif(self.originalPosition[1] > targetY): 
                self.position[1] -= 10
        elif(targetX > self.originalPosition[0]):
            self.position[0] += 10
            self.position[1] = self.line()
        elif(targetX < self.originalPosition[0]): 
            self.position[0] -= 10
            self.position[1] = self.line()
    
    #determines path to target
    def line(self):
        x, y = self.target[0], self.target[1]
        x1, y1 = self.originalPosition[0], self.originalPosition[1]
        m = (y-y1)/(x-x1)
        y2 = m * (self.position[0] - x1) + y1
        return y2
    
    #tests if weapon hits monster
    def monsterHit(self, enemy):
        x1, y1 = enemy.position[0], enemy.position[1]
        x2, y2 = self.position[0], self.position[1]
        return(distance(x1, y1, x2, y2) <= enemy.size + self.size)
    
    #stops weapon movement, returns to original position
    def land(self): 
        self.isMoving = False
        self.target = None
        self.position = [self.originalPosition[0], self.originalPosition[1]]
    
    #tests if weapon goes out of range
    def outOfRange(self):
        x1, y1 = self.position[0], self.position[1]
        x2, y2 = self.tower.position[0], self.tower.position[1]
        return distance(x1, y1, x2, y2) > self.tower.range

class Arrow(Weapon):
    size = 4
    speed = 7
    def __init__(self, position, tower):
        super().__init__(position, tower)
        self.size = Arrow.size
        self.speed = Arrow.speed

class Spell(Weapon):
    size = 4
    speed = 10
    def __init__(self, position, tower):
        super().__init__(position, tower)
        self.size = Spell.size
        self.speed = Spell.speed

class Bomb(Weapon):
    size = 5
    speed = 5
    range = 30
    def __init__(self, position, tower):
        super().__init__(position, tower)
        self.size = Bomb.size
        self.speed = Bomb.speed
        self.range = Bomb.range

# Defense people #
class Defense(object):
    def __init__(self, position, dead=False, isBattling=False, isMoving=False):
        self.position = position
        self.isBattling = isBattling
        self.isMoving = isMoving
        self.dead = dead
        self.deathTime = None
    #moves soldiers towards target
    def run(self, target):
        x, y = target
        currX, currY = self.position[0], self.position[1]
        #tests if weapon is reaching target
        if(distance(currX, currY, x, y) <= self.size + self.speed): 
            self.isMoving = False
            self.position[0], self.position[1] = target
            self.originalPosition = target
        #avoids division by zero when determining straight line path
        elif((self.size > abs(currX - x)) and (currX, currY != target)):
            if(currY > y): self.position[1] -= self.speed
            else: self.position[1] += self.speed
        elif(x > currX): #moves weapon right
            self.position[0] += self.speed
            self.position[1] = self.line(target)
        elif(currX > x): #moves weapon left
            self.position[0] -= self.speed
            self.position[1] = self.line(target)
    
    #determines path to target
    def line(self, target):
        x, y = target
        x1, y1 = self.originalPosition[0], self.originalPosition[1]
        m = (y-y1)/(x-x1)
        y2 = m * (self.position[0] - x1) + y1
        return y2
    
    #runs to monster and fights
    def battle(self, monster): 
        if(self.isBattling): #hurts monster if in battle
            monster.health -= self.damage
            monster.battle(self)
            if(self.health <= 0): #soldier dies :(
                self.dead = True
                self.isMoving = False
                self.isBattling = False
                monster.isMoving = True
                monster.isBattling = False
                self.resetOpponent()
        else: #runs to monster if not yet battling
            monster.isMoving = False
            target = (monster.position[0]+self.size+monster.size, monster.position[1])
            if(self.size < target[0]): self.run(target) #makes sure it doesnt leave screen
            if(self.position == [target[0], target[1]]): self.isBattling = True
    
class Soldier(Defense):
    damage = 1
    size = 10
    speed = 5
    range = 100
    def __init__(self, position, tower, health=100):
        super().__init__(position)
        self.opponent = None
        self.tower = tower
        self.damage = Soldier.damage
        self.health = health
        self.size = Soldier.size
        self.speed = Soldier.speed
        self.range = Soldier.range
        self.originalPosition = copy.copy(position)
    
    #resets opponent
    def resetOpponent(self):
        if(self.opponent != None): 
            self.opponent.isMoving = True
            self.opponent = None
            self.isBattling = False

class Hero(Defense):
    damage = 5
    health = 300
    size = 20
    speed = 15
    range = 200
    def __init__(self, position):
        super().__init__(position)
        self.opponent = None
        self.originalPosition = (position[0], position[1])
        self.damage = Hero.damage
        self.health = Hero.health
        self.size = Hero.size
        self.speed = Hero.speed
        self.range = Hero.range
        self.image = 'hero.png'


    def attack(self, monster):
        if((self.opponent == None) and (not monster.isBattling) 
            and (monster.inHeroRange(self)) and (not self.dead)):
            self.opponent = monster
            monster.isBattling = True
        elif(self.opponent != None):
            self.battle(self.opponent)

    def resetOpponent(self):
        if(self.opponent != None): 
            self.opponent.isMoving = True
            self.opponent = None
            self.isBattling = False
    
    '''#attacks two monsters
    def attack(self, monster):
        self.battling = True
        #adds monster if not already fighting 2
        if(len(self.opponent) < 2 and (not monster.isBattling) 
            and monster.inRange(self) and (not monster.dead)):
            self.opponent.append(monster)
            monster.isBattling = True
        #battles first and second monsters
        if(len(self.opponent) > 0): self.battle(self.opponent[0])
        if(len(self.opponent) > 1): self.battle(self.opponent[1])'''
    
    '''#similar to soldier battle, but accounts for multiple opponents
    def battle(self, monster):
        if(self.isBattling):
            self.health -= monster.damage
            monster.battle(self)
            if(self.health <= 0):
                for opponent in self.opponent:
                    opponent.isMoving = True
                    opponent.isBattling = False
                self.isBattling = False
                self.isMoving = False
                self.opponent = []
                self.dead = True
        else: #runs to each of the opponents in reverse order
            monster.isMoving = False
            target = (monster.position[0]+self.size+monster.size, monster.position[1])
            if(self.size < target[0]): self.run(target)
            if(self.position == [target[0], target[1]]): self.isBattling = True'''

# Towers #
class Tower(object):
    maxLevel = 4
    size = 15
    levelUpCost = 50
    def __init__(self, position, isAttacking=False, image=None, level=0):
        self.position = position
        self.isAttacking = isAttacking
        self.image = image
        self.level = level
        self.range = 0
    
    def attack(self):
        if(self.isAttacking):
            self.weapon.launch()
    
    def stopAttack(self):
        self.isAttacking = False
    
    def levelUp(self):
        self.range += 50
        self.weapon.speed += 2
        self.damage += 5
        self.level += 1

class Arrows(Tower):
    range = 100
    cost = 50
    damage = 2
    def __init__(self, position):
        super().__init__(position)
        self.arrow = Arrow([position[0], position[1] - self.size], self)
        self.weapon = self.arrow
        self.range = Arrows.range
        self.cost = Arrows.cost
        self.damage = Arrows.damage
    
class Magic(Tower):
    range = 100
    cost = 75
    damage = 3
    def __init__(self, position):
        super().__init__(position)
        self.spell = Spell([position[0], position[1]-self.size], self)
        self.weapon = self.spell
        self.range = Magic.range
        self.cost = Magic.cost
        self.damage = Magic.damage

class Explosives(Tower):
    range = 100
    cost = 75
    damage = 5
    def __init__(self, position):
        super().__init__(position)
        self.bomb = Bomb([position[0], position[1] - self.size], self)
        self.weapon = self.bomb
        self.cost = Explosives.cost
        self.damage = Explosives.damage
        self.range = Explosives.range
    
    #similar to regular levelUp but accounts for Bomb range
    def levelUp(self):
        super().levelUp()
        self.weapon.range += 10

class Barracks(Tower):
    soldiers = []
    cost = 100
    range = 100
    def __init__(self, position):
        super().__init__(position)
        self.soldiers = []
        self.cost = Barracks.cost
        self.range = Barracks.range
    
    #positions soldiers on path
    def positionSoldiers(self):
        xdistance = 5
        ydistance = 10
        x = self.position[0]
        y = self.getNearestPath()
        soldier1 = Soldier([x, y], self)
        soldier2 = Soldier([x + xdistance, y - ydistance], self)
        soldier3 = Soldier([x - xdistance, y - ydistance], self)
        self.soldiers = [soldier1, soldier2, soldier3]
    
    #gets path height nearest to tower
    def getNearestPath(self):
        h1, h2, h3 = 350, -50, 100
        x, y = self.position[0], self.position[1]
        pathHeights = [path1(x, h1), path2(x, h2), path3(x, h3)]
        nearestPathHeight = 0
        leastDistance = 1000
        for height in pathHeights:
            dist = abs(y - height)
            if(dist < leastDistance):
                leastDistance = dist
                nearestPathHeight = height
        return nearestPathHeight
    
    #attacks monsters passing tower
    def attack(self, monster):
        for soldier in self.soldiers:
            if((soldier.opponent == None) and (not monster.isBattling) 
                and (monster.inRange(soldier)) and (not soldier.dead)):
                soldier.opponent = monster
                monster.isBattling = True
            elif(soldier.opponent != None):
                soldier.battle(soldier.opponent)
    
    #levelUp but adds an extra soldier
    def levelUp(self):
        self.level += 1
        self.range += 50
        x = self.position[0]
        y = self.getNearestPath()
        self.soldiers.append(Soldier([x, y], self))

# Enemies #
class Monster(object):
    stepLength = 2
    def __init__(self, position, height, health, dead=False, isMoving=True, isBattling=False):
        self.position = position
        self.health = health
        self.height = height
        self.startHeight = height
        self.path = None
        self.path2 = None
        self.isMoving = isMoving
        self.isBattling = isBattling
        self.dead = dead
    
    #moves monsters along path
    def move(self):
        if(self.isMoving):
            self.position[0] += self.speed
            x = self.position[0]
            h1, h2, h3 = 350, -50, 100
            path1y, path2y, path3y = path1(x,h1), path2(x,h2), path3(x,h3)
            #checks which path has been selected
            if(self.path == 'path2'): 
                if(path2y < path1y):
                    self.position[1] = path2(x, h2+self.height)
                elif(path1y < path3y):
                    self.position[1] = path1(x, h1+self.height)
            elif(self.path == 'path3') and (path3y < path1y):
                self.position[1] = path3(x, h3+self.height)
            else: self.position[1] = path1(x, h1+self.height)
            #simulates stepping motion
            if(self.height > self.startHeight):
                self.height -= Monster.stepLength
            else:
                self.height += Monster.stepLength
    
    #battles soldiers
    def battle(self, soldier):
        if(self.isBattling): 
            self.isMoving = False
            soldier.health -= self.damage
        if(self.health <= 0): 
            self.dead = True
            self.isBattling = False
            self.isMoving = False
            soldier.isBattling = False
            soldier.resetOpponent()
    
    def inHeroRange(self, hero):
        assert(isInstance(hero, Hero))
        x1, y1 = self.position[0], self.position[1]
        x2, y2 = hero.position[0], hero.position[1]
        dist = distance(x1, y1, x2, y2)
        return dist <= hero.range 

    #checks if monster is inRange of tower
    def inRange(self, tower):
        x1, y1 = self.position[0], self.position[1]
        x2, y2 = tower.position[0], tower.position[1]
        dist = distance(x1, y1, x2, y2)
        return dist <= tower.range 

class Goblin(Monster):
    damage = 1
    size = 3
    speed = 3
    def __init__(self, position, height, health=15):
        super().__init__(position, height, health)
        self.speed = Goblin.speed
        self.damage = Goblin.damage
        self.size = Goblin.size
        self.image = 'goblin.png'

class Ogre(Monster):
    speed = 2
    armor = 2
    damage = 4
    size = 5
    def __init__(self, position, height, health=30):
        super().__init__(position, height, health)
        self.speed = Ogre.speed
        self.armor = Ogre.armor
        self.damage = Ogre.damage
        self.size = Ogre.size
        self.image = 'ogre.png'

class Spider(Monster):
    speed = 7
    damage = 1
    size = 5
    def __init__(self, position, height, health=20):
        super().__init__(position, height, health)
        self.speed = Spider.speed
        self.damage = Spider.damage
        self.size = Spider.size
        self.image = 'spider.png'

class Wolf(Monster):
    speed = 10
    damage = 2
    size = 3
    def __init__(self, position, height, health=25):
        super().__init__(position, height, health)
        self.speed = Wolf.speed
        self.damage = Wolf.damage
        self.size = Wolf.size
        self.image = 'wolf.png'

class Dark_Knight(Monster):
    speed = 5
    armor = 10
    damage = 10
    size = 6
    def __init__(self, position, height, health=40):
        super().__init__(position, height, health)
        self.speed = Dark_Knight.speed
        self.armor = Dark_Knight.armor
        self.damage = Dark_Knight.damage
        self.size = Dark_Knight.size
        self.image = 'dark_knight.png'

    