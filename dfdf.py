from datetime import date

class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        
        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            buttons = [telebot.types.ReplyKeyboardMarkup(row_width=2).add(telebot.types.KeyboardButton('Клиент'), telebot.types.KeyboardButton('Мастер')).to_json()]
            self.bot.send_message(message.chat.id, 'Добро пожаловать! Нажмите на кнопку ниже, чтобы начать.', reply_markup=buttons)

        @self.bot.message_handler(content_types=['text'])
        def handle_text(message):
            if message.text == 'Клиент':
                self.bot.send_message(message.chat.id, 'Выберите дату, нажав на кнопку ниже.', reply_markup=telebot.types.ReplyKeyboardMarkup(row_width=1).add(telebot.types.KeyboardButton('Выбрать дату')).to_json())

                @self.bot.message_handler(content_types=['text'])
                def handle_date(message):
                    try:
                        date_str = message.text
                        date = date.fromisoformat(date_str)
                        date_manager = DateManager('data/dates.json')
                        date_manager.add_date_to_busy_dates(date)
                        date_manager.update_week(date_manager.get_free_dates())
                        self.bot.send_message(message.chat.id, 'Дата сохранена.')
                    except ValueError:
                        self.bot.send_message(message.chat.id, 'Неверный формат даты. Попробуйте еще раз.')

        @self.bot.message_handler(commands=['stop'])
        def stop_message(message):
            self.bot.stop_polling()

    def run(self):
        self.bot.polling(none_stop=True)

bot = Bot('YOUR_BOT_TOKEN')
bot.run()
