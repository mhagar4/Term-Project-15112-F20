from KingdomClashClasses import *
from cmu_112_graphics import *
from PIL import Image
import math, random, time

def appStarted(app):
    app.towerTypes = (Arrows, Magic, Explosives, Barracks)
    app.monsters = [Goblin, Spider, Wolf, Ogre, Dark_Knight]
    app.highscore = int(open('highscore.txt', 'r').readline())
    app.path1Bounds = (300, 400)
    app.path2Bounds = (-100, 0)
    app.path3Bounds = (50, 150)
    (heroHeight, heroX) = (sum(app.path1Bounds) / 2, app.width - 50)
    app.hero = Hero([heroX, path1(heroX, heroHeight)])
    app.difficultyChosen = False
    app.showInstructions = True
    app.selectedSoldier = None
    app.soldierTarget = None
    app.started = False
    app.paused = True
    app.gameOver = False
    app.heroGrave = 0
    app.grave = []
    app.node1 = 305
    app.node2 = 865
    app.coins = 360
    app.lives = 10
    app.wave = 0
    setMonsters(app)
    setTowers(app)
    loadImages(app)

#ALL IMAGES (path image excluded) MODIFIED FROM: 
#https://www.kingdomrushfrontiers.com/
#https://kingdomrushtd.fandom.com/wiki/Kingdom_Rush_Wiki 
def loadImages(app):
    app.title = app.scaleImage(app.loadImage('title.png'), 3/10)
    app.instructions = app.scaleImage(app.loadImage('dark_knight.png'), 1/10)
    app.heroImage = app.scaleImage(app.loadImage(app.hero.image), 1/20)
    app.emptyPlotImage = app.scaleImage(app.loadImage('empty_plot.png'), 1/30)
    app.soldierImage = app.scaleImage(app.loadImage('soldier.png'), 1/50)
    app.pathImage = app.scaleImage(app.loadImage('path.png'), 1/2)
    app.bombImage = app.scaleImage(app.loadImage('bomb.png'), 1/75)
    app.arrowImage = app.scaleImage(app.loadImage('arrow.png'), 1/75)
    app.spellImage = app.scaleImage(app.loadImage('spell.png'), 1/75)

#initializes monsters
def setMonsters(app):
    app.enemies = []
    app.numEnemies = random.randint(2, 10)
    index = app.wave % len(app.monsters)
    for i in range(app.numEnemies):
        startHeight = random.randint(-20, 20)
        positionX = random.randint(-50, -5)
        positionY = path1(positionX, 350 + startHeight)
        position = [positionX, positionY]
        app.enemies.append(app.monsters[index](position=position, 
                                                height=startHeight))
    app.enemyImage = app.loadImage(app.enemies[0].image)
    app.enemyImage = app.scaleImage(app.enemyImage, 1/50)

#creates "empty" towers
def setTowers(app):
    app.towerPositions = [  (140, 60 ),  (160, 250), (310, 330), (490, 470), 
                            (930, 330),  (460, 240), (620, 375), (750, 70 ),
                            (780, 460),  (770, 270)  ]
    app.towers = []
    app.selectedTower = None
    for i in range(len(app.towerPositions)): 
       app.towers.append(Tower(position=app.towerPositions[i]))

#reacts to key presses
def keyPressed(app, event):
    if(event.key == 'v'): app.enemies[0].speed = 20
    if(not app.started): #on title screen enter starts game, num sets difficulty
        if(event.key == 'Enter' and app.difficultyChosen): app.started = True
        elif(event.key in ['1', '2', '3']): setDifficulty(app, int(event.key))
    else:
        if(app.selectedTower != None): #must select tower/plot to build/upgrade
            if(event.key in ['a', 'm', 'e', 'b'] and 
                not isinstance(app.selectedTower, app.towerTypes)): 
                    buildTower(app, event.key)
            #checks if level up is valid
            elif(isinstance(app.selectedTower, app.towerTypes) and 
                    event.key == 'Up' and app.coins >= Tower.levelUpCost and 
                    app.selectedTower.level < Tower.maxLevel): 
                app.selectedTower.levelUp()
                app.coins -= Tower.levelUpCost
        #other keystroke shortcuts
        if(event.key == 'p'): app.paused = not app.paused
        elif(event.key == 'r'): appStarted(app)
        elif(event.key == 'i'): app.showInstructions = not app.showInstructions
        elif(event.key == 'Right'): app.enemies = []
        elif(event.key == 'Space'): app.gameOver = True

