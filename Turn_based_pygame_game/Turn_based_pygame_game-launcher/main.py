



# Импорт модулей
import pygame
from pygame.locals import *
from launcher import *
from PIL import Image





# Данный класс необходим для совмещения лаунчера и игры 
# Основной класс 
class Main:
    def launcher(self) -> None:
        '''Необходима для запуска и получения инфы из лаунчера'''
        self.class_launcher = Launcher()
        self.class_launcher.connect(self.get_launcher, 30)
        self.class_launcher.show()

    def get_launcher(self) -> None:
        '''Данная функция необходима для получения информации с лаунчера'''
        size, block_scaling, FPS, checkBox = self.class_launcher.get_inform()
        
        self.class_launcher.made_write_options()

        self.class_launcher.destroy()
        del self.class_launcher
        if not checkBox:
            self.command_last_game = main
        self.game(size, FPS, self.load_image(size, block_scaling))
        
    def load_image(self, size:int, block_scaling:int=100) -> int:
        '''Необходима для выбора текстур по параметрам из лаунчера '''
        
        if block_scaling == 50:
            name = 25
        elif block_scaling == 100:
            name = 50
        elif block_scaling == 150:
            name = 75
        elif block_scaling == 200:
            name = 100
        
        image = Image.open("images\\Menu_fon\\fon.jpg")
        new_image = image.resize(size)
        new_image.save('images\\fon_cash.jpg')

        self.image = {
            "floor_grass": pygame.image.load("images\\floor\\grass\\{name}.png".format(name = name)),
            "floor_stone": pygame.image.load("images\\floor\\stone\\{name}.png".format(name = name)),
            "floor_tree": pygame.image.load("images\\floor\\tree\\{name}.png".format(name = name)),
            
            "obstacles_stone": pygame.image.load("images\\obstacles\\stone\\{name}.png".format(name = name)),
            "obstacles_tree": pygame.image.load("images\\obstacles\\tree\\{name}.png".format(name = name)),
            
            "wall_stone": pygame.image.load("images\\wall\\stone\\{name}.png".format(name = name)),
            "wall_tree": pygame.image.load("images\\wall\\tree\\{name}.png".format(name = name)),
            
            "actor": pygame.image.load("images\\hero\\{name}.png".format(name = name)),
            
            "fon": pygame.image.load("images\\fon_cash.jpg"),
            
            "save_point": pygame.image.load("images\\save_point\\{name}.png".format(name = name)),
            
            "opponent": pygame.image.load("images\\opponent\\{name}.png".format(name = name)),
        }
        return name
        
    def command_last_game(self) -> None: '''Необходима для запуска лаунчера после игры'''

        
        
    def game(self, size:list=[1280, 720], fps:int=30, block_size:int=50) -> None:
        '''Необходима для взаимодействия с игрой\n
        size - список указывающий размеры окна игры\n
        fps - обозначает частоту обновления экрана [кадр/сек]\n
        block_size - размер блока'''
        
        #some code


# Основная функция для работы с программой
def main():
    program_main = Main()
    program_main.launcher()
    
    try:
        program_main.command_last_game()
    except: ...


    
    
if __name__ == "__main__":
    main()