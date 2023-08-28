import pygame
from pygame.locals import *
from .Board import *
from .Menu.menu import *
import pickle


# Основной класс для взаимодействия с игрой
class Game:
    def __init__(self, image:dict, size, block_size:int=50) -> None:
        '''Инициализирует класс.\n
        image – словарь с текстурами для игры\n
        block_size - размер блока
        size - список указывающий размеры окна игры\n'''
        self.size = size
        self.image = image
        self.block_size = block_size
        # Словарь где каждая текстура привязана к символу (для уровня)
        self.dic_image_from_level = {
            ".": self.image["floor_grass"], 
            ",": self.image["floor_stone"], 
            "'": self.image["floor_tree"], 
            
            "#": self.image["obstacles_stone"], 
            "$": self.image["obstacles_tree"], 
            
            ":": self.image["wall_stone"], 
            ";": self.image["wall_tree"], 
            
            "@": self.image["actor"],
            "s": self.image["save_point"],
            "/": self.image["opponent"],
            "P": self.image["hil"],
            "C": self.image["coin"]
        }
        
        # Список блоков препятствий
        self.sp_ctop_block = ["#", "$", ":", ";"]
        # символ представляющий персонажа
        self.actor_image = "@"
        # Класс отвечающий за прорисовку уровня
        self.board = Board(self, self.block_size, self.dic_image_from_level, self.sp_ctop_block, self.actor_image)
        # Класс отвечающий за меню
        self.menu = Menu(self.image["fon"])
        # Флаг загруженного уровня True - загружен, False - не загружен
        self.stete_load_level = False
        # Переменная для уровней
        self.levels = None

    def show_menu(self, screen, clock_fps):
        """Отображает титульный экран, пока пользователь не нажмет клавишу\n
        1) Будем искать сохранения и уровни\n
        2) Будем продолжать игру\n
        3) Будем выходить из игры"""
        try:
            file = open("Game\\levels.levl", "rb")
            self.levels = pickle.load(file)
            file.close()
            try:
                file = open("Game\\save\\save.sv", "rb")
                save = pickle.load(file)
                file.close()
            except:
                save = [0, 100, 0]
                file = open("Game\\save\\save.sv", "wb")
                pickle.dump(save, file)
                file.close()

            res = self.menu.show_menu(screen, clock_fps, self.stete_load_level, save[0])
            
            if res == "new_games":
                file = open("Game\\save\\save.sv", "wb")
                pickle.dump([0, 100, 0], file)
                file.close()
                self.show_test_level(0)
                
            elif isinstance(res, int) and res < len(self.levels):
                self.show_test_level(res)
            
        except BreakError:
            pygame.quit()
            return "break"

    def show_test_level(self, ind:int=0) -> None:
        '''Загрузка уровня, переход на следующий\n
        ind - № уровня (индекс списка уровней) № = индекс'''
        self.stete_load_level = True
        self.level = Map(self, self.levels[ind])
        # камера
        self.camera = Camera(self, self.level.width, self.level.height)
        self.board.new(self.level.map, self.camera)

    def run(self, screen) -> None:
        '''Отрисовка'''
        self.board.update()
        self.board.draw(screen)