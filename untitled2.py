import pygame as pg
import random
#================ball=================
class BallSprite(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/smallball.png')
        self.rect = self.image.get_rect()
        self.rect.center = [640,360] #發球位置 感覺發球要做在迴圈中 按某個鍵後發球 @吳
        self.xStep, self.yStep = (-1,1) #球開始的方向 要依照上局誰得分來覺得 @丁
    def update(self):
        # move the ball horizontally
        self.rect.x += self.xStep
        # and vertically
        self.rect.y += self.yStep
        if pg.sprite.spritecollideany(self, horiz_walls):
            self.yStep = -self.yStep
        if pg.sprite.spritecollideany(self, vert_walls):
            self.xStep = -self.xStep
#分裂球的新Sprite
class New_BallSprite(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/smallball.png')
        self.rect = self.image.get_rect()
        self.rect.center = [ball.rect.x,ball.rect.y]
        self.xStep, self.yStep = (random.randint(-1,1),random.randint(-1,1))
    def update(self):
        self.rect.x += self.xStep
        self.rect.y += self.yStep
        if pg.sprite.spritecollideany(self, horiz_walls):
            self.yStep = -self.yStep
        if pg.sprite.spritecollideany(self, vert_walls):
            self.xStep = -self.xStep
#===============wall===================
class BlockSprite(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
#===============player===================
class PlayerLeft(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/block.png')
        self.rect = self.image.get_rect()
        self.rect.center = [240,360]
class PlayerRight(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/block.png')
        self.rect = self.image.get_rect()
        self.rect.center = [960,360]

pg.init()
window_size = (1280,720)
screen = pg.display.set_mode(window_size)
screen.fill((0,0,0))
pg.display.set_caption('攻城獅')

     
#球        
ball = BallSprite()

#牆
WALL_SIZE = 10
top_line = BlockSprite(0, 0, window_size[0],WALL_SIZE)
bottom_line = BlockSprite(0, window_size[1]-WALL_SIZE,window_size[0], WALL_SIZE)
left_line = BlockSprite(0, 0, WALL_SIZE,window_size[1])
right_line = BlockSprite(window_size[0]-WALL_SIZE, 0,WALL_SIZE, window_size[1])

#player
playerleft = PlayerLeft()
playerright = PlayerRight()

#群組
horiz_walls = pg.sprite.Group(top_line, bottom_line)
vert_walls = pg.sprite.Group(left_line, right_line)
balls = pg.sprite.Group(ball)
sprites = pg.sprite.OrderedUpdates(horiz_walls,vert_walls, balls, playerleft, playerright)  
done = False
pause = False  
#============主程式===============
while not done:
# read new event
    for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                done = True
            #分裂球 空白鍵
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    new_balld = New_BallSprite()
                    new_balld.rect.center = [600,360]
                    new_balld.xStep,new_balld.yStep = (ball.xStep,-ball.yStep)
                    new_ballc = New_BallSprite()
                    new_ballc.rect.center = [680,360]
                    new_ballc.xStep,new_ballc.yStep = (ball.xStep,ball.yStep)
                    balls = pg.sprite.Group(ball,new_balld,new_ballc)
                    sprites.add(balls)
                #清除球 delete
                if event.key == pg.K_DELETE:
                    for b in balls:
                        b.kill()
            #player移動 但是動不了哭啊
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    playerl = PlayerLeft()
                    y -= 10



#update game state
#redraw
    screen.fill((0,0,0))
    balls.update()
    sprites.draw(screen)
    pg.display.update()

    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pause = False
            if (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                done = True
                pause = False
pg.quit()
