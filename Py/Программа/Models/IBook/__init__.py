



# Импорт библиотек
import sqlite3
from .GUI_1 import *
from .GUI_2 import *
from .GUI_3 import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *


class IBook:
    def __init__(self, window, GUI_window, text_widgets, main_window):
        # Основное окно 
        self.window = window
        # GUI настройки основного окна
        self.GUI_window = GUI_window
        # Список виджетов для основного окна
        self.text_widgets = text_widgets
        # класс окона
        self.main_window = main_window

    # Инициализируем классы окон
    def init_book_window(self, name_book):
        # Список виджетов окон книги
        sp_widget_book = []
        # Создание окна для книг
        window = QMainWindow()
        # Команды на закрытие через крестик
        GUI_window = self.main_window(window, self.save_close_for_tab)
        
        # Демонстрируем поле для вкладок
        GUI_window.made_tab()
        
        
        # Класс GUI окон 3 порядка
        book_GUI_3 = Book_GUI_3(window, GUI_window, sp_widget_book)
        # Класс GUI окон 2 порядка
        book_GUI_2 = Book_GUI_2(window, GUI_window, sp_widget_book, book_GUI_3)
        # Класс GUI окон 1 порядка
        book_GUI_1 = Book_GUI_1(window, GUI_window, sp_widget_book, book_GUI_2)
        
        
        self.text_widgets.append([GUI_window, sp_widget_book, book_GUI_1, book_GUI_2, book_GUI_3])
        self.GUI_window.show_tab(window, name_book)
        return book_GUI_1
        
        
    def made(self):
        try:
            put_file = QFileDialog.getSaveFileName(self.window, 'Открытие файла', '', 
                                                  'Book (*.ibook);;')[0]
            if len(put_file) == 0:
                return 
            if "/" in put_file:
                put_file = put_file.replace("/", "\\")
                
                con = sqlite3.connect(put_file)
                # Создание курсора
                cur = con.cursor()
                cur.execute("""CREATE TABLE who_take (
                                name_taker   STRING  NOT NULL,
                                Name_book    STRING  REFERENCES inform (Name_book) ON DELETE NO ACTION
                                                                                   ON UPDATE NO ACTION
                                                     NOT NULL,
                                telephon     INTEGER DEFAULT None,
                                class        STRING  NOT NULL,
                                how_math     INTEGER DEFAULT (1),
                                time_start   TIME    DEFAULT None,
                                time_to_have INTEGER DEFAULT (0),
                                time_finish  TIME    DEFAULT None
                            );""")
                cur.execute("""CREATE TABLE name (
                                Name_book STRING PRIMARY KEY
                                                 UNIQUE,
                                type_book STRING,
                                have_book INT
                            );""")
                cur.execute("""CREATE TABLE inform (
                                Name_book   STRING  UNIQUE
                                                    PRIMARY KEY
                                                    REFERENCES name (Name_book),
                                type_book   STRING,
                                inform_book TEXT    DEFAULT Отсутствует,
                                image_book  BLOB    DEFAULT (0),
                                have_book   INTEGER DEFAULT (0) 
                            );""")
            self.init_book_window(put_file.split("\\")[-1]).show(con, cur)
                
                
        except:
            msg = QMessageBox()
            # Указываем тип ошибки (Значок). Конструкция: QMessageBox."Искать нужное в документации"
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Невозможно создать данный файл')
            # Используемые кнопки. Конструкция: QMessageBox."Искать нужное в документации" | QMessageBox."Искать нужное в документации"
            # Для коректного отображения
            msg.exec_()
        
    def open(self, put_file):
        try:
            if "/" in put_file:
                put_file = put_file.replace("/", "\\")

            # Подключение к БД
            con = sqlite3.connect(put_file)
            # Создание курсора
            cur = con.cursor()
            
            self.init_book_window(put_file.split("\\")[-1]).show(con, cur)
        except:
            msg = QMessageBox()
            # Указываем тип ошибки (Значок). Конструкция: QMessageBox."Искать нужное в документации"
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Невозможно открыть данный файл')
            # Используемые кнопки. Конструкция: QMessageBox."Искать нужное в документации" | QMessageBox."Искать нужное в документации"
            # Для коректного отображения
            msg.exec_()
        

    def save(self):
        # Узнаем действующую вкладку основного окна
        ind = self.GUI_window.TAB.get_ind()
        # Получаем виджеты основного окна
        GUI_window, sp_widget_book, book_GUI_1, book_GUI_2, book_GUI_3 = self.text_widgets[ind]
        ind_book = GUI_window.TAB.get_ind()
        
        vidget = sp_widget_book[ind_book]

        if len(vidget) == 4:
            # Должники
            return
        elif len(vidget) == 5 and "GUI_1" in vidget:
            # GUI1
            window, file_GUI, db, con, cur = vidget
            msg = QMessageBox()
            # Указываем заголовок
            msg.setText("Для сохранения закройте файл и окна расширения")
            # Для коректного отображения
            msg.exec_()
            # Фиксируем результаты
            con.commit()
        else:
            book_GUI_2.save_tab(vidget)
            for i in sp_widget_book:
                if len(i) == 5 and "GUI_1" in i:
                    book_GUI_1.found_book(sp_widget_book.index(i))
                elif len(i) == 4:
                    book_GUI_3.found_book(sp_widget_book.index(i))
            
            
                    
    def save_tab(self, index=None, vidget_main=None):
        # Индекс 1
        ind = self.GUI_window.TAB.get_ind()
        # Если передали список из главной вкладки
        if isinstance(vidget_main, list):
            GUI_window, sp_widget_book, book_GUI_1, book_GUI_2, book_GUI_3 = vidget_main
        # Если не передали список из главной вкладки
        else:
            GUI_window, sp_widget_book, book_GUI_1, book_GUI_2, book_GUI_3 = self.text_widgets[ind]
        # Индекс 2
        if isinstance(index, int):
            ind_book = index
        else:
            ind_book = GUI_window.TAB.get_ind()
        vidget_ibook = sp_widget_book.pop(ind_book)
        # Должники
        if len(vidget_ibook) == 4:
            return
        # Основное окно
        elif (len(vidget_ibook) == 5 and "GUI_1" in vidget_ibook) or isinstance(vidget_main, list):
            # Отменяем закрытие
            if len(sp_widget_book) > 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Чтобы сохранить файл закройте вкладки с изменениями книг")
                msg.exec_()
                if isinstance(vidget_main, list):
                    self.text_widgets.insert(ind, [GUI_window, sp_widget_book, book_GUI_1, book_GUI_2, book_GUI_3])
                sp_widget_book.insert(ind_book, vidget_ibook)
                return True
            else:
                window, file_GUI, db, con, cur = vidget_ibook
                if not isinstance(vidget_main, list):
                    self.text_widgets.pop(ind)
                self.GUI_window.TAB.tabwdg.removeTab(ind)
                con.commit()
                con.close()
        else:
            book_GUI_2.save_tab(vidget_ibook)
            for i in sp_widget_book:
                if len(i) == 5 and "GUI_1" in i:
                    book_GUI_1.found_book(sp_widget_book.index(i))
                elif len(i) == 4:
                    book_GUI_3.found_book(sp_widget_book.index(i))
                    
                    
                    
    def close(self, index=None, vidget_main=None):
        # Индекс 1
        ind = self.GUI_window.TAB.get_ind()
        # Если передали список из главной вкладки
        if isinstance(vidget_main, list):
            GUI_window, sp_widget_book, book_GUI_1, book_GUI_2, book_GUI_3 = vidget_main
        # Если не передали список из главной вкладки
        else:
            GUI_window, sp_widget_book, book_GUI_1, book_GUI_2, book_GUI_3 = self.text_widgets[ind]
        # Индекс 2
        if isinstance(index, int):
            ind_book = index
        else:
            ind_book = GUI_window.TAB.get_ind()
        vidget_ibook = sp_widget_book.pop(ind_book)
        
        # Должники
        if len(vidget_ibook) == 4:
            return
        # Основное окно
        elif (len(vidget_ibook) == 5 and "GUI_1" in vidget_ibook) or isinstance(vidget_main, list):
            if not isinstance(vidget_main, list):
                self.text_widgets.pop(ind)
            self.GUI_window.TAB.tabwdg.removeTab(ind)
        else:
            return
        
        
        
        
    def save_close_for_tab(self, index=None, vidget_main=None):
        # Производим опрос
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Желаете ли вы сохранить файл?")
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.exec_()
        # Получаем результат опроса. Если True - сохранить, False - закрыть
        res = msg.result() == QMessageBox.Yes
        if res:
            print(index)
            return self.save_tab(index)
        else:
            self.close(index)
