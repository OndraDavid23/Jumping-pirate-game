import pygame
from decorations import Clouds
from particles import ParticleEffect
from settings import screen_width, tile_size, screen_height
from tiles import Tile, StaticTile, Crate, AnimatedTile
from enemy  import Enemy
from player import Player
from particles import ParticleEffect
from support import import_csv_file_layout, import_cut_graphics
from decorations import Sky, Water

class Level:
    def __init__(self, level_data, surface):
        
        self.display_surface = surface

        #player setup
        player_layout = import_csv_file_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.setup_player(player_layout)

        #level setup
        #terrain setup
        terrain_layout = import_csv_file_layout(level_data["terrain"])
        self.terrain_sprites =  self.create_tile_group(terrain_layout, "terrain")
        self.display_surface = surface

        #grass_setup
        grass_layout = import_csv_file_layout(level_data["grass"])
        self.grass_sprites = self.create_tile_group(grass_layout, "grass")
        self.display_surface = surface

        #crates_setup
        crates_layout = import_csv_file_layout(level_data["crates"])
        self.crates_sprites = self.create_tile_group(crates_layout, "crates" )
        self.display_surface = surface

        #coins_setup
        coins_layout = import_csv_file_layout(level_data["coins"])
        self.coins_sprites = self.create_tile_group(coins_layout, "coins" )
        self.display_surface = surface

        #fg_palms_setup
        fg_palms_layout = import_csv_file_layout(level_data["fg_palms"])
        self.fg_palms_sprites = self.create_tile_group(fg_palms_layout, "fg_palms" )
        self.display_surface = surface

        #bg_palms_setup
        bg_palms_layout = import_csv_file_layout(level_data["bg_palms"])
        self.bg_palms_sprites = self.create_tile_group(bg_palms_layout, "bg_palms" )
        self.display_surface = surface


        #constraints_setup
        constraints_layout = import_csv_file_layout(level_data["constraints"])
        self.constraints_sprites = self.create_tile_group(constraints_layout, "constraints" )
        self.display_surface = surface

        # self.setup_level(level_data)
        self.world_shift = 0  
        self.current_x = 0
        self.current_y = 0
        
        #enemies
        enemies_layout = import_csv_file_layout(level_data["enemies"])
        self.enemies_sprites = self.create_tile_group(enemies_layout, "enemies" )
        self.display_surface = surface
        
        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        #decoration
        self.sky = Sky(5)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)
        self.clouds = Clouds(400, level_width, 20)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "terrain":
                        terrain_tile_list = import_cut_graphics("graphics/terrain/terrain_tiles.png")
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile((x, y), tile_size, tile_surface)


                    if type == "grass":
                        grass_tile_list = import_cut_graphics("graphics/decoration/grass/grass.png")
                        tile_surface = grass_tile_list[int(value)]
                        sprite = StaticTile((x,y), tile_size, tile_surface)
                    
                    if type == "constraints":
                        sprite = Tile((x,y), tile_size)

                    if type == "crates":
                        sprite = Crate((x,y) + pygame.math.Vector2(3,24), tile_size)
                    
                    if type == "coins":
                        sprite = AnimatedTile((x,y) - pygame.math.Vector2(0,64), tile_size, "graphics/coins/gold")

                    if type == "fg_palms":
                        if value == "0":
                            sprite = AnimatedTile((x,y) - pygame.math.Vector2(0,39), tile_size, "graphics/terrain/palm_small")
                        else:
                            sprite = AnimatedTile((x,y) - pygame.math.Vector2(0,72), tile_size, "graphics/terrain/palm_large")

                    if type == "bg_palms":                   
                        sprite = AnimatedTile((x,y) - pygame.math.Vector2(0,64), tile_size, "graphics/terrain/palm_bg")
                        
                    if type == "enemies":                   
                        sprite = Enemy((x,y) - pygame.math.Vector2(0, -18), tile_size)
                        
                    sprite_group.add(sprite)
        
        return sprite_group

    def setup_player(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if value == "0":
                    player_sprite = Player((x,y), self.display_surface, self.create_jump_particles)
                    self.player.add(player_sprite)
                if value == "1":
                    print("End")

            

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

    # def setup_level(self,layout):
    #     self.tiles = pygame.sprite.Group()
    #     self.player = pygame.sprite.GroupSingle()
    #     for row_index, row in enumerate(layout):
    #         for col_index, cell in enumerate(row):
    #             x = col_index * tile_size
    #             y = row_index * tile_size
    #             if cell == "x":
    #                 tile = Tile((x,y), tile_size)
    #                 self.tiles.add(tile)
    #             if cell == "P":
    #                 player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
    #                 self.player.add(player_sprite)

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

        for sprite in self.terrain_sprites.sprites() + self.crates_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left

                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        # for sprite in self.crates_sprites.sprites():
        #     if sprite.rect.colliderect(player.rect):
        #         if player.direction.x < 0:
        #             player.rect.left = sprite.rect.right
        #             player.on_left = True
        #             self.current_x = player.rect.left

        #         if player.direction.x > 0:
        #             player.rect.right = sprite.rect.left
        #             player.on_right = True
        #             self.current_x = player.rect.right
        


        if player.on_left and (player.rect.left < self.current_x or player.direction.x > 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x < 0):
            player.on_right = False

    def enemy_movemenet(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprites, False):
                enemy.reverse_move()

    def enemy_collision(self):
        player = self.player.sprite
        for enemy in self.enemies_sprites.sprites():
            if enemy.rect.colliderect(player.rect):
                pygame.sprite.Sprite.remove(enemy)
                print(enemy.groups)

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
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

        for sprite in self.crates_sprites.sprites():
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

        # for sprite in self.fg_palms_sprites.sprites():
        #     if sprite.rect.colliderect(player.rect):
        #         print("Fanda je debil")
        #         if player.direction.y > 0: 
        #             player.rect.bottom = sprite.rect.top
        #             player.direction.y = 0
        #             player.on_ground = True
        #             self.current_y = player.rect.midbottom

        if player.on_ground and (player.rect.midbottom > self.current_y or player.direction.y < 0 or player.direction.y > 1):
            player.on_ground = False
        if player.on_ceiling and (player.rect.midtop < self.current_y or player.direction.y > 0 or player.direction.y < 0):
            player.on_ceiling = False


    def run(self):
        #decorations
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        #level
        self.scroll_x()
        self.enemy_movemenet()

        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        self.enemies_sprites.update(self.world_shift)
        self.constraints_sprites.update(self.world_shift)
        self.enemies_sprites.draw(self.display_surface)

        self.bg_palms_sprites.update(self.world_shift)
        self.bg_palms_sprites.draw(self.display_surface)

        self.fg_palms_sprites.update(self.world_shift)
        self.fg_palms_sprites.draw(self.display_surface)

        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)

        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)


        #player 
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_land_particles()
        self.player.draw(self.display_surface)  

        self.enemy_collision()
        #water
        self.water.draw(self.display_surface, self.world_shift)



        
        