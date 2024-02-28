



from .have_book_GUI import Ui_Form
from .Command_GUI import Command_GUI
from PyQt5.QtWidgets import *


class Book_GUI_3(Command_GUI):
    def __init__(self, window, GUI_window, sp_widget_book):
        # Основное окно 
        self.window = window
        # GUI настройки основного окна
        self.GUI_window = GUI_window
        # Список виджетов для основного окна
        self.sp_widget_book = sp_widget_book
        self.window_inform = None
        
    # Информация о том кто взял
    def get_who_take(self, cur):
        return cur.execute("select * from who_take").fetchall()
    
    # Показываем вкладку в окне
    def show(self, name_book, con, cur):
        window = QWidget()
        file_GUI = Ui_Form()
        file_GUI.setupUi(window)
        file_GUI.view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        window.setLayout(file_GUI.main_box)

        self.show_inform(file_GUI, self.get_who_take(cur))
        self.connect(file_GUI)
        self.GUI_window.show_tab(window, "Списки должников")
        self.sp_widget_book.append([window, file_GUI, con, cur])
        
    # Добавляем команды к кнопкам
    def connect(self, file_GUI):
        file_GUI.bt_open.clicked.connect(self.current_item_changed)
        file_GUI.bt_append.clicked.connect(self.append_who)
        file_GUI.bt_dell.clicked.connect(self.del_focus)
        file_GUI.bt_new_inform.clicked.connect(self.show_new_inform)
        file_GUI.bt_found.clicked.connect(self.found_book)
        