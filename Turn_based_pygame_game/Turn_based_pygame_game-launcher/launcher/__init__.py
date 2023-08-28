



# Импорт модулей
if __name__ == "__main__":
    from GUI import *
else:
    from .GUI import *
import pickle
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt




class Launcher:
    '''Класс лаунчера'''
    def __init__(self) -> None:
        # Коэффициент масштабирования
        self.sp_scaling = ["50", "100", "150", "200"]
        # Размер экрана 
        self.sp_screen = []
        # QtWidgets.QApplication - Создает приложение 
        # QtWidgets.QWidget - Создает окно
        # Создаем приложение с передачей информации о открытых файлов 
        # 1 идет имя скрипта остальное - открытые файлы с помощью скрипта
        self.prog = QtWidgets.QApplication(sys.argv)
        self.prog.dpiawareness = 0
        # Создание окна
        self.window = QtWidgets.QMainWindow()
        self.GUI = Ui_MainWindow()
        self.GUI.setupUi(self.window)
        self.__scalling()
        self.__show_inform(self.__read_options(), self.__found_size())
        self.window.setWindowTitle("Лаунчер")
    
    def __scalling(self) -> None:
        '''Подгонка интерфейса под масштаб системы'''
        screen = self.prog.screens()[0]
        scalling = screen.logicalDotsPerInchX() / 96.0
        width = height = 360 * scalling
        self.window.setMinimumSize(QtCore.QSize(width, height))
        self.window.setMaximumSize(QtCore.QSize(width, height))
    
    def show(self) -> None:
        '''Данный метод показывает окно лаунчера'''
        # Корректное отображение окна
        self.window.show()
        # Корректное отображение окна
        self.prog.exec()

    def __read_options(self) -> dict:
        '''Данный метод получает словарь из файла параметров'''
        try:
            file = open("launcher\\options.conf", "rb")
            options = pickle.load(file)
            file.close
        except:
            options = {}
        return options
    
    def __found_size(self) -> list:
        '''Ищем размер экрана у пользователя и возвращаем список возможных размеров'''
        screen = self.prog.screens()[0]
        screen = screen.size()
        width, height = screen.width(), screen.height()
        
        #for screen in self.prog.screens():
        #    screen = screen.size()
        #    print(screen)
        #    screen_width, screen_height = screen.width(), screen.height()
        #    if screen_width > width:
        #        width, height = screen_width, screen_height

        if (width / 4) * 3 == height:
            res = ["{0}x{1}".format(str(4 * i), str(3 * i)) for i in range(200, int((width / 4) + 1), 20)]
        elif (width / 16) * 9 == height:
            res = ["{0}x{1}".format(str(16 * i), str(9 * i)) for i in range(60, int((width / 16) + 1), 20)]
        else:
            res = ["{0}x{1}".format(str(16 * i), str(9 * i)) for i in range(60, int((width / 16) + 1), 20)]
            
        return res 
    
    def __show_inform(self, options:dict, options_size:list) -> None:
        '''Записывает словарь из файла параметров на элементы интерфейса'''
        self.sp_screen = options_size
        
        try:
            # Вписываем коэффициент масштабирования
            for i in self.sp_scaling:
                self.GUI.block_scaling.addItem(i)

            if options['block_scaling'] in self.sp_scaling:
                self.GUI.block_scaling.setCurrentIndex(self.sp_scaling.index(options['block_scaling']))
            else:
                self.GUI.block_scaling.setCurrentIndex(1)
        except: self.GUI.block_scaling.setCurrentIndex(1)
        
        try:
            # Вписываем размер экрана 
            for i in self.sp_screen:
                self.GUI.size.addItem(i)

            if options['size'] in self.sp_screen:
                self.GUI.size.setCurrentIndex(self.sp_screen.index(options['size']))
            else:
                self.GUI.size.setCurrentIndex(len(self.sp_screen) -1)
        except: self.GUI.size.setCurrentIndex(len(self.sp_screen) -1)
        
        try:
            # Вписываем FPS
            self.GUI.FPS.setValue(options['FPS'])
        except: self.GUI.FPS.setValue(30)
        
        try:
            if options['checkBox']:
            # Вписываем состояние лаунчера после запуска игры
                self.GUI.checkBox.setCheckState(Qt.Checked)
        except: self.GUI.checkBox.setCheckState(Qt.Checked)
        
    def connect(self, command, FPS:int=30) -> None:
        '''Добавляет функции на элементы интерфейса'''
        self.GUI.write_to_file.clicked.connect(self.__write_file)
        self.GUI.defolt_options.clicked.connect(lambda: self.__made_defolt_options(FPS))
        self.GUI.run_game.clicked.connect(command)
        
    def __made_defolt_options(self, FPS:int=30) -> None:
        '''Устанавливает настройки по умолчанию'''
        self.GUI.block_scaling.setCurrentIndex(1)
        self.GUI.size.setCurrentIndex(0)
        self.GUI.FPS.setValue(FPS)
        self.GUI.checkBox.setCheckState(Qt.Checked)
        
    def __write_file(self) -> None:
        '''Данный метод записывает информацию с лаунчера в файл'''
        dict_options = {'size': self.GUI.size.currentText(), 
                        'block_scaling': self.GUI.block_scaling.currentText(), 
                        'FPS': self.GUI.FPS.value(),
                        'checkBox': self.GUI.checkBox.checkState() == Qt.Checked}
        file =  open('launcher\\options.conf', 'wb')
        pickle.dump(dict_options, file)
        file.close()
        
    def get_inform(self) -> list:
        '''Возвращает информацию с окна в виде списка где\n
        0 - размер окна игры : list\n
        1 - коэффициент масштабирования объектов в игре : int\n
        2 - Как часто обновлять экран в игре : int\n
        3 - Выключить лаунчер после запуска игры : bool'''
        res = []
        res.append([int(i) for i in self.GUI.size.currentText().split("x")])
        res.append(int(self.GUI.block_scaling.currentText()))
        res.append(self.GUI.FPS.value())
        res.append(self.GUI.checkBox.checkState() == Qt.Checked)
        return res
        
    def made_write_options(self) -> None:
        '''Проверяет опции на изменение'''
        old_options = self.__read_options()
        try:
            if old_options['size'] != self.GUI.size.currentText():
                res = True
            elif old_options['block_scaling'] != self.GUI.block_scaling.currentText():
                res = True

            elif old_options['FPS'] != self.GUI.FPS.value():
                res = True

            elif old_options['checkBox'] != self.GUI.checkBox.checkState():
                res = True
            else:
                res = False
        except:
            res = True
        
        if res:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Question)
            # Указываем заголовок
            msg.setWindowTitle("Изменение фала параметров")
            # Указываем текст всплывающего окна 
            msg.setText('Согласны ли вы переписать файл параметров?')
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            # Для коректного отображения
            msg.exec()
            if msg.result() == QtWidgets.QMessageBox.Yes:
                self.__write_file()

    def destroy(self) -> None:
        '''Закрываем лаунчер'''
        # Убиваем QApplication
        self.prog.closeAllWindows()
        
    def __del__(self) -> None:
        '''Удаляем лаунчер'''
        self.destroy()
        del self.sp_scaling
        del self.sp_screen
        del self.prog
        del self.window
        del self.GUI