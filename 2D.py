import pygame as pg
import sys

WIDTH = 800  # ゲームウィンドウの幅
HEIGHT = 600  # ゲームウィンドウの高さ

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    bg_img_r = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("ex05/fig/2.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 1.5)
    kk_img_f = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    mv = 0
    tmr = 0
    rev = 0

class Time:
    """
    タイムに関するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.time = 0
        self.image = self.font.render(f"Time: {self.time}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 550, HEIGHT-50

    def score_up(self, add):
        self.time += add

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.time}", 0, self.color)
        screen.blit(self.image, self.rect)


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0
            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                if mv > 0:
                    mv -= 20
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                mv += 20

        if mv==1599:
            mv=0
            if rev==0:
                rev = 1
            elif rev==1:
                rev = 0
        
        kk_lst = []

        key_lst = pg.key.get_pressed()
        for i in mv:
            if key_lst[i]:
                kk_rct.move_ip(i)
                kk_lst.append(i)
        

        if rev==0:
            screen.blit(bg_img, [-mv, 0])
            screen.blit(bg_img_r, [1600-mv, 0])
        elif rev==1:
            screen.blit(bg_img_r, [-mv, 0])
            screen.blit(bg_img, [1600-mv, 0])
        screen.blit(kk_img,[300,380])

        pg.display.update()
        clock.tick(100)
        print(mv)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()