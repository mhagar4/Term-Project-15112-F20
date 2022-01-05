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
    #y = 10*math.log(10*abs(x+25)**2)+50*math.cos(x**2/50000) - 200 + height
    return y
def path2(x, height):
    y = 3/4*x - 5 - height
    return y
def path3(x, height):
    y = -1/(3*height)*(x-500)**2+350+height
    return y
#get slope of line between 2 points
def slope(x1, y1, x2, y2):
    m = (y2 - y1)/(x2 - x1)
    return m
####################################################

# Weapons #
class Weapon(object):
    def __init__(self, position, target=None):
        self.position = position
        self.target = target
    def weaponPath(self, tower):
        x1, y1 = tower.position[0], tower.position[1]
        x2, y2 = self.target[0], self.target[1]
        if(x1 != x2):
            m = slope(x1, y1, x2, y2)
            b = y1 - m * x1
            y = m * self.position[0] + b
        else:
            y = self.position[1] + 1
        return y
    def moveToTarget(self, tower):
        startX = tower.position[0]
        if(startX < self.target[0]):
            self.position[0] += self.speed
        else:
            self.position[0] -= self.speed
        self.position[1] = self.weaponPath(tower)
    def launchWeapon(self, tower):
        if(self.isMoving):
            self.moveToTarget(tower)
    def monsterHit(self, monster):
        x1, y1 = self.position[0], self.position[1]
        x2, y2 = monster.position[0], monster.position[1]
        return distance(x1, y1, x2, y2) <= (self.size + monster.size + self.speed)
    def targetHit(self):
        x1, y1 = self.position[0], self.position[1]
        x2, y2 = self.target[0], self.target[1]
        return distance(x1, y1, x2, y2) <= (self.size + self.speed)

class Arrow(Weapon):
    size = 2
    speed = 10
    def __init__(self, position):
        super().__init__(position)
        self.size = Arrow.size
        self.speed = Arrow.speed
        self.originalPosition = copy.copy(position)
    def land(self): #only after arrow position = target or monster is hit
        self.isMoving = False
        self.target = None
        self.position = copy.copy(self.originalPosition)


class Spell(Weapon):
    size = 3
    speed = 4
    def __init__(self, position):
        super().__init__(position)
        self.size = Spell.size
        self.speed = Spell.speed
    def land(self): #only after arrow position = target or monster is hit
        self.isMoving = False

class Bomb(Weapon):
    size = 5
    speed = 1
    range = 5
    def __init__(self, position):
        super().__init__(position)
        self.size = Bomb.size
        self.speed = Bomb.speed
        self.range = Bomb.range

# Defense people #
class Defense(object):
    def __init__(self, position, isAttacking=False, isMoving=False):
        self.position = position
        self.isAttacking = isAttacking

class Soldier(Defense):
    damage = 10
    health = 20
    size = 10
    speed = 10
    def __init__(self, position):
        super().__init__(position)
        self.damage = Soldier.damage
        self.health = Soldier.health
        self.size = Soldier.size
        self.speed = Soldier.speed
    def soldierPath(self, target):
        #self.position[1] = path(self.position[0], self.position[1])
        x1, y1 = self.position[0], self.position[1]
        x2, y2 = target[0], target[1]
        if(x1 != x2):
            m = slope(x1, y1, x2, y2)
            b = y1 - m * x1
            y = m * self.position[0] + b
        else:
            y = self.position[1] + 1
        return y
    def runToTarget(self, target):
        if(self.position[0] < target[0]):
            self.position[0] *= self.speed**2
            self.position[1] = self.soldierPath(target)
        elif(self.position[0] > target[0]):
            self.position[0] *= -(self.speed**2)
            self.position[1] = self.soldierPath(target)
        elif(self.position == target): self.isMoving = False
    def run(self, newPosition):
        if(self.isMoving):
            self.runToTarget(newPosition)

class Hero(Defense):
    damage = 10
    health = 20
    size = 10
    def __init__(self, position):
        super().__init__(position)
        self.damage = Hero.damage
        self.health = Hero.health
        self.size = Hero.size

class Reinforcement(Defense):
    damage = 10
    health = 20
    size = 10
    def __init__(self, position):
        super().__init__(position)
        self.damage = Reinforcement.damage
        self.health = Reinforcement.health
        self.size = Reinforcement.size

# Towers #
class Tower(object):
    maxLevel = 4
    def __init__(self, position, color, size=15, level=1, isAttacking=False):
        self.position = position
        self.level = level
        self.color = color
        self.size = size
        self.isAttacking = isAttacking
        self.range = 0
    def levelUp(self):
        if(self.level < Tower.maxLevel):
            self.level += 1
            self.damage += 3
            self.range += 2
    def attack(self):
        if(self.isAttacking):
            self.isAttacking = True
            self.weapon.isMoving = True
            self.weapon.launchWeapon(self)
    def stopAttack(self):
        self.isAttacking = False
