import pygame as pg
import random
#================ball=================
class BallSprite(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/smallball.png')
        self.rect = self.image.get_rect()
        self.rect.center = [640,360] #發球位置 感覺發球要做在迴圈中 按某個鍵後發球 @吳
        self.xStep, self.yStep = (random.choice([12,11,10,9,8,-8,-9,-10,-11,-12]),random.choice([12,11,10,9,8,-8,-9,-10,-11,-12]))
    def update(self):
        # move the ball horizontally
        self.rect.x += self.xStep
        # and vertically
        self.rect.y += self.yStep
        if pg.sprite.spritecollideany(self, horiz_walls):
            self.yStep = -self.yStep
        if pg.sprite.spritecollideany(self, vert_walls):
            self.xStep = -self.xStep
    #偵測碰撞
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)
#分裂球的新Sprite
class New_BallSprite(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/smallball.png')
        self.rect = self.image.get_rect()
        self.rect.center = [ball.rect.x,ball.rect.y]
        self.xStep, self.yStep = (random.randint(-10,10),random.randint(-10,10))
    def update(self):
        self.rect.x += self.xStep
        self.rect.y += self.yStep
        if pg.sprite.spritecollideany(self, horiz_walls):
            self.yStep = -self.yStep
        if pg.sprite.spritecollideany(self, vert_walls):
            self.xStep = -self.xStep
    #偵測碰撞
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)
#===============wall====================
class BlockSprite(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
#===============player==================
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
        self.rect.center = [1040,360]
#==============door====================
class DoorLeft(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/door.png')
        self.rect = self.image.get_rect()
        self.rect.center = [10,360]
class DoorRight(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/door.png')
        self.rect = self.image.get_rect()
        self.rect.center = [1270,360]

   #字     
pg.init()
font = pg.font.SysFont('AppleGothic', 30)
def show_text(x, y, text):
     text = font.render(text, True, (255, 255, 0))
     screen.blit(text, (x, y))

pg.init()
window_size = (1280,720)
screen = pg.display.set_mode(window_size)
screen.fill((0,0,0))
pg.display.set_caption('攻城獅')

     
#球        
ball = BallSprite()

#牆
bg_image = pg.image.load('images/wall.png')
WALL_SIZE = 10
top_line = BlockSprite(0, 0, window_size[0],WALL_SIZE)
bottom_line = BlockSprite(0, window_size[1]-WALL_SIZE,window_size[0], WALL_SIZE)
left_line = BlockSprite(0, 0, WALL_SIZE,window_size[1])
right_line = BlockSprite(window_size[0]-WALL_SIZE, 0,WALL_SIZE, window_size[1])

#門
doorleft = DoorLeft()
doorright = DoorRight()
new_balld = New_BallSprite()
new_ballc = New_BallSprite()
#player
playerleft = PlayerLeft()
playerright = PlayerRight()

#群組
horiz_walls = pg.sprite.Group(top_line, bottom_line)
vert_walls = pg.sprite.Group(left_line, right_line, playerleft, playerright)
balls = pg.sprite.Group(ball)
doors = pg.sprite.Group(doorleft,doorright)
#player = pg.sprite.Group(playerleft, playerleft)
sprites = pg.sprite.OrderedUpdates(horiz_walls,vert_walls, balls, playerleft, playerright, doors)  
done = False
pause = False  
pg.time.set_timer(pg.USEREVENT, 10)
scoreL = 0
scoreR = 0
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

            #讓版子上下動            
            keys=pg.key.get_pressed()
            if keys[pg.K_w] and not pg.sprite.collide_rect(playerleft, top_line):
                playerleft.rect.y -= 10
            if keys[pg.K_s] and not pg.sprite.collide_rect(playerleft, bottom_line):
                playerleft.rect.y += 10
            if keys[pg.K_o] and not pg.sprite.collide_rect(playerright, top_line):
                playerright.rect.y -= 10
            if keys[pg.K_l] and not pg.sprite.collide_rect(playerright, bottom_line):
                playerright.rect.y += 10
            #碰撞球門後刪球
            if ball.is_collided_with(doorleft):
                for b in balls:
                    b.kill()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        ball = BallSprite()
                        balls = pg.sprite.Group(ball)
                        sprites = pg.sprite.OrderedUpdates(horiz_walls,vert_walls, balls, playerleft, playerright, doors)  
            if ball.is_collided_with(doorright):
                for b in balls:
                    b.kill()
                if event.type == pg.KEYDOWN:    
                    if event.key == pg.K_COMMA:
                        ball = BallSprite()
                        balls = pg.sprite.Group(ball)
                        sprites = pg.sprite.OrderedUpdates(horiz_walls,vert_walls, balls, playerleft, playerright, doors)  
            if new_balld.is_collided_with(doorright):
                for b in balls:
                    b.kill()
                if event.type == pg.KEYDOWN:    
                    if event.key == pg.K_COMMA:
                        ball = BallSprite()
                        balls = pg.sprite.Group(ball)
                        sprites = pg.sprite.OrderedUpdates(horiz_walls,vert_walls, balls, playerleft, playerright, doors)  
            if new_balld.is_collided_with(doorleft):
                for b in balls:
                    b.kill()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        ball = BallSprite()
                        balls = pg.sprite.Group(ball)
                        sprites = pg.sprite.OrderedUpdates(horiz_walls,vert_walls, balls, playerleft, playerright, doors)  
            if new_ballc.is_collided_with(doorright):
                for b in balls:
                    b.kill()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_COMMA:
                        ball = BallSprite()
                        balls = pg.sprite.Group(ball)
                        sprites = pg.sprite.OrderedUpdates(horiz_walls,vert_walls, balls, playerleft, playerright, doors)  
            if new_ballc.is_collided_with(doorleft):
                for b in balls:
                    b.kill()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        ball = BallSprite()
                        balls = pg.sprite.Group(ball)
                        sprites = pg.sprite.OrderedUpdates(horiz_walls,vert_walls, balls, playerleft, playerright, doors)  
#update game state
#redraw
    #牆
    screen.blit(bg_image, [0,0])
    #門
    #screen.blit(rightdoor_image,[-10,0])
    #screen.blit(leftdoor_image,[12,0])
    #screen.fill((0,0,0))
    balls.update()
    sprites.draw(screen)
    if ball.is_collided_with(doorleft):
        show_text(530,360,'Right Player Win')
    if ball.is_collided_with(doorright):
        show_text(530,360,'Left Player Win')
    if new_balld.is_collided_with(doorright):
        show_text(530,360,'Left Player Win')
    if new_balld.is_collided_with(doorleft):
        show_text(530,360,'Right Player Win')
    if new_ballc.is_collided_with(doorright):
        show_text(530,360,'Left Player Win')
    if new_ballc.is_collided_with(doorleft):
        show_text(530,360,'Right Player Win')
    pg.display.update()
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pause = False
            if (event.type == pg.KEYUP and event.key == pg.K_h):
                done = True
                pause = False
    

pg.quit()
