import json
import telebot
from DataManager import DataManager

class User:

    def __init__(self, bot):

        self.bot = bot
        self.firstName = ''
        self.userName = ''
        self.userId = ''

    def setFirstName(self, name):
        
        self.firstName = name
    def setUserName(self, name):
        self.userName = name

    def setUserId(self, Id):
        self.userId = Id

    def getFirstName(self):
        return self.firstName
    
    def getUserName(self):
        return self.userName
    
    def getUserId(self):
        return self.userId
    
    def getBot(self):
        return self.bot
    
class Client(User):

    def __init__(self, bot):
        super().__init__(bot)
        self.parentFolder = 'client/%s.json'%(self.getUserId)

    def userToClient(self, User):

        self.bot = User.getBot()
        self.firstName = User.getFirstName()
        self.userName = User.getUserName()
        self.userId = User.getUserId()

    def userTypeSelect(self, message):

        #Вносим первый шаг в сессию
        with open('current_sessions/%s.json'%(self.getUserId()), 'r') as file:
            data = json.load(file)
        userData = data['userData']
        dataSteps = {'step1': 'client'}
        dataW = {'userData': userData, 'dataSteps': dataSteps}
        with open('current_sessions/%s.json'%(self.getUserId()), 'w') as file:
            json.dump(dataW, file)

        textToUser = 'Выберите необходимое действие'

        #Кнопки
        buttons = [telebot.types.ReplyKeyboardMarkup(row_width=1).add(telebot.types.KeyboardButton('Найти мастера'), telebot.types.KeyboardButton('Посмотреть свои записи')).to_json()]
        
        #Сообщение пользователю
        self.bot.send_message(message.chat.id, textToUser, reply_markup=buttons)

    def findTheMaster(self, message):

        with open('current_sessions/%s.json'%(self.getUserId()), 'r') as file:
            data = json.load(file)
        userData = data['userData']
        dataSteps = data['dataSteps']
        dataSteps['step2'] = message.text
        dataW = {'userData': userData, 'dataSteps': dataSteps}
        with open('current_sessions/%s.json'%(self.getUserId()), 'w') as file:
            json.dump(dataW, file)

        textToUser = 'Напишите Никнейм мастера, которого Вы хотите найти'

        #Кнопки
        #buttons = [telebot.types.ReplyKeyboardMarkup(row_width=1).add(telebot.types.KeyboardButton('Найти мастера'), telebot.types.KeyboardButton('Посмотреть свои записи')).to_json()]
        
        #Сообщение пользователю
        self.bot.send_message(message.chat.id, textToUser)

    def setCurrMonth(self, message):
        with open('current_sessions/%s.json'%(self.getUserId()), 'r') as file:
            data = json.load(file)
        userData = data['userData']
        dataSteps = data['dataSteps']
        dataSteps['masterName'] = message.text
        dataW = {'userData': userData, 'dataSteps': dataSteps}
        with open('current_sessions/%s.json'%(self.getUserId()), 'w') as file:
            json.dump(dataW, file)

        textToUser = 'Выберите месяц'

        #Кнопки
        buttons = [telebot.types.ReplyKeyboardMarkup(row_width=1).add(telebot.types.KeyboardButton('Текущий месяц'), telebot.types.KeyboardButton('Следующий месяц')).to_json()]
        
        self.bot.send_message(message.chat.id, textToUser, reply_markup=buttons)

    def getFreeDaysOfMaster(self,message):
        with open('current_sessions/%s.json'%(self.getUserId()), 'r') as file:
            data = json.load(file)
        userData = data['userData']
        dataSteps = data['dataSteps']
        dataSteps['currMonth'] = 'Текущий'
        dataW = {'userData': userData, 'dataSteps': dataSteps}
        with open('current_sessions/%s.json'%(self.getUserId()), 'w') as file:
            json.dump(dataW, file)

        dm = DataManager(self.parentFolder)

        master = dataSteps['masterName']


        with open('users.json', 'r') as file1:
            data1 = json.load(file1)

        masterId = data1[master]

        freeItems = dm.getFreeDays(masterId, dataSteps['currMonth'])

        s = []

        for day, time in freeItems.items():
            s.append('День: %s, Время: %s' %(day, time))

        textToUser = 'Свободные даты:', s

        #Кнопки
        #buttons = [telebot.types.ReplyKeyboardMarkup(row_width=1).add(telebot.types.KeyboardButton('Текущий месяц'), telebot.types.KeyboardButton('Следующий месяц')).to_json()]
        
        self.bot.send_message(message.chat.id, textToUser)


