import pygame

class Bullet:
    def __init__(self, x, y, to_x, to_y):
        self._pos = [x, y]
        self._to = [to_x, to_y]
        self._radius = 7
        self._color = (34, 144, 34)
        # 데미지 도입
        self._damage = 8

    def get_damage(self):
        return self._damage

    def update_and_draw(self, dt, screen):
        width, height = screen.get_size()
        self._pos[0] = (self._pos[0] + self._to[0] * dt) % width
        self._pos[1] = (self._pos[1] + self._to[1] * dt) % height
        pygame.draw.circle(screen, self._color, self._pos, self._radius)

# Bullet을 부모 클래스로 두고 그 아래에 총알의 종류를 자식 클래스로 만든다.
class IronBead(Bullet):
    def __init__(self, x, y, to_x, to_y):
        super().__init__(x, y, to_x, to_y)
        self._radius = 5
        self._color = (190, 0, 0)
        self._damage = 4

class NormalBullet(Bullet):
    def __init__(self, x, y, to_x, to_y):
        super().__init__(x, y, to_x, to_y)

class Canonball(Bullet):
    def __init__(self, x, y, to_x, to_y):
        super().__init__(x, y, to_x, to_y)
        self._radius = 10
        self._color = (201, 228, 225)
        self._damage = 16

class Killer(Bullet):
    def __init__(self, x, y, to_x, to_y):
        super().__init__(x, y, to_x, to_y)
        self._radius = 16
        self._color = (64, 44, 196)
        self._damage = 44444444
