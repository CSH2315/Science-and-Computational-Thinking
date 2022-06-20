from bullets import IronBead
from bullets import NormalBullet
from bullets import Canonball
from bullets import Killer
from random import randint
def Bullet(x, y, to_x, to_y):
    rnd = randint(1, 100)
    if rnd % 44 == 0:
        return Killer(x, y, to_x, to_y)
    elif rnd == 4:
        return Killer(x, y, to_x, to_y)
    elif rnd % 3 == 1:
        return NormalBullet(x, y, to_x, to_y)
    elif rnd % 3 == 2:
        return IronBead(x, y, to_x, to_y)
    elif rnd % 3 == 0:
        return Canonball(x, y, to_x, to_y)
