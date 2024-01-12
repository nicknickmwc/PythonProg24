import json

class DataManager:

    def __init__(self, fileName):
        self.fileName = fileName

    def createMonth(self, userId, days, month):

        m = []

        for i in range(1, 32):

            s = str(i)
            if s in days:
                m.append({'day': i, 'time': '12:00', 'status': 'y'})
            else:
                m.append({'day': i, 'time': '12:00', 'status': 'no'})
        
        data = {month: m}

        with open('master/%s.json'%(userId), 'w') as file:
            json.dump(data, file)

    def updateMonth(self, month):

        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                print('Файл содержит данные.')
        except json.JSONDecodeError:
            print('Файл пуст или не содержит допустимых данных JSON.')


    def add_date(self, apDay):

        data = self.dates
        
        findedDays = [day for day, value in data.items() if value == apDay]

        for day in findedDays:
            data[day] = "Нет"

      

    def getFreeDays(self, userID, month):

        freeDays = {}

        with open('master/%s.json'%(userID), 'r') as file:
            data = json.load(file)

        m = data[month]

        for item in m:
            if item['status'] == 'y':
                freeDays.update({item['day']: item['time']})
        
        return freeDays

    def get_week(self):
        with open(self.fileName, 'r') as file:
            data = json.load(self.fileName, file)
        return data

 
