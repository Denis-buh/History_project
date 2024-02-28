



# Тип данных проект
class Project_file:
    def __init__(self, sp_names = [], sp_put = [], sp_comment = [], sp_dir = [], put_for_proj = None, var_combo = None):
        if not isinstance(sp_names, list) or not isinstance(sp_put, list) or not isinstance(sp_comment, list):
            raise TypeError("Данные должны быть экземплярами класса list")
        elif not isinstance(put_for_proj, str):
            raise TypeError("Путь к файлу должен быть экземпляром класса str")
        else:
            # Список имени файлов
            self.__sp_names = sp_names
            # Список пути к файлам
            self.__sp_put = sp_put
            # Список коментов к файлам
            self.__sp_comment = sp_comment
            # Путь к этому проекту файлу
            self.__put_for_proj = put_for_proj
            # Выбранный файл
            self.__var_combo = var_combo
            # Словарь директорий
            self.__sp_dir = sp_dir
        
    # Вывод при использовании print()
    def __str__(self):
        print_string = ""
        k_p = len(self.__sp_names)
        if k_p > 0:
            for i in range(k_p):
                inform = ""
                inform += "-" * 50 + "\n"
                inform += "Имя файла :" + self.__sp_names[i]
                inform += "\n"
                inform += "Путь к файлу :" + self.__sp_put[i]
                inform += "\n"
                inform += "Коментарий к файлу :" + self.__sp_comment[i]
                inform += "\n"
                inform += "-" * 50 + "\n"
                print_string += inform
        else:
            print_string = "Данные отсутствуют "
        return print_string[:-1]
            
    # Получение ячейки по индексу
    def __getitem__(self, key):
        return [self.__sp_names[key], self.__sp_put[key], self.__sp_comment[key]]
    
    def __del__(self):
        # Список имени файлов
        del self.__sp_names
        # Список пути к файлам
        del self.__sp_put
        # Список коментов к файлам
        del self.__sp_comment
        # Путь к этому проекту файлу
        del self.__put_for_proj
        # Выбранный файл
        del self.__var_combo
        # Директории
        del self.__sp_dir
    
    
    # Возращает число файлов в группе    
    def __len__(self):
        return len(self.__sp_names)
    
    # Возращает путь к проекту
    @property
    def put_for_proj(self):
        return self.__put_for_proj
    
    # Возвращение выбранного файла
    @property
    def var_combo(self):
        return self.__var_combo
    # Установка выбранного файла
    @var_combo.setter
    def var_combo(self, nimber):
        if nimber not in range(len(self.__sp_names)) and nimber != None:
            raise IndexError("Таково индекса нет")
        else:
            self.__var_combo = nimber
            
    # Список директорий
    @property
    def sp_dir(self):
        return self.__sp_dir
    # Удаляем путь папки
    def sp_dir_del(self, put):
        self.__sp_dir.pop(self.__sp_dir.index(put))
    # Добовляем путь папки
    def sp_dir_append(self, put):
        self.__sp_dir.append(put)

    # Получение списка имен или элемента из списка имен по индексу
    @property
    def names(self):
        return self.__sp_names
    # Изменение списка имен или элемента из списка имен по индексу
    @names.setter   
    def names(self, inform = None):
        self.__sp_names = inform
    
    # Получение списка путей или элемента из списка путей по индексу
    @property
    def put(self):
        return self.__sp_put
    # Изменение списка путей или элемента из списка путей по индексу
    @put.setter
    def put(self, inform = None):
        self.__sp_put = inform

    # Получение списка коментов или элемента из списка коментов по индексу
    @property
    def comment(self):
        return self.__sp_comment   
    # Изменение списка коментов или элемента из списка коментов по индексу
    @comment.setter 
    def comment(self, inform = None):
        self.__sp_comment = inform
        
    # Добавляем новый элемент
    def append(self, names = None, put = None, comment = None):
        if not isinstance(names, str) or not isinstance(put, str) or not isinstance(comment, str):
            raise TypeError("Данные должны быть экземплярами класса str")
        else:
            # Список имени файлов
            self.__sp_names.append(names)
            # Список пути к файлам
            self.__sp_put.append(put)
            # Список коментов к файлам
            self.__sp_comment.append(comment)
            
    # Удаляем элемент
    def delete(self, names = None, put = None, comment = None, index = None):
        if index == None:
            if not isinstance(names, str) or not isinstance(put, str) or not isinstance(comment, str):
                raise TypeError("Данные должны быть экземплярами класса str")
            else:
                if names in self.__sp_names and put in self.__sp_put and comment in self.__sp_comment:
                    index = self.__sp_names.index(names)
                    index1 = self.__sp_put.pop(put)
                    index2 = self.__sp_comment.pop(comment)
                    if all([index == index1 == index2, index1 == index2 == index, index2 == index == index1]):
                        # Список имени файлов
                        self.__sp_names.pop(index)
                        # Список пути к файлам
                        self.__sp_put.pop(index)
                        # Список коментов к файлам
                        self.__sp_comment.pop(index)
                    else:
                        raise IndexError("Вы не можете удалить данные разных файлов или данные отсутствуют")
                else:
                    raise IndexError("Таких данных нет в списках")
        if names == None and put == None and comment == None:
            if index not in range(len(self.__sp_names)) and index not in range(-len(self.__sp_names), 0):
                raise IndexError("Таково индекса нет")
            else:
                # Список имени файлов
                self.__sp_names.pop(index)
                # Список пути к файлам
                self.__sp_put.pop(index)
                # Список коментов к файлам
                self.__sp_comment.pop(index)


