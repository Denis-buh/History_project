import sys
import pygame
from pygame.locals import *


class Button:
    '''Класс кнопки для PyGame'''
    def __init__(self, x:int=0, y:int=0, width:int=200, height:int=50, buttonText:str='Button', function=None, 
                 fone:tuple=('Arial', 20), color:dict={'normal': '#B4B4B4', 'hover': '#666666', 'pressed': '#333333'}):
        '''Инициализация класса \n
        - x, y - параметры начального x и y
        - width, height- параметры длины(width) и ширины(height)
        - buttonText - текст кнопки
        - function - функция кнопки
        - fone - параметр шрифта (первое название, второе размер)
        - color - параметр цветов 
            - 'normal' - нормальная кнопка 
            - 'hover' - кнопка под фокусом 
            - 'pressed' - нажатая кнопка '''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        self.color = color
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.SysFont(*fone)
        self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))
        # Статус кнопки (True - нажата, False - не нажата)
        self.alreadyPressed = True

    def process(self, screen):
        '''Клик по кнопке'''
        # Позиция курсора
        mousePos = pygame.mouse.get_pos()
        # Меняем цвет кнопки
        self.buttonSurface.fill(self.color['normal'])
        # Проверяем наличие курсора на кнопке
        if self.buttonRect.collidepoint(mousePos):
            # Меняем цвет кнопки
            self.buttonSurface.fill(self.color['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                # Меняем цвет кнопки
                self.buttonSurface.fill(self.color['pressed'])
                # Проверка на то не нажата ли кнопка
                if not self.alreadyPressed:
                    self.function()
                    # нажата
                    self.alreadyPressed = True
            # Если не нажата
            else:
                self.alreadyPressed = False
        # Если была нажата вне кнопки
        else:
            self.alreadyPressed = True
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
        
        
if __name__ == "__main__":

    def myFunction():
        print('Button Pressed')

    # Configuration
    pygame.init()
    fps = 60
    fpsClock = pygame.time.Clock()
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    
    customButton = Button(30, 30, 200, 50, 'Button One (onePress)', myFunction)
    customButton2 = Button(300, 200, 400, 100, 'Button One ', lambda: print(100))

    # Game loop.
    while True:
        screen.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        customButton.process(screen)
        customButton2.process(screen)

        pygame.display.flip()
        fpsClock.tick(fps)