# 1. set up a background colour and draw a player character using shapes

import pygame
import random
    
class Player:
    def __init__(self):
        # setting the internal variables at start-up
        self.x = screen_size/2
        self.y = screen_size/2
        # center the player in the middle of the screen
        self.rect = pygame.Rect(self.x-50, self.y-50, 100, 100)
        self.speed = 4 # how many pixels it moves every second - debugging
        self.lives = 3
    def move(self, value):
        self.x += value
    def draw(self, skin = "safe"): # safe by default
        x,y = self.x, self.y
        rects = []
        self.rect = pygame.Rect(self.x,self.y,0,0)
        RED = (200, 72, 72)
        BLUE = (24, 72, 88)
        GOLD = (248, 200, 40)
        WHITE = (255, 255, 255)
        # shows different skins depending on player position
        #
        # pygame.draw function returns a Rect object -
        # each Rect is added to the list of rectangles
        if skin == "safe" or skin == 0:
            rects.append(pygame.draw.rect(screen, GOLD, pygame.Rect(x-20, y-15, 40, 20)))
            rects.append(pygame.draw.rect(screen, BLUE, pygame.Rect(x-30, y-30, 20, 35)))
            rects.append(pygame.draw.rect(screen, RED, pygame.Rect(x-35, y-35, 30, 5)))
            rects.append(pygame.draw.polygon(screen, GOLD, [(x+20, y-15), (x+20, y+5), (x+40, y+5)]))
            rects.append(pygame.draw.circle(screen, RED, [x-25, y+10], 10))
            rects.append(pygame.draw.circle(screen, RED, [x+5, y+10], 5)) 
            rects.append(pygame.draw.circle(screen, RED, [x+20, y+10], 5))
        elif skin == "crashed" or skin == 1:
            # flash red
            rects.append(pygame.draw.rect(screen, RED, pygame.Rect(x-20, y-15, 40, 20)))
            rects.append(pygame.draw.rect(screen, RED, pygame.Rect(x-30, y-30, 20, 35)))
            rects.append(pygame.draw.rect(screen, RED, pygame.Rect(x-35, y-35, 30, 5)))
            rects.append(pygame.draw.polygon(screen, RED, [(x+20, y-15), (x+20, y+5), (x+40, y+5)]))
            rects.append(pygame.draw.circle(screen, RED, [x-25, y+10], 10))
            rects.append(pygame.draw.circle(screen, RED, [x+5, y+10], 5)) 
            rects.append(pygame.draw.circle(screen, RED, [x+20, y+10], 5))
        elif skin == "point" or skin == 2:
            # flash white
            rects.append(pygame.draw.rect(screen, WHITE, pygame.Rect(x-20, y-15, 40, 20)))
            rects.append(pygame.draw.rect(screen, WHITE, pygame.Rect(x-30, y-30, 20, 35)))
            rects.append(pygame.draw.rect(screen, WHITE, pygame.Rect(x-35, y-35, 30, 5)))
            rects.append(pygame.draw.polygon(screen, WHITE, [(x+20, y-15), (x+20, y+5), (x+40, y+5)]))
            rects.append(pygame.draw.circle(screen, WHITE, [x-25, y+10], 10))
            rects.append(pygame.draw.circle(screen, WHITE, [x+5, y+10], 5)) 
            rects.append(pygame.draw.circle(screen, WHITE, [x+20, y+10], 5))
        self.rect = self.rect.unionall(rects) # combines all the Rect objects into one hitbox rectangle
        # pygame.draw.rect(screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), self.rect) # rainbow hitbox!

        
class Enemy:
    def __init__(self):
        self.x = random.randint(-screen_size, screen_size) # Places the enemy randomly along the top of the screen
        self.y = 0#random.randint(-screen_size, screen_size)
        self.surf = pygame.image.load("enemy.png").convert_alpha() # produces a Surface object from an image
        self.rect = self.surf.get_rect(center=(self.x, 0)) # produces a Rect object from the Surface
    def move(self, value):
        self.y += value
    def draw(self):
        screen.blit(self.surf, (self.x, self.y)) # blits to screen
        self.rect = self.surf.get_rect(center=(self.x, self.y)) # produces a Rect object from the Surface at new position

        
class Point:
    def __init__(self):
        self.x = random.randint(-screen_size, screen_size)
        self.y = screen_size#random.randint(-screen_size, screen_size)
        self.surf = pygame.image.load("point.png") # produces a Surface object from an image
        self.rect = self.surf.get_rect(center=(self.x, screen_size)) # produces a Rect object from the Surface
    def draw(self):
        screen.blit(self.surf, (self.x, self.y)) # blits to screen
        self.rect = self.surf.get_rect(center=(self.x, self.y))# produces a Rect object from the Surface at new position
    def move(self, value):
        self.y += value


