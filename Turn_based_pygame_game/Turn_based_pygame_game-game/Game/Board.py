import pygame
import pickle
from .Sprites import *


# Класс отвечающий за прорисовку уровня
class Board:
    def __init__(self, game, block_size:int=50, dic_image_from_level:dict={}, sp_ctop_block:list=[], actor_image:str="@"):
        '''Инициализирует класс.\n
        block_size – Размер каждого блока\n
        dic_image_from_level - словарь с текстурами для игры где каждая текстура привязана к символу (для уровня)\n
        sp_ctop_block - Список блоков препятствий\n
        actor_image - символ представляющий персонажа'''
        self.block_size = block_size
        self.dic_image_from_level = dic_image_from_level
        self.sp_ctop_block = sp_ctop_block
        self.actor_image = actor_image
        self.game = game

    def new(self, map, camera):
        '''create a level'''
        self.map = map
        self.camera = camera
        self.all_sprites = pygame.sprite.Group()
        self.empty_tiles = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.num_of_enemies = 0
        self.moving_map = []

        for row, tiles in enumerate(self.map):
            self.moving_map.append([])
            for col, tile in enumerate(tiles):
                if tile in self.sp_ctop_block:
                    Wall(self, col, row, tile)
                    Tile(self, col, row)
                    self.moving_map[row].append(1)
                elif tile == self.actor_image:
                    with open("Game\\save\\save.sv", "rb") as f:
                        save = pickle.load(f)
                        self.player = Player(self, col, row, self.actor_image, hp=save[1], score=save[2])
                        Tile(self, col, row)
                        self.moving_map[row].append(1)
                elif tile == 's':
                    Tile(self, col, row)
                    self.savepoint = SavePoint(self, col, row, tile)
                    self.moving_map[row].append(0)
                elif tile == '/':
                    Enemy(self, col, row, tile)
                    Tile(self, col, row)
                    self.moving_map[row].append(1)
                    self.num_of_enemies += 1
                else:
                    Tile(self, col, row)
                    self.moving_map[row].append(0)

    def update(self):
        if self.player.turn == 2:
            for enemy in self.enemies:
                enemy.action()
                self.player.turn = 0
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_score(self, screen):
        f1 = pygame.font.SysFont('arial', 30)
        text1 = f1.render(f"Ваш счёт: {self.player.score}", 1, (255, 0, 0))
        screen.blit(text1, (20, 60))

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for sprite in self.empty_tiles:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))
            if isinstance(sprite, Enemy):
                sprite.draw_hp_bar(screen)
        self.player.drew_hp_bar(screen)
        self.draw_score(screen)
        pygame.display.update()


class Camera:
    def __init__(self, game, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.game = game

    def apply(self, sprite):
        return sprite.rect.move(self.camera.topleft)

    def update(self, player):
        x = -player.rect.x + int(self.game.size[0] / 2)
        y = -player.rect.y + int(self.game.size[1] / 2)
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Map:
    def __init__(self, game, level:list=[]):
        '''Инициализирует карту уровня\n
        level - уровень в виде списка'''
        self.map = level
        self.tile_width = len(self.map[0])
        self.tile_height = len(self.map)
        self.width = self.tile_width * game.block_size
        self.height = self.tile_height * game.block_size
