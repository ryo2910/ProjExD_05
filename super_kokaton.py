from asyncio import Event
from typing import Any
import pygame as pg
import sys

from pygame.sprite import AbstractGroup

WIDTH = 800
HEIGHT = 600

class Bird(pg.sprite.Sprite):
    """
    ゲームキャラクター(こうかとん)に関するクラス
    """
    def __init__(self,num: int,x: int):
        """
        こうかとん画像Surfaceを生成する
        引数1 num:こうかとん画像ファイル名の番号
        """
        super().__init__()
        self.mode = 0
        self.jump = 0
        self.cnt = 0
        self.img = pg.image.load(f"ex05/fig/{num}.png")
        self.rect = self.img.get_rect()
        self.rect.centerx = x
        self.rect.centery = 450
    def update(self,screen: pg.Surface):
        if self.mode == 0: # こうかとんが右に動いているとき
            screen.blit(self.img,self.rect)
        if self.mode == 1: # こうかとんが左に動いているとき
            screen.blit(pg.transform.flip(self.img,True,False),self.rect)
        if self.jump == 1: # PGUPが押されたとき
            self.rect.centery -= 5
            if self.rect.centery <= 300: # ジャンプの高さ制限
                self.cnt += 1
                self.rect.centery += 5
                if self.cnt >= 20: # 対空時間
                    self.jump = 0
                    self.cnt = 0
        if self.jump == 0 and self.rect.centery < 450:
            self.rect.centery += 5

class Background:
    """
    背景の処理をする
    """
    def __init__(self,screen:pg.Surface):
        self.x=0
        self.bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
        self.bg_img_fl = pg.transform.flip(self.bg_img,True,False)
        screen.blit(self.bg_img_fl,[-800,0])
    def update(self,screen:pg.Surface):
        """
        移動に応じたupdateを行う
        """
        self.x%=3200
        screen.blit(self.bg_img,[800-self.x,0])
        screen.blit(self.bg_img_fl,[2400-self.x,0])
        screen.blit(self.bg_img_fl,[-800-self.x,0])


class Enemy(pg.sprite.Sprite):
    """
    敵に関するクラス
    """
    def __init__(self, screen: pg.Surface, e_x: int, bg: Background):
        """
        引数2 e_x:表示させたいx座標
        """
        super().__init__()
        self.e_x=e_x
        self.ene_img = pg.transform.rotozoom(pg.image.load("ex05/fig/monster11.png"),0,0.2)
        self.rect= self.ene_img.get_rect() # get_rect()でその画像の大きさのrectをとる
        self.rect.centerx = self.e_x - bg.x
        self.rect.centery = 450
        screen.blit(self.ene_img,self.rect)

    def update(self, screen: pg.Surface):
        self.rect.centerx -= 5
        screen.blit(self.ene_img,self.rect)


class Goal(pg.sprite.Sprite):
    """
    ゴールに関するクラス
    """
    def __init__(self, screen: pg.Surface):
        super().__init__()
        self.g_img = pg.transform.rotozoom(pg.image.load("ex05/fig/torinosu_egg.png"),0,0.2)
        self.rect = self.g_img.get_rect()
        self.rect.centerx = 3200
        self.rect.centery = 450
        screen.blit(self.g_img,self.rect)

    def update(self, screen: pg.Surface,bg: Background):
        self.rect.centerx = 3200 - bg.x
        screen.blit(self.g_img,self.rect)

class Coin(pg.sprite.Sprite):
    """
    コインに関するクラス
    """
    def __init__(self, screen: pg.Surface, c_x: int, c_y: int):
        """
        引数1 c_x:コインのx座標
        引数2 x_y:コインのy座標
        """
        super().__init__()
        self.c_x = c_x
        self.c_y = c_y
        self.coin_img = pg.image.load("ex05/fig/food_daizu_meet.png")
        self.rect = self.coin_img.get_rect()
        self.rect.centerx = self.c_x
        self.rect.centery = self.c_y
        screen.blit(self.coin_img, self.rect)
    
    def update(self, screen: pg.Surface):
        screen.blit(self.coin_img, self.rect)

class Time():
    """
    タイムに関するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.time = 0
        self.time_60 = 0
        self.image = self.font.render(f"Time: {self.time}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH - 125, 50 # Time表示位置
        self.time = 60 #時間制限

    def time_up(self, add: int):
        self.time_60 += add 
        if self.time_60 == 60: # カウントが60になったら
            self.time_60 = 0 
            self.time -= 1 

    def update(self, screen: pg.Surface):
        if self.time <= 10:
            self.color = (255, 0, 0)
        self.image = self.font.render(f"Time: {self.time}", 0, self.color)
        screen.blit(self.image, self.rect)

def main():
    pg.display.set_caption("Super_Kokaton")
    screen = pg.display.set_mode((WIDTH,HEIGHT))

    bird = Bird(2,200)
    bg = Background(screen)
    enes = pg.sprite.Group()
    gls = pg.sprite.Group()
    coins = pg.sprite.Group()
    time = Time()
    for i in range(3):
        enes.add(Enemy(screen,i*400+800,bg))
    gl = Goal(screen)
    gls.add(gl)
    for i in range(3):
        coins.add(Coin(screen,i*100,300))

    tmr = 0
    clock = pg.time.Clock()
    
    while True:
        for  event in pg.event.get():
            if event.type == pg.QUIT: return
        if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            bird.mode = 0 # こうかとんが右に動いているmode
            bg.x += 10
        if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
            bird.mode = 1 # こうかとんが左に動いているmode
            bg.x -= 10
        if bg.x <= 0:
            bg.x = 0
        if bird.rect.centerx >= gl.rect.centerx:
            bg.x = 3000
        if bird.rect.centery == 450 and event.type == pg.KEYDOWN and event.key == pg.K_UP:
            bird.jump=1
        if time.time == 0:
            return
        for ene in pg.sprite.spritecollide(bird, enes, True): # こうかとんが敵と当たったら終了する
            return
        for goal in pg.sprite.spritecollide(bird,gls, False): # こうかとんがゴールについたら終了する
            return
        for coin in pg.sprite.spritecollide(bird, coins, True):
            pass
        
        time.time_up(1)
        tmr += 1
        x = tmr%3200

        bg.update(screen)
        bird.update(screen)
        enes.update(screen)
        gls.update(screen,bg)
        time.update(screen)
        coins.update(screen)
        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

