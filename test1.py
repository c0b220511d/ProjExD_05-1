import pygame
import random
import os
import sys
import time

CARD_WIDTH = 100
CARD_HEIGHT = 140
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50

SUITS = {'Hearts': 'h', 'Diamonds': 'd', 'Clubs': 'c', 'Spades': 's'}
RANKS = {'2': '02', '3': '03', '4': '04', '5': '05', '6': '06', '7': '07', '8': '08', '9': '09', '10': '10', 'Jack': '11', 'Queen': '12', 'King': '13', 'Ace': '01'}

def create_deck():
    return [(rank, suit) for suit in SUITS for rank in RANKS]

def card_value(card):
    rank, _ = card
    return 10 if rank in ['Jack', 'Queen', 'King'] else 11 if rank == 'Ace' else int(rank)

def hand_value(hand):
    value = sum(card_value(card) for card in hand)
    num_aces = sum(rank == 'Ace' for rank, _ in hand)
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def load_card_images():
    card_images = {}
    for suit, suit_short in SUITS.items():
        for rank, rank_short in RANKS.items():
            filename = os.path.join('playingcard-mini', f'{suit_short}{rank_short}@2x.png')
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
            card_images[(rank, suit)] = image

    # 裏向きのカード画像を読み込む
    card_images[('Back', 'Back')] = pygame.image.load('playingcard-mini/back@2x.png')
    card_images[('Back', 'Back')] = pygame.transform.scale(card_images[('Back', 'Back')], (CARD_WIDTH, CARD_HEIGHT))
    
    return card_images

def draw_text(screen, text, size, x, y, font_path=None):
    font = pygame.font.Font(font_path, size) if font_path else pygame.font.Font(None, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(screen, text, x, y, width, height):
    pygame.draw.rect(screen, (0, 0, 0), [x, y, width, height])
    draw_text(screen, text, 30, x + 10, y + 10, 'Meiryo.ttf')  # Meiryo.ttfフォントを使用

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("ブラックジャック")

    card_images = load_card_images()
    deck = create_deck()
    random.shuffle(deck)

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    message = ""
    running = True
    game_over = False
    dealer_reveal = False
    reveal_animation = False
    animation_start_time = 0
    back_card_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if 50 <= mouse_x <= 50 + BUTTON_WIDTH and 600 <= mouse_y <= 600 + BUTTON_HEIGHT:
                        player_hand.append(deck.pop())
                        if hand_value(player_hand) > 21:
                            message = "プレイヤーがバーストしました。"
                            game_over = True
                    elif 250 <= mouse_x <= 250 + BUTTON_WIDTH and 600 <= mouse_y <= 600 + BUTTON_HEIGHT:
                        while hand_value(dealer_hand) < 17:
                            dealer_hand.append(deck.pop())
                            back_card_count += 1
                        game_over = True
                        dealer_reveal = True
                        reveal_animation = True
                        animation_start_time = time.time()

            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if 450 <= mouse_x <= 450 + BUTTON_WIDTH and 600 <= mouse_y <= 600 + BUTTON_HEIGHT:
                        # ゲームを再開
                        deck = create_deck()
                        random.shuffle(deck)
                        player_hand = [deck.pop(), deck.pop()]
                        dealer_hand = [deck.pop(), deck.pop()]
                        message = ""
                        game_over = False
                        dealer_reveal = False
                        reveal_animation = False
                        animation_start_time = 0
                        back_card_count = 0

        screen.fill((0, 128, 0))  # グリーン色の背景

        # プレイヤーの手札を描画
        for i, card in enumerate(player_hand):
            screen.blit(card_images[card], (50 + i * (CARD_WIDTH + 10), 400))

        # ディーラーの手札を描画
        for i, card in enumerate(dealer_hand):
            if i == 0 and not dealer_reveal:
                # 裏向きのカードを描画
                screen.blit(card_images[('Back', 'Back')], (50 + i * (CARD_WIDTH + 10), 50))
            else:
                # 表向きのカードを描画
                screen.blit(card_images[card], (50 + i * (CARD_WIDTH + 10), 50))

        # プレイヤーとディーラーの手札の合計値を描画
        draw_text(screen, f"プレイヤーの手札: {hand_value(player_hand)}", 30, 50, 550, 'Meiryo.ttf')
        if dealer_reveal:
            draw_text(screen, f"ディーラーの手札: {hand_value(dealer_hand)}", 30, 50, 10, 'Meiryo.ttf')

        # ヒットとスタンドのボタンを描画
        if not game_over:
            draw_button(screen, "ヒット", 50, 600, BUTTON_WIDTH, BUTTON_HEIGHT)
            draw_button(screen, "スタンド", 250, 600, BUTTON_WIDTH, BUTTON_HEIGHT)
        else:
            # ゲーム結果メッセージと再プレイボタンを描画
            if reveal_animation:
                if time.time() - animation_start_time > 0.5:
                    back_card_count -= 1
                    animation_start_time = time.time()
                    if back_card_count == 0:
                        reveal_animation = False
                        if hand_value(player_hand) > 21:
                            message = "プレイヤーがバーストしました。ディーラーの勝利！"
                        elif hand_value(dealer_hand) > 21:
                            message = "ディーラーがバーストしました。プレイヤーの勝利！"
                        elif dealer_reveal:
                            if hand_value(player_hand) == hand_value(dealer_hand):
                                message = "引き分けです。"
                            elif hand_value(player_hand) > hand_value(dealer_hand):
                                message = "プレイヤーの勝利！"
                            else:
                                message = "ディーラーの勝利！"
            draw_text(screen, message, 40, 50, 300, 'Meiryo.ttf')
            draw_button(screen, "再プレイ", 450, 600, BUTTON_WIDTH, BUTTON_HEIGHT)

        # 裏向きのカードを描画
        for i in range(back_card_count):
            card_image = card_images[('Back', 'Back')].copy()
            screen.blit(card_image, (50 + i * (CARD_WIDTH + 10), 50))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
