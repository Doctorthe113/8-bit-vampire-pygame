from math import ceil, floor
from time import sleep
import pygame

width = 640
height = 480
keepWindow = True

score = 0
gameOver = False

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/music/Stage01.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
gameOverSound = pygame.mixer.Sound("assets/music/VbiteGameOver.mp3")
gameOverSound.set_volume(0.05)
jumpSound = pygame.mixer.Sound("assets/music/jump.mp3")
jumpSound.set_volume(0.3)
scoreSound = pygame.mixer.Sound("assets/music/score-up.mp3")
scoreSound.set_volume(0.3)

pygame.display.set_caption("8Bit vampire hunt")
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font("assets/Minecraft.ttf", 30)


class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = 5
        self.dx = 0
        self.health = 20
        self.direction = 0
        self.playerIdleImage = pygame.image.load("assets/player/idle.png").\
            convert_alpha()
        self.playerRunImage = pygame.image.load("assets/player/run.png").\
            convert_alpha()
        self.playerHitImage = pygame.image.load("assets/player/hit.png").\
            convert_alpha()
        self.Rect = pygame.Rect((self.x - 32), (self.y - 64), 32, 64)
        self.mask = pygame.mask.from_surface(pygame.Surface((32, 64)))
        self.hitRect = None
        self.hitting = False
        self.jumping = False
        self.frame = 0.0
        self.jumpFrame = 0.0
        self.hitFrame = 0.0
        self.runFrame = 0.0

    def update(self):
        # for jumping
        if self.jumping:
            self.dy -= 10
            self.jumpFrame += 1
            if self.jumpFrame == 5:
                self.jumpFrame = 0
                self.jumping = False
        else: 
            self.dy = 10


        # for checking collisions
        collisionTiles = bgWithColisionObj.tileRects
        for tiles in collisionTiles:
            # for checking collision in y direction
            if tiles.colliderect(self.Rect.x, (self.Rect.y + self.dy), 32, 64):
                # for checking jumping collision
                if (self.dy < 0):
                    self.dy = tiles.bottom - self.Rect.top
                # for checking falling collision
                elif (self.dy >= 0):
                    self.dy = tiles.top - self.Rect.bottom

            if tiles.colliderect((self.Rect.x + (self.dx)), self.Rect.y, 32, 64):
                self.dx = 0


        # adds or subtracts x and y coordinates
        self.Rect.y += self.dy


        # TODO: This is a temp workaround untill i figure out a way to refactor
        # todo: it so background image blit is inside its class.
        screen.blit(bgWithColisionObj.BGImage, bgWithColisionObj.Rect)

        # for idle animation
        if (self.dx == 0) and (not self.hitting):
            tempImage = pygame.Surface((16, 32)).convert_alpha()
            tempImage.fill((0, 0, 0, 0))
            tempImage.blit(self.playerIdleImage, (0, 0), ((16 * floor(self.frame)), 0, 16, 32))
            tempImage = pygame.transform.scale(tempImage, (32, 64))

            self.frame += 0.25
            if self.frame == 4:
                self.frame = 0
            
            playerIdleSprite = tempImage

            if (self.direction < 0):
                playerIdleSprite = pygame.transform.flip(tempImage, True, False)
            if (self.direction >= 0):
                playerIdleSprite = tempImage

            self.mask = pygame.mask.from_surface(playerIdleSprite)
            screen.blit(playerIdleSprite, self.Rect)


        # for moving in x direction
        if (abs(self.dx) > 0) and (not self.hitting):
            tempImage = pygame.Surface((16, 32)).convert_alpha()
            tempImage.fill((0, 0, 0, 0))
            tempImage.blit(self.playerRunImage, (0, 0), ((16 * floor(self.runFrame)), 0, 16, 32))
            tempImage = pygame.transform.scale(tempImage, (32, 64))

            self.runFrame += 0.125
            if self.runFrame == 4:
                self.runFrame = 0

            playerRunSprite = tempImage

            if (self.direction < 0):
                playerRunSprite = pygame.transform.flip(tempImage, True, False)
            if (self.direction > 0):
                playerRunSprite = tempImage

            self.mask = pygame.mask.from_surface(playerRunSprite)
            screen.blit(playerRunSprite, self.Rect)


        # for player attacking
        if self.hitting:
            tempImage = pygame.Surface((32, 32)).convert_alpha()
            tempImage.fill((0, 0, 0, 0))
            tempImage.blit(self.playerHitImage, (0, 0), ((32 * floor(self.hitFrame)), 0, 32, 32))
            tempImage = pygame.transform.scale(tempImage, (64, 64))

            self.hitFrame += 0.25
            if self.hitFrame == 2:
                self.hitFrame = 0
                self.hitting = False

            playerHitSprite = tempImage

            if (self.direction < 0):
                playerHitSprite = pygame.transform.flip(tempImage, True, False)
            if (self.direction > 0):
                playerHitSprite = tempImage

            
            self.mask = pygame.mask.from_surface(playerHitSprite)
            self.hitRect = playerHitSprite.get_rect(topleft=((self.Rect.x), (self.Rect.y)))
            screen.blit(playerHitSprite, self.Rect)


        pygame.draw.rect(screen, (255, 255, 255), self.Rect, 2)

    def attacked(self):
        self.health -= 0.0625
        if (self.health == 0):
            gameOverBar = font.render("GAME OVER!", False, "orange")
            screen.blit(gameOverBar, (((width/2) - 110), (height/2)))
            pygame.display.update()
            pygame.mixer.music.pause()
            gameOverSound.play(loops=0)
            pygame.display.update()
            sleep(5)
            pygame.quit()
        pass



