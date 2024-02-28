



import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt



class MyTab:
    def __init__(self, window, command=None, *sp_arg, **sp_name_args):
        # command=None - команда на закрытие
            # *sp_arg - ее порядковые аргументы
            # **sp_name_args - ее именые аргументы
        self.command, self.sp_arg, self.sp_name_args = command, sp_arg, sp_name_args
        self.window = window
        self.const_slov = {}
        
    # Делаем поле для вкладок
    def made_tab(self):
        self.tabwdg = QTabWidget()
        # Контекстное меню
        self.tabwdg.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabwdg.customContextMenuRequested.connect(self.show_menu_context)
        
        self.tabwdg.setTabsClosable(True) # включение отображения кнопок закрытия
        self.tabwdg.tabCloseRequested.connect(self.closeTab) # связывание сигнала нажатия на "крестик" с обработчиком
        box = QVBoxLayout()
        box.addWidget(self.tabwdg)
        self.window.setLayout(box)
        
    # Добавлем команды с словарь для контекстного меню
    def get_close_context(self, slov):
        self.const_slov = slov
    
    # показываем контекстное меню на вкладку
    def show_menu_context(self, point):
        # Создание меню
        self.menu = qtw.QMenu(self.tabwdg)
        
        for i in self.const_slov:
            # Сообщение в контекстном меню
            action = self.menu.addAction(i)
            # Команда для контекстного меню
            action.triggered.connect(self.const_slov[i])
        self.menu.exec(self.window.mapToGlobal(point))
        
    # Добавление вкладок
    def append_tab(self, window, name = "Безымянная"):
        # Добавление вкладок
        self.tabwdg.addTab(window, name)
         
    # Закрываем активную вкладку
    def closeActivTab(self):
        activ_tab_ind = self.tabwdg.currentIndex()
        self.closeTab(activ_tab_ind)

    # Закрываем вкладку по крестику
    def closeTab(self, ind):
        print(ind)
        if self.command != None:
            res = self.command(index=ind, *self.sp_arg, **self.sp_name_args) != True
            if res:
                self.tabwdg.removeTab(ind)
        else:
            self.tabwdg.removeTab(ind)
        # метод закрывает вкладку под номером ind
        
        
    # Получаем индекс вкладки
    def get_ind(self):
        # Получаем индекс вкладки
        return self.tabwdg.currentIndex()
        
    # Делаем функцию для изменения доп команды на закрытие
    def new_command(self, command=None, *sp_arg, **sp_name_args):
        # command=None - команда на закрытие
            # *sp_arg - ее порядковые аргументы
            # **sp_name_args - ее именые аргументы
        self.command, self.sp_arg, self.sp_name_args = command, sp_arg, sp_name_args
        
    def show_tab_for_index(self, index):
        self.tabwdg.setCurrentIndex(index)
        