#sets difficulty of game
def setDifficulty(app, difficulty):
    app.difficultyChosen = True
    app.numEnemies *= difficulty
    for monster in app.monsters:
        monster.speed += 2 * (difficulty - 1)
        monster.damage += difficulty - 1

#"builds" corresponding tower by replacing empty tower with type
def buildTower(app, key):
    position = app.selectedTower.position
    index = app.towers.index(app.selectedTower)
    if(key == 'a'):
        if(app.coins >= Arrows.cost):
            app.towers[index] = Arrows(position=position)
            app.coins -= Arrows.cost
            app.towers[index].image = app.loadImage('arrows.png')
            app.towers[index].image = app.scaleImage(app.towers[index].image, 
                                                        1/30)
    elif(key == 'm'):
        if(app.coins >= Magic.cost):
            app.towers[index] = Magic(position=position)
            app.coins -= Magic.cost
            app.towers[index].image = app.loadImage('magic.png')
            app.towers[index].image = app.scaleImage(app.towers[index].image, 
                                                        1/30)
    elif(key == 'e'):
        if(app.coins >= Explosives.cost):
            app.towers[index] = Explosives(position=position)
            app.coins -= Explosives.cost
            app.towers[index].image = app.loadImage('explosives.png')
            app.towers[index].image = app.scaleImage(app.towers[index].image, 
                                                        1/30)
    elif(key == 'b'):
        if(app.coins >= Barracks.cost):
            app.towers[index] = Barracks(position=position)
            app.towers[index].positionSoldiers()
            app.coins -= Barracks.cost
            app.towers[index].image = app.loadImage('barracks.png')
            app.towers[index].image = app.scaleImage(app.towers[index].image, 
                                                        1/30)

def mousePressed(app, event):
    x, y = event.x, event.y
    #makes sure you only select one soldier at a time
    if(app.selectedSoldier == None): 
        selectSoldiersAtPoint(app, x, y)
    #chooses target for selected soldier if there aren't soldiers moving
    elif(not app.selectedSoldier.isMoving): 
        #makes sure soldiers can't move out of range of their tower or off path
        if(isViableTarget(app, x, y)):
            app.soldierTarget = (x, y)
            app.selectedSoldier.isMoving = True
        #unselects soldier if target was not viable
        else: app.selectedSoldier = None
    #selects new tower
    app.selectedTower = None 
    selectTowerAtPoint(app, x, y)

#tests if soldier target is valid
def isViableTarget(app, x, y):
    return (pointInPath(app, x, y) and pointInBarracksRange(app, x, y))

#tests if mouse press in range of barracks
def pointInBarracksRange(app, x, y):
    if(isinstance(app.selectedSoldier, Soldier)):
        tower = app.selectedSoldier.tower
        x1, y1 = tower.position[0], tower.position[1]
        return (distance(x, y, x1, y1) <= tower.range)
    return True

#tests if mouse press is in path
def pointInPath(app, x, y):
    inPath1 = path1(x, app.path1Bounds[0]) <= y <= path1(x, app.path1Bounds[1])
    inPath2 = (path2(x, app.path2Bounds[0]) >= y >= path2(x, app.path2Bounds[1]) 
                and (y <= app.path1Bounds[0]))
    inPath3 = (path3(x, app.path3Bounds[0]) <= y <= path3(x, app.path3Bounds[1]) 
                and (y <= app.path1Bounds[0]))
    return (inPath1 or inPath2 or inPath3)

#selects soldiers at mousepress
def selectSoldiersAtPoint(app, x, y):
    for tower in app.towers:
        if(isinstance(tower, Barracks)):
            for soldier in tower.soldiers:
                x2, y2 = soldier.position[0], soldier.position[1]
                if((distance(x, y, x2, y2) <= soldier.size)):
                    app.selectedSoldier = soldier
                    return
    if(app.hero != None):
        x2, y2 = app.hero.position[0], app.hero.position[1]
        if((distance(x, y, x2, y2) <= app.hero.size) and
            (not app.hero.isBattling)):
            app.selectedSoldier = app.hero