class flyingMonster(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.health = 3
        self.Rect = pygame.Rect((self.x - 16), (self.y - 64), 32, 64)
        self.living = True
        self.monsterFrame = 0

    def update(self):
        tempImage = pygame.Surface((16, 32)).convert_alpha()
        flyingMonsterIdle = pygame.image.load("assets/monsters/flying-monster.png").convert_alpha()
        tempImage.fill((0, 0, 0, 0))
        tempImage.blit(flyingMonsterIdle, (0, (16 * floor(self.monsterFrame))), ((16 * floor(self.monsterFrame)), 0, 16, 16))
        tempImage = pygame.transform.scale(tempImage, (32, 64))

        self.monsterFrame += 0.25
        if self.monsterFrame == 2:
            self.monsterFrame = 0

        self.Rect.x -= playerObj.dx
        screen.blit(tempImage, self.Rect)

        # checks if player is colliding with monster or not
        if self.Rect.colliderect(playerObj.Rect):
            playerObj.attacked()
        try:
            # checks if player is colliding with player hit rect
            # and if player is hitting or not
            if self.Rect.colliderect(playerObj.hitRect) and playerObj.hitting:
                self.health -= 1
                playerObj.hitting = False
                if self.health == 0:
                    self.living = False
                    global score
                    score += 1
                    scoreSound.play(loops=0)
                    self.kill()
        except: pass



class sky(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.skyImage = pygame.image.load("assets/background/sky-bg.png").convert_alpha()

    def update(self):
        screen.blit(self.skyImage, (self.x, 0))
        self.x -= 0.5
        if (self.x < -1066):
            self.x = 0



class bgWithColision(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.BGImage = pygame.image.load("assets/background/background.png").convert_alpha()
        self.Rect = self.BGImage.get_rect(topleft=(self.x, self.y))
        self.tileRects = [pygame.Rect(0, 300, 25, 165), pygame.Rect(184, 370, 41, 19), 
                        pygame.Rect(273, 304, 828, 21), pygame.Rect(1036, 0, 45, 226), 
                        pygame.Rect(1079, 164, 39, 17), pygame.Rect(1163, 245, 32, 17),
                        pygame.Rect(1193, 101, 43, 194), pygame.Rect(1236, 268, 301, 27),
                        pygame.Rect(1527, 103, 51, 188), pygame.Rect(1192, 80, 299, 26),
                        pygame.Rect(1521, 80, 62, 84), pygame.Rect(1737, 134, 402, 26),
                        pygame.Rect(1897, 429, 16, 35), pygame.Rect(1913, 400, 296, 65),
                        pygame.Rect(2208, 369, 32, 97), pygame.Rect(2566, 369, 32, 97),
                        pygame.Rect(2598, 400, 296, 65), pygame.Rect(2699, 134, 402, 26),
                        pygame.Rect(3014, 324, 32, 16), pygame.Rect(3193,  280, 32, 16),
                        pygame.Rect(3355, 234, 32, 16), pygame.Rect(3195, 182, 32, 16),
                        pygame.Rect(0, 464, 3414, 16)]

    def update(self):
        for tiles in self.tileRects:
            tiles.x -= playerObj.dx
            pygame.draw.rect(screen, "white", tiles, 2)

        self.Rect.x -= playerObj.dx
        # screen.blit(self.BGImage, self.Rect)




# loads the bgWithCollision object
bgWithColisionObj = bgWithColision()
# loads the sky object
skyObj = sky()
# loads the player
playerObj = player(320, 420)
# loads the monster classes for monsters(group) object
monsters = pygame.sprite.Group()
monster1, monster2 = flyingMonster(64, 455), flyingMonster(128, 455)
monsters.add(monster1, monster2)


# main loop that keeps game running
while keepWindow:
    for event in pygame.event.get():
        # quits the game
        if (event.type == pygame.QUIT):
            keepWindow = False 

        if (event.type == pygame.KEYDOWN):
            # for jumping
            if (event.key == pygame.K_SPACE) and (playerObj.dy == 0):
                playerObj.jumping = True
                jumpSound.play(loops=0)
            # for hitting/attacking
            if (event.key == pygame.K_f):
                playerObj.hitting = True

        # for checking left click
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (event.button == 1):
                playerObj.hitting = True



    # for checking key presses and directions
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        playerObj.direction = 1
        playerObj.dx = 10

    elif (keys[pygame.K_LEFT] or keys[pygame.K_a]):
        playerObj.direction = -1
        playerObj.dx = -10

    else: playerObj.dx = 0



    skyObj.update()
    # TODO: This is a temp workaround untill i figure out a way to refactor
    # todo: it so background image blit is inside its class.
    playerObj.update()
    bgWithColisionObj.update()
    monsters.update()


    # loads the HPbar
    hpBar = font.render(str(ceil(playerObj.health)), False, "red")
    screen.blit(hpBar, (10, 10))
    # loads the timer
    timeBar = font.render(str(floor(pygame.time.get_ticks() / 1000)), False, "white")
    screen.blit(timeBar, (((width/2) - 20), 10))
    # loads the scorebar
    scoreBar = font.render(str(score), False, "white")
    screen.blit(scoreBar, (580, 10))


    # update the display
    pygame.display.update()
    # set the framerate to 30FPS
    pygame.time.Clock().tick(30)

pygame.quit()