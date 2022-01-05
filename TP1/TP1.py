from TPClasses2 import *
from cmu_112_graphics import *
import math, random
from PIL import Image

def appStarted(app):
    app.started = False
    app.paused = False
    app.difficultyChosen = False
    app.path1Bounds = (300, 400)
    app.path2Bounds = (0, 100)
    app.path3Bounds = (100, 175)
    app.timerDelay = 50
    app.hero = Hero([950, path1(950, 350)])
    app.soldiersMoving = False
    app.soldierTarget = None
    setEnemies(app)
    setTowers(app)

#initializes enemies
def setEnemies(app):
    app.goblins= []
    app.numGoblins =  7
    for i in range(app.numGoblins): #initializes goblin positions
        startHeight = random.randint(-20, 20)
        positionX = random.randint(0, 50)
        positionY = path1(positionX, 350 + startHeight)
        position = [positionX, positionY]
        app.goblins.append(Goblin(position=position, height=startHeight))

#creates "empty" towers
def setTowers(app):
    app.towers = []
    app.numTowers = 10
    app.selectedTower = None
    for i in range(1, app.numTowers + 1): 
        x = i*app.width//app.numTowers
        if(i%2==0):
            position = [x, path1(x, 250)]
        else:
            position = [x, path1(x, 450)]
        app.towers.append(Tower(position=position, color='tan'))

#reacts to key presses
def keyPressed(app, event):
    if(event.key == 'Space'):
        shoot(app)
    if(not app.started): #when on title screen
        if(event.key == 'Enter' and app.difficultyChosen): #enter starts game
            app.started = True
        elif(event.key in ['1', '2', '3']): #choose difficulty
            setDifficulty(app, int(event.key))
    elif(app.selectedTower != None and event.key in ['a', 'm', 'e', 'b', 's']):
        if(event.key == 's' and isinstance(app.selectedTower, Barracks)): #for testing
            app.soldiersMoving = True
            for soldier in app.selectedTower.soldiers:
                soldier.isMoving = True
        else:
            buildTower(app, event.key) #builds towers
    if(event.key == 'p'):
        app.paused = not app.paused

#tests if arrow hits any monsters
def hitMonster(app):
    for tower in app.towers:
        if(tower.isAttacking):
            for goblin in app.goblins:
                if(tower.weapon.target != None):
                    if(tower.weapon.monsterHit(goblin)):
                        tower.weapon.land()
                        goblin.health -= tower.damage
                if(tower.weapon.target != None):
                    if(tower.weapon.targetHit()):
                        tower.weapon.land()

#sets difficulty of game
def setDifficulty(app, difficulty):
    app.difficultyChosen = True
    app.numGoblins *= difficulty

#"builds" corresponding tower by replacing empty tower with type
def buildTower(app, key):
    position = app.selectedTower.position
    index = app.towers.index(app.selectedTower)
    if(key == 'a'):
        app.towers[index] = (Arrows(position=position, color='lightGreen'))
    elif(key == 'm'):
        app.towers[index] = (Magic(position=position, color='light blue'))
    elif(key == 'e'):
        app.towers[index] = (Explosives(position=position, color='orange'))
    elif(key == 'b'):
        app.towers[index] = (Barracks(position=position, color='violet'))
        print(type(app.towers[index]))
        app.towers[index].positionSoldiers()

#reacts to mouse press by selecting tower
def mousePressed(app, event):
    if(app.soldiersMoving):
        app.soldierTarget = [event.x, event.y]
    app.selectedTower = None
    selectTowerAtPoint(app, event.x, event.y)

#selects tower if clicked on 
def selectTowerAtPoint(app, x, y):
    for tower in app.towers:
        x0 = tower.position[0] - tower.size
        y0 = tower.position[1] - tower.size
        x1 = tower.position[0] + tower.size
        y1 = tower.position[1] + tower.size
        if(x0 <= x <= x1 and y0 <= y <= y1):
            app.selectedTower = tower

#returns true if a point is in a dot
def pointInDot(cx, cy, r, x, y):
    dist = distance(cx, cy, x, y)
    return (dist <= r)

#arrow and magic towers shoot at enemies
def shoot(app):
    x, y = None, None
    for tower in app.towers:
        for goblin in app.goblins:
            if goblin.inRange(tower):
                tower.isAttacking = True
                if(tower.weapon.target == None):
                    x, y = goblin.position[0], goblin.position[1]
                    #land function makes this freak a little bit
                    tower.weapon.target = (x, y)
                if(tower.weapon.target != None):
                    tower.attack()
                    #hitMonster(app)
                break #this is so each tower only has one target at a time
                if(goblin.health <= 0):   
                    goblin.size = 0
            elif(tower.isAttacking):
                tower.stopAttack()