#selects tower if clicked on 
def selectTowerAtPoint(app, x, y):
    for tower in app.towers:
        x0 = tower.position[0] - tower.size
        y0 = tower.position[1] - tower.size
        x1 = tower.position[0] + tower.size
        y1 = tower.position[1] + tower.size
        if(x0 <= x <= x1 and y0 <= y <= y1):
            app.selectedTower = tower

#towers and soldiers attack enemies
def playTowerDefense(app):
    for enemy in app.enemies:
        if(app.hero != None): heroAttack(app, enemy)
    for tower in app.towers:
        for enemy in app.enemies:
            if(isinstance(tower, Barracks)): barracksAttack(app, tower, enemy) 
            elif(enemy.inRange(tower)):
                towerShoot(app, tower, enemy)
                break #this is so each tower only has one target at a time
            elif(tower.isAttacking): tower.stopAttack()

#hero attacks monsters in range
def heroAttack(app, monster):
    if(monster.inRange(app.hero)):
        app.hero.battle(monster)

#barracks attack monsters in range
def barracksAttack(app, tower, monster):
    tower.isAttacking = True
    tower.attack(monster)

#shooting towers attack monsters in range
def towerShoot(app, tower, monster):
    if(tower.weapon.target == None): #chooses target if target=None
        selectTarget(tower, monster)
    else: #shoots target
        tower.isAttacking = True
        tower.attack()
        if(tower.weapon.monsterHit(monster)): hitMonster(app, tower, monster)
        elif(tower.weapon.outOfRange()): tower.weapon.land()

#towers select their targets
def selectTarget(tower, monster):
    targetX = monster.position[0] + 10
    targetY = monster.position[1] 
    target  = (targetX, targetY)
    tower.weapon.target = target
    tower.weapon.isMoving = True

#weapons react to hitting a monster
def hitMonster(app, tower, monster):
    if(isinstance(tower, Explosives)): explode(app, tower)
    else:
        tower.weapon.land()
        monster.health -= tower.damage
        app.coins += 2

#bomb explode when hitting monster
def explode(app, tower):
    for enemy in app.enemies:
        if(enemy.inRange(tower.weapon)):
            enemy.health -= tower.damage
            app.coins += 2
    tower.weapon.land()

#moves monsters along path
def timerFired(app):
    soldiersMove(app)
    if(not app.paused and app.started and not app.gameOver):
        playTowerDefense(app)
        enemiesAdvance(app)
        killMonsters(app)
        updateScore(app)
        callWave(app)
        soldiersFall(app)
        resurrectSoldiers(app)

#enemies move along path
def enemiesAdvance(app):
    for enemy in app.enemies:
        if(enemy.position[0] < app.node1 and enemy.path == None):
            enemy.path = bestPathToNode(app, app.node1, enemy)
        elif(enemy.position[0] > app.node1):
            if(enemy.path2 == None): 
                enemy.path2 = bestPathToNode(app, app.node2, enemy)
                enemy.path = enemy.path2
        enemy.move()

#soldiers run to points from mouse press
def soldiersMove(app):
    if(app.selectedSoldier != None and app.soldierTarget != None):
        app.selectedSoldier.run(app.soldierTarget)
        currX = app.selectedSoldier.position[0]
        currY = app.selectedSoldier.position[1]
        if((currX, currY) == app.soldierTarget):
            app.selectedSoldier.isMoving = False
            app.selectedSoldier = None
            app.soldierTarget = None

