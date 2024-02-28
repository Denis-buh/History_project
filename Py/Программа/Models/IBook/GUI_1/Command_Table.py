



class Command_Table:
    # Создаем таблицу
    def made_names(self, cur):
        try:
            self.del_names(cur)
        except:
            pass
        # произвобим обход таблицы с информацией о книгах для вывода имен книг
        res = cur.execute('''select inform.Name_book
                    from inform;''').fetchall()
        
        # Создаем таблицу с именами
        cur.execute('''CREATE TABLE name (
                    Name_book STRING PRIMARY KEY
                                     UNIQUE,
                    type_book STRING,
                    have_book INT
                    );''')
        for i in res:
            name = i[0]
            res = cur.execute('''select how_math
                                   from who_take
                                   where Name_book ="{0}";'''.format(name)).fetchall()
            if len(res) == 0:
                not_have = 0
            else:
                not_have = 0
                for i in range(len(res)):
                    not_have += res[i][0]
                
            sp = cur.execute('''select type_book, have_book
                               from inform
                               where Name_book ="{0}";'''.format(name)).fetchall()
            type, have = sp[0]
            have = int(have) - int(not_have)
            cur.execute('''INSERT INTO name (Name_book, type_book, have_book)
                        VALUES ("{0}", "{1}", "{2}");'''.format(name, type, have))

    # Информация с таблицы
    def get_names(self, cur):
        # /* показываем таблицу имен
        return cur.execute('''select * from name;''').fetchall()
    
    # Удаляем таблицу имен
    def del_names(self, cur):
        # /* удаляем таблицу имен
        cur.execute('''DROP TABLE name; ''')
        
