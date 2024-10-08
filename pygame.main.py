import pygame
import time
# 리스트 저장
import pickle
from player import Player
from bullet import Bullet
import random as rnd

def collision(obj1, obj2):
    dist = ((obj1._pos[0] - obj2.pos[0]) ** 2 + (obj1._pos[1] - obj2.pos[1]) ** 2) ** 0.5
    return dist < 20

def draw_text(txt, size, pos, color):
    font = pygame.font.Font('freesansbold.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, pos)

# 점수를 기록할 리스트 추가
scores = []
# 파일 열어 읽기
try:
    with open ('highscores.txt', 'rb') as f:
        scores = pickle.load(f)
except:
    print("score file not found")

pygame.init()
WIDTH, HEIGHT = 800, 600

pygame.mixer.init()

pygame.display.set_caption("총알 피하기")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS = 60

# 충돌 횟수 세기
# collisioncount = 0


bg_image = pygame.image.load('bg.jpg')
# 배경화면의 가운데에 오도록 조정
bg_pos = (-400, -300)
bg_goto = (0, 0)
# player.py에 mixer 도입했음
player = Player(WIDTH/2, HEIGHT/2, pygame.mixer)


# 평상시 = 0
gamechannel = pygame.mixer.Channel(0)
# 배경음악을 게임채널에서 재생
gamechannel.play(pygame.mixer.Sound('bgm.wav'), -1)
'''
pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.play(-1)
'''

# 더 이상 bullet을 따로 지정해줄 필요 없음
# bullet1 = Bullet(0,0,0.5,0.5)
bullets = []
for i in range(1):
    bullets.append(Bullet(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5))

time_for_adding_bullets = 0

start_time = time.time()

score = 0
# 추가: 최초 실행 시 최고기록은 0점
bs = scores[9]

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
    '''bullet1.update_and_draw(dt, screen)'''
    for b in bullets:
        b.update_and_draw(dt, screen)

    '''
    for b in bullets:
        if collision(b, player):
            # 폭발
            Exploding = pygame.image.load('explode.jpg')
            Exploding = pygame.transform.scale(Exploding, (128, 128))
            screen.blit(Exploding, (player.pos[0] - 64, player.pos[1] - 64))
            # 충돌 효과음
            ExplodeSound = pygame.mixer.Sound("explosion.wav")
            ExplodeSound.play(0, 0, 0)
            collisioncount += 1
            if collisioncount < 5:
                player.invincibility = True
                player.invincibility_during = 3000
                player.invincibility_during -= dt
                if player.invincibility_during < 0:
                    player.invincibility = False
            elif collisioncount == 5:
                gameover = True
    '''

    

    if gameover:
        '''screen.blit(Exploding, (player.pos[0] - 64, player.pos[1] - 64))'''
        draw_text("GAME OVER", 100, (WIDTH/2 - 300, HEIGHT/2 - 50), (255,255,255))
        # txt = f"Time: {score:.3f}, Bullets: {len(bullets)}"
        # 이제 점수를 파일에서 가져온다.
        txt = f"score: {s}"
        for i in range(min(len(scores), 10)):
            if s == float(scores[9]):
                draw_text(txt, 48, (WIDTH/2 - 307, HEIGHT/2 + 50), (196, 156, 72))
            elif s == float(scores[8]):
                draw_text(txt, 48, (WIDTH/2 - 307, HEIGHT/2 + 50), (192, 192, 192))
            elif s == float(scores[7]):
                draw_text(txt, 48, (WIDTH/2 - 307, HEIGHT/2 + 50), (191, 137, 112))
            elif s in scores:
                # 텍스트 크기와 색 다르게 하여 강조
                draw_text(txt, 48, (WIDTH/2 - 307, HEIGHT/2 + 50), (64, 224, 208))
            else:
                draw_text(txt, 32, (WIDTH/2 - 210, HEIGHT/2 + 50), (255, 255, 255))

    else:
        score = time.time() - start_time
        txt = f"Time: {score:.3f}, Bullets: {len(bullets)}, HP = {player.get_hp()}, Best = {bs:.3f}"
        draw_text(txt, 32, (10, 10), (255, 255, 255))

    pygame.display.update()

    if not gameover:
        for b in bullets:
            if collision(b, player):
                # 데미지를 가져와 hp 차감
                if player.hit(b.get_damage()):
                    gameover = True
                    # scores에 점수 기록
                    s = float(score)
                    scores.append(s)
                    scores.sort()
                    # 리스트 요소 개수가 10개를 넘기면 가장 앞 것을 자른다.
                    if len(scores) > 10:
                        scores.pop(0)
                    else:
                        pass
                    # 추가; 최고기록
                    bs = float(scores[9])
                    with open('highscores.txt', 'wb') as f:
                        pickle.dump(scores, f)

                    print(scores)
                    
            
        if time_for_adding_bullets > 1000:
            bullets.append(Bullet(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5))
            time_for_adding_bullets -= 1000
