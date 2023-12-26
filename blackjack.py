import os
import sys
import math
import pygame as pg

WIDTH = 1600
HEIGHT = 900
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
ROUND_NOW = 0

class Card:
    card = {
        "h":
            {
                "A": 'h01@2x.png',
                "2": 'h02@2x.png',
                "3": 'h03@2x.png',
                "4": 'h04@2x.png',
                "5": 'h05@2x.png',
                "6": 'h06@2x.png',
                "7": 'h07@2x.png',
                "8": 'h08@2x.png',
                "9": 'h09@2x.png',
                "10": 'h10@2x.png',
                "J": 'h11@2x.png',
                "Q": 'h12@2x.png',
                "K": 'h13@2x.png'
            },
        "s":
            {
                "A": 's01@2x.png',
                "2": 's02@2x.png',
                "3": 's03@2x.png',
                "4": 's04@2x.png',
                "5": 's05@2x.png',
                "6": 's06@2x.png',
                "7": 's07@2x.png',
                "8": 's08@2x.png',
                "9": 's09@2x.png',
                "10": 's10@2x.png',
                "J": 's11@2x.png',
                "Q": 's12@2x.png',
                "K": 's13@2x.png'
            },
        "d":
            {
                "A": 'd01@2x.png',
                "2": 'd02@2x.png',
                "3": 'd03@2x.png',
                "4": 'd04@2x.png',
                "5": 'd05@2x.png',
                "6": 'd06@2x.png',
                "7": 'd07@2x.png',
                "8": 'd08@2x.png',
                "9": 'd09@2x.png',
                "10": 'd10@2x.png',
                "J": 'd11@2x.png',
                "Q": 'd12@2x.png',
                "K": 'd13@2x.png'
            },
        "k":
            {
                "A": 'k01@2x.png',
                "2": 'k02@2x.png',
                "3": 'k03@2x.png',
                "4": 'k04@2x.png',
                "5": 'k05@2x.png',
                "6": 'k06@2x.png',
                "7": 'k07@2x.png',
                "8": 'k08@2x.png',
                "9": 'k09@2x.png',
                "10": 'k10@2x.png',
                "J": 'k11@2x.png',
                "Q": 'k12@2x.png',
                "K": 'k13@2x.png'
            }
        }
    
    def __init__(self, s, r):
        self.r = r
        self.s = s
        self.img = pg.transform.rotozoom(pg.image.load(f'{MAIN_DIR}/playingcard-mini/{__class__.card[s][r]}'), 0, 2.0)
        self.rct = self.img.get_rect()
        self.rct.center = (800, 450)
        
    def update(self, screen: pg.Surface):
        screen.blit(self.img, self.rct)
        

class Round:
    """
    ラウンド数に関するクラス
    """
    def __init__(self, round_max: int):
        """
        ラウンド数を数えたい
        引数 round: ゲームを何回行うか
        """
        self.round_max = round_max

    def update(self, screen:pg.Surface):
        """
        ラウンド数を更新したい
        """
        font = pg.font.SysFont(None, 100)
        text = font.render("round "+str(ROUND_NOW)+"/"+str(self.round_max), True, (0, 255, 255))
        screen.blit(text, [1200, 0])


def main():
    global ROUND_NOW
    pg.display.set_caption('black jack')
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    round = Round(5)
    card = Card("d",'A')
    clock = pg.time.Clock()
    tmr = 0

    while True:
        screen.fill((70, 128, 79))
        key_lst = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
        card.update(screen)
        if ROUND_NOW<5:  # 1ゲーム終わったところに書きたい
            ROUND_NOW += 1
        round.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()