



# Импорт необходимых модулей
import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
import shutil
# My модули
from Models import *
from Models.main_window import *
from Models.Project import *
from Models.IBook import *
import webbrowser


class Help:
    def __init__(self, winow, GUI_window, text_widgets):
        self.window, self.GUI_window = winow, GUI_window
        self.text_widgets = text_widgets
        self.slow = {}
        
    def show_manu(self):
        self.GUI_window.GUI.menu_help.addAction('Открытие файлов в программе', lambda: webbrowser.open('https://youtu.be/UhBek94FsU8', new=2))  
        self.GUI_window.GUI.menu_help.addAction('Сохранение файлов в программе', lambda: webbrowser.open("https://youtu.be/HKNtOmRo28E", new=2))  
        
        
class Samples:
    
    good_put = "\\".join(sys.argv[0].split("\\")[:-1]) + "\\"
    
    good_put = good_put.split(":")
    good_put = ":".join([good_put[0].upper(), good_put[1]])
    def copi_class(self):
        print("class")
        put_files = QFileDialog.getExistingDirectory(self, 'Открытие директории', '')
        print(put_files)
        print(self.good_put)
        print(os.listdir(path=self.good_put + "samples\\Классы"))   
        print(put_files.replace("/", "\\") + "\\Классы")
        # print(shutil.copytree(self.good_put + "samples\\Классы", put_files.replace("/", "\\") + "\\Классы"))
        # рекурсивно копирует всё дерево директорий с корнем в src, возвращает директорию назначения.
        
        
        
    def copi_book(self):
        print("book")
        put_files = QFileDialog.getExistingDirectory(self, 'Открытие директории', '')
        print(put_files)
        print(self.good_put)
        print(shutil.copytree(self.good_put + "samples\\Методические пособия", put_files.replace("/", "\\") + "\\Методические пособия"))


# Класс основного окна
class Program(QMainWindow, Samples):
    def __init__(self, sp=[]):
        # QApplication - Создает приложение 
        super().__init__()
        # Создание окна
        #self.window = QMainWindow()
        self.setAcceptDrops(True)
        #self.samples = Samples()
        # Список виджетов для основного окна
        self.text_widgets = []
        # Область добавления виджетов для окна
        self.GUI_window = main_window(self, self.close)
        self.GUI_window.show()
        # Демонстрируем поле для вкладок
        self.GUI_window.made_tab()
        # Инициализация класса для работы с книгами
        self.ibook = IBook(self, self.GUI_window, self.text_widgets, main_window)
        
        # Инициализация класса для работы с проектами
        self.pproj = Pproj(self, self.GUI_window, self.text_widgets, self.ibook)
        
        self.help = Help(self, self.GUI_window, self.text_widgets)
        self.help.show_manu()
        self.setGeometry(300, 300, 1200, 600)

        # Конектим команды к меню окна
        # menu_menu_help = отвечает за "Справка"
        # menu_made_proj = отвечает за "Создать проект"
        # menu_made_ibok = отвечает за "Создать описание книги"
        # menu_import_file = отвечает за "Импортировать файл"
        # menu_file_save = отвечает за "Сохранить файл"
        self.GUI_window.connect(menu_made_proj = self.pproj.made,
                                menu_made_ibok = self.ibook.made,
                                menu_import_file =self.open,
                                menu_file_save = self.save,)
                                #file_sample_1 = self.copi_class,
                                #file_sample_2 = self.copi_book)
        # Указываем имя окна
        self.setWindowTitle("Library")
        # Корректное отображение окна
        self.open(sp)


    def dragEnterEvent(self, event):
        mime = event.mimeData()
        # Если перемещаются ссылки
        if mime.hasUrls():
            
            # Разрешаем
            event.acceptProposedAction()
        
    def dropEvent(self, event):
        # Обработка события Drop
        for url in event.mimeData().urls():
            file_name = url.toLocalFile()
            self.open([file_name])




        
    def open(self, roat_to_file=None):
        if isinstance(roat_to_file, list):
            put_files = roat_to_file
        else:
            # Выбираем множество файлов
            put_files = QFileDialog.getOpenFileNames(self, 'Открытие файла', '', 
                                                      'Все (*.ibook; *.projp);;Project (*.projp);;Book (*.ibook);;Прочее (*)')[0]
        for i in put_files:
            put_file =i.replace("/", "\\")
            if ".projp" in put_file:
                self.pproj.open(put_file)
            elif ".ibook" in put_file:
                self.ibook.open(put_file)
            else:
                os.startfile(put_file)
                
    # Функция на закрытия окна
    def closeEvent(self, event):
        if len(self.text_widgets) > 0:
            # Производим опрос
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("Желаете ли вы закрыть окно без сохранения файлов (Если нет - файлы не будут сохранены)?")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.exec_()
            # Получаем результат опроса. Если True - сохранить, False - закрыть
            res = msg.result() == QMessageBox.No
            if res:
                return
            else:
                for i in range(len(self.text_widgets)):
                    if self.close(0):
                        event.ignore()
                
    def save(self):
        # Узнаем действующую вкладку
        ind = self.GUI_window.TAB.get_ind()
        # Если нет вкладок
        if ind == -1:
            return
        vidget = self.text_widgets[ind]
        # Для проекта  projp
        if len(vidget) == 4:
            self.pproj.save(vidget)
        # 1 Тип GUI окна ibook
        if len(vidget) == 5:
            self.ibook.save()


    # Закрытие/сохранение для крестика вкладки
    def close(self, index=None):
        if isinstance(index, int):
            ind = index
        else:
            # Узнаем действующую вкладку
            ind = self.GUI_window.TAB.get_ind()
        # Если нет вкладок
        if ind == -1:
            return
        vidget = self.text_widgets.pop(ind)
        
        # Производим опрос
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Желаете ли вы сохранить файл?")
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.exec_()
        # Получаем результат опроса. Если True - сохранить, False - закрыть
        res = msg.result() == QMessageBox.Yes
        
        # Для проекта  projp
        if len(vidget) == 4:
            if res:
                self.pproj.save(vidget)
            else:
                self.pproj.close(vidget) 
        # 1 Тип GUI окна ibook
        if len(vidget) == 5:
            if res:
                return self.ibook.save_tab(vidget_main=vidget)
            else:
                self.ibook.close(vidget_main=vidget)


# Если скрипт открыт не как модуль
if __name__ == "__main__":
    if len(sys.argv) > 1:
        sp = sys.argv[1:]
    else:
        sp = []
        
    prog = QApplication(sys.argv)
    window = Program(sp)
    window.show()
    sys.exit(prog.exec())



