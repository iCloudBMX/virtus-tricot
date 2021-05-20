import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config.settings import BOT_TOKEN

from .models import BotUser, Category, Product, Order
from . import step, constants, buttons_generate as buttons
from .commands import BotController, admins


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message):
    controller = BotController(message)

    user = BotUser.objects.get(chat_id=message.from_user.id)

    if user.step == step.IS_ANONYM:
        controller.language_selection()
    elif user.step == 0:
        controller.main_menu()



@bot.callback_query_handler(func = lambda call: True)
def callback_handler(call):

    controller = BotController(call)

    user = BotUser.objects.get(chat_id=call.message.chat.id)
    data = call.data
    
    if data.split()[0] == "lang" and user.step == step.IS_ANONYM:
        controller.user_initialize_lang(data.split()[1])
    elif data.split()[0] == "lang" and user.step == step.EDIT_LANG:
        controller.setting_edit_lang(data.split()[1])
    
    elif data.split()[0] == "change_page":
        controller.change_page(data)
    
    elif data.split()[0] == "order":
        controller.add_bascet(data)

    elif data == "exit":
        controller.delete_message()



@bot.message_handler(content_types=['text'])
def message_handler(message):
    controller = BotController(message)
    
    user = BotUser.objects.get(chat_id=message.from_user.id)

    """
       Main menu buttons 
    """
    if message.text == constants.MAIN_BUTTONS["menu"][user.lang]:
        controller.get_categories()
    elif message.text == constants.MAIN_BUTTONS["contact"][user.lang]:
        controller.contact_us()
    elif message.text == constants.MAIN_BUTTONS["settings"][user.lang]:
        controller.user_settings()

    elif message.text == constants.MAIN_BUTTONS["orders"][user.lang]:
        controller.get_orders()
    
    elif message.text == constants.CLEAR_BUTTON[user.lang]:
        controller.clear_bascet()
    
    elif message.text == constants.SEND_ADMIN_BUTTON[user.lang]:
        controller.send_order_to_admin()

    """
        Back button
    """

    if message.text == message.text == constants.BACK_BUTTON[user.lang] and (user.step == step.EDIT_LANG or user.step == step.EDIT_NAME or user.step == step.EDIT_PHONE):
        controller.user_settings()

    elif message.text == message.text == constants.BACK_BUTTON[user.lang] and user.step == step.MAIN_MENU:
        controller.main_menu()

    elif message.text == message.text == constants.BACK_BUTTON[user.lang] and user.step == step.MENU_CATEGORY:
        controller.main_menu()
    
    elif message.text == message.text == constants.BACK_BUTTON[user.lang] and user.step == step.BACK_CATEGORY:
        controller.get_categories()

    """
        Settings menu buttons
    """

    if message.text == constants.SETTINGS_BUTTONS["name"][user.lang]:
        controller.setting_name_selection()
    elif message.text == constants.SETTINGS_BUTTONS["phone"][user.lang]:
        controller.setting_phone_selection()
    elif message.text == constants.SETTINGS_BUTTONS["lang"][user.lang]:
        controller.setting_lang_selection()


    """
        User step
    """
    if user.step == step.INITIALIZE_NAME:
        controller.user_initialize_name()
    elif user.step == step.INITIALIZE_PHONE:
        controller.user_initialize_phone()
    elif user.step == step.INITIALIZE_COMPANY:
        controller.user_initialize_company()
    elif user.step == step.EDIT_NAME and message.text != constants.BACK_BUTTON[user.lang]:
        controller.setting_edit_name()
    elif user.step == step.EDIT_PHONE and message.text != constants.BACK_BUTTON[user.lang]:
        controller.setting_edit_phone()
    elif user.step == step.EDIT_PHONE and message.text != constants.BACK_BUTTON[user.lang]:
        controller.setting_edit_phone()


    elif user.step == step.MENU_CATEGORY:
        category = None

        if user.lang == "uz":
            category = Category.objects.get(name_uz=message.text)
        else:
            category = Category.objects.get(name_ru=message.text)
        
        controller.get_products(category)

        
    """
        Order selection
    """


    



@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    controller = BotController(message)
    
    user = BotUser.objects.get(chat_id=message.from_user.id)
    if user.step == step.INITIALIZE_PHONE:
        controller.user_initialize_phone()
    if user.step == step.EDIT_PHONE:
        controller.setting_edit_phone()


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    if message.chat.id in admins:
        controller = BotController(message)

        controller.send_photo_id()

    