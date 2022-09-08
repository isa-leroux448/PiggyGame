import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
blue = (152,235,255)
light_blue = (116,193,211)
background = pygame.image.load('background.png')
menu = pygame.image.load('menu.png')
gameOverImage = pygame.image.load('Gameover.png')
font = pygame.font.SysFont("comicsansms",24)
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Mon cochon!')

pigImage = pygame.image.load('pig.png')
foodImage = pygame.image.load('donut.png')
enemyImage = pygame.image.load('chicken.png')

oink = pygame.mixer.Sound('Oink.wav')
chomp = pygame.mixer.Sound('Chomp.wav')
bawk = pygame.mixer.Sound('Bawk.wav')
music = pygame.mixer.music.load('music.wav')

highscore = 0
            
def drawText(text, font, surface, x, y):
    textobj = font.render(text,1,black)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

def text_objects(text,font):
    textSurface = font.render(text,True,black)
    return textSurface,textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text,largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

def button(msg,x,y,w,h,ic,ac,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            if action == "jouer":
                pygame.mixer.music.play(-1, 0.0)
                pygame.mixer.music.set_volume(0.08)
                game_loop()
            if action == "rejouer":
                pygame.mixer.music.unpause()
                game_loop()
            elif action == "quitter":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",24)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

                
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        gameDisplay.blit(menu,(0,0))
        largeText = pygame.font.SysFont("comicsansms", 85)
        TextSurf, TextRect = text_objects("Mon cochon!", largeText)
        TextRect.center = ((display_width/2), 100)
        gameDisplay.blit(TextSurf, TextRect)

        button("Jouer", 175,500,150,50,blue,light_blue,"jouer")
        button("Quitter", 475, 500, 150, 50, blue,light_blue, "quitter")

        pygame.display.update()
        clock.tick(15)

def game_loop():
    Score = 0
    x_change = 0
    y_change = 0
    foodCounter = 0
    list = ["Vertical","Horizontal"]
    baddies = []
    item = 0

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    foodx = random.randrange(48, display_width - 48)
    foody = random.randrange(54, display_height - 54)

    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -6
                if event.key == pygame.K_RIGHT:
                    x_change = 6
                if event.key == pygame.K_UP:
                    y_change = -6
                if event.key == pygame.K_DOWN:
                    y_change = 6
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
                
        if x > 705:
            x_change = 0
            x = 705
        if x < -10:
            x_change = 0
            x = -10
        if y < -15:
            y_change = 0
            y = -15
        if y > 505:
            y_change = 0
            y = 505

        x += x_change
        y += y_change

        gameDisplay.fill(white)
        gameDisplay.blit(background,(-50,-50))
        global highscore
        drawText('Score: %s' % (Score), font, gameDisplay, 10, 0)
        drawText('Meilleur Score: %s' % (highscore), font, gameDisplay, 10, 25)

        food = pygame.Rect(foodx, foody,48 , 54)
        
        if foodCounter == 0:
            gameDisplay.blit(foodImage, food)

        player = pygame.Rect(x, y,93,89)

        if player.colliderect(food):
            foodCounter += -1
            Score += 1
            foodx = random.randrange(48, display_width - 48)
            foody = random.randrange(54, display_height - 54)
            foodCounter += 1
            chomp.play()

            if Score % 2 == 0:
            
                item = random.randint(1, len(list))

                if item == 1:
                    newchicken = {'rect':pygame.Rect(random.randint(0,display_width-45),0,32,34),
                                  'surface':pygame.transform.scale(enemyImage,(45,50)),
                                  'vertical': "vertical",
                                  'speed': random.randrange(2,5),
                                  'down': "down"
                                  }
                    item = 0
                    baddies.append(newchicken)
                    bawk.play()

                if item == 2:
                    newchicken = {'rect':pygame.Rect(0,random.randint(0,display_height-45),32,34),
                                  'surface': pygame.transform.scale(enemyImage, (45,50)),
                                  'horizontal': "horizontal",
                                  'speed': random.randrange(2,5),
                                  'right': "right"
                                  }
                    item = 0
                    baddies.append(newchicken)
                    bawk.play()

        gameDisplay.blit(pigImage, player)
        for b in baddies:
            gameDisplay.blit(b['surface'],b['rect'])
            

        for b in baddies:
            if "vertical" in b:
                if "down" in b:
                    if not b['rect'].bottom >= 589:
                        b['rect'].move_ip(0, b['speed'])
                    if b['rect'].bottom >= 589:
                        del b['down']
                        b["up"] = "up"
                if "up" in b:
                    if not b['rect'].top <= 5:
                        b['rect'].move_ip(0,b['speed']-(b['speed']*2))
                    if b['rect'].top <= 5: 
                        del b ['up']
                        b["down"] = "down"

            if "horizontal" in b:
                if "right" in b:
                    if not b['rect'].right >= 791:
                        b['rect'].move_ip(b['speed'],0)
                    if b['rect'].right >= 791:
                        del b['right']
                        b['left'] = "left"
                if "left" in b:
                    if not b['rect'].left <= 5:
                        b['rect'].move_ip(b['speed']-(b['speed']*2),0)
                    if b['rect'].left <= 5:
                        del b ['left']
                        b['right'] = "right"

            if player.colliderect(b['rect']):
                oink.play()
                pygame.mixer.music.pause()
                if Score > highscore:
                    highscore = Score
                gameOver()

        pygame.display.update()
        clock.tick(60)
        
def gameOver():
    gameOver = True
    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(gameOverImage,(200,150))
        button("Rejouer", 225, 325,150,50,blue,light_blue,"rejouer")
        button("Quitter", 425, 325, 150, 50, blue,light_blue, "quitter")
        pygame.display.update()
        clock.tick(15)
                    
game_intro()
game_loop()
