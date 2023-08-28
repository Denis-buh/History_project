import pygame
from pygame.locals import *
from .button import Button
from .Errors import *


def breaker():
    '''Функция для завершения игры\n
    Возбуждает исключение BreakError'''
    raise BreakError


class Menu:
    def __init__(self, image):
        '''Инициализация класса\n
        image – изображение меню'''
        self.image = image
        
    def __dide_menu(self):
        '''Функция для: "Продолжить игру"'''
        self.fleg_dide_menu = True
        
    def __dide_load_menu(self):
        '''Функция для: "Новая игра"'''
        self.fleg_load_dide_menu = True
        
    def __load_save(self):
        '''Функция для: "Загрузка сохранения"'''
        self.load_save = True
    
    
    def show_menu(self, screen, clock_fps, stete_load_level:bool, nimder_level:int):
        """Отображает титульный экран, пока пользователь не нажмет кнопку\n
        clock_fps - fps\n
        stete_load_level - Флаг загруженного уровня True - загружен, False - не загружен\n
        nimder_level - № уровня"""
        
        titleRect = self.image.get_rect()
        screen.fill((17, 189, 234))
        screen.blit(self.image, titleRect)
        
        # Переменная для: "Продолжить игру"
        self.fleg_dide_menu = False
        # Переменная для: "Новая игра"
        self.fleg_load_dide_menu = False
        # Переменая для: "Загрузка сохранения"
        self.load_save = False
        
        if stete_load_level:
            buton_run = Button(30, 30, 200, 50, 'Продолжить игру', self.__dide_menu)
        else:
            buton_run = Button(30, 30, 200, 50, 'Новая игра', self.__dide_load_menu)
            
        buton_save_load = Button(30, 100, 200, 50, 'Загрузка сохранения', self.__load_save)
        
        buton_exit = Button(30, 170, 200, 50, 'Выйти из игры', breaker)
        
        while True: # Основной цикл для стартового экрана.
            # Продолжить игру
            if self.fleg_dide_menu:
                return
            # Новая игра
            elif self.fleg_load_dide_menu:
                return "new_games"
            elif self.load_save:
                return nimder_level
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise BreakError
            
            buton_run.process(screen)
            buton_save_load.process(screen)
            buton_exit.process(screen)
            
            pygame.display.flip()
            pygame.display.update()
            clock_fps.tick()