#moves monsters along path
def timerFired(app):
    shoot(app)
    if(app.soldiersMoving):
        for soldier in app.selectedTower.soldiers:
            soldier.run((500, 500))
            if(not soldier.isMoving):
                app.soldiersMoving = False
    if(not app.paused and app.started):
        for goblin in app.goblins:
            goblin.move()

def drawGoblin(app, canvas):
    for goblin in app.goblins:
        x0 = goblin.position[0] - goblin.size
        y0 = goblin.position[1] - goblin.size
        x1 = goblin.position[0] + goblin.size
        y1 = goblin.position[1] + goblin.size
        canvas.create_oval(x0, y0, x1, y1, fill="black")

def drawPath(app, canvas):
    for x in range(0, app.width-2, 1):
        width = 0
        canvas.create_line(x, path1(x, 400), x+1, path1(x+1, 400))
        canvas.create_line(x, path1(x, 300), x+1, path1(x+1, 300))
        if(path2(x, -100) <= path1(x, 300)):
            canvas.create_line(x, path2(x, -100), x+1, path2(x+1, -100))
        if(path2(x, 0) <= path1(x, 300)):
            canvas.create_line(x, path2(x, 0), x+1, path2(x+1, 0))
        if(path3(x, 100) >= path1(x, 400)):
            canvas.create_line(x, path3(x, 100), x+1, path3(x+1, 100))
        if(path3(x, 175) >= path1(x, 400)):
            canvas.create_line(x, path3(x, 175), x+1, path3(x+1, 175))
 
def drawTowers(app, canvas):
    for tower in app.towers:
        x0 = tower.position[0] - tower.size
        y0 = tower.position[1] - tower.size
        x1 = tower.position[0] + tower.size
        y1 = tower.position[1] + tower.size
        if(tower is app.selectedTower):
            canvas.create_rectangle(x0, y0, x1, y1, fill='red')
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill=tower.color)

def drawArrow(app, canvas):
    for tower in app.towers:
        if isinstance(tower, Arrows) and tower.isAttacking:
            x0 = tower.arrow.position[0]-tower.arrow.size 
            y0 = tower.arrow.position[1]-tower.arrow.size
            x1 = tower.arrow.position[0]+tower.arrow.size 
            y1 = tower.arrow.position[1]+tower.arrow.size
            canvas.create_oval(x0, y0, x1, y1, fill='brown')

def drawSpell(app, canvas):
    for tower in app.towers:
        if isinstance(tower, Magic) and tower.isAttacking:
            x0 = tower.spell.position[0]-tower.spell.size 
            y0 = tower.spell.position[1]-tower.spell.size
            x1 = tower.spell.position[0]+tower.spell.size 
            y1 = tower.spell.position[1]+tower.spell.size
            canvas.create_oval(x0, y0, x1, y1, fill='cyan')

def drawHero(app, canvas):
    x0 = app.hero.position[0] - app.hero.size
    y0 = app.hero.position[1] - app.hero.size
    x1 = app.hero.position[0] + app.hero.size
    y1 = app.hero.position[1] + app.hero.size
    canvas.create_oval(x0, y0, x1, y1, fill='red')

def drawSoldiers(app, canvas):
    for tower in app.towers:
        if(isinstance(tower, Barracks)):
            for soldier in tower.soldiers:
                x0 = soldier.position[0] - 2
                y0 = soldier.position[1] - 2
                x1 = soldier.position[0] + 2
                y1 = soldier.position[1] + 2
                canvas.create_oval(x0, y0, x1, y1, fill="yellow")

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='red')

def drawTitleScreen(app, canvas):
    canvas.create_text(app.width//2, app.height//2 - 25, 
                        text="Game Title!", font="Arial 32 bold")
    canvas.create_text(app.width//2, app.height//2 + 15, 
                        text="Choose Difficulty:", font='Arial 20 bold')
    canvas.create_text(app.width//3, app.height//2 + 45, 
                        text="easy (press 1)", font='Arial 15 bold')   
    canvas.create_text(app.width//2, app.height//2 + 45, 
                        text="medium (press 2)", font='Arial 15 bold')      
    canvas.create_text(2*app.width//3, app.height//2 + 45, 
                        text="hard (press 3)", font='Arial 15 bold')       
    canvas.create_text(app.width//2, app.height//2 + 70, 
                        text="press Enter to begin", font='Arial 15 bold')       

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawPath(app, canvas)
    drawTowers(app, canvas)
    drawGoblin(app, canvas)
    drawArrow(app, canvas)
    drawSpell(app, canvas)
    drawHero(app, canvas)
    drawSoldiers(app, canvas)
    if(not app.started):
        drawBackground(app, canvas)
        drawTitleScreen(app, canvas)

def main():
    runApp(width=1000, height=600)

if __name__ == '__main__':
    main()