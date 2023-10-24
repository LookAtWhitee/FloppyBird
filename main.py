import pygame
import random
import time 

pygame.init()
background = pygame.image.load('img/background.png')
base = pygame.image.load('img./base.png')
tubedown = pygame.image.load('img/tube.png')
tubeup = pygame.transform.flip(tubedown, False, True)
Bird = pygame.image.load('img/Bird.png')
gameover = pygame.image.load('img/gameover.png')

SCREEN = pygame.display.set_mode((288,512))
velocityGame = 3
FPS = 40
FONT = pygame.font.SysFont('Comic Sans MS', 50, bold = True)


class tube:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75, 150)
        
    def advence_and_draw(self):
        self.x -= velocityGame
        SCREEN.blit(tubedown, (self.x,self.y+210))
        SCREEN.blit(tubeup, (self.x, self.y-210))
        
    def collision(self, Bird, Birdx, Birdy):
        tollerance = 5
        Bird_dx = Birdx + Bird.get_width() - tollerance
        Bird_sx = Birdx + tollerance
        Bird_down = Birdy + tollerance 
        Bird_up = Birdy + Bird.get_height() - tollerance
        tube_dx = self.x 
        tube_sx = self.x + tubedown.get_width()
        tube_up = self.y + 110
        tube_down = self.y + 210
        
        if(Bird_dx > tube_dx and Bird_sx < tube_sx):
            if(Bird_up < tube_up or Bird_down > tube_down):
                u_lose()
        
    def points(self, Bird, Birdx):
        
        Bird_dx = Birdx + Bird.get_width()
        Bird_sx = Birdx
        tube_dx = self.x 
        tube_sx = self.x + tubedown.get_width()
        if(Bird_dx > tube_dx and Bird_sx < tube_sx):
            return True

def refresh():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

def draw():
    SCREEN.blit(background, (0,0))
    for t in tubes:
        t.advence_and_draw()
    SCREEN.blit(Bird, (Birdx,Birdy))
    SCREEN.blit(base, (basex,400))
    points_render = FONT.render(str(points), 1, (255,255,255))
    SCREEN.blit(points_render, (144,0))

def start():
    global Birdx, Birdy, Bird_vely, basex, tubes, points, BetwTubes
    BetwTubes = False
    points = 0
    tubes = []
    tubes.append(tube())
    basex = 0
    Birdx, Birdy = 60, 150
    Bird_vely = 0

def u_lose():
    SCREEN.blit(gameover, (50,180))
    refresh()
    time.sleep(1)
    restart = False
    while not restart:
        for event in pygame.event.get():
            if(event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE)):
                restart = True
                start()
            if(event.type == pygame.QUIT):
                pygame.quit()
        
    



start()
done = False
while not done:
    #Game progression
    Bird_vely += 1
    Birdy += Bird_vely
    basex -= velocityGame
    
    #continue the base
    if basex < -45: basex = 0
    
    #getting tubes
    if tubes[-1].x < 150: 
        tubes.append(tube())
    
    #Collision
    for t in tubes:
        t.collision(Bird, Birdx, Birdy)
    
    #Increment points
    if not BetwTubes:
        for t in tubes:
            if t.points(Bird, Birdx):
                BetwTubes = True
                break
        
    if BetwTubes:
        BetwTubes = False
        for t in tubes:
            if t.points(Bird, Birdx):
                BetwTubes = True
                break
        if not BetwTubes:
            points += 1
         
    #Collision with base 
    if Birdy > 385 or Birdy < 0:
        u_lose()        
    #Key press
    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP)):
            Bird_vely = -10
        if(event.type == pygame.QUIT):
            pygame.quit()
       
    #Refresh Screen
    draw()
    refresh()