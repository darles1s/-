import telebot
from telebot import types

TOKEN = '7344026874:AAFoMgZO-z652A0iygM-qBoHjtLHq4YjPNM'

bot = telebot.TeleBot(TOKEN)

# Функция для расчета нормы КБЖУ
def calculate_macros(weight, height, age, gender, goal):
    if gender == 'М':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    if goal == 'Набрать вес':
        total_calories = bmr * 1.2 + 300
    elif goal == 'Сбросить вес':
        total_calories = bmr * 0.8
    else:
        total_calories = bmr * 1.0
    
    protein = total_calories * 0.3 / 4
    carbs = total_calories * 0.5 / 4
    fat = total_calories * 0.2 / 9
    
    return int(total_calories), int(protein), int(carbs), int(fat)

# Функция для отправки сообщения с примерами питания
def send_meal_examples(chat_id):
    message = "Вот несколько примеров питания для вас:\n\n" \
              "Завтрак:\n" \
              "- Овсяная каша с ягодами\n" \
              "- Яичница с тостами\n\n" \
              "Обед:\n" \
              "- Куриная грудка с рисом и овощами\n" \
              "- Сэндвич с индейкой и зеленью\n\n" \
              "Ужин:\n" \
              "- Запеченная рыба с картофелем и салатом\n" \
              "- Гречка с грибами и зеленью"
    bot.send_message(chat_id, message)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
    btn1 = types.KeyboardButton("Набрать вес")
    btn2 = types.KeyboardButton("Сбросить вес")
    btn3 = types.KeyboardButton("Поддержать вес")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Здравствуйте! Я бот, который поможет вам рассчитать дневную норму КБЖУ и предоставит примеры питания. Выберите свою цель:", reply_markup=markup)

# Обработчик ответов на кнопки
@bot.message_handler(content_types=['text'])
def handle_goals(message):
    goal = message.text
    if goal in ['Набрать вес', 'Сбросить вес', 'Поддержать вес']:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да, ввести данные")
        markup.add(btn1)
        bot.send_message(message.chat.id, "Отлично, продолжим? ", reply_markup=markup)
        bot.register_next_step_handler(message, get_user_data, goal)


def get_user_data(message, goal):
    if message.text == "Да, ввести данные":
        msg = bot.send_message(message.chat.id, "Введите ваш вес (в кг):")
        bot.register_next_step_handler(msg, get_weight, goal)

def get_weight(message, goal):
    weight = float(message.text)
    msg = bot.send_message(message.chat.id, "Введите ваш рост (в см):")
    bot.register_next_step_handler(msg, get_height, weight, goal)

def get_height(message, weight, goal):
    height = float(message.text)
    msg = bot.send_message(message.chat.id, "Введите ваш возраст:")
    bot.register_next_step_handler(msg, get_age, weight, height, goal)

def get_age(message, weight, height, goal):
    age = int(message.text)
    msg = bot.send_message(message.chat.id, "Укажите ваш пол (М/Ж):")
    bot.register_next_step_handler(msg, get_gender, weight, height, age, goal)

def get_gender(message, weight, height, age, goal):
    gender = message.text
    total_calories, protein, carbs, fat = calculate_macros(weight, height, age, gender, goal)
    bot.send_message(message.chat.id, f"Ваша дневная норма КБЖУ:\n"
         f"Калории: {total_calories} ккал\n"
         f"Белки: {protein} г\n"
         f"Углеводы: {carbs} г\n"
         f"Жиры: {fat} г")
    send_meal_examples(message.chat.id)


def calculate_meal_sizes(total_calories, protein, carbs, fat):
    breakfast_calories = total_calories * 0.25
    lunch_calories = total_calories * 0.35
    dinner_calories = total_calories * 0.4

    breakfast_protein = protein * 0.25
    lunch_protein = protein * 0.35
    dinner_protein = protein * 0.4

    breakfast_carbs = carbs * 0.25
    lunch_carbs = carbs * 0.35
    dinner_carbs = carbs * 0.4

    breakfast_fat = fat * 0.25
    lunch_fat = fat * 0.35
    dinner_fat = fat * 0.4

    return (breakfast_calories, lunch_calories, dinner_calories,
            breakfast_protein, lunch_protein, dinner_protein,
            breakfast_carbs, lunch_carbs, dinner_carbs,
            breakfast_fat, lunch_fat, dinner_fat)

def get_gender(message, weight, height, age, goal):
    gender = message.text
    total_calories, protein, carbs, fat = calculate_macros(weight, height, age, gender, goal)
    (breakfast_calories, lunch_calories, dinner_calories,
     breakfast_protein, lunch_protein, dinner_protein,
     breakfast_carbs, lunch_carbs, dinner_carbs,
     breakfast_fat, lunch_fat, dinner_fat) = calculate_meal_sizes(total_calories, protein, carbs, fat)

    bot.send_message(message.chat.id, f"Ваша дневная норма КБЖУ:\n"
                                     f"Калории: {total_calories} ккал\n"
                                     f"Белки: {protein} г\n"
                                     f"Углеводы: {carbs} г\n"
                                     f"Жиры: {fat} г\n\n"
                                     f"Рекомендованные размеры приемов пищи:\n"
                                     f"Завтрак: {breakfast_calories:.0f} ккал, {breakfast_protein:.0f} г белка, {breakfast_carbs:.0f} г углеводов, {breakfast_fat:.0f} г жира\n"
                                     f"Обед: {lunch_calories:.0f} ккал, {lunch_protein:.0f} г белка, {lunch_carbs:.0f} г углеводов, {lunch_fat:.0f} г жира\n"
                                     f"Ужин: {dinner_calories:.0f} ккал, {dinner_protein:.0f} г белка, {dinner_carbs:.0f} г углеводов, {dinner_fat:.0f} г жира" )
    

    send_meal_examples(message.chat.id)

bot.polling()






