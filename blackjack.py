import os
import sys
import math
import random
import pygame as pg
from pygame.sprite import AbstractGroup
import time
import random

WIDTH = 1600
HEIGHT = 900
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
ROUND_NOW = 0  # 今何ラウンド目か

class Card(pg.sprite.Sprite):
    '''
    カードに関するクラス
    '''
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
            },
        None:
            {
                None: "back@2x.png"
            }
        }
    suits = ['h', 's', 'd', 'k']

    ranks = ["A","2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    used_card = {}
    def __init__(self, s: str, r: str):
        '''
        カード画像のSurfaceを生成する
        引数1 s: カードの絵柄
        引数2 r: カードの数字
        '''
        self.r = r
        self.s = s
    
    def number(self) -> int:
        '''
        カードの数字を返す関数
        戻り値 num: カードの数字
        '''
        if self.r == 'J' or self.r == 'Q' or self.r == 'K':
            num = 10
        elif self.r == 'A':
            num = 1
        else:
            num = int(self.r)
        return num
    
    def __str__(self):
        return self.s


class Deck():
    '''
    カードをシャッフルし、山札とするクラス
    このクラスを利用することで重複をなくす
    '''
    def __init__(self):
        self.cards = []
        for i in Card.suits:
            for j in Card.ranks:
                self.cards.append(Card(i, j))
        random.shuffle(self.cards)

    def draw(self) -> Card:
        '''
        シャッフルされたカードのリストから要素を取り出す関数
        戻り値: Cardクラスのインスタンス
        '''
        if len(self.cards) == 0:
            return
        return self.cards.pop()


class Image(pg.sprite.Sprite):
    '''
    カードのSurfaceを作成するクラス
    '''
    def __init__(self, s: str, r: int, xy: tuple[int, int]):
        '''
        引数1: カードの絵柄
        引数2: カードの数字
        '''
        super().__init__()
        self.s = s
        self.r = r
        self.image = pg.transform.rotozoom(pg.image.load(f'{MAIN_DIR}/playingcard-mini/{Card.card[s][r]}'), 0, 1.5)
        self.rect = self.image.get_rect()
        self.rect.center = xy


class Player():
    '''
    プレイヤーのトータルを保存し、バースト判定を行うクラス
    '''
    def __init__(self):
        self.total = 0
        self.ofer = False
        
    def match(self):
        '''
        トータルからバーストしていないか確認する関数
        '''
        if self.total == 21:
            return True
        
        elif self.total > 21:
            return True
        
        else:
            return False

class Deck():
    '''
    カードをシャッフルし、山札とするクラス
    このクラスを利用することで重複をなくす
    '''
    def __init__(self):
        self.cards = []
        for i in Card.suits:
            for j in Card.ranks:
                self.cards.append(Card(i, j))
        random.shuffle(self.cards)

    def draw(self) -> Card:
        '''
        シャッフルされたカードのリストから要素を取り出す関数
        戻り値: Cardクラスのインスタンス
        '''
        if len(self.cards) == 0:
            return
        return self.cards.pop()


class Chip:
    """
    チップに関するクラス
    """
    def __init__(self, c: int):
        self.value = c      # 手持ちのチップの数
        self.bet = 0        # ベットするチップの数
        self.now_bet = 0    # ベットされたチップの数
        self.bet_flag = 0   # ベットしたかどうか
        self.font = pg.font.Font(None, 100)
        self.color = (128, 0, 0)
        self.image_v = self.font.render(f"Chip: {self.value}", 0, self.color)
        self.rect_v = self.image_v.get_rect()
        self.rect_v.center = 180, HEIGHT-50
        self.image_b = self.font.render(f"Bet?: {self.bet}", 0, self.color)
        self.rect_b = self.image_b.get_rect()
        self.rect_b.center = 130, 50
        self.image_nb = self.font.render(f"Bet: {self.now_bet}", 0, self.color)
        self.rect_nb = self.image_nb.get_rect()
        self.rect_nb.center = 110, 50

    def update(self, screen: pg.Surface):
        self.image_v = self.font.render(f"Chip: {self.value}", 0, self.color)
        screen.blit(self.image_v, self.rect_v)

        if self.bet_flag == 0:
            self.image_b = self.font.render(f"Bet?: {self.bet}", 0, self.color)
            screen.blit(self.image_b, self.rect_b)
            
                
        else:
            self.image_nb = self.font.render(f"Bet: {self.now_bet}", 0, self.color)
            screen.blit(self.image_nb, self.rect_nb)


class Player():
    '''
    プレイヤーのトータルを保存し、バースト判定を行うクラス
    '''
    def __init__(self):
        self.total = 0
        self.ofer = False
        
    def match(self):
        '''
        トータルからバーストしていないか確認する関数
        '''
        if self.total == 21:
            return True
        
        elif self.total < 21:
            return True
          
        else:
            return False
    

class Hit(pg.sprite.Sprite):
    """
    ヒットに関するクラス
    """
    def __init__(self, card: Card, hit_num):
        """
        新たにトランプを一枚引く
        引数1 card：持ち札のカード
        引数2 hit_num：ヒットした回数
        """
        super().__init__()
        gara = ["h", "s", "d", "k"]
        num = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        # self.img = pg.transform.rotozoom(pg.image.load(f'{MAIN_DIR}/playingcard-mini/{Card.card[random.choice(gara)][random.choice(num)]}'), 0, 1.5)
        self.img = deck.draw()
        self.rct = self.img.get_rect()
        self.rct.centerx = 850 + 100*hit_num
        self.rct.centery = 900-225

    def update(self, screen: pg.Surface):
        screen.blit(self.img, self.rct)


class Stand(pg.sprite.Sprite):
    """
    スタンドに関するクラス
    """
    def __init__(self, life: int):
        # スタンドと表示する
        super().__init__()
        self.font = pg.font.Font(None, 50)
        self.color = (255, 0, 0)
        self.image = self.font.render(f"Stand", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH/2, HEIGHT/2
        self.life = life

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Stand", 0, self.color)
        screen.blit(self.image, self.rect)
        self.life -= 1
        if self.life < 0:
            self.kill()


class Round:
    """
    ラウンド数に関するクラス
    """
    def __init__(self, round_max: int):
        """
        ラウンド数を数えたい
        引数 round_max: ゲームを何回行うか
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
    chip = Chip(200)
    screen.fill((70, 128, 79))
    pg.mouse.set_visible(True)  # マウスカーソル表示

    
    player_cards = pg.sprite.Group()  # プレイヤーのカードを保存するスプリットグループ
    dealer_cards = pg.sprite.Group()  # ディーラーのカードを保存するスプリットグループ
    #buttons = pg.sprite.Group()
    hit = pg.sprite.Group()
    stand = pg.sprite.Group()
    
    p = Player()
    d = Player()
    
    deck = Deck()
    p1 = deck.draw() 
    p2 = deck.draw()
    d1 = deck.draw()
    d2 = deck.draw()
    
    p.total += int(p1) + int(p2)
    d.total += int(d1) + int(d2)
    

    print(p.total)
    
    round_max = 1  # 何ラウンドゲームを行うか
    round_flag = 1  # ラウンド数設定画面か否か
    card = Card("d",'A')
    clock = pg.time.Clock()
    
    hit_num = 0  # プレイヤーがそのラウンドでヒットした回数

    while round_flag:  # ラウンド数設定
        screen.fill((70, 128, 79))
        key_lst = pg.key.get_pressed()
        
        font = pg.font.SysFont(None, 50)
        text1 = font.render("Set the number of rounds using the arrow keys.", True, (0, 255, 255))
        text2 = font.render("Confirm with enter key.", True, (0, 255, 255))
        screen.blit(text1, [0, 0])
        screen.blit(text2, [0, 50])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:  # 上キーで増やす
                round_max += 1
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:  # 下キーで減らす
                if round_max > 1:
                    round_max -= 1
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:  # リターンキーで決定
                round_flag = 0
        round = Round(round_max)
        round.update(screen)
        pg.display.update()

    while True:
        screen.fill((70, 128, 79))
        key_lst = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
            # h押下でヒット
            if event.type == pg.KEYDOWN and event.key == pg.K_h:
                hit_num += 1
                p3 = deck.draw()
                p.total += int(p3)
                player_cards.add(Image(str(p3), p3.r, (850+hit_num*100, 900-225)))
                print(p.total)
                if p.match() == False:
                    pg.display.update()
                    time.sleep(2)
                    return
            
            # s押下でスタンド
            if event.type == pg.KEYDOWN and event.key == pg.K_s:
                hit_num = 0  # ヒット回数のリセット
                stand.add(Stand(60))
            
            if chip.bet_flag == 0:
                if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    if chip.bet < chip.value :
                        chip.bet += 1
                if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    if chip.bet > 0:
                        chip.bet -= 1
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    chip.bet_flag = 1
                    chip.now_bet = chip.bet
                    chip.value -= chip.bet
                    chip.bet = 0
            
        card.update(screen)
        chip.update(screen)
        pg.display.update()
        hit.update(screen)
        stand.update(screen)
        tmr += 1
        clock.tick(50)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
