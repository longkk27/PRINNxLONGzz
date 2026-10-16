import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get('BOT_TOKEN', 'ដាក់_TOKEN_របស់អ្នកនៅទីនេះ')
bot = telebot.TeleBot(BOT_TOKEN)

# ទិន្នន័យរបស់អ្នកប្រើប្រាស់ (សាកល្បង)
user_languages = {}
user_balances = {} 

TEXTS = {
    'km': {
        'btn_account': '👨🏻‍💻 គណនី',
        'btn_shop': '🛍️ ហាងសេវា',
        'btn_deposit': '💸 បញ្ជូលប្រាក់',
        'btn_lang': '🌐 ប្ដូរភាសា',
        'welcome': 'សួស្ដី <b>{name}</b>! សូមស្វាគមន៍មកកាន់ Bot របស់យើង។ សូមជ្រើសរើសជម្រើសខាងក្រោម៖',
        'account_info': '🧾 <b>ព័ត៌មានគណនីរបស់អ្នក៖</b>\n\n👤 ឈ្មោះ៖ <b>{name}</b>\n🆔 លេខសម្គាល់៖ <code>{user_id}</code>\n💰 សមតុល្យ៖ <b>${balance}</b>',
        'shop_info': '🛒 <b>ហាងសេវាកម្ម</b>\n\nសូមជ្រើសរើសសេវាកម្មហ្គេមដែលអ្នកចង់បាន៖',
        'deposit_info': 'សូមជ្រើសរើសវិធីសាស្ត្របង់ប្រាក់ (ឧទាហរណ៍៖ ABA, ACLEDA...) ដើម្បីបញ្ចូលប្រាក់។',
        'choose_lang': 'សូមជ្រើសរើសភាសា / Please select a language:',
        'lang_changed': '✅ ភាសាត្រូវបានផ្លាស់ប្តូរដោយជោគជ័យ!',
        'invalid': 'សូមជ្រើសរើសជម្រើសដែលមាននៅលើប៊ូតុង។',
        'selected_roblox': '🎮 អ្នកបានជ្រើសរើស <b>Roblox</b>។ (សូមរង់ចាំការអាប់ដេតកញ្ចប់សេវាកម្ម...)',
        'selected_ml': '⚔️ អ្នកបានជ្រើសរើស <b>Mobile Legends</b>។ (សូមរង់ចាំការអាប់ដេតកញ្ចប់សេវាកម្ម...)'
    },
    'en': {
        'btn_account': '👨🏻‍💻 Account',
        'btn_shop': '🛍️ Shop',
        'btn_deposit': '💸 Deposit',
        'btn_lang': '🌐 Change Language',
        'welcome': 'Hello <b>{name}</b>! Welcome to our Bot. Please select an option below:',
        'account_info': '🧾 <b>Your Account Information:</b>\n\n👤 Name: <b>{name}</b>\n🆔 ID: <code>{user_id}</code>\n💰 Balance: <b>${balance}</b>',
        'shop_info': '🛒 <b>Service Shop</b>\n\nPlease choose a game service below:',
        'deposit_info': 'Please select a payment method to deposit money.',
        'choose_lang': 'Please select a language / សូមជ្រើសរើសភាសា:',
        'lang_changed': '✅ Language changed successfully!',
        'invalid': 'Please choose an option from the menu.',
        'selected_roblox': '🎮 You selected <b>Roblox</b>. (Packages coming soon...)',
        'selected_ml': '⚔️ You selected <b>Mobile Legends</b>. (Packages coming soon...)'
    }
}

def send_main_menu(chat_id, user_name):
    lang = user_languages.get(chat_id, 'km')
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    markup.add(
        KeyboardButton(TEXTS[lang]['btn_account']),
        KeyboardButton(TEXTS[lang]['btn_shop'])
    )
    markup.add(
        KeyboardButton(TEXTS[lang]['btn_deposit']),
        KeyboardButton(TEXTS[lang]['btn_lang'])
    )
    
    msg_text = TEXTS[lang]['welcome'].format(name=user_name)
    bot.send_message(chat_id, msg_text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_main_menu(message.chat.id, message.from_user.first_name)

# មុខងារសម្រាប់បង្ហាញហាងសេវា (Shop Menu)
def send_shop_menu(chat_id):
    lang = user_languages.get(chat_id, 'km')
    markup = InlineKeyboardMarkup(row_width=2)
    
    # បង្កើតប៊ូតុងសម្រាប់ហ្គេម
    btn_roblox = InlineKeyboardButton("🎮 Roblox", callback_data="shop_roblox")
    btn_ml = InlineKeyboardButton("⚔️ Mobile Legends", callback_data="shop_ml")
    
    markup.add(btn_roblox, btn_ml)
    
    bot.send_message(chat_id, TEXTS[lang]['shop_info'], reply_markup=markup, parse_mode="HTML")

def send_language_options(chat_id):
    lang = user_languages.get(chat_id, 'km')
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🇰🇭 ខ្មែរ", callback_data="lang_km"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )
    bot.send_message(chat_id, TEXTS[lang]['choose_lang'], reply_markup=markup)

# ចាប់យកការចុចលើប៊ូតុង Inline ទាំងអស់ (ភាសា និង ហាងសេវា)
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_callbacks(call):
    chat_id = call.message.chat.id
    lang = user_languages.get(chat_id, 'km')
    
    # សម្រាប់ប្ដូរភាសា
    if call.data.startswith('lang_'):
        user_languages[chat_id] = 'km' if call.data == 'lang_km' else 'en'
        lang = user_languages[chat_id]
        
        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, TEXTS[lang]['lang_changed'])
        send_main_menu(chat_id, call.from_user.first_name)
        
    # សម្រាប់ពេលចុចលើហ្គេមក្នុងហាងសេវា
    elif call.data == 'shop_roblox':
        bot.answer_callback_query(call.id) # ដើម្បីកុំឱ្យប៊ូតុង loading យូរ
        bot.send_message(chat_id, TEXTS[lang]['selected_roblox'], parse_mode="HTML")
        
    elif call.data == 'shop_ml':
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, TEXTS[lang]['selected_ml'], parse_mode="HTML")

@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    chat_id = message.chat.id
    lang = user_languages.get(chat_id, 'km')
    text = message.text
    
    if text in [TEXTS['km']['btn_account'], TEXTS['en']['btn_account']]:
        user_id = message.from_user.id
        balance = user_balances.get(chat_id, 0.00) 
        msg_text = TEXTS[lang]['account_info'].format(
            name=message.from_user.first_name,
            user_id=user_id,
            balance=f"{balance:.2f}"
        )
        bot.send_message(chat_id, msg_text, parse_mode="HTML")
        
    elif text in [TEXTS['km']['btn_shop'], TEXTS['en']['btn_shop']]:
        # ហៅមុខងារបង្ហាញហាងសេវា
        send_shop_menu(chat_id)
        
    elif text in [TEXTS['km']['btn_deposit'], TEXTS['en']['btn_deposit']]:
        bot.send_message(chat_id, TEXTS[lang]['deposit_info'])
        
    elif text in [TEXTS['km']['btn_lang'], TEXTS['en']['btn_lang']]:
        send_language_options(chat_id)
        
    else:
        bot.send_message(chat_id, TEXTS[lang]['invalid'])

if __name__ == "__main__":
    print("Bot កំពុងដំណើរការ...")
    bot.polling(none_stop=True)
