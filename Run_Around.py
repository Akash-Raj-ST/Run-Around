import pygame,sys,time
from pygame.locals import*
pygame.init()
clock=pygame.time.Clock()
screenSize=[1500,700]
# colours
red=(255,0,0)
green=(0,255,0)
black=(0,0,0)
blue=(0,0,255)
white=(255,255,255)
# setting screen
pygame.display.set_caption('RunAround')
screen=pygame.display.set_mode(screenSize)
screen.fill((0,0,0))
# images
canvas=pygame.Surface((2950,1200))
logo=pygame.image.load('logo.png')
pygame.display.set_icon(logo)
canvas.fill(green)
endScreen=pygame.image.load('over.jpg')
endScreen=pygame.transform.scale(endScreen,(2950,1200))
startScreen=pygame.image.load('startScreen.jpg')
startScreen=pygame.transform.scale(startScreen,screenSize)
instruction=pygame.image.load("instruction.jpg")
instruction=pygame.transform.scale(instruction,screenSize)
# soundTrack
rectCross=pygame.mixer.Sound('rectCross.wav')
hit=pygame.mixer.Sound('hit.wav')
collision=pygame.mixer.Sound('collision.wav')
pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)

def main():
# initial position of rects
    playerOneMove=[70,70]
    playerTwoMove=[70,520]


    time=0
    count=10 #to limit sound effect affect collision

    #image
    wallImage=pygame.image.load('rock.png')
    # playerRect
    playerOneRect=pygame.Rect(playerOneMove[0],playerOneMove[1],90,90)
    playerTwoRect=pygame.Rect(playerTwoMove[0],playerTwoMove[1],90,90)
    # parameters
    moveUp=False
    moveRight=False
    moveLeft=False
    moveDown=False
    moveTwoUp=False
    moveTwoDown=False
    moveTwoRight=False
    moveTwoLeft=False
    canMove=True
 
# functions
    def load_map(path):
        f = open(path + '.txt','r')
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))
        return game_map

    gameMap = load_map('gameMap')
    def collisionTest(rect,tiles):
        hitList=[]
        for tile in tiles:
            if rect.colliderect(tile):
                pygame.mixer.Sound.play(hit)
                hitList.append(tile)
        return hitList

    def moveOne(rectOne,movement,tiles1,tiles3):
        tiles=tiles1+tiles3
        rectOne.x+=movementOne[0]
        hitList = collisionTest(rectOne,tiles)
        for tile in hitList:
            if movementOne[0] > 0:
                rectOne.right = tile.left   
            elif movementOne[0] < 0:
                rectOne.left = tile.right  
        rectOne.y+=movementOne[1]  
        hitList = collisionTest(rectOne,tiles)
        for tile in hitList:
            if movementOne[1] > 0:
                rectOne.bottom = tile.top
            elif movementOne[1] < 0:
                rectOne.top = tile.bottom
        return rectOne        
    def moveTwo(rectTwo,movement,tiles1,tiles2):
        tiles=tiles1+tiles2
        rectTwo.x+=movementTwo[0]
        hitList = collisionTest(rectTwo,tiles)
        for tile in hitList:
            if movementTwo[0] > 0:
                rectTwo.right = tile.left   
            elif movementTwo[0] < 0:
                rectTwo.left = tile.right  
        rectTwo.y+=movementTwo[1]  
        hitList = collisionTest(rectTwo,tiles)
        for tile in hitList:
            if movementTwo[1] > 0:
                rectTwo.bottom = tile.top
            elif movementTwo[1] < 0:
                rectTwo.top = tile.bottom
        return rectTwo
    enter=True
    timeRun=True #to stop time runnnin after collision
    displayTime=True
 
