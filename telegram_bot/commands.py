import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputMediaPhoto
from config.settings import BOT_TOKEN

from .models import BotUser, Category, Product, Order
from . import step, constants, buttons_generate as buttons

bot = telebot.TeleBot(BOT_TOKEN)

admins = ()

class BotController:
    def __init__(self, message):
        self.message = message
        self.chat_id = message.from_user.id
        self.user, _ = BotUser.objects.get_or_create(chat_id=self.chat_id)
        self.message_id = message.message_id if hasattr(message, "message_id") else message.message.message_id
        self.call_id = message.id
    
    def language_selection(self):
        markup = buttons.language_buttons()
        bot.send_message(self.chat_id, f"<b>{constants.SELECT_LANGUAGE['uz']}</b>\n\n<b>{constants.SELECT_LANGUAGE['ru']}</b>", parse_mode='html', reply_markup=markup)

    
    def user_initialize_lang(self, lang):
        bot.delete_message(self.chat_id, self.message_id)
        self.user.lang = lang
        self.user.save()
        bot.send_message(self.chat_id, constants.GREETINGS_NAME[lang])
        self.set_step(step.INITIALIZE_NAME)

    def user_initialize_name(self):
        self.user.name = self.message.text
        self.user.save()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton(constants.CONTACT_BUTTON[self.user.lang], request_contact = True)) 
        bot.send_message(self.chat_id, constants.GREETINGS_PHONE[self.user.lang], reply_markup=markup)
        self.set_step(step.INITIALIZE_PHONE)

    def user_initialize_phone(self):
        self.user.phone = self.message.text if self.message.contact == None else self.message.contact.phone_number 
        self.user.save()
        bot.send_message(self.chat_id, constants.GREETINGS_COMPANY[self.user.lang], reply_markup=ReplyKeyboardRemove())
        self.set_step(step.INITIALIZE_COMPANY)
    
    def user_initialize_company(self):
        self.user.company = self.message.text
        self.user.save()
        self.main_menu()
        self.set_step(step.ZERO)

    def main_menu(self):
        markup = buttons.main_buttons(self.user.lang)

        bot.send_message(self.chat_id, constants.MAIN_MENU[self.user.lang], parse_mode='html', reply_markup=markup)

        self.set_step(step.ZERO)
    
    def get_categories(self):
        markup = buttons.category_buttons(self.user.lang)

        if markup != None:
            bot.send_message(self.chat_id, constants.MENU_CATALOG_SELECTION[self.user.lang], parse_mode='html', reply_markup=markup)  
        else:
            bot.send_message(self.chat_id, constants.NO_MENU_CATALOG[self.user.lang], parse_mode='html')
        
        self.set_step(step.MENU_CATEGORY)
    
    def contact_us(self):
        bot.send_message(self.chat_id, constants.CONTACT_US[self.user.lang] , parse_mode='html')        

    
    def user_settings(self):
        markup = buttons.settings_buttons(self.user.lang)

        bot.send_message(self.chat_id, constants.MENU_SETTINGS_SELECTION[self.user.lang], parse_mode='html', reply_markup=markup)

        self.set_step(step.MAIN_MENU)


    def setting_name_selection(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add(KeyboardButton(constants.BACK_BUTTON[self.user.lang]))

        text = constants.MENU_SETTINGS_NAME_SELECTION[self.user.lang].replace("name", self.user.name)
        bot.send_message(self.chat_id, text, parse_mode='html', reply_markup=markup)

        self.set_step(step.EDIT_NAME)

    def setting_phone_selection(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add(KeyboardButton(constants.CONTACT_BUTTON[self.user.lang], request_contact = True), KeyboardButton(constants.BACK_BUTTON[self.user.lang]))

        text = constants.MENU_SETTINGS_PHONE_SELECTION[self.user.lang].replace("phone", self.user.phone)
        bot.send_message(self.chat_id, text, parse_mode='html', reply_markup=markup)

        self.set_step(step.EDIT_PHONE)
    
    def setting_lang_selection(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add(KeyboardButton(constants.BACK_BUTTON[self.user.lang]))
        text = constants.MENU_SETTINGS_LANG_SELECTION[self.user.lang].replace("lang", self.user.lang.upper())
        bot.send_message(self.chat_id, text, parse_mode='html', reply_markup=markup)

        markup = buttons.language_buttons()
        bot.send_message(self.chat_id, f"<b>{constants.EDIT_LANG['uz']}</b>\n\n<b>{constants.EDIT_LANG['ru']}</b>", parse_mode='html', reply_markup=markup)
        self.set_step(step.EDIT_LANG)
    
    def setting_edit_name(self):
        self.user.name = self.message.text
        self.user.save()

        bot.send_message(self.chat_id, constants.SUCCESSFUL_CHANGED[self.user.lang], parse_mode='html')

        self.user_settings()
    
    def setting_edit_phone(self):
        self.user.phone = self.message.text if self.message.contact == None else self.message.contact.phone_number 
        self.user.save()

        bot.send_message(self.chat_id, constants.SUCCESSFUL_CHANGED[self.user.lang], parse_mode='html')

        self.user_settings()
    
    def setting_edit_lang(self, lang):
        bot.delete_message(self.chat_id, self.message_id)
        self.user.lang = lang
        self.user.save()

        bot.send_message(self.chat_id, constants.SUCCESSFUL_CHANGED[self.user.lang], parse_mode='html')

        self.user_settings()

    def get_products(self, category):
        products = Product.objects.filter(category=category)

        if len(products) > 0:
 
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

            keyboard.add(KeyboardButton(constants.BACK_BUTTON[self.user.lang]))

            text = category.name_uz if self.user.lang == "uz" else category.name_ru
            
            bot.send_message(self.chat_id, text, reply_markup=keyboard)

            markup = InlineKeyboardMarkup()
            
            markup.add(InlineKeyboardButton(text="⬅️", callback_data=f"change_page -1 {category.pk}"), InlineKeyboardButton(text="➡️", callback_data=f"change_page 1 {category.pk}"))
            
            markup.add(InlineKeyboardButton(text = constants.BASCET_BUTTON[self.user.lang], callback_data=f"order {products[0].pk}"), InlineKeyboardButton("❌", callback_data="exit"))

            text = products[0].name_uz if self.user.lang == "uz" else products[0].name_ru
            bot.send_photo(self.chat_id, products[0].image_id, f"<b>{text}</b>", parse_mode='html', reply_markup=markup)
            self.set_step(step.BACK_CATEGORY)

            return 

        bot.send_message(self.chat_id, constants.NO_PRODUCT[self.user.lang])

        

    def change_page(self, call_data):
        data = int(call_data.split()[1])
        
        if data == -1:
            bot.answer_callback_query(self.call_id, constants.FIRST_PAGE[self.user.lang])
            return
        
        products = Product.objects.filter(category = int(call_data.split()[-1]))
        if len(products) <= data:
            
            bot.answer_callback_query(self.call_id, constants.LAST_PAGE[self.user.lang])
            return

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⬅️", callback_data = f"change_page {data-1} {call_data.split()[-1]}"), InlineKeyboardButton("➡️", callback_data = f"change_page {data + 1} {call_data.split()[-1]}"))
        markup.add(InlineKeyboardButton(constants.BASCET_BUTTON[self.user.lang], callback_data=f"order {products[data].pk}"), InlineKeyboardButton("❌", callback_data="exit"))

        text = products[data].name_uz if self.user.lang == "uz" else products[data].name_ru

        media = InputMediaPhoto(media=products[data].image_id, caption=f"<b>{text}</b>", parse_mode='html')
       
        bot.edit_message_media(media, chat_id=self.chat_id, message_id=self.message_id, reply_markup=markup)

    
    def delete_message(self):
        bot.delete_message(self.chat_id, self.message_id)
    

    def add_bascet(self, call_data):
        product = Product.objects.get(pk = int(call_data.split()[-1]))
        order = Order.objects.filter(user=self.user, product = product)
        if len(order) == 0:
            new_order = Order.objects.create(user=self.user, product = product) 
            new_order.save() 
            bot.answer_callback_query(self.call_id, constants.NOW_ADDED_TO_BASCET[self.user.lang])
        else:
            bot.answer_callback_query(self.call_id, constants.ORDER_ADDED_TO_BASCET[self.user.lang])

    def get_orders(self):
        orders = Order.objects.filter(user=self.user)


        if len(orders) > 0:

            markup = ReplyKeyboardMarkup(resize_keyboard=True)

            markup.add(KeyboardButton(constants.SEND_ADMIN_BUTTON[self.user.lang]) , KeyboardButton(constants.CLEAR_BUTTON[self.user.lang])) 
            markup.add(KeyboardButton(constants.BACK_BUTTON[self.user.lang]))

            text = f"<b>{constants.USER_ORDERS[self.user.lang]}</b>\n\n"

            for order in orders:
                name = order.product.name_uz if self.user.lang == "uz" else order.product.name_ru

                text = text + name + "\n"
        
            bot.send_message(self.chat_id, text, parse_mode='html', reply_markup=markup) 
            self.set_step(step.MENU_CATEGORY)
        else:
            bot.send_message(self.chat_id, constants.BASCET_EMPTY[self.user.lang]) 


    def clear_bascet(self):
        Order.objects.filter(user = self.user).delete()

        bot.send_message(self.chat_id, constants.BASCET_CLEARED[self.user.lang])

        self.main_menu()
    

    def send_order_to_admin(self):
        
        orders = Order.objects.filter(user=self.user)

        if len(orders) > 0:
            text = "<b>Янги ҳаридлар</b>\n\n"

            for order in orders:
                name = order.product.name_uz if self.user.lang == "uz" else order.product.name_ru

                text = text + name + "\n"

            text = text + f"\nМижоз: <b>{self.user.name}</b>\nКомпания: <b>{self.user.company}</b>\nТелефон: <b>{self.user.phone}</b>"

            for admin in admins:
                bot.send_message(admin, text, parse_mode='html')
                
            bot.send_message(self.chat_id, constants.PRODUCT_SEND_ADMIN[self.user.lang])
            
            self.main_menu()

    
    def send_photo_id(self):
        photo_id = self.message.photo[-1].file_id

        bot.send_message(self.chat_id, f"`{photo_id}`", parse_mode='markdown')

    def set_step(self, step):
        self.user.step = step
        self.user.save()    