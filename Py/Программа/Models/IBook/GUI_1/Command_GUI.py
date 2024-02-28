



from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem


class Command_Book_GUI_1:
    # Открываем книгу
    def current_item_changed(self):
        # Узнаем действующую вкладку
        ind = self.GUI_window.TAB.get_ind()
        vidget = self.sp_widget_book[ind]
        window, file_GUI, db, con, cur = vidget
        try:
            # Получаем выбраную строку
            row = file_GUI.view.currentRow()
            # Пулучаем элемент таблицы (строка, колонка). Получаем имя книги
            name_book = file_GUI.view.item(row, 0).text()
            name_tab_book = "Книга: " + name_book
            self.book_GUI_2.show(name_tab_book, name_book, con, cur)
        except AttributeError:
            msg = QMessageBox()
            # Указываем тип ошибки (Значок). Конструкция: QMessageBox."Искать нужное в документации"
            msg.setIcon(QMessageBox.Warning)
            # Указываем текст всплывающего окна 
            msg.setText("Вы не выбрали книгу!")
            # Для коректного отображения
            msg.exec_()
            
    # Удалить выбранное
    def del_focus(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        # Указываем текст всплывающего окна 
        msg.setText("Согласны ли вы удалить книгу?")
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.exec_()
        if msg.result() == QMessageBox.Yes:
            # Узнаем действующую вкладку
            ind = self.GUI_window.TAB.get_ind()
            vidget = self.sp_widget_book[ind]
            window, file_GUI, db, con, cur = vidget
            try:
                # Получаем выбраную строку
                row = file_GUI.view.currentRow()
                # Пулучаем элемент таблицы (строка, колонка). Получаем имя книги
                name_book = file_GUI.view.item(row, 0).text()
                cur.execute('''DELETE FROM inform
                            where Name_book = "{0}";'''.format(name_book))
                self.show_new_inform()
            except AttributeError:
                msg = QMessageBox()
                # Указываем тип ошибки (Значок). Конструкция: QMessageBox."Искать нужное в документации"
                msg.setIcon(QMessageBox.Warning)
                # Указываем текст всплывающего окна 
                msg.setText("Вы не выбрали книгу!")
                # Для коректного отображения
                msg.exec_()
                
    # Добавить книгу
    def append_book(self):
        # Узнаем действующую вкладку
        ind = self.GUI_window.TAB.get_ind()
        vidget = self.sp_widget_book[ind]
        window, file_GUI, db, con, cur = vidget
        self.book_GUI_2.show_to_append(con, cur)

  
    # Обновить таблицу
    def show_new_inform(self, fleg=False, ind=None):
        # Узнаем действующую вкладку
        if isinstance(ind, int):
            vidget = self.sp_widget_book[ind]
        else:
            ind = self.GUI_window.TAB.get_ind()
            vidget = self.sp_widget_book[ind]
        window, file_GUI, db, con, cur = vidget
        if fleg:
            self.made_names(cur)
            self.show_inform(file_GUI, self.get_names(cur))
        else:
            self.found_book()
        
    # Найти
    def found_book(self, ind=None):
        # Узнаем действующую вкладку
        if isinstance(ind, int):
            vidget = self.sp_widget_book[ind]
        else:
            ind = self.GUI_window.TAB.get_ind()
            vidget = self.sp_widget_book[ind]
        window, file_GUI, db, con, cur = vidget
        name = file_GUI.le_name.text().strip()
        type_book = file_GUI.le_type.text().strip()
        self.show_new_inform(True, ind=ind)
        res = cur.execute('''select * FROM name
                          where Name_book LIKE "%{0}%"  and type_book LIKE "%{1}%";'''.format(name, type_book)).fetchall()
        self.del_names(cur)
        # Создаем таблицу с именами
        cur.execute('''CREATE TABLE name (
                    Name_book STRING PRIMARY KEY
                                     UNIQUE,
                    type_book STRING,
                    have_book INT
                    );''')
        for i in res:
            cur.execute('''INSERT INTO name (Name_book, type_book, have_book)
                        VALUES ("{0}", "{1}", "{2}");'''.format(*i))
        self.show_inform(file_GUI, self.get_names(cur))
        
    # Заполняем таблицу полученными элементами
    def show_inform(self, file_GUI, inform):
        file_GUI.view.setRowCount(len(inform))
        try:
            file_GUI.view.setColumnCount(len(inform[0]))
            # Заполнили таблицу полученными элементами
            for i, elem in enumerate(inform):
                for j, val in enumerate(elem):
                    file_GUI.view.setItem(i, j, QTableWidgetItem(str(val)))
            file_GUI.view.setHorizontalHeaderLabels(['Имя книги', 'Класс книги', 'Сколько осталось'])
        except IndexError:
            file_GUI.view.setColumnCount(3)