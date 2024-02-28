




import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
import pickle

# Создать проект
def proj_made(window):
        while True:
            filename = QFileDialog.getSaveFileName(window, 'Предварительное сохранение проекта', 'Новый проект',
                                                   'projp (*.projp)')[0]
            if len(filename) > 0:
                filename = filename.replace("/", "\\")
                
                file_read = {"Names_files": [],
                             "put_file": [],
                             "comment_file": [],
                             "dir": []}
                file = open(filename, "wb")
                pickle.dump(file_read, file)
                file.close()
                
                pu_proj = "\\".join(filename.split("\\")[:-1])
                name_proj, sp_names, sp_put, sp_comment = filename.split("\\")[-1], [], [], []
                sp_dir = []
                if len(name_proj) == 0:
                    name_proj = "Безымянный"
                return name_proj, sp_names, sp_put, sp_comment, sp_dir, pu_proj
            else:
                msg = QMessageBox()
                # Указываем тип ошибки (Значок). 
                # Конструкция: QMessageBox."Искать нужное в документации"
                msg.setIcon(QMessageBox.Warning)
                # Указываем заголовок
                msg.setText("Вы не ввели путь сохранения проекта. Желаете ли вы произвести повторную попытку ввода пути?")
                # Используемые кнопки. Конструкция: QMessageBox.
                # "Искать нужное в документации" | QMessageBox."Искать нужное в документации"
                msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
                # Для коректного отображения
                msg.exec_()
                # Получаем результат в 10-ричной системе счисления. 
                # Чтоб сравнивать нужно в документации найти нужную кнопку и ее код в 16-ричной системе счисления
                if msg.result() == QMessageBox.No:
                    raise ValueError("Введите путь к проекту")


# Импортировать проект
def proj_open(put_file):
    if "/" in put_file:
        put_file = put_file.replace("/", "\\")
    pu_proj = "\\".join(put_file.split("\\")[:-1])
    name_proj = put_file.split("\\")[-1]
    if len(put_file) != 0:
        file_read = pickle.load(open(put_file, "rb"))
        sp_names = file_read["Names_files"]
        sp_put = file_read["put_file"]
        sp_comment = file_read["comment_file"]
        sp_dir = file_read["dir"]
        return name_proj, sp_names, sp_put, sp_comment, sp_dir, pu_proj
    
# Сохранение проекта
def save(vidget):
    window, file_GUI, name_proj, file_proj = vidget
    try:
        index = file_proj.names.index(file_GUI.name_file.currentText())
        file_proj.comment[index] = file_GUI.text_file.toPlainText()
        file_read = {"Names_files": file_proj.names,
                     "put_file": file_proj.put,
                     "comment_file": file_proj.comment,
                     "dir": file_proj.sp_dir}
        file = open(file_proj.put_for_proj + "\\" + name_proj, "wb")
        pickle.dump(file_read, file)
        file.close()
    except ValueError:
        file_read = {"Names_files": [],
                     "put_file": [],
                     "comment_file": [],
                     "dir": []}
        file = open(file_proj.put_for_proj + "\\" + name_proj, "wb")
        pickle.dump(file_read, file)
        file.close()

# Закрытие проекта
def close(vidget):
    window, file_GUI, name_proj, file_proj = vidget
    del window, file_GUI, name_proj, file_proj