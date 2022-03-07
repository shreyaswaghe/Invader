from enum import Enum


class Sprite:
    def __init__(self, img, x:int, y:int, xchange:int, ychange:int):
        self._Image = img
        self.X = x
        self.Y = y
        self._xchange = xchange
        self._ychange = ychange

    def image(self):
        return self._Image

    def position(self):
        return (self.X, self.Y)
    
    def moveX(self):
        self.X += self._xchange
    
    def moveY(self):
        self.Y += self._ychange

    def x(self):
        return self.X
    
    def y(self):
        return self.Y
    
    def xchange(self):
        return self._xchange

    def set_xchange(self, val):
        self._xchange = val

    def set_ychange(self, val):
        self._ychange = val
    
    def setpos(self, pos):
        self.X, self.Y = pos

    def setx(self, val):
        self.X = val
    
    def sety(self, val):
        self.Y = val


class Enemy(Sprite):
    def __init__(self, num, img, x, y, xchange = 3, ychange = 40):
        self.sprite = super()
        self.sprite.__init__(img, x, y, xchange, ychange)
        self.num = num
    
    # Override
    def moveX(self):
        self.sprite.moveX()
        self.boundary()
        
    def boundary(self):
        if self.sprite.x() <= 0:
            self.flip_xchange()
            self.sprite.moveY()
        elif self.sprite.x() >= 750:
            self.flip_xchange()
            self.sprite.moveY()

    def flip_xchange(self):
        self.sprite.set_xchange(self.sprite.xchange() * -1)

    def defeated(self, bound = 400):
        return self.sprite.y() > bound

    def x(self):
        return self.sprite.x()

    def setnew_pos(self, pos:tuple[int,int]):
        self.sprite.setpos(pos)
    
    def getnum(self):
        return self.num


class Bullet(Sprite):
    def __init__(self, img, x:int=0, y:int=450, ychange:int=-5):
        self.sprite = super()
        self.sprite.__init__(img, x, y, 0, ychange)
        self.state = BulletStates.READY
    
    def flip_state(self):
        self.state = BulletStates.READY if self.state is BulletStates.FIRED else BulletStates.FIRED

    def position(self):
        x,y = self.sprite.position()
        return (x+10, y-20)
    
    def isReady(self):
        return self.state is BulletStates.READY
    
    def setFired(self):
        self.state = BulletStates.FIRED

    def setReady(self):
        self.state = BulletStates.READY
    

class BulletStates(Enum):
    READY = 0
    FIRED = 1

class Player(Sprite):
    def __init__(self, img, x=370, y=450,xchange=0,ychange=0):
        self.sprite = super()
        self.sprite.__init__(img,x,y,xchange,ychange)

    def moveX(self):
        self.sprite.moveX()
        self.boundary()

    def boundary(self):
        x = self.sprite.x()
        if x <= 0:
            self.sprite.setx(0)
        elif x >= 750:
            self.sprite.setx(750)

    def changeDir(self):
        self.sprite.set_xchange(self.sprite.xchange()*-1)
    
    def set_xchange(self, val):
        return self.sprite.set_xchange(val)