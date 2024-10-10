import abc
from telebot import TeleBot, types

from bin.db_work import BasicDb
from bin.data_work import BasicData
from bin.markups import BasicMarkups
from bin.table import BasicTable


class BasicTgBot(abc.ABC):
    @abc.abstractmethod
    def __init__(self, token: str, data: BasicData, db: BasicDb, markups: BasicMarkups, table: BasicTable) -> None:
        pass
    
    @abc.abstractmethod
    def run(self) -> None:
        pass


class TgBot(TeleBot, BasicTgBot):
    def __init__(self, token: str, data: BasicData, db: BasicDb, markups: BasicMarkups, table: BasicTable) -> None:
        self.__markups: BasicMarkups = markups
        self.__data: BasicData = data
        self.__db: BasicDb = db
        self.__table: BasicTable = table
        
        self.__db.create_data_table()
        
        super().__init__(token)
        
        self.__commands: dict = {"Помощь": self.__help,
                                 "Начать регистрацию": self.__change_cerate_user_data,
                                 "Изменить данные": self.__change_cerate_user_data,
                                 "Мои данные": self.__show_user_data,
                                 "Оценки": self.__get_person_data,
                                 "Обновить оценки": self.__save_person_data
                                 }
        
        
    def run(self) -> None:
        self.register_message_handler(self.__start, commands=["start"])
        self.register_message_handler(self.__get_person_data, commands=["grades"])

        self.register_callback_query_handler(self.__show_person_data, func=lambda callback: callback.data in ("message", "table"))
        
        self.register_message_handler(self.__text_messages, content_types=["text"])
        
        self.polling(non_stop=True)
        # self.infinity_polling()
    
    
    def __start(self, message: types.Message) -> None:
        if self.__db.user_in_table(message.chat.id):
            markup: types.ReplyKeyboardMarkup = self.__markups.all()
            self.send_message(message.chat.id, "Вы уже зарегистрированы и можете пользоваться ботом", reply_markup=markup)
        else:
            markup: types.ReplyKeyboardMarkup = self.__markups.registration()
            self.send_message(message.chat.id, "Вы пока не зарегистрированы или ваши данные были утеряны, прйдите регистрацию", reply_markup=markup)
    
    
    def __text_messages(self, message: types.Message) -> None:
        if message.text in self.__commands:
            self.__commands[message.text](message)
        else:
            self.send_message(message.chat.id, "Сожалею, но я вас не понимаю")
            self.send_message(message.chat.id, "Можете обратиться к админу, чтоб прикрутил ИИ :)")
        
    def __help(self, message: types.Message) -> None:
        self.send_message(message.chat.id, "Обратитесь к администратору: https://t.me/l_or_not_l")
    
    
    def __change_cerate_user_data(self, message: types.Message, login: str = None, password: str = None) -> None:
        if login is None or password is None:
            self.send_message(message.chat.id, "Введите логин:")
            self.register_next_step_handler(message, self.__get_login)
            return
        
        if self.__db.user_in_table(message.chat.id):
            self.__db.update_log_pas(message.chat.id, login, password)
            self.__data.delete_cookies_marks_school_schooler_num(message.chat.id)
        else:
            self.__db.create_new_user(message.chat.id, login, password)
        
        markup: types.ReplyKeyboardMarkup = self.__markups.all()
        self.send_message(message.chat.id, "Ваши данные успешно сохранены", reply_markup=markup)

    def __get_login(self, message: types.Message) -> None:
        login: str = message.text.strip()
        self.send_message(message.chat.id, "Введите пароль:")
        self.register_next_step_handler(message, self.__get_password, login)
    
    def __get_password(self, message: types.Message, login: str) -> None:
        password: str = message.text.strip()
        self.__change_cerate_user_data(message, login, password)
    
    
    def __show_user_data(self, message: types.Message) -> None:
        if self.__db.user_in_table(message.chat.id):
            user_data: tuple = self.__db.get_log_pas(message.chat.id)
            self.send_message(message.chat.id, f"Ваш логин: {user_data[0]}")
            self.send_message(message.chat.id, f"Ваш пароль: {user_data[1]}")
        else:
            markup: types.ReplyKeyboardMarkup = self.__markups.registration()
            self.send_message(message.chat.id, f"Сначала зарегистрируйтесь", reply_markup=markup)
    
    def __save_person_data(self, message: types.Message) -> None:
        self.send_message(message.chat.id, "Это займет некоторе время")
        if self.__data.create_data(message.chat.id):
            self.send_message(message.chat.id, "Всё прошло успешно")
        else:
            self.send_message(message.chat.id, "Видимо вы ввели некоректные данные, поробуйте изменить их")


    def __get_person_data(self, message: types.Message) -> None:
        markup: types.ReplyKeyboardMarkup = self.__markups.marks()
        self.send_message(message.chat.id, "В каком виде отправить вам оценки?", reply_markup=markup)
    
    def __show_person_data(self, callback: types.CallbackQuery) -> None:
        data: dict = self.__data.get_data(callback.from_user.id)
        if data:
            if callback.data == "message":
                self.__show_person_data_messages(callback, data)
            elif callback.data == "table":
                self.__show_person_data_table(callback, data)
            return
                
        if self.__db.user_in_table(callback.from_user.id):
            self.edit_message_text("Сначала обновите оценки", callback.from_user.id, callback.message.message_id)
        else:
            self.edit_message_text("Сначала зарегистрируйтесь", callback.from_user.id, callback.message.message_id )
    
    def __show_person_data_messages(self, callback: types.CallbackQuery, data: dict):
        message: str = ""
        for i in range(len(data["subjects"])):
            if data["marks"][i][0] != "Нет выставленных оценок":
                message += f"{data["subjects"][i]}: {', '.join(data["marks"][i])} --- {data["sr_marks"][i]}\n\n"
            else:
                message += f"{data["subjects"][i]} - пока нет оценок\n\n"
        self.edit_message_text(message, callback.from_user.id, callback.message.message_id)
    
    def __show_person_data_table(self, callback: types.CallbackQuery, data: dict):
        table: str = self.__table.create_table(data)
        self.edit_message_text(f"<pre>{table}</pre>", callback.from_user.id, callback.message.message_id, parse_mode="HTML")
    