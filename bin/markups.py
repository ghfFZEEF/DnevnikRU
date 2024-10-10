import abc
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class BasicMarkups(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def marks() -> ReplyKeyboardMarkup:
        pass
    
    @staticmethod
    @abc.abstractmethod
    def registration() -> ReplyKeyboardMarkup:
        pass

    @staticmethod
    @abc.abstractmethod
    def all() -> ReplyKeyboardMarkup:
        pass


class Markups(BasicMarkups):
    @staticmethod
    def marks() -> InlineKeyboardMarkup:
        marks = InlineKeyboardMarkup()
        message = InlineKeyboardButton('Сообщением', callback_data='message')
        table = InlineKeyboardButton('Таблицей', callback_data='table')    
        marks.add(message, table)
        return marks

    
    @staticmethod
    def registration() -> ReplyKeyboardMarkup:
        registration: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        start_registration: KeyboardButton = KeyboardButton("Начать регистрацию")
        help: KeyboardButton = KeyboardButton("Помощь")
        registration.add(start_registration, help)
        return registration
    
    @staticmethod
    def all():
        all: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        get_user_data: KeyboardButton = KeyboardButton("Мои данные")
        change_user_data: KeyboardButton = KeyboardButton("Изменить данные")
        get_person_data: KeyboardButton = KeyboardButton("Оценки")
        load_person_data: KeyboardButton = KeyboardButton("Обновить оценки")
        help: KeyboardButton = KeyboardButton("Помощь")
        all.add(get_user_data, change_user_data, get_person_data, load_person_data, help)
        return all
