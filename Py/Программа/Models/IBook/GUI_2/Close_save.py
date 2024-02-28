



from PyQt5.QtWidgets import QMessageBox


class Close_save:
    # Если сохранение по вкладке
    def save_tab(self, vidget):
        print("save")
        try:
            window, file_GUI, name_book, con, cur  = vidget
            new_name_book, type_book, inform_book, how_have, image = self.return_inform(file_GUI)

            # Если случилась новая книга
            if name_book == "":
                # Получаем имена всех книг
                names_book = cur.execute('select Name_book from inform;').fetchall()
                for i in names_book:
                    if new_name_book in i:
                        inform = "Данная книга уже есть в списке. Книга не будет добавлена"
                        raise AssertionError
                if type_book == None:
                    inform = "Вы не указали класс книги. Книга не будет добавлена"
                    raise AssertionError

                cur.execute('''INSERT INTO inform (Name_book, type_book, inform_book, image_book, have_book)
                            VALUES (?, ?, ?, ?, ?);''',(new_name_book, type_book, inform_book, image, how_have))
            # Если не случилась новая книга
            else:
                cur.execute('''UPDATE inform SET 
                            Name_book = ?,
                            type_book = ?,
                            inform_book = ?,
                            image_book = ?,
                            have_book = ?
                                where inform.Name_book = ?;''', (new_name_book, type_book, inform_book, image, how_have, name_book))
                cur.execute('''UPDATE who_take SET 
                            Name_book = ?
                                where who_take.Name_book = ?;''', (new_name_book, name_book))
        except AssertionError:
            msg = QMessageBox()
            # Указываем тип ошибки (Значок). Конструкция: QMessageBox."Искать нужное в документации"
            msg.setIcon(QMessageBox.Critical)
            # Указываем текст всплывающего окна 
            msg.setText(inform)
            # Для коректного отображения
            msg.exec_()
            
    

