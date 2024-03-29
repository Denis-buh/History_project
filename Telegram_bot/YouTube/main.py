



from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import mixins
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from random import choice
from const import *
from modle.Files import * # NET_ERROR, LINK_ERROR, FORMAT_ERROR
from modle.command_bd import *
# from modle.User.file import NET_ERROR, LINK_ERROR


# Экземпляр бота
bot = Bot(TOKEN)
# Диспечер бота. Отсеживает сообщения
dp = Dispatcher(bot)
# Подключаемся к БД
con, cur = connect_bd("db\\user.db")
# maid_bd(con, cur)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    '''Помощь для пользователя '''
    await message.reply(TEXT_FOR_HELP, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    '''Приветствие пользователя '''
    # Список стикеров для приветствия пользователя
    sp = ["static//img/lili_hello.png", "static//img/lili.png"]
    # Стикер приветствия
    await message.answer_sticker(open(choice(sp), 'rb'))
    # Список приветствий для пользователя
    sp = ["Добро пожаловать,", "Привет,", "Привет, пользователь"]
    # Пишем  приветствие для пользователя
    await message.answer("{hello} {user}!".format(user = message.from_user.first_name, 
                                                               hello = choice(sp)))
    # await bot.send_message(message.chat.id, "Я {bot}, могу скачивать видео и аудио".format(bot = bot.get_me().first_name))
    await message.answer("Я Lili, могу скачивать видео и аудио из социальный сетей")
    await dowload(message)


@dp.message_handler(commands=['dowload'])
async def dowload(message: types.Message):
    '''Перезапуск функции скачки'''
    message.text = ""
    await wright(message, True)


@dp.message_handler(content_types=["text"])
async def wright(message: types.Message, flag:bool=False):
    '''Необходима для взаимодействия с пользователем'''
    # Класс пользователя. Получаем с БД
    # id - id пользователя
    id = message.from_user.id
    file = get_iser(cur, id)
    if file == None:
        # Если юзера нет в системе
        file = File()
        append_user(con, cur, id, file)
    
    if flag:
        "Перезапуск функции скачки"
        file.reset()
    
    # Флаг первичного запроса данных
    flag = False
    
    if file.stage == 0:
        # Если выбор соц. сети
        if message.text != "":
            "После того как пользователь ввел соц сеть"
            try:
                file.append_net(message.text)
                await message.answer("Вы выбрали: {0}".format(message.text))
                flag = True
            # НЕ УДАЛЯТЬ
            # except NET_ERROR:
            #     await message.answer("Выбрана не верная социальная сеть. Выберете из предложенных")
            except Exception as er:
                await message.answer(er)
        else:
            "До того как пользователь ввел соц сеть"
            # resize_keyboard - адаптация под интерфейс
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3) # default - False
            b1, b2, b3 = KeyboardButton('YouTube'), KeyboardButton('TikTok'), KeyboardButton('VK')
            markup.add(b1, b2, b3)
            await message.answer("Из какой социальной сети будем что-либо скачивать:", reply_markup=markup)
            
    if file.stage == 1:
        # Если ввод ссылки
        if flag:
            # Удаляем кнопки
            hideBoard = ReplyKeyboardRemove()
            await message.answer("Введите ссылку: ", reply_markup=hideBoard)
        else:
            try:
                '''После того, как пользователь ввел ссылку'''
                file.append_link(message.text)
                await message.answer("Вы ввели следующею ссылку: {0}".format(message.text))
                flag = True
            # НЕ УДАЛЯТЬ
            # except LINK_ERROR:
            #     await message.answer("Введена не допустимая ссылка")
            #     await message.answer("Введите ссылку: ")
            except Exception as er:
                '''Недопустимая ссылка'''
                await message.answer(er)
                await message.answer("Введите ссылку: ")
            
    if file.stage == 2:
        # Если ввод формата файла
        if file.net == "YouTube":
            if flag:
                markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
                for i in file.class_net.format():
                    # Добавляем на кнопки форматы
                    markup.insert(KeyboardButton(i))
                await message.answer("Выберете необходимый вам формат файла", reply_markup=markup)
            else:
                try:
                    '''После того, как пользователь ввел формат файла'''
                    await message.answer("Вы ввели следующий формат : {0}".format(message.text))
                    file.sheck_format(message.text)
                    flag = True
                except FORMAT_ERROR:
                    await message.answer("Введен недопустимый формат файла. Выберете из предложенных")
                except Exception as er:
                    '''Недопустимый формат файла'''
                    await message.answer(er)
    
    if file.stage == "question_format":
        # Согласны ли вы изменить формат
        if file.net == "YouTube":
            if flag:
                await message.answer("Данный формат является аудио дорожкой. Согласны ли вы изменить формат (да/нет)?")
            else:
                file.check_question_format()
        
    if file.stage == 3:
        # Если ввод типа файла
        if file.net == "YouTube":
            if flag:
                if file.class_net.found_vidio() and file.class_net.found_audio():
                    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                    markup.add(KeyboardButton("Видео")).insert(KeyboardButton("Аудио"))
                    await message.answer("Выберете необходимый вам тип файла", reply_markup=markup)
                if file.class_net.found_audio() and not file.class_net.found_vidio():
                    file.append_type("audio")
                    flag = True
                if file.class_net.found_vidio() and not file.class_net.found_audio():
                    file.append_type("video")
                    flag = True
            else:
                #try:
                    file.append_type(message.text)
                    flag = True
                # НЕ УДАЛЯТЬ
                # except TYPE_ERROR:
                #     await message.answer("Выбран не верный тип. Выберете из предложенных")
                #except Exception as er:
                #    '''Недопустимый тип файла'''
                #    await message.answer(er)
                
    if file.stage == 4:
        # Выбор бит рейда у аудио дорожки или выбор разрешения видео
        if file.net == "YouTube":
            if flag:
                if file.class_net.found_audio():
                    files = file.inform_audio()
                    
                if file.class_net.found_vidio():
                    files = file.inform_vidio()

                markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
                for i in files:
                    markup.add(KeyboardButton(i))
                await message.answer("Выберете файл по следующим параметрам", reply_markup=markup)
            else:
                #try:
                    if file.class_net.found_audio():
                        dowload_file = file.dowload_audio(message.text)
                    if file.class_net.found_vidio():
                        dowload_file = file.dowload_audio(message.text)
                        
                    await bot.send_document(message.from_user.id, dowload_file)
                    flag = True
                    message.text = ""
                    file.reset()
            # НЕ УДАЛЯТЬ
            # except TYPE_ERROR:
            #     await message.answer("Выбран не верный тип. Выберете из предложенных")
            #except Exception as er:
            #    '''Недопустимый тип файла'''
            #    await message.answer(er)
        


        
        
        
    # Сохранение изменений в БД
    uppdete_user(con, cur, id, file)


if __name__ == "__main__":
    # Старт бота
    executor.start_polling(dp)
    


# t.me/liliindexsbot - ссылка на бота