class Arrows(Tower):
    damage = 10
    range = 200
    frequency = 15
    def __init__(self, position, color, speed=1):
        super().__init__(position, color)
        self.speed = speed
        self.arrow = Arrow([position[0], position[1] - self.size])
        self.weapon = self.arrow
        self.damage = Arrows.damage
        self.range = Arrows.range
        self.frequency = Arrows.frequency
    def levelUp(self):
        super().levelUp(self)
        frequency += 5
        #change image
    
class Magic(Tower):
    damage = 10
    range = 200
    frequency = 10
    speed = 5
    def __init__(self, position, color):
        super().__init__(position, color)
        self.spell = Spell([position[0], position[1]-self.size])
        self.weapon = self.spell
        self.damage = Magic.damage
        self.range = Magic.range
        self.frequency = Magic.frequency
        self.speed = Magic.speed
    def levelUp(self):
        super().levelUp(self)
        frequency += 5
        #change image

class Explosives(Tower):
    damage = 10
    range = 30
    frequency = 10
    def __init__(self, position, color):
        super().__init__(position, color)
        self.damage = Explosives.damage
        self.range = Explosives.range
        self.frequency = Explosives.frequency
    def levelUp(self):
        super().levelUp(self)
        frequency += 5
        #change image
    def attack(self, target):
        pass    

class Barracks(Tower):
    damage = 10
    range = 30
    restTime = 10
    soldiers = []
    def __init__(self, position, color):
        super().__init__(position, color)
        self.damage = Barracks.damage
        self.range = Barracks.range
        self.restTime = Barracks.restTime
        self.soldiers = []
    def levelUp(self):
        super().levelUp(self)
        restTime -= 5
        #change image
    def positionSoldiers(self):
        x = self.position[0]
        y = path(self.position[0], 350)
        soldier1 = Soldier([x, y])
        soldier2 = Soldier([x - 5, y + 5])
        soldier3 = Soldier([x + 5, y + 5])
        self.soldiers.extend([soldier1, soldier2, soldier3])
    def attack(self, target):
        pass 
    def __type__(self):
        return 'Barracks'


# Enemies #
class Monster(object):
    stepLength = 2
    def __init__(self, position, height, health):
        self.position = position
        self.health = health
        self.height = height
        self.startHeight = height
    def move(self):
        path1Height = 350 + self.height
        path2Height = -50 + self.height
        path3Height = 137.5 + self.height
        self.position[0] += self.speed
        if(path1(self.position[0], 400) > path3(self.position[0], 137.5)):
            self.position[1] = path1(self.position[0], path1Height)
        else:
            self.position[1] = path3(self.position[0], path3Height)
        if(self.height > self.startHeight):
            self.height -= Monster.stepLength
        else:
            self.height += Monster.stepLength
    def attack(self, soldier):
        soldier.health -= self.damage
    def inRange(self, tower):
        x1, y1 = self.position[0], self.position[1]
        x2, y2 = tower.position[0], tower.position[1]
        dist = distance(x1, y1, x2, y2)
        return dist <= tower.range 

class Goblin(Monster):
    speed = 5
    armor = 0
    damage = 5
    size = 3
    def __init__(self, position, height, health=20):
        super().__init__(position, height, health)
        self.speed = Goblin.speed
        self.armor = Goblin.armor
        self.damage = Goblin.damage
        self.size = Goblin.size

class Ogre(Monster):
    speed = 5
    armor = 2
    damage = 10
    size = 5
    def __init__(self, position, height, health=30):
        super().__init__(position, height, health)
        self.speed = Ogre.speed
        self.armor = Ogre.armor
        self.damage = Ogre.damage
        self.size = Ogre.size

class Spider(Monster):
    speed = 15
    armor = 0
    damage = 3
    size = 5
    def __init__(self, position, height, health=20):
        super().__init__(position, height, health)
        self.speed = Spider.speed
        self.armor = Spider.armor
        self.damage = Spider.damage
        self.size = Spider.size

class Wolf(Monster):
    speed = 20
    armor = 0
    damage = 2
    size = 3
    def __init__(self, position, height, health=25):
        super().__init__(position, height, health)
        self.speed = Wolf.speed
        self.armor = Wolf.armor
        self.damage = Wolf.damage
        self.size = Wolf.size

class Dark_Knight(Monster):
    speed = 12
    armor = 10
    damage = 10
    size = 6
    def __init__(self, position, height, health=40):
        super().__init__(position, height, health)
        self.speed = Dark_Knight.speed
        self.armor = Dark_Knight.armor
        self.damage = Dark_Knight.damage
        self.size = Dark_Knight.size
    