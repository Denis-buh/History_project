



from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from .GUI import inform_who


class Command_GUI:
    # Открываем должника
    def current_item_changed(self):
        # Узнаем действующую вкладку
        ind = self.GUI_window.TAB.get_ind()
        vidget = self.sp_widget_book[ind]
        window, file_GUI, con, cur = vidget
        try:
            # Получаем выбраную строку
            row = file_GUI.view.currentRow()
            # Пулучаем элемент таблицы (строка, колонка). Получаем имя книги
            inform = (file_GUI.view.item(row, 0).text(), file_GUI.view.item(row, 1).text(), 
                      file_GUI.view.item(row, 2).text(), file_GUI.view.item(row, 3).text(),
                      file_GUI.view.item(row, 4).text(), file_GUI.view.item(row, 5).text(),
                      file_GUI.view.item(row, 6).text(), file_GUI.view.item(row, 7).text())
            Names_books = cur.execute('''select inform.Name_book
                                      from inform;''').fetchall()
            
            self.window_inform = inform_who(self.close, *inform, Names_books, new = False)
            
        except AttributeError:
            msg = QMessageBox()
            # Указываем тип ошибки (Значок). Конструкция: QMessageBox."Искать нужное в документации"
            msg.setIcon(QMessageBox.Warning)
            # Указываем текст всплывающего окна 
            msg.setText("Вы не выбрали должника!")
            # Для коректного отображения
            msg.exec_()
            
    # Закрытие окна
    def close(self, fleg_new_close=False, *inform):
        if len(inform) != 10 and len(inform) != 8:
            return
        # Узнаем действующую вкладку
        ind = self.GUI_window.TAB.get_ind()
        vidget = self.sp_widget_book[ind]
        window, file_GUI, con, cur = vidget

        
        if fleg_new_close:
            print("hydgcd")
            cur.execute('''INSERT INTO who_take 
                        (name_taker, Name_book, telephon, class, how_math, time_start, time_to_have, time_finish)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);''', (inform[0], inform[1], inform[2], inform[3], inform[4], inform[5], inform[6], inform[7]))
        else:
            old_name_taker, old_Name_book = inform[8:]
            inform = inform[:8]
            cur.execute('''UPDATE who_take SET 
                        name_taker = ?, 
                        Name_book = ?,
                        telephon = ?,
                        class = ?,
                        how_math = ?,
                        time_start = ?,
                        time_to_have = ?,
                        time_finish = ?
                        where Name_book = "{0}" and name_taker = "{1}";'''.format(old_Name_book, old_name_taker), 
                        (inform[0], inform[1], inform[2], inform[3], inform[4], inform[5], inform[6], inform[7]))
        self.show_new_inform()
        self.window_inform = None

        

    
    # Добавить должника
    def append_who(self):
        print("Добавить должника+")
        # Узнаем действующую вкладку
        ind = self.GUI_window.TAB.get_ind()
        vidget = self.sp_widget_book[ind]
        window, file_GUI, con, cur = vidget
        Names_books = cur.execute('''select inform.Name_book
                                  from inform;''').fetchall()
        self.window_inform = inform_who(self.close, Names_books, new = True)

    
    # Удалить выбранное
    def del_focus(self):
        print("Удалить должника")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        # Указываем текст всплывающего окна 
        msg.setText("Согласны на удаление ?")
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.exec_()
        if msg.result() == QMessageBox.Yes:
            # Узнаем действующую вкладку
            ind = self.GUI_window.TAB.get_ind()
            vidget = self.sp_widget_book[ind]
            window, file_GUI, con, cur = vidget
            try:
                # Получаем выбраную строку
                row = file_GUI.view.currentRow()
                # Пулучаем элемент таблицы (строка, колонка). Получаем имя книги
                name_taker, name_book = file_GUI.view.item(row, 0).text(), file_GUI.view.item(row, 1).text()
                file_GUI.view.removeRow(row)
                cur.execute('''DELETE FROM who_take
                            where Name_book = "{0}" and name_taker = "{1}";'''.format(name_book, name_taker))
                self.show_new_inform()
            except AttributeError:
                msg = QMessageBox()
                # Указываем тип ошибки (Значок). Конструкция: QMessageBox."Искать нужное в документации"
                msg.setIcon(QMessageBox.Warning)
                # Указываем текст всплывающего окна 
                msg.setText("Вы не выбрали строки на удаление!")
                # Для коректного отображения
                msg.exec_()
    


  
    # Обновить таблицу
    def show_new_inform(self, fleg=False, ind=None):
        # Узнаем действующую вкладку
        if isinstance(ind, int):
            vidget = self.sp_widget_book[ind]
        else:
            ind = self.GUI_window.TAB.get_ind()
            vidget = self.sp_widget_book[ind]
        window, file_GUI, con, cur = vidget
        if fleg:
            self.show_inform(file_GUI, self.get_who_take(cur))
        else:
            self.found_book()
        
    # Найти , ind=None
    def found_book(self):
        ## Узнаем действующую вкладку
        #if isinstance(ind, int):
        #    vidget = self.sp_widget_book[ind]
        #else:
        ind = self.GUI_window.TAB.get_ind()
        vidget = self.sp_widget_book[ind]
        print(vidget)
        window, file_GUI, con, cur = vidget
        name = file_GUI.le_name.text().strip()
        class_who = file_GUI.le_class.text().strip()
        #self.show_new_inform(True)
        res = cur.execute('''select * FROM who_take
                          where name_taker LIKE "%{0}%"  and class LIKE "%{1}%";'''.format(name, class_who)).fetchall()
        self.show_inform(file_GUI, res)

    
    
    
    
    # Заполняем таблицу полученными элементами
    def show_inform(self, file_GUI, inform):
        file_GUI.view.setRowCount(len(inform))
        try:
            file_GUI.view.setColumnCount(len(inform[0]))
            # Заполнили таблицу полученными элементами
            for i, elem in enumerate(inform):
                for j, val in enumerate(elem):
                    file_GUI.view.setItem(i, j, QTableWidgetItem(str(val)))
            file_GUI.view.setHorizontalHeaderLabels(['ФИО', 'Название книги', 'Телефон', 'Класс', 'Сколько взято', 'Когда взял', 'Срок (в месяцах)', 'Когда нужно вернуть'])
        except IndexError:
            file_GUI.view.setColumnCount(8)