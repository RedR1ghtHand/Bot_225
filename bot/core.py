from telebot import *
from telebot.callback_data import CallbackData
from db_manager import DB_Manager
from calculate import calculate_cart
from _token import TOK
bot = telebot.TeleBot(TOK)
menu_factory = CallbackData('dish_id', prefix='dish')
mrkp = None
db = DB_Manager()
menu_dict = {item[0]: item[1] for item in db.get_list_from_dishes()}
dish_list = [item[0] for item in db.get_list_from_dishes()]



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}, tap /menu for start')

    user_id = message.chat.id
    db = DB_Manager()
    db.create_user_cart(user_id)


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    category = types.KeyboardButton('/Категорії')
    food_rating = types.KeyboardButton('/Рейтинг')
    schedue = types.KeyboardButton('/Планувальник')
    markup.add(category, food_rating, schedue)

    bot.send_message(message.chat.id, 'Оберіть розділ 👇', reply_markup=markup)


@bot.message_handler(commands=['Категорії'])
def category(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    susi = types.KeyboardButton('/Роли_Суші')
    burgers = types.KeyboardButton('/Бургери')
    pasta = types.KeyboardButton('/Паста')
    back_to_menu = types.KeyboardButton('/menu')
    markup.add(susi, burgers, pasta, back_to_menu)

    bot.send_message(message.chat.id, 'Оберіть категорію 👇', reply_markup=markup)


@bot.message_handler(commands=['Роли_Суші'])
def susi_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    nigiri = types.KeyboardButton('Гункани')
    o_nigiri = types.KeyboardButton('Онігірадзу')
    roll = types.KeyboardButton('Роли')
    back = types.KeyboardButton('/Категорії')
    markup.add(nigiri, o_nigiri, roll, back)

    bot.send_message(message.chat.id, 'Оберіть страву 👇', reply_markup=markup)


@bot.message_handler(commands=['Паста'])
def pasta_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    lasagna = types.KeyboardButton('Лазанья')
    carbonara = types.KeyboardButton('Карбонара')
    back = types.KeyboardButton('/Категорії')
    markup.add(lasagna, carbonara, back)

    bot.send_message(message.chat.id, 'Оберіть страву 👇', reply_markup=markup)


@bot.message_handler(commands=['Бургери'])
def burgers_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    classic_burger = types.KeyboardButton('Бургер класичний')
    chicken_burger = types.KeyboardButton('Бургер курячий')
    back = types.KeyboardButton('/Категорії')
    markup.add(classic_burger, chicken_burger, back)

    bot.send_message(message.chat.id, 'Оберіть страву 👇', reply_markup=markup)


@bot.message_handler(commands=['Рейтинг'])
def rating(message):
    db = DB_Manager()

    dish_name = [item[0] for item in db.get_dish_rating()]
    dish_rating = [item[1] for item in db.get_dish_rating()]
    rating_list = f'ТОП 3 СТРАВ ПО ЗАПИТАМ:\n\n' \
                  f'{dish_name[0]}: {dish_rating[0]} запити(тів)\n\n' \
                  f'{dish_name[1]}: {dish_rating[1]} запити(тів)\n\n' \
                  f'{dish_name[2]}: {dish_rating[2]} запити(тів)\n\n'

    bot.send_message(message.chat.id, rating_list)


@bot.message_handler(commands=['Планувальник'])
def scheduler(message):
    bot.send_message(message.chat.id, 'Ласкаво просимо до планувальника меню!\n'
                                      '1) оберіть список страв\n'
                                      '2) натисніть меню "РОЗРАХУВАТИ"\n'
                                      '3) бот розрахує для Вас перелік усіх інгредієнтів для готування та зручних покупок!')

    global mrkp
    mrkp = types.InlineKeyboardMarkup(row_width=2)

    calculate = types.InlineKeyboardButton(text='РОЗРАХУВАТИ', callback_data='calculate')
    clear = types.InlineKeyboardButton(text='Очистити кошик', callback_data='clear')

    mrkp.add(*[types.InlineKeyboardButton(text=dish[1],
                                          callback_data=menu_factory.new(dish_id=dish[0])) for dish in menu_dict.items()])

    mrkp.add(clear)
    mrkp.add(calculate)

    bot.send_message(message.chat.id, 'Оберіть страви зі списку:\nКорзина:', reply_markup=mrkp)


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_answers(callback):
    dish_data = callback.data[callback.data.find(':')+1::]
    if dish_data in dish_list:
        db.add_to_cart(callback.message.chat.id, data=menu_dict[dish_data])

        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.id,
                              reply_markup=mrkp,
                              text='Оберіть страви зі списку:\nКорзина:\n{user_cart}'
                              .format(user_cart=db.get_user_cart_str(callback.message.chat.id)))

    elif callback.data == 'calculate':
        calculate_ingredients = calculate_cart(callback.message.chat.id)
        bot.send_message(callback.message.chat.id, f'Розраховуємо інгредієнти:\n{calculate_ingredients}')

        db.clear_user_cart(callback.message.chat.id)

    elif callback.data == 'clear':
        db.clear_user_cart(callback.message.chat.id)
        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.id,
                              reply_markup=mrkp,
                              text='Оберіть страви зі списку:\nКорзина:')


@bot.message_handler(content_types=["text"])
def display_ingredients(message):
    if message.text in menu_dict.values():
        ingredients = db.get_ingredients_by_dish_name(message.text)

        result = ''
        for item in ingredients:
            result += f'{item[0]} : {item[1]}\n'

        bot.reply_to(message, result)
        db.add_rating(message.text)


bot.infinity_polling()