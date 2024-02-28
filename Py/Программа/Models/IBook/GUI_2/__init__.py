



# Импорт библиотек
from .inform_book_GUI import *
from .Command_Table import Command_Table
from .Command_GUI import Command_GUI
from .Close_save import Close_save
from PyQt5.QtWidgets import QWidget


class Book_GUI_2(Command_GUI, Command_Table, Close_save):
    def __init__(self, window, GUI_window, sp_widget_book, book_GUI_3):
        # Основное окно 
        self.window = window
        # GUI настройки основного окна
        self.GUI_window = GUI_window
        # Список виджетов для основного окна
        self.sp_widget_book = sp_widget_book
        # Класс GUI окон 3 порядка
        self.book_GUI_3 = book_GUI_3
        
    # Добавляем функции к кнопкам
    def connect(self, file_GUI):
        file_GUI.bt_show_have_book.clicked.connect(self.show_who_take)
        file_GUI.bt_append.clicked.connect(self.append_image)
        file_GUI.bt_oth.clicked.connect(self.made_othet)

    # Показываем вкладку в основном окне
    def show(self, name_tab_book, name_book, con, cur):
        window = QWidget()
        name_book, type_book, inform_book, image_book, have_book = self.get_inform(cur, name_book) 
        
        file_GUI = inform_book_GUI.Ui_Form()
        file_GUI.setupUi(window)
        
        window.setLayout(file_GUI.main_box)
        how_take = self.found_who_take(cur, name_book)
        self.inform_show(file_GUI, name_book, type_book, inform_book, image_book, have_book, how_take)
        self.connect(file_GUI)
        self.GUI_window.show_tab(window, name_tab_book)
        self.sp_widget_book.append([window, file_GUI, name_book, con, cur])
        
    # случилось отображение новой книги
    def show_to_append(self, con, cur):
        window = QWidget()
        
        file_GUI = inform_book_GUI.Ui_Form()
        file_GUI.setupUi(window)
        
        window.setLayout(file_GUI.main_box)

        self.inform_show(file_GUI, "Новая книга", "", "", b"0", 0, 0)
        self.connect(file_GUI)
        self.GUI_window.show_tab(window, "Новая книга")
        self.sp_widget_book.append([window, file_GUI, "", con, cur])
        
