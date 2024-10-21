import pygame
pygame.init()
import random
import os
"""Plan: final game will have a snake crawling aroung screen hunting birds
 that fly across the screen. Every time snake eats a bird it grows in
 length.
 Steps:1. snake on the screen. 
    2. snake moves around the screen.
    3. bird flies across screen.
    4. snake eats bird.
    5. generate new bird when bird is eaten.
    6. snake grows with each bird eaten and score goes up by one.
    7. if a bird gets all the way across screen score goes down by one.
    9. record high_score and place at top of screen.
plan: show running score at top of screen."""

clock = pygame.time.Clock()
FPS = 60

#game variables
WIDTH = 800
HEIGHT = 800
cell_size = 20
direction = 1 #1 is up, 2 is right,3 is down, 4 is left
update_snake = 0
score = 0

#define colors
color_inner = (50,125,75)
color_outer = (0,0,0)
red = (255,0,0)
black = (0,0,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Bird eating snake")

#define fonts
font_small = pygame.font.SysFont("Lucida Sans", 40)
font_large = pygame.font.SysFont("lucida Sans",46)

#load high score if it exists else create the file
if os.path.exists("score.txt"):
    with open('score.txt','r') as file:
        high_score = int(file.read())
else:
    high_score = 0

#function to draw text to screen
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

#create snake
snake_pos = [[WIDTH//2,HEIGHT//2 ]]
snake_pos.append([WIDTH//2,HEIGHT//2 + cell_size])
snake_pos.append([WIDTH//2,HEIGHT//2 + cell_size * 2])

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        for frame in range(1,5):
            img = pygame.image.load(f"Bird A/frame-{frame}.png")
            self.img = pygame.transform.scale(img,(80,80))
            self.animation_list.append(self.img)
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.index = 0
        self.counter = 0
        self.new_food = True #True when nuw food can be added
    def update(self):
        #Animate bird
        cooldown = 20
        global score
        global high_score
        
        self.counter += 1
        if self.counter > cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= 4:
                self.index = 0
            self.image = self.animation_list[self.index]

        #check if snake collides with bird
        snake = snake_pos[0]
        #convert head of snake to a rectangle to be used in collide
        snake_rect = pygame.Rect(snake_pos[0][0],snake_pos[0][1],20,20)
        if snake_rect.colliderect(self.rect) and self.new_food == True:
            #create a new piece for the snake at the snake's tails
            new_piece = list(snake_pos[-1])
            if direction == 1:
                new_piece[1] += cell_size
            if direction == 3:
                new_piece[1] -= cell_size
            if direction == 2:
                new_piece[0] -= cell_size
            if direction == 4:
                new_piece[0] += cell_size
            #attach new piece to the end of the snake
            snake_pos.append(new_piece)
            #kill the eaten bird
            score += 1
            self.kill()
            self.new_food = False
        
        #bird moves across screen
        self.rect.x += 1
        if self.rect.left > WIDTH:
            score -= 1
            self.kill() 

        #update high_score
        if score > high_score:
            high_score = score
            with open("score.txt","w") as file:
                file.write(str(high_score))

bird_group = pygame.sprite.Group()
bird = Bird(50,100)
bird_group.add(bird)

run = True
while run:
    clock.tick(FPS)
    screen.fill((255,255,255))

    bird_group.update()
    bird_group.draw(screen)

    draw_text("Score: " + str(score),font_small,black,30,30)
    draw_text("High_score: " + str(high_score),font_large,black,30,50)

    if len(bird_group) <= 1:
        bird = Bird(0,random.randint(10,HEIGHT//2))
        bird_group.add(bird)

    #draw snake
    head = 1
    for x in snake_pos:
        if head == 0:
            pygame.draw.rect(screen,color_outer,(x[0],x[1],cell_size,cell_size))
            pygame.draw.rect(screen,color_inner,(x[0]+1,x[1]+1,cell_size-2,cell_size-2))
        if head == 1:
            pygame.draw.rect(screen,color_outer,(x[0],x[1],cell_size,cell_size))
            pygame.draw.rect(screen,red,(x[0]+1,x[1]+1,cell_size-2,cell_size-2))
            head = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            if event.key == pygame.K_RIGHT and direction != 4:
                direction = 2
            if event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            if event.key == pygame.K_LEFT and direction != 2:
                direction = 4

    #control movement of snake
    update_snake += 1
    if update_snake > 10:
        update_snake = 0
        snake_pos = snake_pos[-1:] + snake_pos[:-1] # ignore head
        #heading up
        #snake_pos[0] is the head segment
        #the x and y coordinates of head are adjusted realtive to the next segmt->[1]
        #thus [0][0]=x coord head, [1][0]=x coord next segment
        if direction == 1: #upward move
            snake_pos[0][0] = snake_pos[1][0] #x coord of head = x of next segment along
            snake_pos[0][1] = snake_pos[1][1] - cell_size#head_y up one cell_size above next segmt
        if direction == 3: #downward move
            snake_pos[0][0] = snake_pos[1][0]#x of head = x of next segment
            snake_pos[0][1] = snake_pos[1][1] + cell_size #y of head = y of next segment + cell_size
        if direction == 2:#move right
            snake_pos[0][1] = snake_pos[1][1]#y of head = y of next segment
            snake_pos[0][0] = snake_pos[1][0] + cell_size #x of head = x of next segment + cell_size
        if direction == 4:#move left
            snake_pos[0][1] = snake_pos[1][1]# y of head = y of next segment 
            snake_pos[0][0] = snake_pos[1][0] - cell_size # x of head = x of next segment - cell_size
    


    pygame.display.update()

    

pygame.quit()

