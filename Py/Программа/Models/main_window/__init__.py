



import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from .Window_GUI import *
from .Tab import *



class main_window:
    def __init__(self, window, command=None, *sp_arg, **sp_name_args):
        # command=None - команда на закрытие
            # *sp_arg - ее порядковые аргументы
            # **sp_name_args - ее именые аргументы
        self.window = window
        # Окно для лояутов
        self.form_widget = QWidget()
        self.GUI = Ui_MainWindow()
        self.TAB = MyTab(self.form_widget, command, *sp_arg, **sp_name_args)
        self.TAB.made_tab()
        
        
    # Показываем интерфейс окна
    def show(self):
        self.GUI.setupUi(self.window)
        self.slov = {"menu_menu_help": self.GUI.menu_help,
                     "menu_made_proj": self.GUI.made_proj,
                     "menu_made_ibok": self.GUI.made_ibok,
                     "menu_import_file": self.GUI.import_file,
                     "menu_file_save": self.GUI.file_save, }
                     #"file_sample_1": self.GUI.file_sample_1,
                     #"file_sample_2": self.GUI.file_sample_2}
        
    # Подключаем функции к меню окна
    def connect(self, **connect_slow):
        #.triggered.connect(qApp.quit)
        for i in connect_slow:
            self.slov[i].triggered.connect(connect_slow[i])

    # Демонстрируем поле для вкладок
    def made_tab(self):
        self.window.setCentralWidget(self.form_widget)
    
    # Демонстрируем новые вкладки
    def show_tab(self, widow, name = "Безымянная"):
        if isinstance(widow, QWidget) and name != "":
            self.TAB.append_tab(widow, str(name))
        elif isinstance(widow, QWidget):
            self.TAB.append_tab(widow, "Безымянная")
        else:
            print('Должно быть подано QWidget и str')
    
    # Закрываем активную вкладку
    def close_tab(self):
        self.TAB.closeActivTab()
    
    # Делаем функцию для изменения доп команды на закрытие
    def new_command(self, command=None, *sp_arg, **sp_name_args):
        self.TAB.new_command(command, *sp_arg, **sp_name_args)
        
    # 
    def context_command(self, slov):
        self.TAB.get_close_context(slov)
        

        
        