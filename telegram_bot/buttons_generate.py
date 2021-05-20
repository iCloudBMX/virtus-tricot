import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from .models import BotUser, Category, Product, Order
from . import constants

def language_buttons():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(constants.LANG_BUTTONS[0], callback_data="lang uz"), 
                InlineKeyboardButton(constants.LANG_BUTTONS[1], callback_data="lang ru"))
    
    return markup


def main_buttons(lang):

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    _list = []

    for button in constants.MAIN_BUTTONS:
        _list.append(constants.MAIN_BUTTONS[button][lang])
    
    markup.add(*_list)

    return markup


def category_buttons(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    _list = []

    if len(Category.objects.all()) > 0:
        for category in Category.objects.all():
            _list.append(category.name_uz if lang == "uz" else category.name_ru)
        
        _list.append(constants.BACK_BUTTON[lang])
        markup.add(*_list)
        
        return markup
    
    else:
        return None


def settings_buttons(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    _list = []

    for button in constants.SETTINGS_BUTTONS:
        _list.append(constants.SETTINGS_BUTTONS[button][lang])
        
    _list.append(constants.BACK_BUTTON[lang])
    markup.add(*_list)
        
    return markup
