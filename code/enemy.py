import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, pos, size):
        super().__init__(pos, size, "graphics/enemy/run")
        self.offset_y = self.image.get_size()[1]
        self.speed = randint(3,5)
        self.rect = self.image.get_rect(topleft = pos)

    def move(self):
        self.rect.x += self.speed

    def reverse_move(self):
        self.speed *= -1

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()
        self.move()
        self.reverse_image()
