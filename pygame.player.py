import pygame
# hp가 10씩 줄어야 하는데 그 이상 줄거나 바로 gameover되는 경우 발생 -> 시간지연 위해 import
import time

class Player:
    # 폭발할 때 효과음도 player에서 표현
    def __init__(self, x, y, mixer):
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.attacked_image = pygame.image.load('explode.png')
        self.attacked_image = pygame.transform.scale(self.attacked_image, (128, 128))
        self.show_attacked = False
        self.show_attacked_during = 0
        self.pos = [x, y]
        self.to = [0, 0]
        self.angle = 0
        # 플레이어 소리 도입
        self.channel = mixer.Channel(1)
        # 총알에 맞으면 폭발음이 들린다.
        self.sound = mixer.Sound('explosion.wav')
        # 플레이어 생명력 도입
        self.hp = 50
        # 플레이어 무적상태 도입
        self.invincibility = False
        self.invincibility_during = 0

    def get_hp(self):
        # 플레이어의 생명력 상태를 표시
        return self.hp

    def goto(self, x, y):
        self.to[0] += x
        self.to[1] += y
        if x < 0:
            # 화면 외부가 보이지 않도록
            x = 800
        elif x > 800:
            x = 0
        if y < 0:
            # 화면 외부가 보이지 않도록
            y = 600
        elif y > 600:
            y = 0

    def update(self, dt, screen):
        width, height = screen.get_size();
        phw = self.image.get_width() / 2
        phh = self.image.get_height() / 2
        self.pos[0] = self.pos[0] + dt * self.to[0]
        self.pos[1] = self.pos[1] + dt * self.to[1]
        self.pos[0] = min(max(self.pos[0], phw), width-phw)
        self.pos[1] = min(max(self.pos[1], phh), height-phh)
        #if self.pos[0] < player_half_width : 
        #   self.pos[0] = player_half_width
        #if self.pos[0] > width - player_half_width : 
        #    self.pos[0] = width - player_half_width
        #if self.pos[1] < player_half_height:
        #    self.pos[1] = player_half_height
        #if self.pos[1] > height - player_half_height:
        #    self.pos[1] = height - player_half_height
        # 총알 맞았을 때 효과 지속시간
        self.show_attacked_during -= dt
        if self.show_attacked_during < 0:
            self.show_attacked = False

        # 무적 효과 지속시간
        self.invincibility_during -= dt
        if self.invincibility_during < 0:
            self.invincibility = False

    def hit(self, damage):
        # 무적상태가 아니라면?
        if not self.invincibility:
            # 오류 없애기 위해 0.1초 정지
            # 맞으면 폭발
            time.sleep(0.1)
            self.show_attacked = True
            self.show_attacked_during = 300
            # 맞으면 폭발음
            self.channel.play(self.sound)
            # 무적상태 돌입
            self.invincibility = True
            self.invincibility_during = 1000
            # 맞으면 hp 깎임
            # main으로 가져가서 사용하므로 여기서 bullets의 Bullet 클래스를 import 하지 않음
            self.hp -= damage
        if self.hp <= 0:
            return True # hp가 0이면 gameover = True로 하기 위함


    def draw(self, screen):
        
        if self.to == [-1, -1]: self.angle = 45
        elif self.to == [-1, 0]: self.angle = 90
        elif self.to == [-1, 1]: self.angle = 135
        elif self.to == [0, 1]: self.angle = 180
        elif self.to == [1, 1]: self.angle = 225
        elif self.to == [1, 0]: self.angle = 270
        elif self.to == [1, -1]: self.angle = 315
        elif self.to == [0, -1]: self.angle = 0

        rotated = None
        calib_pos = [0, 0]

        if self.show_attacked:
            rotated = pygame.transform.rotate(self.attacked_image, self.angle)
            calib_pos = (self.pos[0] - rotated.get_width()/2, self.pos[1] - rotated.get_height()/2)
            screen.blit(rotated, calib_pos)
        else:
            rotated = pygame.transform.rotate(self.image, self.angle)

        calib_pos = (self.pos[0] - rotated.get_width()/2, self.pos[1] - rotated.get_height()/2)
        

        # 무적이면 깜빡인다.
        if self.invincibility:
            if self.invincibility_during // 100 % 2 == 0:
                screen.blit(rotated, calib_pos)
        else:
            screen.blit(rotated, calib_pos)
