import pygame
import random

pygame.init()
pygame.display.set_caption("Ludo")

screen   = pygame.display.set_mode((680, 600))

board    = pygame.image.load('Board.jpg')
one      = pygame.image.load('1.png')
two      = pygame.image.load('2.png')
three    = pygame.image.load('3.png')
four     = pygame.image.load('4.png')
five     = pygame.image.load('5.png')
six      = pygame.image.load('6.png')

DICE     = [one, two, three, four, five, six]

red      = pygame.image.load('red.png')
blue     = pygame.image.load('blue.png')
green    = pygame.image.load('green.png')
yellow   = pygame.image.load('yellow.png')

color    = [red, green, yellow, blue]
number   = 1
currentPlayer = 0
playerKilled = False
diceRolled = False

HOME     = [[(110, 58),  (61, 107),  (152, 107), (110, 152)],   # Red
            [(466, 58),  (418, 107), (509, 107), (466, 153)],  # Green
            [(466, 415), (418, 464), (509, 464), (466, 510)],  # Yellow
            [(110, 415), (61, 464),  (152, 464), (110, 510)]]  # Blue

SAFE     = [(50, 240), (328, 50), (520, 328), (240, 520)]

position = [[[110, 58],  [61, 107],  [152, 107], [110, 152]],   # Red
            [[466, 58],  [418, 107], [509, 107], [466, 153]],  # Green
            [[466, 415], [418, 464], [509, 464], [466, 510]],  # Yellow
            [[110, 415], [61, 464],  [152, 464], [110, 510]]]  # Blue

jump     = {(202, 240): (240, 202),
            (328, 202): (368, 240),
            (368, 328): (328, 368),
            (240, 368): (202, 328)}

WINNER =[[240,284],
         [284,240],
         [330,284],
         [284,330]]

def to_home(x,y):
    #  R2
    if (position[x][y][1] == 284 and position[x][y][0] <= 202 and x==0) \
        and (position[x][y][0] + 38*number > WINNER[x][0]) :
            return False        
           
    #  Y2
    elif  (position[x][y][1] == 284 and 368 < position[x][y][0] and x==2) \
        and (position[x][y][0] - 38*number < WINNER[x][0]) :
            return False           
    #  G2
    elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x==1) \
        and (position[x][y][1] + 38*number > WINNER[x][1]) :
            return False
    #  B2
    elif  (position[x][y][0] == 284 and position[x][y][1] >= 368 and x==3) \
        and (position[x][y][1] - 38*number < WINNER[x][1]) :
            return False
    return True


def move_token(x, y):
    global currentPlayer,diceRolled
    if tuple(position[x][y]) in HOME[currentPlayer] and number == 6:
            position[x][y] = list(SAFE[currentPlayer])
            diceRolled=False



    elif tuple(position[x][y]) not in HOME[currentPlayer]:
        diceRolled=False
        if not number==6 :
            currentPlayer=(currentPlayer+1)%4

        #  R2
        if (position[x][y][1] == 284 and position[x][y][0] <= 202 and x==0) \
          and (position[x][y][0] + 38*number <= WINNER[x][0]) :
            position[x][y][0] += 38*number
           
        #  Y2
        elif  (position[x][y][1] == 284 and 368 < position[x][y][0] and x==2) \
            and (position[x][y][0] - 38*number >= WINNER[x][0]) :
            position[x][y][0] -= 38*number
              
        #  G2
        elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x==1) \
            and (position[x][y][1] + 38*number <= WINNER[x][1]) :
            position[x][y][1] += 38*number
        #  B2
        elif  (position[x][y][0] == 284 and position[x][y][1] >= 368 and x==3) \
            and (position[x][y][1] - 38*number >= WINNER[x][1]) :
            position[x][y][1] -= 38*number

        else:
            for _ in range(number):

                #  R1,Y3
                if (position[x][y][1] == 240 and position[x][y][0] < 202) \
                    or (position[x][y][1] == 240 and 368<=position[x][y][0] < 558):
                    position[x][y][0] += 38
                # R3->R2->R1
                elif (position[x][y][0] == 12 and position[x][y][1] > 240):
                    position[x][y][1] -= 44

                #  R3,Y1
                elif (position[x][y][1] == 328 and 12 < position[x][y][0] <= 202) \
                    or (position[x][y][1] == 328 and 368 < position[x][y][0]):
                    position[x][y][0] -= 38
                #  Y3->Y2->Y1
                elif (position[x][y][0] == 558 and position[x][y][1] <328):
                    position[x][y][1] += 44

                #  G3, B1
                elif (position[x][y][0] == 240 and 12 < position[x][y][1] <= 202) \
                    or (position[x][y][0] == 240 and 368 < position[x][y][1]):
                    position[x][y][1] -= 38
                # G3->G2->G1
                elif (position[x][y][1] == 12 and  240 <= position[x][y][0] < 328):
                    position[x][y][0] += 44

                #  B3, G1
                elif (position[x][y][0] == 328 and position[x][y][1] < 202) \
                    or (position[x][y][0] == 328 and 368 <= position[x][y][1] < 558):
                    position[x][y][1] += 38
                #  B3->B2->B1
                elif (position[x][y][1] == 558 and position[x][y][0] > 240):
                    position[x][y][0] -= 44
                
                else:
                    for i in jump:
                        if position[x][y] == list(i):
                            position[x][y] = list(jump[i])
                            break

        if tuple(position[x][y]) not in SAFE:
            for i in range(len(position)):
                for j in range(len(position[i])):
                    if position[i][j] == position[x][y] and i != x:
                        position[i][j] = list(HOME[i][j])
                        playerKilled = True
                        currentPlayer=(currentPlayer+3)%4


running = True
while(running):
    screen.fill((255, 255, 255))
    screen.blit(board, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            coordinate = pygame.mouse.get_pos()
            if not diceRolled and (605 <= coordinate[0] <= 669) and (270 <= coordinate[1] <= 334) :
                number = random.randint(1, 6)
                flag=True
                for i in range(len(position[currentPlayer])):
                    if tuple(position[currentPlayer][i]) not in HOME[currentPlayer] and to_home(currentPlayer,i): # i not in WINNER:
                        flag=False
                if (flag and number==6 ) or not flag:
                    diceRolled=True

                else:
                    currentPlayer=(currentPlayer+1)%4
            

            elif diceRolled:
                for j in range(len(position[currentPlayer])):
                    if position[currentPlayer][j][0] <= coordinate[0] <= position[currentPlayer][j][0]+31 \
                      and position[currentPlayer][j][1] <= coordinate[1] <= position[currentPlayer][j][1]+31:
                        move_token(currentPlayer, j)
                        break
                       

    screen.blit(DICE[number-1], (605, 270))

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(color[i], j)

    screen.blit(color[currentPlayer], (600, 8))
    

    pygame.display.update()
