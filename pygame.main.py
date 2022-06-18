import pygame
import time
from player import Player
from bullet import Bullet
import random as rnd

def collision(obj1, obj2):
    dist = ((obj1.pos[0] - obj2.pos[0]) ** 2 + (obj1.pos[1] - obj2.pos[1]) ** 2) ** 0.5
    return dist < 20

def draw_text(txt, size, pos, color):
    font = pygame.font.Font('freesansbold.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, pos)

pygame.init()
WIDTH, HEIGHT = 800, 600

pygame.display.set_caption("총알 피하기")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS = 60


pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.play(-1)

bg_image = pygame.image.load('bg.jpg')
bg_pos = (0, 0)
bg_goto = (0, 0)
player = Player(WIDTH/2, HEIGHT/2)

bullet1 = Bullet(0,0,0.5,0.5)
bullets = []
for i in range(1):
    bullets.append(Bullet(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5))

time_for_adding_bullets = 0

start_time = time.time()

score = 0

gameover = False
running = True
while running:
    
    dt = clock.tick(FPS)
    time_for_adding_bullets += dt

    #이벤트 받는 부분
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 플레이어가 이동하면 배경화면도 같이 이동(배경이 유지되도록 플레이어와 반대로 이동)
            if event.key == pygame.K_LEFT:
                player.goto(-1, 0)
                bg_goto = (1, 0)
            elif event.key == pygame.K_RIGHT:
                player.goto(1, 0)
                bg_goto = (-1, 0)
            elif event.key == pygame.K_UP:
                player.goto(0, -1)
                bg_goto = (0, 1)
            elif event.key == pygame.K_DOWN:
                player.goto(0, 1)
                bg_goto = (0, -1)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.goto(1, 0)
                bg_goto = (-1, 0)
                # KEYUP 상태에서 계속 화면이 움직이는 것을 방지
                bg_goto = (0, 0)
            elif event.key == pygame.K_RIGHT:
                player.goto(-1, 0)
                bg_goto = (1, 0)
                bg_goto = (0, 0)
            elif event.key == pygame.K_UP:
                player.goto(0, 1)
                bg_goto = (0, -1)
                bg_goto = (0, 0)
            elif event.key == pygame.K_DOWN:
                player.goto(0, -1)
                bg_goto = (0, 1)
                bg_goto = (0, 0)
            

    player.update(dt, screen)

    #화면 갱신
    # screen.fill((0, 0, 0)) # 검정색
    bg_pos = (bg_pos[0] + bg_goto[0] * 0.01 * dt, bg_pos[1] + bg_goto[1] * 0.01 * dt)
    screen.blit(bg_image, bg_pos)
    player.draw(screen)
    bullet1.update_and_draw(dt, screen)
    for b in bullets:
        b.update_and_draw(dt, screen)

    for b in bullets:
        if collision(b, player):
            gameover = True
            # 충돌 효과음
            ExplodeSound = pygame.mixer.Sound("explosion.wav")
            ExplodeSound.play(0, 0, 0)

    

    if gameover:
        # 폭발
        Exploding = pygame.image.load('explode.jpg')
        Exploding = pygame.transform.scale(Exploding, (128, 128))
        screen.blit(Exploding, (player.pos[0] - 64, player.pos[1] - 64))
        draw_text("GAME OVER", 100, (WIDTH/2 - 300, HEIGHT/2 - 50), (255,255,255))
        txt = f"Time: {score:.3f}, Bullets: {len(bullets)}"
        draw_text(txt, 32, (WIDTH/2 - 150, HEIGHT/2 + 50), (255, 255, 255))
    else:
        score = time.time() - start_time
        txt = f"Time: {score:.3f}, Bullets: {len(bullets)}"
        draw_text(txt, 32, (10, 10), (255, 255, 255))

        if time_for_adding_bullets > 1000:
            bullets.append(Bullet(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5))
            time_for_adding_bullets -= 1000

    pygame.display.update()
