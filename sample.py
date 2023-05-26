import pygame
import random

# ゲーム画面の幅と高さ
WIDTH = 800
HEIGHT = 600

# 色の定義
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

def main():
    # 初期化
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("マリオブラザーズ風ゲーム")

    clock = pygame.time.Clock()

    # プレイヤーの位置と速度
    player_x = 50
    player_y = HEIGHT - 100
    player_speed_x = 0
    player_speed_y = 0
    player_jump = False

    # 床の位置とサイズ
    floor_x = 0
    floor_y = HEIGHT - 50
    floor_width = WIDTH
    floor_height = 50

    # 敵の位置と速度
    enemy_x = WIDTH
    enemy_y = HEIGHT - 100
    enemy_speed = 5

    # ジャンプの設定
    jump_count = 10
    jump_height = 200

    # プレイヤーが床に接しているかどうかのフラグ
    on_floor = False

    # ゲームループ
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_floor:
                    player_jump = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_speed_x = -5
        elif keys[pygame.K_RIGHT]:
            player_speed_x = 5
        else:
            player_speed_x = 0

        # プレイヤーの移動
        player_x += player_speed_x
        player_y += player_speed_y

        # ジャンプ処理
        if player_jump:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player_speed_y = (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                player_jump = False
                jump_count = 10

        # 重力処理
        if not on_floor:
            player_speed_y += 0.5

        # プレイヤーが床に接しているか判定
        if player_y >= floor_y - 50:
            on_floor = True
            player_y = floor_y - 50
            player_speed_y = 0
        else:
            on_floor = False

        # 敵の移動
        enemy_x -= enemy_speed
        if enemy_x <= -50:
            enemy_x = WIDTH
            enemy_y = HEIGHT - 100

        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (player_x, player_y, 50, 50))
        pygame.draw.rect(screen, BLUE, (floor_x, floor_y, floor_width, floor_height))
        pygame.draw.rect(screen, BLUE, (enemy_x, enemy_y, 50, 50))

        pygame.display.flip
    if __name__ == "__main__":
        main()