class Bg:
    def __init__(self):
        self.surf = pygame.image.load("grass.png")
        self.offset = 0
    def draw(self):
        self.offset = (self.offset+1)%1200
        screen.blit(self.surf, (-self.offset, 0))


class Tree:
    def __init__(self):
        self.x = screen_size
        self.y = random.randint(0, screen_size)
        self.surf = pygame.image.load("tree.png")
        self.speed = abs(screen_size/2-self.y)/10
        # ^ the further from the train, the faster it moves.
    def draw(self): # NB: draws and moves in the same function
        # pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.x-10, self.y-10, 20, 20))
        screen.blit(self.surf, (self.x, self.y))
        self.x -= self.speed
        self.x -= count//60
        
########################################################
# main code
pygame.init()  

clock = pygame.time.Clock()

# set the screen dimensions
screen_size = 800#int(input("Enter screen size: "))
screen = pygame.display.set_mode([screen_size, screen_size])
# ^ allows for the screen to be resized while keeping aspect ratio

# Run until the user asks to quit
running = True
game = True
cooldown = 0

# Setup variables
player = Player()
bg = Bg()
enemies = []    # lists for storing
points = []     # instances of points,
trees = []      # enemies, trees
count = 0 # counts how many ticks since the start of game
heart = pygame.image.load("heart.png")
hit = 0 # for flashing on collision

while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if game == True:
        keys = pygame.key.get_pressed() # listen for keypress

        if keys[pygame.K_SPACE]:
            player.move(player.speed)
            # if space pressed move forwards...
        else:
            player.move(-player.speed)
            # ...else move backwards

        bg.draw()
        
        count += 1
        if count % 60 == 0: # called every second or 60 ticks
            points.append(Point())
            trees.append(Tree())
        if count % 10 == 0: # called every sixth of a second or 10 ticks
            enemies.append(Enemy())
        #debugging
        if count % 1200 <= 10:
            screen.fill((0,255,255))

        # detects out of bounds collision
        if player.x < 0:
            player.lives -= 1
            player.move(screen_size/2) # moves back to middle of screen
        if player.x > screen_size:
            player.lives -= 1
            player.move(-screen_size/2) # moves back to middle of screen
            
        # screen.blit(bg, (0,0))
        
        for enemy in enemies:
            enemy.draw()
            enemy.move(5+count//1200)
            # delete the enemy/point once it goes out of bounds
            if enemy.y > screen_size:
                enemies.remove(enemy) 
            if pygame.Rect.colliderect(player.rect, enemy.rect): # detect collision between player and enemies
                enemies.remove(enemy)
                player.lives -= 1
                hit = 15 # flashes red for 1/4 of a second or 15 ticks
        for point in points:
            point.draw()
            point.move(-5-count//1200)
            # delete the enemy/point once it goes out of bounds
            if point.y < 0:
                points.remove(point)
            if pygame.Rect.colliderect(player.rect, point.rect): # detect collision between player and points
                points.remove(point)
                player.lives += 1
                hit = -15 # flashes white for 1/4 of a second or 15 ticks
        for tree in trees:
            tree.draw()
            # deletes the enemy/point once it goes out of bounds
            if tree.x < 0:
                trees.remove(tree)
            
        if hit > 0: 
            player.draw(1) # flash red
            hit -= 1
        elif hit < 0: 
            player.draw(2) # flash white
            hit += 1
        else:
            player.draw() # normal colours

        # blitting life bar
        # creates default 50x50 boxes with 20px margin
        x=20
        for i in range(player.lives):
            screen.blit(heart, (x, screen_size-70))
            x+=70
            
        if player.lives <= 0:
            cooldown = 180
            game= False # uh oh, player died
             
    else: # game = False
        screen.fill((0,0,0))
        keys = pygame.key.get_pressed() # listen for keypress

        if keys[pygame.K_SPACE]:
            if cooldown <= 0:
                player = Player()
                bg = Bg()
                enemies = []    # lists for storing
                points = []     # instances of points,
                trees = []      # enemies, trees
                count = 0 # counts how many ticks since the start of game
                heart = pygame.image.load("heart.png")
                hit = 0 # for flashing on collision
                cooldown = 0
                game = True # will be menu screen
        elif keys[pygame.K_ESCAPE]:
            running = False
        cooldown -= 1
        print(cooldown) # debugging
    # Flip the display
    pygame.display.flip()
    clock.tick(60)
# Done! Time to quit.
pygame.quit()
