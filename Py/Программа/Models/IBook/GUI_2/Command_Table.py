



class Command_Table:
    # Получаем информацию с названия книги
    def get_inform(self, cur, Name_book):
        return cur.execute('''select * from inform
                           where Name_book= "''' + str(Name_book) + '"').fetchall()[0]
        
    # Узнаем о должниках
    def found_who_take(self, cur, name_book):
        # произвобим обход таблицы с информацией о книгах для вывода имен книг
        res = cur.execute('''select who_take.how_math
                          from who_take
                          where who_take.Name_book = "{0}";'''.format(name_book)).fetchall()
        if len(res) == 0:
            return 0
        else:
            suma = 0
            for i in range(len(res)):
                suma += res[i][0]
            return suma