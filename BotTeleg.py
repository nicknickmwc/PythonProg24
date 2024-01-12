import telebot
import json
from User import User
from User import Master
from User import Client
from DataManager import DataManager

#Создаем экземляр Telebot с токеном бота 
bot = telebot.TeleBot('6981064969:AAHMLPhtn-peRDVmrENc9y5GUCVAt_olct0')

#Создаем объект Пользователя(П)
user = User(bot)

#Стадия сообщений
messageLevel = 1

#Обработчик старта
@bot.message_handler(commands=['start'])
def start_message(message):

    #Устанавливаем данные о текущем П
    user.setUserId(message.from_user.id)
    user.setUserName(message.from_user.username)
    user.setFirstName(message.from_user.first_name)

    #Создаем сессию 
    userData = {'userId': user.getUserId(), 'userName': user.getUserName(), 'firstName': user.getFirstName()}
    with open('current_sessions/%s.json'%(user.getUserId()), 'w') as file:
        json.dump({'userData': userData}, file)
    
    #Добавляем пользователя в список
    with open('users.json', 'r') as file:
        data = json.load(file)
    
    if not user.getUserName() in data:
        data[user.getUserName()] = user.getUserId()
        with open('users.json', 'w') as file1:
            json.dump(data, file1)

    #Кнопки раздела старта
    buttons = [telebot.types.ReplyKeyboardMarkup(row_width=1).add(telebot.types.KeyboardButton('Клиент'), telebot.types.KeyboardButton('Мастер')).to_json()]
    #Сообщение П на старте
    bot.send_message(message.chat.id, 'Добро пожаловать, %s! Нажмите на кнопку ниже, чтобы начать.'%(user.getUserName()), reply_markup=buttons)

#Обработчик следующего этапа
@bot.message_handler(content_types=['text'])
def handle_user(message):

    #Создаем Мастера(М) из П
    master = Master()
    client = Client(user.bot)
    master.userToMaster(user)
    client.userToClient(user)

    with open('users.json', 'r') as usersFile:
        users = json.load(usersFile)

    #//////////////////////////////////////////Первая стадия

    if (message.text == 'Мастер'):

        #Предоставляем М выбрать действие
        master.userTypeSelect(message)

    if (message.text == 'Клиент'):

        #Предоставляем М выбрать действие
        client.userTypeSelect(message)
        
    #//////////////////////////////////////////Первая стадия
        
        
    #//////////////////////////////////////////Вторая стадия

    if (message.text == 'Посмотреть расписание') or (message.text == 'Изменить расписание'):
        print('Начась 2 стадия')
        master.actionSelect(message)
    
    if (message.text == 'Найти мастера'):
        client.findTheMaster(message)

    #//////////////////////////////////////////Вторая стадия
        
    #//////////////////////////////////////////Третья стадия
        
    if(message.text == 'Текущий') or (message.text == 'Следующий'):

        master.setCurrMonth(message)

    if (message.text in list(users.keys())):

        client.setCurrMonth(message)
        
    #//////////////////////////////////////////Третья стадия
        
    #//////////////////////////////////////////Четвертая стадия
        
    if (message.text == 'Текущий месяц'):

        client.getFreeDaysOfMaster(message)
        
    elif (message.text):
        

        with open('current_sessions/777725549.json', 'r') as file:
            data = json.load(file)

            print("Есть текст")

            if 'dataSteps' in data:
                dataSteps = data['dataSteps']

                if 'step3' in dataSteps:
                    master.sheduleChanger(message)
    
     #//////////////////////////////////////////Четвертая стадия
        
         
        
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat.id, message.text)

bot.polling()