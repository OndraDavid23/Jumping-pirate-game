import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift

class StaticTile(Tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image = surface
 
class Crate(StaticTile):
    def __init__(self, pos, size):
        super().__init__(pos, size, pygame.image.load("graphics/terrain/crate.png"))

class AnimatedTile(Tile):
    def __init__(self,pos, size, path):
        super().__init__(pos,size)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.animation_speed = 0.1
        self.animate()
        self.image = self.frames[int(self.frame_index)]

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift

class Coin(AnimatedTile):
    def __init__(self, pos, size, path, offset):
        super().__init__(pos, size, path)
        offset_y = pos - offset
        self.rect.topleft = (pos - offset_y)




        