#gets the safest path for the monster to travel along
def bestPathToNode(app, node, monster):
    path1weight, path2weight, path3weight = 0, 0, 0
    path1height = sum(app.path1Bounds)/2
    path2height = sum(app.path2Bounds)/2
    path3height = sum(app.path3Bounds)/2
    x, y = monster.position[0], monster.position[1]
    for i in range(x, node+1, monster.speed): #models monsters path
        y1 = path1(i, path1height + monster.startHeight)
        y2 = path2(i, path2height + monster.startHeight)
        y3 = path3(i, path3height + monster.startHeight)
        testMonster1 = Monster(position=[i, y1], height=monster.height, 
                                health=20)
        testMonster2 = Monster(position=[i, y2], height=monster.height, 
                                health=20)
        testMonster3 = Monster(position=[i, y3], height=monster.height,
                                health=20)
        for tower in app.towers:
            if(testMonster1.inRange(tower)):
                path1weight += pathWeightFromTower(app, tower, node, 'path1')
            if(testMonster2.inRange(tower) and node == app.node1):
                path2weight += pathWeightFromTower(app, tower, node, 'path2')
            if(testMonster3.inRange(tower) and node == app.node2):
                path3weight += pathWeightFromTower(app, tower, node, 'path3')
    if(path2weight == min(path1weight, path2weight) and node == app.node1):
        return 'path2'
    elif(path3weight == min(path1weight, path3weight) and node == app.node2):
        return 'path3'
    else:
        return 'path1'

#gets the weight from a certain tower
def pathWeightFromTower(app, tower, node, path):
    weight = 0
    for type in [Arrows, Magic, Explosives]:
        if(isinstance(tower, type)): weight += type.damage
    if(isinstance(tower, Barracks)): 
        for soldier in tower.soldiers:
            x = soldier.position[0]
            if(soldierInPath(app, soldier, path)) and (beforeNode(x, node)):
                weight += (soldier.health + soldier.damage) // 2
    return weight

#tests if a soldier is in a given path
def soldierInPath(app, soldier, path):
    x, y = soldier.position[0], soldier.position[1]
    if(path == 'path1'):
        return path1(x, app.path1Bounds[0]) <= y <= path1(x, app.path1Bounds[1])
    elif(path == 'path2'):
        return path2(x, app.path2Bounds[1]) <= y <= path2(x, app.path2Bounds[0])
    else:
        return path3(x, app.path3Bounds[0]) <= y <= path3(x, app.path3Bounds[1])

#tests if a certain position occurs before the given node
def beforeNode(x, node):
    return x <= node

#keeps track of lives when enemies reach kingdom
def updateScore(app):
    i=0
    while i < len(app.enemies):
        if(app.enemies[i].position[0] > app.width):
            app.enemies.pop(i)
            app.lives-=1
            if(app.lives == 0): app.gameOver = True
        i+=1

#calls new wave when old one is either dead or gone
def callWave(app):
    if(app.enemies == []):
        app.wave += 1
        soldiersHalt(app)
        if(app.wave > app.highscore):
            app.highscore = open('highscore.txt', 'w')
            app.highscore.write(f'{app.wave}')
            app.highscore = open('highscore.txt', 'r')
            app.highscore = int(app.highscore.readline())
        setMonsters(app)

def soldiersHalt(app):
    for tower in app.towers:
        if(isinstance(tower, Barracks)):
            for soldier in tower.soldiers: 
                soldier.isBattling = False

#pops enemies from app.enemies if they die and awards coins
def killMonsters(app):
    i=0
    while i < len(app.enemies):
        if(app.enemies[i].dead):
            if(app.hero != None and app.enemies[i] == app.hero.opponent):
                app.hero.opponent = None
            app.enemies.pop(i)
            app.coins += 5
        i+=1

#removes soldiers if they die
def soldiersFall(app):
    for tower in app.towers:
        if(isinstance(tower, Barracks)):
            i = 0
            while i < len(tower.soldiers):
                if(tower.soldiers[i].dead):
                    soldier = tower.soldiers.pop(i)
                    app.grave.append(soldier)
                    index = app.grave.index(soldier)
                    app.grave[index].deathTime = time.time()
                i+=1
    if(app.hero != None and app.hero.dead):
        app.heroGrave = app.hero
        app.hero = None
        app.heroGrave.deathTime = time.time()

#resurrects dead soldiers after a given wait time
def resurrectSoldiers(app):
    waitTime = 15
    i=0
    while i < len(app.grave): 
        if(time.time() >= app.grave[i].deathTime + waitTime):
            app.grave[i].deathTime = None
            app.grave[i].health = 100
            app.grave[i].dead = False
            app.grave[i].tower.soldiers.append(app.grave.pop(i))
        i+=1
    if(app.heroGrave != 0):
        if(time.time() >= app.heroGrave.deathTime + 2*waitTime):
            app.heroGrave.deathTime = None
            app.heroGrave.health = 300
            app.heroGrave.dead = False
            app.hero = app.heroGrave
            app.heroGrave = 0

