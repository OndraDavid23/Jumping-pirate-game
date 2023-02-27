from msilib.schema import Directory
import pygame
from particles import ParticleEffect
from settings import screen_width, tile_size
from tiles import Tile
from player import Player
from particles import ParticleEffect

class Level:
    def __init__(self, level_data, surface):
        
        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0    
        self.current_x = 0
        self.current_y = 0
        
        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_jump_particles(self, pos):
        jump_particle_sprite = ParticleEffect(pos, "jump")
        self.dust_sprite.add(jump_particle_sprite)

    def create_land_particles(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites() and self.player.sprite.status != "run":
            if self.player.sprite.facing_right:
                land_particle_sprite = ParticleEffect(self.player.sprite.rect.midbottom - pygame.math.Vector2(10,20), "land")
            else:
                land_particle_sprite = ParticleEffect(self.player.sprite.rect.midbottom - pygame.math.Vector2(-10,20), "land")
            self.dust_sprite.add(land_particle_sprite)
        else:
            print("air: " + str(self.player_on_ground))
            print("ground: " + str(self.player.sprite.on_ground))

    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == "x":
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile)
                if cell == "P":
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x < screen_width/4  and direction_x < 0:
            self.world_shift = player.speed_set
            player.speed = 0
        elif player_x > screen_width/4*3 and direction_x > 0:
            self.world_shift = -player.speed_set
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = player.speed_set

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        # print(player.direction, player.rect.x, player.rect.y)
        # print("ground" + str(player.on_ground))

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left

                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right


        if player.on_left and (player.rect.left < self.current_x or player.direction.x > 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x < 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    self.current_y = player.rect.midbottom

                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    self.current_y = player.rect.midtop

        if player.on_ground and (player.rect.midbottom > self.current_y or player.direction.y < 0 or player.direction.y > 1):
            player.on_ground = False
        if player.on_ceiling and (player.rect.midtop < self.current_y or player.direction.y > 0 or player.direction.y < 0):
            player.on_ceiling = False


    def run(self):

        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #level
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        #player 
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_land_particles()
        self.player.draw(self.display_surface)  


        
        