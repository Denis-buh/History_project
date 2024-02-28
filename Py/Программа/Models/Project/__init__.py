



import sys
import os
from PyQt5 import *
from PyQt5.QtWidgets import *
from .Open_Close_pproj import * 
from .Project_file import *
from .Pproj_GUI import *


# Клас для дополнений класса Project
class __Append_pproj:
    # Функция для кнопки "Удалить с проекта" в окне проекта
    def delete_for_proj(self):
        # Узнаем действующую вкладку
        ind = self.GUI_window.TAB.get_ind()
        vidget = self.text_widgets[ind]
        window, file_GUI, name_proj, file_proj = vidget
        # Получаем выбранный элемент в списке (Как текс(элемент списка))
        ind_text = file_GUI.name_file.currentText()
        # Получаем индекс из класса проекта
        try:
            index = file_proj.names.index(ind_text)
            file_GUI.name_file.clear() 
            file_GUI.text_file.clear()
            file_proj.var_combo = 0
            file_proj.delete(index = index)
            file_GUI.name_file.addItems(file_proj.names) 
            file_GUI.text_file.insertPlainText(file_proj.comment[file_proj.var_combo])
        except:
            file_GUI.text_file.insertPlainText("Вы удалили все файлы с проекта!\n")
            file_proj.var_combo = None
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В проекте нет файлов! Вы удалили все файлы с проекта!")
            msg.exec_()
        # "Вы удалили все файлы с проекта!"
        
    def show_dir(self): 
        # Узнаем действующую вкладку
        ind = self.GUI_window.TAB.get_ind()
        vidget = self.text_widgets[ind]
        window, file_GUI, name_proj, file_proj = vidget
        # Получаем выбранный элемент в списке (Как текс(элемент списка))
        ind_text = file_GUI.name_file.currentText()
        # Получаем индекс из класса проекта
        try:
            index = file_proj.names.index(ind_text)
        except:
            return
        put_file = file_proj.put_for_proj + "\\" + file_proj.put[index]
        if put_file.count(":") > 1:
            put_file = file_proj.put[index]
        if "." in put_file:
            put_file = "\\".join(put_file.split("\\")[:-1])
        print(put_file)
        os.startfile(put_file)

    # Функция для кнопки "Открыть" в окне проекта
    def open_for_proj(self):
        # Узнаем действующую вкладку
        ind = self.GUI_window.TAB.get_ind()
        vidget = self.text_widgets[ind]
        window, file_GUI, name_proj, file_proj = vidget
        # Получаем выбранный элемент в списке (Как текс(элемент списка))
        ind_text = file_GUI.name_file.currentText()
        # Получаем индекс из класса проекта
        try:
            index = file_proj.names.index(ind_text)
        except:
            return
        put_file = file_proj.put_for_proj + "\\" + file_proj.put[index]
        if put_file.count(":") > 1:
            put_file = file_proj.put[index]
        # Проверка на существования пути
        if os.path.exists(put_file):
            if ".ibook" in put_file:
                self.ibook.open(put_file)
                #self.dicti_options.read_write(name = combo.get().split(".")[0], fleg_proj = put_file)
            elif ".projp" in put_file:
                self.open(put_file)
            else:
                os.startfile(put_file)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Не правильный путь файла. \nЖелаете ли вы указать новый путь к файлу?")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.exec_()
            if msg.result() != QMessageBox.No:
                if file_proj.put[index] in file_proj.sp_dir:
                    self.append_dir(flag_open="dir", inform=file_proj.comment[index])
                    file_proj.sp_dir_del(file_proj.put[index])
                else:
                    self.append_file_for_proj(flag_open="file", inform=file_proj.comment[index])
                file_proj.delete(index = index)
                file_GUI.name_file.clear() 
                file_GUI.name_file.addItems(file_proj.names) 
            else:
                file_proj.delete(index = index)
                file_GUI.name_file.clear() 
                file_GUI.text_file.clear()
                file_GUI.name_file.addItems(file_proj.names)
                if len(file_proj) > 0:
                    file_proj.var_combo = 0
                    file_GUI.text_file.insertPlainText(file_proj.comment[0])    

    # Функция для кнопки "Добавить файл" в окне проекта
    def append_file_for_proj(self, flag_open=None, inform=None):
        if flag_open == "file":
            put_files = [QFileDialog.getOpenFileName(self.window, 'Открытие файлов', '')[0]]
        else:
            put_files = QFileDialog.getOpenFileNames(self.window, 'Открытие файлов', '')[0]
        
        for put_file in put_files:
            put_file = put_file.replace("/", "\\")
            if len(put_file) != 0:
                # Узнаем действующую вкладку
                ind = self.GUI_window.TAB.get_ind()
                vidget = self.text_widgets[ind]
                window, file_GUI, name_proj, file_proj = vidget
                if file_proj.put_for_proj in put_file:
                    flege = True
                    # [1:] - Необходимо для избавления крайне левой \
                    put_file = put_file.replace(file_proj.put_for_proj, "")[1:]
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Файл, который вы собираетесь добавить не имеет общей папки с проектом из-"+
                                "за чего придется записывать полный путь вместо относительного." +
                                "\nПри перемещении добавляемого файла он будет не доступен. Вы согласны продолжить?")
                    msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
                    msg.exec_()
                    flege = msg.result() != QMessageBox.No
                if flege:
                    name = put_file.split("\\")[-1]
                    if put_file not in file_proj.put:
                        if flag_open == "file" and inform != None:
                            file_proj.append(names = name, put = put_file, comment = inform)
                        else:
                            file_proj.append(names = name, put = put_file, comment = "")
                        if name in file_proj.names:
                            # Переименовка имен в пути
                            for i in file_proj.names:
                                if file_proj.names.count(i) > 1:
                                    file_proj.names[ind] = file_proj.put[ind]
                                ind += 1
                        if file_proj.var_combo == None:
                            file_proj.var_combo = 0
                        file_GUI.name_file.clear() 
                        file_GUI.name_file.addItems(file_proj.names) 
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText('Данный файл уже есть в проекте.')
                        msg.exec_()
                else:
                    continue
        
    # Добавление директории
    def append_dir(self, flag_open=None, inform=None):
        if flag_open == "dir":
            put_files = [QFileDialog.getExistingDirectory(self.window, 'Открытие директории', '')]
        else:
            put_files = [QFileDialog.getExistingDirectory(self.window, 'Открытие директории', '')]
        for put_file in put_files:
            put_file = put_file.replace("/", "\\")
            if len(put_file) != 0:
                # Узнаем действующую вкладку
                ind = self.GUI_window.TAB.get_ind()
                vidget = self.text_widgets[ind]
                window, file_GUI, name_proj, file_proj = vidget
                if file_proj.put_for_proj in put_file:
                    flege = True
                    # [1:] - Необходимо для избавления крайне левой \
                    put_file = put_file.replace(file_proj.put_for_proj, "")[1:]
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Директория, которую вы собираетесь добавить не имеет общей папки с проектом из-"+
                                "за чего придется записывать полный путь вместо относительного." +
                                "\nПри перемещении добавленной директории она будет не доступена. Вы согласны продолжить?")
                    msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
                    msg.exec_()
                    flege = msg.result() != QMessageBox.No
                if flege:
                    name = put_file.split("\\")[-1]
                    if put_file not in file_proj.put:
                        if flag_open == "dir" and inform != None:
                            file_proj.append(names = name, put = put_file, comment = inform)
                        else:
                            file_proj.append(names = name, put = put_file, comment = "")
                        file_proj.sp_dir_append(put_file)
                        if name in file_proj.names:
                            # Переименовка имен в пути
                            for i in file_proj.names:
                                if file_proj.names.count(i) > 1:
                                    file_proj.names[ind] = file_proj.put[ind]
                                ind += 1
                        if file_proj.var_combo == None:
                            file_proj.var_combo = 0
                        file_GUI.name_file.clear() 
                        file_GUI.name_file.addItems(file_proj.names) 
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText('Данная директория уже есть в проекте.')
                        msg.exec_()
                else:
                    continue


