import pygame
import random

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TOTAL_WIDTH = WINDOW_WIDTH * 2 + 50

ai_punishment_count = 0
base_fall_interval = 1000
ai_fall_multiplier = 0.5
pygame.mixer.init()
pygame.mixer.music.load('盖世英雄0.3.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


# 方块大小和颜色
BLOCK_SIZE = 30
COLORS = [
    (0, 0, 0),  # 黑色
    (255, 0, 0),  # 红色
    (0, 255, 0),  # 绿色
    (0, 0, 255),  # 蓝色
    (255, 255, 0),  # 黄色
    (255, 165, 0),  # 橙色
    (0, 255, 255),  # 青色
    (128, 0, 128),  # 紫色
]

window = pygame.display.set_mode((TOTAL_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("TETRIS - Player vs AI")


player_game_area = [[0] * (WINDOW_WIDTH // BLOCK_SIZE) for _ in range(WINDOW_HEIGHT // BLOCK_SIZE)]
ai_game_area = [[0] * (WINDOW_WIDTH // BLOCK_SIZE) for _ in range(WINDOW_HEIGHT // BLOCK_SIZE)]

# 定义各种形状的俄罗斯方块
tetriminos = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# 初始化玩家方块
current_tetrimino = random.choice(tetriminos)
current_color = random.choice(COLORS[1:])  # 不包含白色
current_x = (WINDOW_WIDTH // BLOCK_SIZE) // 2 - len(current_tetrimino[0]) // 2
current_y = 0

#init for Ai
ai_tetrimino = current_tetrimino.copy()
ai_color = current_color
ai_x = current_x
ai_y = current_y

"""
def draw_start_screen():
    window.fill((0, 0, 0))
    font_big = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 50)

    # 标题
    title = font_big.render('TETRIS', True, (255, 255, 255))
    title_rect = title.get_rect(center=(TOTAL_WIDTH // 2, WINDOW_HEIGHT // 3))
    window.blit(title, title_rect)

    # 开始提示
    start_text = font_small.render('Press SPACE to Start', True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(TOTAL_WIDTH // 2, WINDOW_HEIGHT * 2 // 3))
    window.blit(start_text, start_rect)

    pygame.display.update()

"""

def draw_game_areas():
    # 绘制玩家区域
    for y in range(WINDOW_HEIGHT // BLOCK_SIZE):
        for x in range(WINDOW_WIDTH // BLOCK_SIZE):
            if player_game_area[y][x] != 0:
                pygame.draw.rect(window, COLORS[player_game_area[y][x]],
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(window, (0, 0, 0),
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 1)




    offset_x = WINDOW_WIDTH + 50
    for y in range(WINDOW_HEIGHT // BLOCK_SIZE):
        for x in range(WINDOW_WIDTH // BLOCK_SIZE):
            if ai_game_area[y][x] != 0:
                pygame.draw.rect(window, COLORS[ai_game_area[y][x]],
                                 (offset_x + x * BLOCK_SIZE, y * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(window, (0, 0, 0),
                                 (offset_x + x * BLOCK_SIZE, y * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 1)


# 检查碰撞
def check_collision():
    for y in range(len(current_tetrimino)):
        for x in range(len(current_tetrimino[0])):
            if current_tetrimino[y][x] == 1:
                if (current_y + y >= WINDOW_HEIGHT // BLOCK_SIZE or
                        current_x + x < 0 or
                        current_x + x >= WINDOW_WIDTH // BLOCK_SIZE or
                        (player_game_area[current_y + y][current_x + x] != 0 and
                         COLORS[player_game_area[current_y + y][current_x + x]] != (255, 255, 255))):
                    return True
    return False



def check_collision_ai():
    for y in range(len(ai_tetrimino)):
        for x in range(len(ai_tetrimino[0])):
            if ai_tetrimino[y][x] == 1:
                if (ai_y + y >= WINDOW_HEIGHT // BLOCK_SIZE or
                        ai_x + x < 0 or
                        ai_x + x >= WINDOW_WIDTH // BLOCK_SIZE or
                        (ai_game_area[ai_y + y][ai_x + x] != 0 and
                         COLORS[ai_game_area[ai_y + y][ai_x + x]] != (255, 255, 255))):
                    return True
    return False


# 放置方块
def place_tetrimino():
    for y in range(len(current_tetrimino)):
        for x in range(len(current_tetrimino[0])):
            if current_tetrimino[y][x] == 1:
                player_game_area[current_y + y][current_x + x] = COLORS.index(current_color)




def place_tetrimino_ai():
    for y in range(len(ai_tetrimino)):
        for x in range(len(ai_tetrimino[0])):
            if ai_tetrimino[y][x] == 1:
                ai_game_area[ai_y + y][ai_x + x] = COLORS.index(ai_color)


# 消除行
def clear_lines():
    lines_cleared = 0
    y = WINDOW_HEIGHT // BLOCK_SIZE - 1
    while y >= 0:
        if all(player_game_area[y][x] != 0 and COLORS[player_game_area[y][x]] != (255, 255, 255)
               for x in range(WINDOW_WIDTH // BLOCK_SIZE)):
            del player_game_area[y]
            player_game_area.insert(0, [0] * (WINDOW_WIDTH // BLOCK_SIZE))
            lines_cleared += 1
        else:
            y -= 1
    return lines_cleared





def clear_lines_ai():
    lines_cleared = 0
    y = WINDOW_HEIGHT // BLOCK_SIZE - 1
    while y >= 0:
        if all(ai_game_area[y][x] != 0 and COLORS[ai_game_area[y][x]] != (255, 255, 255)
               for x in range(WINDOW_WIDTH // BLOCK_SIZE)):
            del ai_game_area[y]
            ai_game_area.insert(0, [0] * (WINDOW_WIDTH // BLOCK_SIZE))
            lines_cleared += 1
        else:
            y -= 1
    return lines_cleared


# AI evaluation function
def evaluate_position(test_tetrimino, test_x, test_y, test_game_area):
    score = 0


    temp_game_area = [row[:] for row in test_game_area]
    for y in range(len(test_tetrimino)):
        for x in range(len(test_tetrimino[0])):
            if test_tetrimino[y][x] == 1:
                temp_game_area[test_y + y][test_x + x] = 1

#消一行100！
    lines_to_clear = 0
    for y in range(WINDOW_HEIGHT // BLOCK_SIZE):
        if all(temp_game_area[y][x] != 0 for x in range(WINDOW_WIDTH // BLOCK_SIZE)):
            lines_to_clear += 1
    score += lines_to_clear * 100

    # 2. 高度惩罚
    heights = []
    for x in range(WINDOW_WIDTH // BLOCK_SIZE):
        for y in range(WINDOW_HEIGHT // BLOCK_SIZE):
            if temp_game_area[y][x] != 0:
                heights.append(WINDOW_HEIGHT // BLOCK_SIZE - y)
                break
    if heights:
        score -= max(heights) * 2

    # 3. 空洞惩罚
    holes = 0
    for x in range(WINDOW_WIDTH // BLOCK_SIZE):
        found_block = False
        for y in range(WINDOW_HEIGHT // BLOCK_SIZE):
            if temp_game_area[y][x] != 0:
                found_block = True
            elif found_block and temp_game_area[y][x] == 0:
                holes += 1
    score -= holes * 4

    return score


# AI寻找最佳移动
def find_best_move():
    best_score = float('-inf')
    best_x = ai_x
    best_rotation = ai_tetrimino

    # 尝试所有可能的旋转
    test_tetrimino = [row[:] for row in ai_tetrimino]
    for _ in range(4):  # 最多旋转4次
        # 尝试所有可能的x位置
        for test_x in range(WINDOW_WIDTH // BLOCK_SIZE - len(test_tetrimino[0]) + 1):
            # 找到最低的可能位置
            test_y = 0
            while test_y < WINDOW_HEIGHT // BLOCK_SIZE - len(test_tetrimino):
                test_y += 1
                if test_y + len(test_tetrimino) > WINDOW_HEIGHT // BLOCK_SIZE or any(
                        test_tetrimino[y][x] == 1 and ai_game_area[test_y + y][test_x + x] != 0
                        for y in range(len(test_tetrimino))
                        for x in range(len(test_tetrimino[0]))
                ):
                    test_y -= 1
                    break


            score = evaluate_position(test_tetrimino, test_x, test_y, ai_game_area)
            if score > best_score:
                best_score = score
                best_x = test_x
                best_rotation = [row[:] for row in test_tetrimino]

        # 旋转方块进行下一次测试
        rotated = [[test_tetrimino[j][i] for j in range(len(test_tetrimino) - 1, -1, -1)]
                   for i in range(len(test_tetrimino[0]))]
        test_tetrimino = rotated

    return best_x, best_rotation


def reset_game():
    global current_tetrimino, current_color, current_x, current_y
    global ai_tetrimino, ai_color, ai_x, ai_y
    global player_game_area, ai_game_area
    global player_score, ai_score
    global fall_interval, fall_timer
    global ai_punishment_count, base_fall_interval

    pygame.mixer.music.rewind()
    pygame.mixer.music.play(-1)
    player_game_area = [[0] * (WINDOW_WIDTH // BLOCK_SIZE) for _ in range(WINDOW_HEIGHT // BLOCK_SIZE)]


    ai_game_area = [[0] * (WINDOW_WIDTH // BLOCK_SIZE) for _ in range(WINDOW_HEIGHT // BLOCK_SIZE)]

    current_tetrimino = random.choice(tetriminos)
    current_color = random.choice(COLORS[1:])
    current_x = (WINDOW_WIDTH // BLOCK_SIZE) // 2 - len(current_tetrimino[0]) // 2
    current_y = 0

    ai_tetrimino = [row[:] for row in current_tetrimino]
    ai_color = current_color
    ai_x = current_x
    ai_y = 0




    player_score = 0
    ai_score = 0
    ai_punishment_count = 0
    base_fall_interval = 1000
    fall_timer = pygame.time.get_ticks()


def draw_game_over_screen(player_score, ai_score):
    overlay = pygame.Surface((TOTAL_WIDTH, WINDOW_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    window.blit(overlay, (0, 0))

    title_font = pygame.font.Font(None, 64)
    score_font = pygame.font.Font(None, 48)
    message_font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 36)

    # 绘制Game Over文字
    game_over_text = title_font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(TOTAL_WIDTH // 2, WINDOW_HEIGHT // 4))
    window.blit(game_over_text, game_over_rect)

    # 绘制分数
    player_score_text = score_font.render(f"Player Score: {player_score}", True, (255, 255, 255))
    punishment_text = score_font.render(f"AI Punishment Count: {ai_punishment_count}", True, (255, 255, 255))

    player_score_rect = player_score_text.get_rect(center=(TOTAL_WIDTH // 2, WINDOW_HEIGHT // 4 + 80))
    ai_score_rect = ai_score_text.get_rect(center=(TOTAL_WIDTH // 2, WINDOW_HEIGHT // 4 + 130))
    punishment_rect = punishment_text.get_rect(center=(TOTAL_WIDTH // 2, WINDOW_HEIGHT // 4 + 180))

    window.blit(player_score_text, player_score_rect)
    window.blit(ai_score_text, ai_score_rect)
    window.blit(punishment_text, punishment_rect)

    # 根据punishment_count显示不同的消息
    if ai_punishment_count == 0:
        message_text = message_font.render("Sometimes AI are dumber than us, it's true", True, (255, 200, 200))
    else:
        message_text = message_font.render("Maybe trying copy AI's move next time!", True, (255, 200, 200))
    message_rect = message_text.get_rect(center=(TOTAL_WIDTH // 2, WINDOW_HEIGHT // 4 + 230))
    window.blit(message_text, message_rect)

    button_width = 200

    button_height = 50

    button_margin = 20

    play_again_button = pygame.Rect(
        TOTAL_WIDTH // 2 - button_width - button_margin,
        WINDOW_HEIGHT * 3 // 4,
        button_width,
        button_height
    )
    pygame.draw.rect(window, (0, 255, 0), play_again_button)
    play_text = button_font.render("Play Again", True, (0, 0, 0))
    play_text_rect = play_text.get_rect(center=play_again_button.center)
    window.blit(play_text, play_text_rect)


    quit_button = pygame.Rect(
        TOTAL_WIDTH // 2 + button_margin,
        WINDOW_HEIGHT * 3 // 4,
        button_width,
        button_height
    )
    pygame.draw.rect(window, (255, 0, 0), quit_button)
    quit_text = button_font.render("Quit", True, (0, 0, 0))
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    window.blit(quit_text, quit_text_rect)

    return play_again_button, quit_button





running = True
game_active = True
clock = pygame.time.Clock()
fall_timer = 0
base_fall_interval = 1000
fall_interval = base_fall_interval
player_score = 0
ai_score = 0
ai_punishment_count = 0



ai_waiting = False
last_ai_position = None
while running:
    if game_active:
        window.fill((0, 0, 0))
        pygame.draw.line(window, (255, 255, 255),
                         (WINDOW_WIDTH + 25, 0),
                         (WINDOW_WIDTH + 25, WINDOW_HEIGHT))

        draw_game_areas()

        current_time = pygame.time.get_ticks()

        # AI方块下落逻辑（更快的下落速度）
        if current_time - fall_timer >= fall_interval * ai_fall_multiplier and not ai_waiting:
            ai_y += 1
            if check_collision_ai():
                ai_y -= 1
                # 记录AI的最终位置
                last_ai_position = (ai_x, ai_tetrimino)
                ai_waiting = True  # AI等待玩家

        # 玩家方块下落逻辑
        if current_time - fall_timer >= fall_interval:
            fall_timer = current_time
            current_y += 1
            if check_collision():
                current_y -= 1

                # 检查玩家是否按照AI的方式放置方块
                if last_ai_position:
                    if (current_x != last_ai_position[0] or
                            current_tetrimino != last_ai_position[1]):
                        ai_punishment_count += 1
                        # 增加下落速度
                        base_fall_interval = max(base_fall_interval - 20, 200)
                        fall_interval = base_fall_interval

                        # 完全同步AI的位置到玩家的位置
                        ai_x = current_x
                        ai_y = current_y
                        ai_tetrimino = [row[:] for row in current_tetrimino]

                # 放置方块并处理消行
                place_tetrimino()
                lines_cleared = clear_lines()
                player_score += lines_cleared

                # AI放置方块并重置
                if ai_waiting:
                    place_tetrimino_ai()
                    lines_cleared = clear_lines_ai()
                    ai_score += lines_cleared

                    # 重置双方的方块
                    current_tetrimino = random.choice(tetriminos)
                    current_color = random.choice(COLORS[1:])
                    current_x = (WINDOW_WIDTH // BLOCK_SIZE) // 2 - len(current_tetrimino[0]) // 2
                    current_y = 0

                    ai_tetrimino = [row[:] for row in current_tetrimino]
                    ai_color = current_color
                    ai_x = current_x
                    ai_y = 0

                    ai_waiting = False
                    last_ai_position = None

                    # 检查新方块是否会导致游戏结束
                    if check_collision() or check_collision_ai():
                        game_active = False
                        continue

        # AI移动逻辑
        if not ai_waiting:
            best_x, best_rotation = find_best_move()
            ai_tetrimino = best_rotation
            move_speed = 3
            if ai_x < best_x:
                ai_x += move_speed
                if ai_x > best_x:
                    ai_x = best_x
                if check_collision_ai():
                    ai_x -= move_speed
            elif ai_x > best_x:
                ai_x -= move_speed
                if ai_x < best_x:
                    ai_x = best_x
                if check_collision_ai():
                    ai_x += move_speed

        # 处理用户输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_x -= 1
                    if check_collision():
                        current_x += 1
                elif event.key == pygame.K_RIGHT:
                    current_x += 1
                    if check_collision():
                        current_x -= 1
                elif event.key == pygame.K_DOWN:
                    current_y += 1
                    if check_collision():
                        current_y -= 1
                elif event.key == pygame.K_UP:
                    rotated = [[current_tetrimino[j][i]
                                for j in range(len(current_tetrimino) - 1, -1, -1)]
                               for i in range(len(current_tetrimino[0]))]
                    old_tetrimino = current_tetrimino
                    current_tetrimino = rotated
                    if check_collision():
                        current_tetrimino = old_tetrimino

        # 绘制当前方块（玩家）
        for y in range(len(current_tetrimino)):
            for x in range(len(current_tetrimino[0])):
                if current_tetrimino[y][x] == 1:
                    pygame.draw.rect(window, current_color,
                                     ((current_x + x) * BLOCK_SIZE,
                                      (current_y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(window, (0, 0, 0),
                                     ((current_x + x) * BLOCK_SIZE,
                                      (current_y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 1)

        # 绘制当前方块（AI）
        offset_x = WINDOW_WIDTH + 50
        for y in range(len(ai_tetrimino)):
            for x in range(len(ai_tetrimino[0])):
                if ai_tetrimino[y][x] == 1:
                    pygame.draw.rect(window, ai_color,
                                     (offset_x + (ai_x + x) * BLOCK_SIZE,
                                      (ai_y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(window, (0, 0, 0),
                                     (offset_x + (ai_x + x) * BLOCK_SIZE,
                                      (ai_y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 1)

        # 显示分数和惩罚计数
        font = pygame.font.Font(None, 36)
        player_score_text = font.render(f'Player: {player_score}', True, (255, 255, 255))
        ai_score_text = font.render(f'AI: {ai_score}', True, (255, 255, 255))
        punishment_text = font.render(f'AI Punishment: {ai_punishment_count}', True, (255, 255, 255))
        window.blit(player_score_text, (10, 10))
        window.blit(ai_score_text, (WINDOW_WIDTH + 60, 10))
        window.blit(punishment_text, (10, 50))

    else:
        # 游戏结束界面
        play_again_button, quit_button = draw_game_over_screen(player_score, ai_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_again_button.collidepoint(mouse_pos):
                    reset_game()
                    game_active = True
                elif quit_button.collidepoint(mouse_pos):
                    running = False

    pygame.display.update()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()