# LOOP
    while enter:
        
        if timeRun:
            time+=1
        realTime=time*0.0397
        realTime=int(realTime)
        movementOne=[0,0]
        movementTwo=[0,0]
        canvas.fill(black)
        y=0
        tiles=[]
        tiles2=[]
        tiles3=[]
        for block in gameMap:
            x=0
            for tile in block:
                if tile=='1' or tile=='3' or tile=='2':
                    canvas.blit(wallImage,(x*64,y*64))
                
                if tile=='1':
                    tileRect=pygame.Rect(x*64,y*64,64,64)
                    tiles.append(pygame.Rect(x*64,y*64,64,64))
                if tile=='2':
                    tileRect=pygame.Rect(x*64,y*64,64,64)
                    tiles2.append(pygame.Rect(x*64,y*64,64,64))
                    pygame.draw.rect(canvas,[40,255,18],tileRect)
                if tile=='3':
                    tileRect=pygame.Rect(x*64,y*64,64,64)
                    tiles3.append(pygame.Rect(x*64,y*64,64,64))
                    pygame.draw.rect(canvas,[50,104,241],tileRect)
                x+=1
            y+=1
        for tile in tiles2:
            if playerOneRect.colliderect(tile):
                if not playerOneRect.colliderect(playerTwoRect):
                    pygame.mixer.Sound.play(rectCross)
        for tile in tiles3:
            if playerTwoRect.colliderect(tile):
                if not playerOneRect.colliderect(playerTwoRect):
                    pygame.mixer.Sound.play(rectCross)    
        if playerOneRect.colliderect(playerTwoRect):    #check collision
            canMove=False
            moveUp=False
            moveRight=False
            moveLeft=False
            moveDown=False
            moveTwoUp=False
            moveTwoDown=False
            moveTwoRight=False
            moveTwoLeft=False
            displayTime=False
            count-=1
            music=False
            if count>0:
                pygame.mixer.Sound.play(collision)
            canvas.fill(white)
            fontName='roman.ttf'
            fontSize=70
            font=pygame.font.Font(fontName, fontSize)
            canvas.blit(endScreen,(0,0))
            minute=realTime//60
            sec=realTime%60
            text=font.render('Evader survived for: '+str(minute)+' minutes '+str(sec)+" seconds",True,white,black)
            text2=font.render('Press SPACE',True,green,black)
            text21=font.render('To play again',True,green,black)

            text3=font.render('Press esc',True,red,black)
            text31=font.render('To quit',True,red,black)

            canvas.blit(text,(550,850))
            canvas.blit(text2,(850,1000))
            canvas.blit(text21,(800,1100))

            canvas.blit(text3,(1600,1000))
            canvas.blit(text31,(1650,1100))

            timeRun=False
            if event.type==KEYDOWN and event.key==K_SPACE:
                main()
            if event.type==KEYDOWN and event.key==K_ESCAPE:
                pygame.quit()
                sys.exit()
        if moveUp==True:
            movementOne[1]-=16
        if moveDown==True:
            movementOne[1]+=16
        if moveRight==True:
            movementOne[0]+=16
        if moveLeft==True:
            movementOne[0]-=16

        # playerTwo
        if moveTwoUp==True:
            movementTwo[1]-=18
        if moveTwoDown==True:
            movementTwo[1]+=18
        if moveTwoRight==True:
            movementTwo[0]+=18
        if moveTwoLeft==True:
            movementTwo[0]-=18
        playerOneMoveWithRect=moveOne(playerOneRect,movementOne,tiles,tiles3)
        playerTwoMoveWithRect=moveTwo(playerTwoRect,movementTwo,tiles,tiles2)
        pygame.draw.rect(canvas,(16,148,2),playerOneMoveWithRect)
        pygame.draw.rect(canvas,(12,60,181),playerTwoMoveWithRect)
        fontName='Arial'
        fontSize=65
        font=pygame.font.SysFont(fontName, fontSize)
        minute=realTime//60
        sec=realTime%60
        text=font.render(str(minute)+':'+str(sec),True,white,black)
        if displayTime:
            canvas.blit(text,(1400,0))
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if canMove:
                if event.type==KEYDOWN:
                    if event.key==K_RIGHT:
                        moveRight=True
                    if event.key==K_DOWN:
                        moveDown=True
                    if event.key==K_UP:
                        moveUp=True
                    if event.key==K_LEFT:
                        moveLeft=True
                        # playertwo
                    if event.key==K_w:  #UP
                        moveTwoUp=True
                    if event.key==K_s: #DOWN
                        moveTwoDown=True
                    if event.key==K_a: #LEFT
                        moveTwoLeft=True
                    if event.key==K_d: #RIGHT
                        moveTwoRight=True

                if event.type==KEYUP:
                    if event.key==K_RIGHT:
                        moveRight=False
                    if event.key==K_DOWN:
                        moveDown=False
                    if event.key==K_UP:
                        moveUp=False
                    if event.key==K_LEFT:
                        moveLeft=False
                        # playerTwo
                    if event.key==K_w:  #UP
                        moveTwoUp=False
                    if event.key==K_s: #DOWN
                        moveTwoDown=False
                    if event.key==K_a: #LEFT
                        moveTwoLeft=False
                    if event.key==K_d: #RIGHT
                        moveTwoRight=False   
        screen.blit(pygame.transform.scale(canvas,screenSize),(0,0))
        pygame.display.update()
        clock.tick(60)
def intro():
   home=True 
   while True:
     if home:
      screen.fill(white)
      screen.blit(startScreen,(0,0))
      pygame.display.update()
     for event in pygame.event.get():
        if event.type==KEYDOWN and event.key==K_i:
            home=False
            screen.fill(white)
            screen.blit(instruction,(0,0))
            pygame.display.update()
        if event.type == KEYDOWN and event.key==K_RETURN:
              main()
        if event.type==QUIT:
            pygame.quit()
            sys.exit()




intro()



