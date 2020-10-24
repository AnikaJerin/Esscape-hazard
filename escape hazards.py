
import random #for generating random numbers
import sys #if someone press the exit button the game will be stopped.we will use sys.exit to exit the game
import pygame
from pygame.locals import * #basic pygame imports
#global variables for the game
FPs=32 #frame per second. 32 is enough-less lagging+
screenwidth=289
screenheight=511
#creating screen
screen=pygame.display.set_mode((screenwidth,screenheight)) #creats a display serface. Initialize a window or screen for display
groundy= screenheight*.8 #ground height will be the 80% of my game screen(ground named pic)
game_sprites={} #images I'll be using in this game
game_sounds={} #sounds I\l be using
player='game/sprites/bird.png'
background='game/sprites/background.png'
pipe='game/sprites/cac.png'

def welcomeScreen():
    '''Shows welcome screen'''
    playerx=int(screenwidth/5) #defining player's x position
    playery=int((screenheight-game_sprites['player'].get_height())/2) #here, we are taking the height of the player image
    # which is inside the sprites folder and then subtracting it from the total screen height so that our player's
    # position remains in the center of the screen
    messagex=int((screenwidth-game_sprites['message'].get_width())/2)
    messagey=int(screenheight*0.13)
    basex=0
    while True:
        for event in pygame.event.get(): #mouse e kothay click korlam keyboard er event egula dekhay
            #if user presses on cross button,close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.type==K_ESCAPE): #keydown means a key is pressed
                pygame.quit() #quit the game
                sys.exit() #exit the program
                # if the user presses the space or up key start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key==K_UP):
                #return the welcomesreec function means stop the welcomesreen function and go to the main function
                return
            else:
                screen.blit(game_sprites['background'],(0,0))#1st blitting the background image, image name and position
                screen.blit(game_sprites['player'],(playerx,playery))
                screen.blit(game_sprites['message'],(messagex,messagey))
                screen.blit(game_sprites['base'],(basex,groundy))
                pygame.display.update()#screen won't change unless this runs
                fpsclock.tick(FPs)
