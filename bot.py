import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ទាញយក Token ពី Environment Variables របស់ Railway
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'ដាក់_TOKEN_របស់អ្នកនៅទីនេះ')
bot = telebot.TeleBot(BOT_TOKEN)

# មុខងារសម្រាប់ពាក្យបញ្ជា /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # បង្កើត Keyboard Buttons
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton('👨🏻‍💻 គណនី')
    btn2 = KeyboardButton('🛍️ ហាងសេវា')
    btn3 = KeyboardButton('💸 បញ្ជូលប្រាក់')
    
    # រៀបចំប៊ូតុងចូលគ្នា
    markup.add(btn1, btn2)
    markup.add(btn3)
    
    bot.send_message(message.chat.id, "សួស្ដី! សូមស្វាគមន៍មកកាន់ Bot របស់យើង។ សូមជ្រើសរើសជម្រើសខាងក្រោម៖", reply_markup=markup)

# មុខងារសម្រាប់ឆ្លើយតបពេលចុចប៉ះប៊ូតុង
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == '👨🏻‍💻 គណនី':
        bot.send_message(message.chat.id, "នេះគឺជាព័ត៌មានគណនីរបស់អ្នក។ ឈ្មោះ៖ " + message.from_user.first_name)
    elif message.text == '🛍️ ហាងសេវា':
        bot.send_message(message.chat.id, "សូមស្វាគមន៍មកកាន់ហាងសេវាកម្មរបស់យើង! តើអ្នកចង់ជាវសេវាកម្មអ្វីដែរ?")
    elif message.text == '💸 បញ្ជូលប្រាក់':
        bot.send_message(message.chat.id, "សូមជ្រើសរើសវិធីសាស្ត្របង់ប្រាក់ (ឧទាហរណ៍៖ ABA, ACLEDA...) ដើម្បីបញ្ចូលប្រាក់។")
    else:
        bot.send_message(message.chat.id, "សូមជ្រើសរើសជម្រើសដែលមាននៅលើប៊ូតុង។")

if __name__ == "__main__":
    print("Bot កំពុងដំណើរការ...")
    bot.polling(none_stop=True)
