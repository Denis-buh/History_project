import pickle


class Len_Error(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Len_Error, {0} '.format(self.message)
        else:
            return 'Len_Error'
        
class Player_Error(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Player_Error, {0} '.format(self.message)
        else:
            return 'Player_Error'

class Save_point_Error(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Save_point_Error, {0} '.format(self.message)
        else:
            return 'Save_point_Error'
        
        
class Flager_Error(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Flager_Error, {0} '.format(self.message)
        else:
            return 'Flager_Error'


simvol_floor = [".", ",", "/"]
simvol_obstacles = ["#", "$"]
simvol_wall = [":", ";"]
simvol_player = "@"
simvol_save_point = "s"

simvoles = [".", ",", "/", "#", "$", ":", ";", "@", "s"]


class Map:
    '''Класс уровня'''
    def __init__(self):
        '''Инициализирует класс и создает список для строчек уровня'''
        self.list = []
        # Количество актеров (Всего возможно только 1 за весь уровень) False - количество = 0
        self.flag_actor = False
        # Количество save_point (Всего возможно только 1 за весь уровень) False - количество = 0
        self.flag_save_point = False
        # Длина чстрочки для уровня
        self.len_level = None
        
    def get_flag(self) -> tuple:
        '''Возвращает кортеж из flag_actor, flag_save_point'''
        return self.flag_actor, self.flag_save_point
    
    def append_string(self, level_string:str):
        '''Добавляет к уровню строку '''
        if len(level_string) != self.len_level and self.len_level != None:
            # print("Строчка имеет не правильную длину. Данная строка отклонена")
            raise Len_Error


        if simvol_player in level_string:
            if self.flag_actor:
                # Если актер уже был добавлен и он есть в строке
                # print("Актер уже был добавлен. Данная строка отклонена:")
                raise Player_Error
            elif level_string.count(simvol_player) > 1:
                # Если количество актеров более 1 в строке
                # print("Более одного актера в строке. Данная строка отклонена")
                raise Player_Error
            else:
                self.flag_actor = True
            
            
        if simvol_save_point in level_string:  
            if self.flag_save_point:
                # print("Точка сохранения уже была добавлена. Данная строка отклонена")
                raise Save_point_Error
            elif level_string.count(simvol_save_point) > 1:
                # print("Более одной точки сохранения в строке. Данная строка отклонена")
                raise Save_point_Error
            else:
                self.flag_save_point = True
            
        sp_string_level = []
        for i in level_string:
            if i not in simvoles:
                # print("Данный символ \'{0}\' нельзя использовать в уровне. Данная строка отклонена".format(str(i)))
                return 
            else:
                sp_string_level.append(i)
        else:
            # print("Данная строка записана ")
            self.len_level = len(level_string)
            self.list.append(sp_string_level)
            
    def append_list(self, *sp):
        for i in sp:
            stri = "".join(i)
            # print("Добавление строки:\n{0}".format(stri))
            self.append_string(stri)
        
            
    def get_map(self) -> list:
        '''Возвращает карту'''
        return self.list 
            


class Writer:
    '''Класс для записи уровней в файл'''
    def __init__(self, roat_file:str) -> None:
        '''Инициализирует класс и открывает файл в режиме перезаписи'''
        try:
            file = open(roat_file, "rb")
            self.old_inform = pickle.load(file)
            print(self.old_inform)
            file.close()
        except:
            self.old_inform = {}
        self.file = open(roat_file, "wb")
        # Список уровней
        self.list_level = []
        
    def append(self, maper:Map)-> None:
        if all(maper.get_flag()):
            self.list_level.append(maper.get_map())
        else:
            print("На карте отсутствует герой или точка сохранения. Уровень не добавлен")
            print("Уровень")
            for i in maper.get_map():
                print(i) 
            raise Flager_Error
        #print("Уровни")
        #for i in self.list_level:
        #    print(i)
        
            
    def save(self):
        pickle.dump(self.list_level, self.file)
        self.file.close()
        
        
    def __len__(self):
        return len(self.list_level)


if __name__ == "__main__":
    # Класс для добавления уровней
    list_levels = Writer("levels.levl")
    # Уровень 1
    lvl1 = Map()
    lvl1.append_list(['.', '.', '.', '#', '#', '#', '.', '.', '.', '.', '.'],
                     ['.', '.', '#', '#', '.', '#', '.', '#', '#', '#', '#'],
                     ['.', '#', '#', '.', '.', '#', '#', '#', '.', '.', '#'],
                     ['#', '#', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
                     ['#', '.', '.', '.', '@', '.', '.', '#', '.', '.', '#'],
                     ['#', '#', '#', '.', '.', '#', '#', '#', '.', '.', '#'],
                     ['.', '.', '#', '.', '.', '#', '.', '.', '.', '.', '#'],
                     ['.', '#', '#', '.', '#', '#', '.', '#', '.', '#', '#'],
                     ['.', '#', '/', '.', '.', '.', '/', '.', 's', '#', '.'],
                     ['.', '#', '.', '.', '.', '.', '.', '#', '#', '.', '.'],
                     ['.', '#', '#', '#', '#', '#', '#', '#', '.', '.', '.'])
    list_levels.append(lvl1)
    
    # Уровень 2
    lvl2 = Map()
    lvl2.append_list(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                     ['#', '#', '/', '.', '.', '.', '.', '.', '.', '.', '/', '#', '#', '.', '/', '.', '.', '.', '@', '#'],
                     ['#', '.', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '#', '.', '.', '.', '.', '.', '.', '#'],
                     ['#', '.', '#', '.', '.', '/', '.', '.', '.', '.', '.', '.', '#', '#', '#', '.', '.', '.', '.', '#'],
                     ['#', '.', '#', '/', '.', '.', '.', '.', '.', '.', '.', '.', '/', '.', '.', '.', '.', '.', '.', '#'],
                     ['#', '/', '#', '.', '.', '.', '.', '.', '/', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '#'],
                     ['#', '.', '.', '#', '#', '#', '#', '#', '#', '#', '.', '#', '.', '.', '#', '.', '.', '.', '.', '#'],
                     ['#', '#', 's', '.', '.', '/', '.', '.', '.', '.', '/', '.', '.', '#', '#', '.', '.', '.', '.', '#'],
                     ['.', '#', '#', '#', '#', '#', '#', '#', '#', '.', '.', '.', '#', '#', '.', '.', '.', '.', '.', '#'],
                     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])
    list_levels.append(lvl2)
    
    
    # Уровень 3
    lvl3 = Map()
    lvl3.append_list(['#', '#', '#', '#', '#', '#', '#'],
                     ['#', '#', '.', '.', '.', '@', '#'],
                     ['#', '#', '.', '.', '.', '.', '#'],
                     ['#', '#', '.', '.', '.', '.', '#'],
                     ['#', '#', '/', '.', '.', '.', '#'],
                     ['#', '#', '.', '.', '.', '.', '#'],
                     ['#', '#', '.', '.', '.', '.', '#'],
                     ['#', '#', '/', '.', '.', '.', '#'],
                     ['#', 's', '/', '/', '/', '.', '#'],
                     ['#', '#', '#', '#', '#', '#', '#'])
    list_levels.append(lvl3)
    
    # Уровень 4
    lvl4 = Map()
    lvl4.append_list(['#', '#', '#', '#', '#', '#', '#', '#'],
                     ['.', '#', '.', '.', '.', '.', '.', '#'],
                     ['.', '#', '.', '.', '@', '.', '.', '#'],
                     ['.', '#', '#', '.', '#', '.', '#', '#'],
                     ['.', '#', '.', '.', '#', '.', '/', '#'],
                     ['.', '#', '.', '.', '#', '.', '.', '#'],
                     ['.', '#', '.', '/', '#', '.', '.', '#'],
                     ['#', '#', '.', '#', '#', '.', '#', '#'],
                     ['#', '.', '/', '.', '.', '/', '.', '#'],
                     ['#', '/', '.', '.', '.', '.', '/', '#'],
                     ['#', '#', '#', '.', '.', '/', 's', '#'],
                     ['#', '#', '#', '#', '#', '#', '#', '#'])
    list_levels.append(lvl4)
    
    
    # Уровень 5
    lvl5 = Map()
    lvl5.append_list(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                     ['#', '#', '#', '#', '/', '.', '#', '/', 's', '#', '#'],
                     ['#', '#', '#', '#', '.', '.', '.', '/', '/', '#', '#'],
                     ['#', '.', '.', '.', '.', '#', '.', '.', '.', '/', '#'],
                     ['#', '/', '.', '.', '.', '.', '/', '.', '.', '.', '#'],
                     ['#', '#', '#', '/', '#', '.', '#', '.', '#', '/', '#'],
                     ['#', '.', '.', '.', '.', '.', '.', '/', '.', '.', '#'],
                     ['#', '.', '.', '/', '.', '#', '.', '.', '.', '.', '#'],
                     ['#', '.', '#', '#', '.', '/', '.', '.', '/', '#', '#'],
                     ['#', '@', '#', '#', '.', '.', '#', '.', '.', '#', '#'],
                     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])
    list_levels.append(lvl5)
    


    list_levels.save()
