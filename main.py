import aiogram
from datetime import datetime
import telebot
from auth_data import token


def get_data():
    req = aiogram.get("https://yobit.net/api/3/ticker/ltc_btc")
    response = req.json()
    print(response)
    sell_price = response["btc_usd"]["sell"]
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%H')}\nSell BTC price: {sell_price}")
    
def telegram_bot(token):
    bot = telebot.TeleBot(token)
    
    @bot.message_handler(commands=["start"])
    
    def start_message(message):
        bot.send_message(message.chat.id, "Hello friend! Write the 'price' out yhe cost of BTC!")
    
    bot.polling()
    
if __name__ == '__main__':
     get_data()
     telegram_bot(token)