######## view functions #########
def drawEnemy(app, canvas):
    for enemy in app.enemies:
        x = enemy.position[0]
        y = enemy.position[1]
        canvas.create_image(x, y, image=ImageTk.PhotoImage(app.enemyImage))

def drawPath(app, canvas):
    x, y = app.width/2 - 10, app.height/2
    canvas.create_image(x, y, image=ImageTk.PhotoImage(app.pathImage))

def drawTowers(app, canvas):
    for tower in app.towers:
        x0 = tower.position[0] - tower.size
        y0 = tower.position[1] - tower.size
        x1 = tower.position[0] + tower.size
        y1 = tower.position[1] + tower.size
        x = tower.position[0]
        y = tower.position[1]
        if(tower is app.selectedTower):
            canvas.create_oval(x0, y0, x1, y1)
        if(tower.image == None): 
            canvas.create_image(x, y, 
                                image=ImageTk.PhotoImage(app.emptyPlotImage))
        else: 
            canvas.create_image(x, y, image=ImageTk.PhotoImage(tower.image))

def drawArrow(app, canvas):
    for tower in app.towers:
        if isinstance(tower, Arrows) and tower.isAttacking:
            x = tower.arrow.position[0]
            y = tower.arrow.position[1]
            canvas.create_image(x, y, image=ImageTk.PhotoImage(app.arrowImage))

def drawSpell(app, canvas):
    for tower in app.towers:
        if isinstance(tower, Magic) and tower.isAttacking:
            x = tower.spell.position[0]
            y = tower.spell.position[1]
            canvas.create_image(x, y, image=ImageTk.PhotoImage(app.spellImage))

def drawBomb(app, canvas):
    for tower in app.towers:
        if isinstance(tower, Explosives) and tower.isAttacking:
            x = tower.bomb.position[0]
            y = tower.bomb.position[1]
            canvas.create_image(x, y, image=ImageTk.PhotoImage(app.bombImage))

def drawHero(app, canvas):
    if(app.hero != None and not app.hero.dead):
        x = app.hero.position[0]
        y = app.hero.position[1]
        canvas.create_image(x, y, image=ImageTk.PhotoImage(app.heroImage))


def drawSoldiers(app, canvas):
    for tower in app.towers:
        if(isinstance(tower, Barracks)):
            for soldier in tower.soldiers:
                x0 = soldier.position[0] - soldier.size
                y0 = soldier.position[1] - soldier.size
                x1 = soldier.position[0] + soldier.size
                y1 = soldier.position[1] + soldier.size
                x = soldier.position[0]
                y = soldier.position[1]
                if(soldier == app.selectedSoldier): 
                    canvas.create_oval(x0, y0, x1, y1, fill='blue')
                canvas.create_image(x, y, 
                                    image=ImageTk.PhotoImage(app.soldierImage))

def drawGameOver(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='dark green')
    canvas.create_text(app.width/2, app.height/2 - 80, text="GAME OVER", 
                        font="Times 50 bold", fill='lawn green')
    canvas.create_text(app.width/2, app.height/2, 
                        text=f"Waves Survived: {app.wave}", 
                        font="Times 40 bold", fill='lawn green')
    canvas.create_text(app.width/2, app.height/2 + 80, 
                        text=f"Highscore: {app.highscore}", 
                        font="Times 40 bold", fill='lawn green')
    canvas.create_text(app.width/2, app.height/2 + 150, 
                        text="press 'r' to restart", font="Times 20 bold", 
                        fill='lawn green')

def drawScore(app, canvas):
    textPt1 = f'highscore: {app.highscore}  wave: {app.wave+1} / ∞  '
    textPt2 = f'lives: {app.lives}  coins: {app.coins}'
    text = textPt1 + textPt2
    canvas.create_text(app.width-4*len(text), 20, text=text, 
                        font='Arial 13 bold')

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='green')

