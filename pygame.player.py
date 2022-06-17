import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.pos = [x, y]
        self.to = [0, 0]
        self.angle = 0

    def goto(self, x, y):
        self.to[0] += x
        self.to[1] += y

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


    def draw(self, screen):
        
        if self.to == [-1, -1]: self.angle = 45
        elif self.to == [-1, 0]: self.angle = 90
        elif self.to == [-1, 1]: self.angle = 135
        elif self.to == [0, 1]: self.angle = 180
        elif self.to == [1, 1]: self.angle = 225
        elif self.to == [1, 0]: self.angle = 270
        elif self.to == [1, -1]: self.angle = 315
        elif self.to == [0, -1]: self.angle = 0

        rotated = pygame.transform.rotate(self.image, self.angle)

        calib_pos = (self.pos[0] - rotated.get_width()/2, self.pos[1] - rotated.get_height()/2)


        screen.blit(rotated, calib_pos)