class Master(User):

    def __init__(self):

        self.parentFolder = 'master/%s.json'%(self.getUserId)
        self.currMonth = ''

    def getCurrMonth(self):
        return self.currMonth
    
    def getParentFolder(self):
        return self.parentFolder

    def userToMaster(self, User):

        self.bot = User.getBot()
        self.firstName = User.getFirstName()
        self.userName = User.getUserName()
        self.userId = User.getUserId()

    #Выбор действия мастером
    def userTypeSelect(self, message):

        #Вносим первый шаг в сессию
        with open('current_sessions/%s.json'%(self.getUserId()), 'r') as file:
            data = json.load(file)
        userData = data['userData']
        dataSteps = {'step1': 'master'}
        dataW = {'userData': userData, 'dataSteps': dataSteps}
        with open('current_sessions/%s.json'%(self.getUserId()), 'w') as file:
            json.dump(dataW, file)

        textToUser = 'Выберите необходимое действие'

        #Кнопки
        buttons = [telebot.types.ReplyKeyboardMarkup(row_width=1).add(telebot.types.KeyboardButton('Посмотреть расписание'), telebot.types.KeyboardButton('Изменить расписание')).to_json()]
        
        #Сообщение пользователю
        self.bot.send_message(message.chat.id, textToUser, reply_markup=buttons)

    #Выбор месяца мастером
    def actionSelect(self, message):

        #Вносим второй шаг в сессию
        with open('current_sessions/%s.json'%(self.getUserId()), 'r') as file:
            data = json.load(file)
        userData = data['userData']
        dataSteps = data['dataSteps']
        dataSteps.update({'step2':message.text})
        dataW = {'userData': userData, 'dataSteps': dataSteps}
        with open('current_sessions/%s.json'%(self.getUserId()), 'w') as file:
            json.dump(dataW, file)

        textToUser = 'Выберите месяц'

        #Кнопки
        buttons = [telebot.types.ReplyKeyboardMarkup(row_width=1).add(telebot.types.KeyboardButton('Текущий'), telebot.types.KeyboardButton('Следующий')).to_json()]
        
        #Сообщение пользователю
        self.bot.send_message(message.chat.id, textToUser, reply_markup=buttons)

        #Сохраяем месяц
        self.currMonth = message.text

    def setCurrMonth(self, message):

        #Вносим третий шаг в сессию
        with open('current_sessions/%s.json'%(self.getUserId()), 'r') as file:
            data = json.load(file)
        userData = data['userData']
        dataSteps = data['dataSteps']
        dataSteps.update({'step3':message.text})
        dataW = {'userData': userData, 'dataSteps': dataSteps}
        with open('current_sessions/%s.json'%(self.getUserId()), 'w') as file:
            json.dump(dataW, file)

        self.currMonth = message.text

        textToUser = 'Напишите свободные для приема дни (числа через запятую без пробелов)'
        self.bot.send_message(message.chat.id, textToUser)



    def sheduleChanger(self, message):

        with open('current_sessions/%s.json'%(self.getUserId()), 'r') as file:
            data = json.load(file)
        dataSteps = data['dataSteps']
        userData = data['userData']

        userId = userData['userId']
        month = dataSteps['step3']

        dataManager = DataManager(self.parentFolder)

        days = message.text.split(',')

        print("Дни:", days)

        dataManager.createMonth(userId, days, month)



    #def sheduleGetter(self, message):


    