def mainGame():
    score=0 #initializes score with 0
    playerx = int(screenwidth / 5)  # defining player's x position
    playery = int(screenwidth/2)
    basex=0
    #pipe generation logics
    '''
    1st we'll take get random pipe which returns a list and this list contains a dict{values for upper pipe}
    and the 2nd content of the dict{values for lower pipe}. 1st we'll place the lower pipe then place the upper pipe 
    in such a way that there is a gap between two pipes.calculate the offset.we will place the x position= screenwidth+
    10(outside the screen.then we we'll move to the left).
    for y position we'll generate a random number=offset ,(screenheight-base-1.2*offset)
    for upper pipe's y position calculate y1, which is the length of the pipe that'll be outside the screen.
    y1=pipeheight-y2(the height of the lower pipe+offset)
    '''
    #create 2 pipes for blitting on the screen
    newpipe1=getRandomPipe()
    newpipe2=getRandomPipe()
    #list of upperpipes
    upperPipes = [
        {'x': screenwidth + 200, 'y': newpipe1[0]['y']},
        {'x': screenwidth + 200 + (screenwidth / 2), 'y': newpipe2[0]['y']},
    ]
    
    #list of lower pipes
    lowerPipes = [
        {'x': screenwidth + 200, 'y': newpipe1[1]['y']},
        {'x': screenwidth + 200 + (screenwidth / 2), 'y': newpipe2[1]['y']},
    ]

    pipevelx = -4 #pipe moving velocity

    playervely = -9 #player -9 velocity te niche porbe
    playermaxvely = 10
    playerminvely = -8
    playeraccy = 1 #niche porar somoy er acceleration
    #arrow keys press korle jei velocity change hobe

    playerflyacc = -8  # velocity while flapping means object ta jokhn agabe
    playerflew = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit() #game quitting
                sys.exit() #program is quitting
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0: #means if the player is inside the screen (game on)
                    playervely = playerflyacc
                    playerflew = True
                    game_sounds['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes,lowerPipes)  # This function will return true if the player is crashed
        if crashTest:
            return

            # check for score
        playerMidPos = playerx + game_sprites['player'].get_width() / 2 #player er center jodi pipe ke pass kore then score bere jabe
        for pipe in upperPipes:
            pipemidpos = pipe['x'] + game_sprites['pipe'][0].get_width() / 2 #pipe er mid position
            if pipemidpos <= playerMidPos < pipemidpos + 4:
                score += 1 #score icreases
                print(f"Your score is {score}")
                game_sounds['point'].play() #point pele ei sound play hobe

        if playervely < playermaxvely and not playerflew:
            playervely += playeraccy

        if playerflew:
            playerflew = False #jodi upper key barbar press kore tahole true hobe ar ekbar press kre rekhe dile false hoye jabe
        playerheight = game_sprites['player'].get_height()
        playery = playery + min(playervely, groundy - playery - playerheight) #playery tokhn ebarbe jotokkhn niche
        # asbenajokhniche asbe tokhn eder min 0 hoye jabe mane player ground/base er uopr ei thakbe er niche nambena

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes): #zip duita list ke zip kore
            upperPipe['x'] += pipevelx #velocity negative assign kora hoise ekhn upper pipe er x e add kora mane
            #take left e niye jawa
            lowerPipe['x'] += pipevelx

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

            # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            # left e aste aste pipe ta jokhn ber hoye jabe mane pipe er x neg hobe tokhn remove
            upperPipes.pop(0)  # .pop element remove kore
            lowerPipes.pop(0)

            # Lets blit our sprites now
        screen.blit(game_sprites['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(game_sprites['base'], (basex, groundy))
        screen.blit(game_sprites['player'], (playerx, playery))

        #gonna show scores
        myDigits = [int(x) for x in list(str(score))]
        width = 0

        for digit in myDigits:
            width += game_sprites['numbers'][digit].get_width()
        Xoffset = (screenwidth - width) / 2 #screen er moddhe kothayscore dekhabo 1st digit score er

        for digit in myDigits:
            screen.blit(game_sprites['numbers'][digit], (Xoffset, screenheight * 0.12))
            Xoffset += game_sprites['numbers'][digit].get_width() #score er porer digit. evabe blit hote thakbe
        pygame.display.update()
        fpsclock.tick(FPs)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> groundy - 25  or playery<0:
        game_sounds['hit'].play()
        return True

    for pipe in upperPipes:

        pipeHeight = game_sprites['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < game_sprites['pipe'][0].get_width()):
            game_sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + game_sprites['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()
            return True

    return False



def getRandomPipe():
    #generating positions for the pipes(one bottom straight and one top rotated) for blitting on the screen
    pipeheight= game_sprites['pipe'][0].get_height() #gamesprites er pipe pic er height nibe
    offset=screenheight/3
    y2=offset+random.randrange(0,int(screenheight-game_sprites['base'].get_height()-1.2*offset))
    pipex= screenwidth+10
    y1=pipeheight-y2+offset
    pipe=[{'x':pipex,'y':-y1}, #upper pipe
          {'x':pipex,'y':y2}#lower pipe
     ]
    return pipe




if __name__=="__main__":
    #this will be the main function from where our game will start
    pygame.init() #initializes all the pygame modeules
    fpsclock=pygame.time.Clock() #Created clock object.if I run clock.tick40 then program will run nomore than 40frps
    # program won't run any times more than the second which has been set inside the clock.tick
    pygame.display.set_caption('EsCaPe HaZaRdS') #setting caption
    game_sprites['numbers']= (
        pygame.image.load('game/sprites/0.png').convert_alpha(),
        pygame.image.load('game/sprites/1.png').convert_alpha(),#convert alpha is used for fast rendering image
        pygame.image.load('game/sprites/2.png').convert_alpha(),#convert alpha is used for fast rendering image
        pygame.image.load('game/sprites/3.png').convert_alpha(),#convert alpha is used for fast rendering image
        pygame.image.load('game/sprites/4.png').convert_alpha(),#convert alpha is used for fast rendering image
        pygame.image.load('game/sprites/5.png').convert_alpha(),#convert alpha is used for fast rendering image
        pygame.image.load('game/sprites/6.png').convert_alpha(),#convert alpha is used for fast rendering image
        pygame.image.load('game/sprites/7.png').convert_alpha(),#convert alpha is used for fast rendering image
        pygame.image.load('game/sprites/8.png').convert_alpha(),#convert alpha is used for fast rendering image
        pygame.image.load('game/sprites/9.png').convert_alpha(),#convert alpha is used for fast rendering image
    ) #numbers is a key. numbers inside the game sprites are gonna be a tuple
    game_sprites['message']=pygame.image.load('game/sprites/message.png').convert_alpha()
    game_sprites['base']=pygame.image.load('game/sprites/base.png').convert_alpha()
    game_sprites['pipe']=(pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180),
    pygame.image.load(pipe).convert_alpha())
    #game_sounds
    game_sounds['die']=pygame.mixer.Sound('game/audio/die.wav')
    game_sounds['hit']=pygame.mixer.Sound('game/audio/die.wav')
    game_sounds['point']=pygame.mixer.Sound('game/audio/point.wav')
    game_sounds['swoosh']=pygame.mixer.Sound('game/audio/swoosh.wav')
    game_sounds['wing']=pygame.mixer.Sound('game/audio/wing.wav')

    game_sprites['background']= pygame.image.load(background).convert() #only convert changes the images only
    game_sprites['player']=pygame.image.load(player).convert_alpha() #alpha cahnges the pixels of image

    while True:

        welcomeScreen() # shows the welcome screen to the user until he presses a button.this function will return whenever user press a button on the keyboard and maingame will start
        mainGame() #this function will return when the game is over



