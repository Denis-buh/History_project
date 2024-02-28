



# Импорт необходимых модулей
from PyQt5 import *
from PyQt5.QtWidgets import *
from .inform_who import Ui_Form
from datetime import *


class inform_who:
    def __init__(self, close_command, *infrom, **sp_names):
        # Команда на закрытие
        self.close_command = close_command
        self.sp_names = sp_names
        self.window = QWidget()
        self.file_GUI = Ui_Form()
        self.file_GUI.setupUi(self.window)
        self.window.setWindowTitle("Library")
        self.window.setLayout(self.file_GUI.box_main)
        self.window.show()
        
        if not  self.sp_names["new"]:
            self.name_taker, self.Name_book = infrom[0], infrom[1]
        self.show_inform(*infrom)

    # Показываем полученную информацию
    def show_inform(self, *infrom):
        if self.sp_names["new"]:
            try:
                self.file_GUI.sb_how_math.setValue(1)
                self.file_GUI.sb_time_to_have.setValue(1)
                
                sp = []
                for i in infrom[0]:
                    sp.append(i[0])
                self.file_GUI.cb_names_book.addItems(sp)
                try:
                    self.file_GUI.cb_names_book.setCurrentIndex(sp.index(infrom[0]))
                except:
                    pass
                
            except:
                self.file_GUI.cb_names_book.addItems([])
        else:
            try:
                self.file_GUI.le_name_taker.setText(str(infrom[0]))
            except:
                self.file_GUI.le_name_taker.setText("")

            try:
                sp = []
                for i in infrom[8]:
                    sp.append(i[0])
                self.file_GUI.cb_names_book.addItems(sp)
                try:
                    self.file_GUI.cb_names_book.setCurrentIndex(sp.index(infrom[1]))
                except:
                    pass
            except:
                self.file_GUI.cb_names_book.addItems([])
            
            try:
                self.file_GUI.le_telephon.setText(str(infrom[2]))
            except:
                self.file_GUI.le_telephon.setText("")
                
            try:
                self.file_GUI.le_class.setText(str(infrom[3]))
            except:
                self.file_GUI.le_class.setText("")
                
            try:
                self.file_GUI.sb_how_math.setValue(int(infrom[4]))
            except:
                self.file_GUI.sb_how_math.setValue(1)
                
            try:
                year, month, day = infrom[5].split("-")
                self.file_GUI.de_time_start.setDate(datetime.date(int(year), int(month), int(day)) )
            except:
                pass
                
            try:
                self.file_GUI.sb_time_to_have.setValue(int(infrom[6]))
            except:
                self.file_GUI.sb_time_to_have.setValue(1)
        # Сейчас Календарь
        self.file_GUI.pb_now.clicked.connect(self.show_now)
        # Сохранить кнопка
        self.file_GUI.pb_save.clicked.connect(lambda: self.window_close(True))
        # Закрыть кнопка
        self.file_GUI.pb_close.clicked.connect(lambda: self.window_close(False))
        
    # Показываем дату на данный момент
    def show_now(self):
        dt = datetime.today()
        dt.date()
        self.file_GUI.de_time_start.setDate(dt)
        
    # Получаем информацию из окна
    def get_inform(self):
        # Время из виджета
        dt = self.file_GUI.de_time_start.date()
        # Время взятия книги
        time =  date(dt.year(), dt.month(), dt.day()) 
        # Срок взятия книги
        hov_have = self.file_GUI.sb_time_to_have.value()

        if (hov_have % 12) == 0:
            res = dt.month() + hov_have
            mon = dt.month()
            yea = res // 12
        if (hov_have % 12) != 0:
            res = dt.month() + hov_have
            if res % 12 == 0:
                mon = 12
            else:
                mon = (dt.month() + (hov_have % 12)) % 12
            yea = res // 12
        # Время возврата книги
        time_to_return = date(dt.year() + yea, mon, dt.day()) 
        # Имя берущего книгу
        name_taker = self.file_GUI.le_name_taker.text()
        if len(name_taker) == 0:
            raise ValueError
        # Класс берущего книгу
        klass = self.file_GUI.le_class.text()
        if len(klass) == 0:
            raise ValueError
        # Сколько взял
        len_take = self.file_GUI.sb_how_math.value()
        if len_take < 0:
            raise TypeError

        if self.sp_names["new"]:
            return  [name_taker,
                     self.file_GUI.cb_names_book.currentText(),
                     self.file_GUI.le_telephon.text(),
                     klass,
                     self.file_GUI.sb_how_math.value(),
                     time,
                     hov_have, 
                     time_to_return]
        else:
            return  [name_taker,
                     self.file_GUI.cb_names_book.currentText(),
                     self.file_GUI.le_telephon.text(),
                     klass,
                     self.file_GUI.sb_how_math.value(),
                     time,
                     hov_have, 
                     time_to_return,
                     self.name_taker, 
                     self.Name_book]
    
    # Закрытие окна
    def window_close(self, save_fleg):
        if save_fleg:
            try:
                self.close_command(self.sp_names["new"], *self.get_inform())
                del self.window
            except ValueError:
                msg = QMessageBox()
                # Указываем тип ошибки (Значок). Конструкция: QMessageBox."Искать нужное в документации"
                msg.setIcon(QMessageBox.Warning)

                msg.setText("Введите данные")
                # Указываем текст всплывающего окна 
                # Для коректного отображения
                msg.exec_()
                
            except TypeError:
                msg = QMessageBox()
                # Указываем тип ошибки (Значок). Конструкция: QMessageBox."Искать нужное в документации"
                msg.setIcon(QMessageBox.Warning)

                msg.setText("Введены не верные данные ")
                msg.exec_()
        else:
            del self.window