class Pproj(__Append_pproj):
    def __init__(self, window, GUI_window, text_widgets, ibook):
        # Основное окно 
        self.window = window
        # GUI настройки основного окна
        self.GUI_window = GUI_window
        # Список виджетов для основного окна
        self.text_widgets = text_widgets
        self.ibook = ibook
        
    # Делаем новый проект
    def made(self):
        try:
            name_proj, *inform = proj_made(self.window)
            file_proj = Project_file(*inform)
            self.GUI(name_proj, file_proj)
        except ValueError:
            pass

    # Открываем проект
    def open(self, put_file):
        try:
            name_proj, *inform = proj_open(put_file)
            file_proj = Project_file(*inform)
            self.GUI(name_proj, file_proj)
        except:
            pass
        #put_file = filedialog.askopenfilenames(filetypes = (("Все",("*.dicti","*.proj")),("Dictionary","*.dicti"),("Project","*.proj"),("Прочее", ("*"))))
    
    def save(self, vidget): save(vidget)
        
    def close(self, vidget): close(vidget)

    # Для сохранения описания при перелистовании
    def save_comment_list_combo(self, text):
        # Узнаем действующую вкладку
        ind = self.GUI_window.TAB.get_ind()
        vidget = self.text_widgets[ind]
        window, file_GUI, name_proj, file_proj = vidget
        try:
            file_proj.comment[file_proj.var_combo] = file_GUI.text_file.toPlainText()
            file_proj.var_combo = file_proj.names.index(text)
            file_GUI.text_file.clear()
            file_GUI.text_file.insertPlainText(file_proj.comment[file_proj.var_combo])
        except:
            if file_GUI.text_file.toPlainText() == "Вы удалили все файлы с проекта!\n":
                file_GUI.text_file.clear()
            file_proj.var_combo = file_proj.names.index(text)

    # Конектим кнопки проекта к функциям
    def connect(self, file_GUI):
        # file_GUI.name_file - отвечает за файлы (листать файлы)
        # file_GUI.append_file   "Добавить файл"
        # file_GUI.append_dir   "Добавить папку"
        # file_GUI.bt_del   "Удалить из проекта"
        # file_GUI.open   "Открыть"
        #file_GUI.name_file.clicked.connect(lambda:print("листать файлы"))
        file_GUI.name_file.activated[str].connect(self.save_comment_list_combo)
        file_GUI.append_file.clicked.connect(self.append_file_for_proj)
        file_GUI.append_dir.clicked.connect(self.append_dir)
        file_GUI.bt_del.clicked.connect(self.delete_for_proj)
        file_GUI.open.clicked.connect(self.open_for_proj)
        file_GUI.open_dir.clicked.connect(self.show_dir)
        
    def GUI(self, name_proj, file_proj):
        window = QWidget()
        file_GUI = Ui_Form()
        file_GUI.setupUi(window)
        window.setLayout(file_GUI.main_box)
        # Конектим кнопки проекта к функциям
        self.connect(file_GUI)
        self.GUI_window.show_tab(window, name_proj)
        self.text_widgets.append([window, file_GUI, name_proj, file_proj])
        if len(file_proj) > 0:
            file_proj.var_combo = 0
            file_GUI.name_file.addItems(file_proj.names) 
            file_GUI.text_file.insertPlainText(file_proj.comment[file_proj.var_combo])
            
        
        
    