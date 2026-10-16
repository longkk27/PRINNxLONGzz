import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ទាញយក Token ពី Environment Variable (BOT_TOKEN) នៅក្នុង Railway
TOKEN = os.getenv('BOT_TOKEN') 
bot = telebot.TeleBot(TOKEN)

# មុខងារសម្រាប់ពេលមានអ្នកចុច /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # បង្កើតផ្ទាំងប៊ូតុងគោល (Main Menu)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = KeyboardButton('👨🏻‍💻 គណនី')
    btn2 = KeyboardButton('🎥 ហាងរឿង')
    btn3 = KeyboardButton('🛍️ បញ្ជូលប្រាក់')
    btn4 = KeyboardButton('🛠️ ភាសា') # ទុកតែប៊ូតុងភាសាមួយនេះសិន
    
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    
    bot.send_message(
        message.chat.id, 
        "សួស្តី! សូមស្វាគមន៍មកកាន់ Bot របស់យើង។\nសូមជ្រើសរើសជម្រើសណាមួយខាងក្រោម៖", 
        reply_markup=markup
    )

# មុខងារសម្រាប់ឆ្លើយតបពេលគេចុចប៊ូតុងលើ Main Menu
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text
    chat_id = message.chat.id
    
    if text == '👨🏻‍💻 គណនី':
        bot.send_message(chat_id, f"នេះគឺជាព័ត៌មានគណនីរបស់អ្នក។\nឈ្មោះ៖ {message.from_user.first_name}")
        
    elif text == '🎥 ហាងរឿង':
        bot.send_message(chat_id, "សូមស្វាគមន៍មកកាន់ហាងរឿង! 🎬 សូមជ្រើសរើសរឿងដែលអ្នកចង់មើល។")
        
    elif text == '🛍️ បញ្ជូលប្រាក់':
        bot.send_message(chat_id, "សូមជ្រើសរើសវិធីសាស្ត្របង់ប្រាក់ (ABA, ACLEDA, វីង...)។ 💸")
        
    elif text == '🛠️ ភាសា':
        # បង្កើត Inline Keyboard សម្រាប់រើសភាសា (ប៊ូតុងជាប់សារ)
        inline_markup = InlineKeyboardMarkup()
        btn_kh = InlineKeyboardButton('🇰🇭 ខ្មែរ', callback_data='lang_kh')
        btn_en = InlineKeyboardButton('🇬🇧 English', callback_data='lang_en')
        inline_markup.row(btn_kh, btn_en)
        
        bot.send_message(chat_id, "សូមជ្រើសរើសភាសា / Please select a language 👇", reply_markup=inline_markup)
        
    else:
        bot.send_message(chat_id, "សូមអភ័យទោស ខ្ញុំមិនយល់ទេ។ សូមជ្រើសរើសប៊ូតុងខាងក្រោម។")

# មុខងារសម្រាប់ឆ្លើយតបពេលគេចុចប៊ូតុង Inline (ខ្មែរ ឬ English)
@bot.callback_query_handler(func=lambda call: True)
def handle_language_selection(call):
    chat_id = call.message.chat.id
    
    if call.data == 'lang_kh':
        # លុបសញ្ញា loading លើប៊ូតុង
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "✅ អ្នកបានប្តូរទៅប្រើប្រាស់ ភាសាខ្មែរ។")
        
    elif call.data == 'lang_en':
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "✅ You have successfully switched to English.")

# ដំណើរការ Bot អោយដើររហូត
if __name__ == "__main__":
    print("Bot កំពុងដំណើរការ...")
    bot.polling(none_stop=True)
