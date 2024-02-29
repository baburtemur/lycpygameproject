import pygame
import random
import os
import sys
from pygame._sdl2.video import Window

pygame.init()

tile_size = 10
map_width = 40
map_height = 30
screen_width = tile_size * map_width
screen_height = tile_size * map_height
x = 800
y = 420
speed_difficulty = 0
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
clock = pygame.time.Clock
pygame.display.set_caption("my lyc game")
font = pygame.font.SysFont('Arial', 30)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen = pygame.display.set_mode((1000, 400))
    intro_text = ["Найстройки скорости:",
                  "Нажмите ЛКМ чтобы начать игру в обычном режиме",
                  "Нажмите ПКМ чтобы начать игру в ускоренном режиме",
                  "Нажмите КОЛЕСИКО чтобы начать игру в замедленном режиме"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (1000, 400))
    screen.blit(fon, (0, 0))
    text_coord = 50
    keys = pygame.key.get_pressed()
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 1
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font1 = pygame.font.SysFont('Arial', 16)
    intro_text = ["Двигайтесь по спирали",
                  "и нажимайте ПРОБЕЛ",
                  "чтобы перейти в следующую комнату",
                  "Вам надо закрасить все красные клетки"]
    for line in intro_text:
        string_rendered = font1.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 720
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            global speed_difficulty
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                speed_difficulty = 500
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                speed_difficulty = 1000
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                speed_difficulty = 300
                return
        pygame.display.flip()

def load_image(name):
    fullname = os.path.join('textures', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


start_screen()

player_pos = [map_width // 2, map_height // 2]
screen = pygame.display.set_mode((screen_width, screen_height))
tick = 0
leveld = [i for i in range(9)]
levels = []
window = Window.from_display_module()
for i in range(9):
    temp_ari = []
    for i in range(map_width):
        temp_arj = []
        for j in range(map_width):
            temp_arj.append(random.choice(["E", "*", "X"]))
        temp_ari.append(temp_arj)
    levels.append(temp_ari)

score = 0


def level_generate(scope):
    maplt = levels[scope]
    global score
    for i in range(map_width):
        for j in range(map_width):
            if maplt[i][j] == "E" and i - round(score / (dlm + score * 0.2) + 1) / 2 <= player_pos[0] <= i + round(
                    score / \
                    (dlm + score * 0.2)) / 2 and j - round(score / (dlm + score * 0.2) + 1) / 2 <= player_pos[1] <= j + \
                    round(score / (dlm + score * 0.2)) / 2:
                maplt[i][j] = "X"
                score += 1
            if maplt[i][j] == "E":
                pygame.draw.rect(screen, (255, 0, 0), (i * tile_size, j * tile_size, tile_size, tile_size))
            if maplt[i][j] == "*":
                pygame.draw.rect(screen, (0, 0, 0), (i * tile_size, j * tile_size, tile_size, tile_size))
            if maplt[i][j] == "X":
                pygame.draw.rect(screen, (255, 255, 255), (i * tile_size, j * tile_size, tile_size, tile_size))
            if maplt[i][j] == "W":
                pygame.draw.rect(screen, (255, 255, 0), (i * tile_size, j * tile_size, tile_size, tile_size))


cur_scope = 0
speed = 1
dlm = 100
time_score = 100000
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if tick > speed_difficulty:
        time_score -= 1
        tick = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += speed
        if keys[pygame.K_UP]:
            player_pos[1] -= speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += speed
        player_pos[0] = max(0, min(player_pos[0], map_width - round(score / (dlm + score * 0.2) + 1)))
        player_pos[1] = max(0, min(player_pos[1], map_height - round(score / (dlm + score * 0.2) + 1)))
        if (cur_scope == 0 or cur_scope == 6 or cur_scope == 7) and keys[pygame.K_SPACE]:
            if player_pos[0] < (round(score / (dlm + score * 0.5) + 1)):
                cur_scope += 1
                player_pos[0] = map_width - (round(score / (dlm + score * 0.2) + 1))
                print(cur_scope)
                x -= screen_width
                window.position = (x, y)
        if cur_scope == 1 and keys[pygame.K_SPACE]:
            if player_pos[1] < (round(score / (dlm + score * 0.5) + 1)):
                cur_scope += 1
                player_pos[1] = map_height - (round(score / (dlm + score * 0.2) + 1))
                print(cur_scope)
                y -= screen_height
                window.position = (x, y)
        if cur_scope == 2 or cur_scope == 3 and keys[pygame.K_SPACE]:
            if player_pos[0] >= map_width - (round(score / (dlm + score * 0.2) + 1)):
                cur_scope += 1
                player_pos[0] = (round(score / (dlm + score * 0.5) + 1))
                print(cur_scope)
                x += screen_width
                window.position = (x, y)
        if cur_scope == 4 or cur_scope == 5 and keys[pygame.K_SPACE]:
            if player_pos[1] >= map_height - (round(score / (dlm + score * 0.2) + 1)):
                cur_scope += 1
                player_pos[1] = (round(score / (dlm + score * 0.2) + 1))
                print(cur_scope)
                y += screen_height
                window.position = (x, y)
        if cur_scope == 8 and keys[pygame.K_SPACE]:
            if player_pos[0] < (round(score / (dlm + score * 0.2) + 1)):
                break
        level_generate(cur_scope)

        pygame.draw.rect(screen, (255, 255, 0),
                         (player_pos[0] * tile_size, player_pos[1] * tile_size,
                          tile_size * round(score / (dlm + score * 0.2) + 1),
                          tile_size * round(score / (dlm + score * 0.2) + 1)))
        pygame.display.flip()
    tick += 1
    pygame.display.update()


bb = True
def result_check():
    not_painted = 0
    for k in range(9):
        for i in range(map_width):
            for j in range(map_width):
                if levels[k][i][j] == "E":
                    not_painted += 1
    return not_painted

not_painted_f = result_check()


def end_screen():
    screen = pygame.display.set_mode((1000, 400))
    intro_text = ["Ваши результаты:",
                  f"Баллы за скорость: {time_score}",
                  f"Клеток закрашено: {score}",
                  f"Клеток незакрашено: {not_painted_f}",
                  f"Достигнут уровень: {round(score / (dlm + score * 0.5) + 1)}"]
    if not_painted_f == 0:
        intro_text.append("Поздравляем! вы закрасили все клетки")

    fon = pygame.transform.scale(load_image('end.jpg'), (1000, 400))
    screen.blit(fon, (0, 0))
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()

end_screen()


pygame.quit()