def drawInstructions(app, canvas):
    font = 'Times 14 bold'
    canvas.create_rectangle(app.width/3-10, app.height/3-10, 3*app.width/4-10, 
                            3*app.height/4-10, fill='darkOliveGreen', 
                            outline='darkOliveGreen')
    canvas.create_rectangle(app.width/3, app.height/3, 3*app.width/4, 
                            3*app.height/4, fill='seagreen', outline='seagreen')
    canvas.create_rectangle(100, app.height/2, 300, 3*app.height/4, 
                            fill='darkOliveGreen3', outline='darkOliveGreen3')
    canvas.create_image(850, app.height/2 + 70, 
                        image=ImageTk.PhotoImage(app.instructions))
    canvas.create_text(200, app.height/2+20, text="Tower Costs",
                        font='Times 20 bold')
    canvas.create_text(110, app.height/2+35, anchor=NW, font=font,
                        text=f"Arrows: {Arrows.cost} coins")
    canvas.create_text(110, app.height/2+55, anchor=NW, font=font,
                        text=f"Magic: {Magic.cost} coins")
    canvas.create_text(110, app.height/2+75, anchor=NW, font=font,
                        text=f"Explosives: {Explosives.cost} coins")
    canvas.create_text(110, app.height/2+95, anchor=NW, font=font,
                        text=f"Barracks: {Barracks.cost} coins")
    canvas.create_text(110, app.height/2+115, anchor=NW, font=font,
                        text=f"Level Ups: {Tower.levelUpCost} coins")
    canvas.create_text(app.width/2, app.height/3+15, text="Instructions:", 
                        font='Times 24 bold')
    canvas.create_text(app.width/3+20, app.height/3+35, anchor=NW, font=font,
                        text="click on an empty plot to build a tower")
    canvas.create_text(app.width/3+20, app.height/3+55, anchor=NW, font=font,
                        text="press 'a' to build Arrows tower")
    canvas.create_text(app.width/3+20, app.height/3+75, anchor=NW, font=font,
                        text="press 'b' to build Barracks tower")
    canvas.create_text(app.width/3+20, app.height/3+95, anchor=NW, font=font,
                        text="press 'm' to build Magic tower")
    canvas.create_text(app.width/3+20, app.height/3+115, anchor=NW, font=font,
                        text="press 'e' to build Explosives tower")
    canvas.create_text(app.width/3+20, app.height/3+135, anchor=NW, font=font,
                        text="press up arrow to update tower")  
    canvas.create_text(app.width/3+20, app.height/3+155, anchor=NW, font=font,
                        text="press 'p' to start play and toggle pause")
    canvas.create_text(app.width/3+20, app.height/3+175, anchor=NW, font=font,
                        text="press 'i' to show and hide instructions")     
    canvas.create_text(app.width/3+20, app.height/3+195, anchor=NW, font=font,
                        text="press 'r' to reset game")           
    canvas.create_text(app.width/3+20, app.height/3+215, anchor=NW, font=font,
                        text="click on soldiers to move them (w/in range)")

def drawTitleScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='lightGreen')
    x, y = app.width//2, app.height//2 - 75
    canvas.create_image(x, y, image=ImageTk.PhotoImage(app.title))
    canvas.create_text(app.width//2, app.height - 120, 
                        text="Choose Difficulty:", font='Arial 20 bold')
    canvas.create_text(app.width//3, app.height - 85, 
                        text="easy (press 1)", font='Arial 15 bold')   
    canvas.create_text(app.width//2, app.height - 85, 
                        text="medium (press 2)", font='Arial 15 bold')      
    canvas.create_text(2*app.width//3, app.height - 85, 
                        text="hard (press 3)", font='Arial 15 bold')       
    canvas.create_text(app.width//2, app.height - 50, 
                        text="press Enter to begin", font='Arial 15 bold')       

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawPath(app, canvas)
    drawTowers(app, canvas)
    drawSoldiers(app, canvas)
    drawHero(app, canvas)
    drawEnemy(app, canvas)
    drawArrow(app, canvas)
    drawSpell(app, canvas)
    drawBomb(app, canvas)
    drawScore(app, canvas)
    if(app.showInstructions): drawInstructions(app, canvas)
    if(not app.started): drawTitleScreen(app, canvas)
    if(app.gameOver): drawGameOver(app, canvas)

def main():
    runApp(width=1000, height=600)

if __name__ == '__main__':
    main()