import pygame
from pygame.locals import *
from Game import *
# from launcher import *
from PIL import Image


class Main:
    def launcher(self) -> None:
        '''Необходима для запуска и получения инфы из лаунчера'''
        # Тестовые значения
        size : list = [1280, 720]
        block_scaling : int = 100
        fps : int = 30
        block_size : int = self.load_image(size, block_scaling)
        self.game(size, fps, block_size)
        
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
            
            "hil": pygame.image.load("images\\hil\\{name}.png".format(name = name)),
            "coin": [pygame.image.load("images\\coin\\0\\{name}.png".format(name = name)),
                     pygame.image.load("images\\coin\\45\\{name}.png".format(name = name)),
                     pygame.image.load("images\\coin\\90\\{name}.png".format(name=name)),
                     pygame.image.load("images\\coin\\135\\{name}.png".format(name=name))
                     ]
        }
        return name
        
    def command_last_game(self) -> None: '''Необходима для запуска лаунчера после игры'''

    def game(self, size:list=[1280, 720], fps:int=30, block_size:int=50) -> None:
        '''
        Необходима для взаимодействия с игрой\n
        size - список указывающий размеры окна игры\n
        fps - обозначает частоту обновления экрана [кадр/сек]\n
        block_size - размер блока
        '''

        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.display.set_caption('Игра')
        
        clock_fps = pygame.time.Clock()
        
        screen = pygame.display.set_mode(size)

        pygame.mixer.music.load('sounds/determination.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        s_bit = pygame.mixer.Sound('sounds/bit.ogg')
        s_bit.set_volume(0.1)
        s_potion = pygame.mixer.Sound('sounds/potion.ogg')
        s_potion.set_volume(0.1)
        s_coin = pygame.mixer.Sound('sounds/coin.ogg')
        s_coin.set_volume(0.1)

        game = Game(self.image, size, block_size)
        res = game.show_menu(screen, clock_fps)
        
        game_process = True
        while game_process:
            # Если в меню выбрали закрыть меню
            if res == "break":
                break

            if game.board.player.hp <= 0:
                dead = True
                while dead:

                    f1 = pygame.font.SysFont('arial', 30)
                    text1 = f1.render('Вы погибли', 1, (255, 0, 0))
                    text2 = f1.render(f'Ваш счет: {game.board.player.score}', 1, (255, 0, 0))
                    text3 = f1.render('Нажмите любую клавишу чтобы продолжить', 1, (255, 0, 0))

                    screen.blit(text1, (round(size[0] / 4), round(size[1] / 4)))
                    screen.blit(text2, (round(size[0] / 4), round(size[1] / 4) + 32))
                    screen.blit(text3, (round(size[0] / 4), round(size[1] / 4) + 64))

                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game_process = False
                            dead = False
                            break

                        if event.type == KEYDOWN:
                            save = game.board.savepoint.get_cur_num_of_lvl()
                            game.show_test_level(save[0])
                            dead = False
                            break
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_process = False
                    break
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if game.board.player.attack():
                            game.board.player.turn += 1
                            s_bit.play()
                
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        res = game.show_menu(screen, clock_fps)
                        
                    elif event.key == K_UP or event.key == K_w:
                        if game.board.player.moving(y=-1):
                            game.board.player.turn += 1
                            
                    elif event.key == K_DOWN or event.key == K_s:
                        if game.board.player.moving(y=1):
                            game.board.player.turn += 1
                            
                    elif event.key == K_RIGHT or event.key == K_d:
                        if game.board.player.moving(x=1):
                            game.board.player.turn += 1
                            
                    elif event.key == K_LEFT or event.key == K_a:
                        if game.board.player.moving(x=-1):
                            game.board.player.turn += 1

                    elif event.key == K_e:
                        item = game.board.player.take()
                        if item == 1:
                            s_potion.play()
                            game.board.player.turn += 1
                        elif item == 2:
                            s_coin.play()
                            game.board.player.turn += 1
                    elif event.key == K_SPACE:
                        game.board.player.turn += 1

                    elif event.key == K_n or event.key == K_RETURN:
                        if game.board.savepoint.check():
                            save = game.board.savepoint.get_cur_num_of_lvl()
                            if save[0] + 1 < len(game.levels):
                                game.show_test_level(game.board.savepoint.make_save(save))
                            else:
                                winner = True
                                while winner:
                                    
                                    f1 = pygame.font.SysFont('arial', 30)
                                    text1 = f1.render('Вы полностью прошли игру!', 1, (255, 0, 0))
                                    text2 = f1.render(f'Ваш счет: {game.board.player.score}', 1, (255, 0, 0))
                                    text3 = f1.render('Нажмите любую клавишу для начала новой игры', 1, (255, 0, 0))

                                    screen.blit(text1, (round(size[0] / 4), round(size[1] / 4)))
                                    screen.blit(text2, (round(size[0] / 4), round(size[1] / 4) + 32))
                                    screen.blit(text3, (round(size[0] / 4), round(size[1] / 4) + 64))


                                    pygame.display.update()
                                    
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            game_process = False
                                            winner = False
                                            break
                                        
                                        if event.type == KEYDOWN:
                                            game.board.savepoint.make_save([0, 100, 0], 0)
                                            game.show_test_level(0)
                                            winner = False
                                            break
         
            if res == "break":
                break 
            game.run(screen)
            clock_fps.tick(fps)
            # смена (отрисовка) кадра:
            pygame.display.flip()
        # Убираем экран игры
        pygame.quit()


# Основная функция для работы с программой
def main():
    program_main = Main()
    program_main.launcher()
    
    try:
        program_main.command_last_game()
    except: ...


if __name__ == "__main__":
    main()
