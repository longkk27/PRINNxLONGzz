import os
import time
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get('BOT_TOKEN', 'ដាក់_TOKEN_របស់អ្នកនៅទីនេះ')
bot = telebot.TeleBot(BOT_TOKEN)

# ==================== កន្លែងផ្ទុកទិន្នន័យ (សាកល្បង) ====================
user_languages = {}
user_balances = {} 
last_message_time = {} 
user_states = {} # សម្រាប់ចំណាំថា User កំពុងធ្វើអ្វី (ឧ. កំពុងវាយបញ្ចូលទឹកប្រាក់ ឬ រង់ចាំផ្ញើរូប)

# កំណត់រូបភាព KHQR របស់អ្នក
KHQR_IMAGE_URL = "https://img.sanishtech.com/u/dd2a3178b476e2329cff92e51b489463.jpeg"
RATE_LIMIT_SECONDS = 1.0 

# ==================== អត្ថបទ (Text) ====================
TEXTS = {
    'km': {
        'btn_account': '👨🏻‍💻 គណនី',
        'btn_shop': '🛍️ ហាងសេវា',
        'btn_deposit': '💸 បញ្ជូលប្រាក់',
        'btn_lang': '🌐 ប្ដូរភាសា',
        'welcome': 'សួស្ដី <b>{name}</b>! សូមស្វាគមន៍មកកាន់ Bot របស់យើង។ សូមជ្រើសរើសជម្រើសខាងក្រោម៖',
        'account_info': '🧾 <b>ព័ត៌មានគណនីរបស់អ្នក៖</b>\n\n👤 ឈ្មោះ៖ <b>{name}</b>\n🆔 លេខសម្គាល់៖ <code>{user_id}</code>\n💰 សមតុល្យ៖ <b>${balance}</b>',
        'shop_info': '🛒 <b>ហាងសេវាកម្ម</b>\n\nសូមជ្រើសរើសសេវាកម្មហ្គេមដែលអ្នកចង់បាន៖',
        'deposit_ask_amount': 'សូមវាយបញ្ចូលចំនួនទឹកប្រាក់ដែលអ្នកចង់ដាក់ ៖\n<i>(ឧទាហរណ៍៖ វាយលេខ 5 សម្រាប់ការដាក់ 5$)</i>',
        'deposit_generating': '⏳ កំពុងបង្កើត KHQR CODE ជូនលោកអ្នក...',
        'deposit_qr_caption': 'សូមស្កេន KHQR ខាងលើដើម្បីបង់ប្រាក់ចំនួន <b>${amount}</b>។\n\n📸 បន្ទាប់ពីបង់ប្រាក់រួចរាល់ <b>សូមផ្ញើរូបភាពប្រតិបត្តិការ (Screenshot)</b> មកកាន់ទីនេះ ដើម្បីឲ្យយើងពិនិត្យ។',
        'deposit_invalid_amount': '❌ សូមបញ្ចូលចំនួនទឹកប្រាក់ជាលេខឲ្យបានត្រឹមត្រូវ! (ឧ. 5 ឬ 10.5)',
        'deposit_receipt_received': '✅ យើងទទួលបានរូបភាពប្រតិបត្តិការរបស់អ្នកហើយ! \nប្រាក់នឹងត្រូវបានបញ្ចូលទៅក្នុងគណនីរបស់អ្នក បន្ទាប់ពីក្រុមការងារយើងធ្វើការត្រួតពិនិត្យរួចរាល់។',
        'choose_lang': 'សូមជ្រើសរើសភាសា / Please select a language:',
        'lang_changed': '✅ ភាសាត្រូវបានផ្លាស់ប្តូរដោយជោគជ័យ!',
        'invalid': 'សូមជ្រើសរើសជម្រើសដែលមាននៅលើប៊ូតុង។',
        'spam_warning': '⚠️ សូមមេត្តាកុំចុចលឿនពេក។ សូមរង់ចាំបន្តិច!'
    },
    'en': {
        'btn_account': '👨🏻‍💻 Account',
        'btn_shop': '🛍️ Shop',
        'btn_deposit': '💸 Deposit',
        'btn_lang': '🌐 Change Language',
        'welcome': 'Hello <b>{name}</b>! Welcome to our Bot. Please select an option below:',
        'account_info': '🧾 <b>Your Account Information:</b>\n\n👤 Name: <b>{name}</b>\n🆔 ID: <code>{user_id}</code>\n💰 Balance: <b>${balance}</b>',
        'shop_info': '🛒 <b>Service Shop</b>\n\nPlease choose a game service below:',
        'deposit_ask_amount': 'Please enter the deposit amount:\n<i>(Example: type 5 for $5)</i>',
        'deposit_generating': '⏳ Generating KHQR CODE...',
        'deposit_qr_caption': 'Please scan the KHQR above to pay <b>${amount}</b>.\n\n📸 After payment, <b>please send the transaction screenshot</b> here for verification.',
        'deposit_invalid_amount': '❌ Please enter a valid numeric amount! (e.g., 5 or 10.5)',
        'deposit_receipt_received': '✅ Transaction screenshot received!\nYour balance will be updated as soon as our team verifies the payment.',
        'choose_lang': 'Please select a language / សូមជ្រើសរើសភាសា:',
        'lang_changed': '✅ Language changed successfully!',
        'invalid': 'Please choose an option from the menu.',
        'spam_warning': '⚠️ Please do not click too fast. Please wait!'
    }
}

# ==================== អនុគមន៍ជំនួយ ====================
def is_spam(user_id):
    current_time = time.time()
    if user_id in last_message_time:
        if current_time - last_message_time[user_id] < RATE_LIMIT_SECONDS:
            return True
    last_message_time[user_id] = current_time
    return False

def send_main_menu(chat_id, user_name):
    user_states[chat_id] = None # Reset ស្ថានភាព
    lang = user_languages.get(chat_id, 'km')
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton(TEXTS[lang]['btn_account']), KeyboardButton(TEXTS[lang]['btn_shop']))
    markup.add(KeyboardButton(TEXTS[lang]['btn_deposit']), KeyboardButton(TEXTS[lang]['btn_lang']))
    
    msg_text = TEXTS[lang]['welcome'].format(name=user_name)
    bot.send_message(chat_id, msg_text, reply_markup=markup, parse_mode="HTML")

# ==================== Handlers ====================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if is_spam(user_id): return
    send_main_menu(message.chat.id, message.from_user.first_name)

# ចាប់យករូបភាព (Photos) សម្រាប់ពេលភ្ញៀវផ្ញើវិក្កយបត្រ
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    chat_id = message.chat.id
    lang = user_languages.get(chat_id, 'km')
    
    # ពិនិត្យមើលថាតើគាត់កំពុងស្ថិតក្នុងវគ្គរង់ចាំផ្ញើវិក្កយបត្រឬទេ
    if user_states.get(chat_id) == 'WAITING_RECEIPT':
        bot.send_message(chat_id, TEXTS[lang]['deposit_receipt_received'])
        user_states[chat_id] = None # Reset state មកធម្មតាវិញ
        
        # 💡 (កំណត់ចំណាំសម្រាប់អ្នកសរសេរកូដ): 
        # កន្លែងនេះអ្នកអាចបន្ថែមមុខងារ Forward រូបភាពនេះទៅ Group Admin ដើម្បីឲ្យ Admin ឆែកមើល រួច Top-up លុយចូលឲ្យ។
        # ឧ. bot.forward_message(ADMIN_GROUP_ID, chat_id, message.message_id)

@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    lang = user_languages.get(chat_id, 'km')
    
    if is_spam(user_id):
        bot.send_message(chat_id, TEXTS[lang]['spam_warning'])
        return

    text = message.text
    
    # 1. ពេលចុចប៉ះប៊ូតុង Menu គោល (វានឹងកាត់ផ្តាច់ State ចាស់ទាំងអស់)
    if text in [TEXTS['km']['btn_account'], TEXTS['en']['btn_account']]:
        user_states[chat_id] = None
        balance = user_balances.get(chat_id, 0.00) 
        msg_text = TEXTS[lang]['account_info'].format(
            name=message.from_user.first_name,
            user_id=user_id,
            balance=f"{balance:.2f}"
        )
        bot.send_message(chat_id, msg_text, parse_mode="HTML")
        
    elif text in [TEXTS['km']['btn_shop'], TEXTS['en']['btn_shop']]:
        user_states[chat_id] = None
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton("🎮 Roblox", callback_data="shop_roblox"),
                   InlineKeyboardButton("⚔️ Mobile Legends", callback_data="shop_ml"))
        bot.send_message(chat_id, TEXTS[lang]['shop_info'], reply_markup=markup, parse_mode="HTML")
        
    elif text in [TEXTS['km']['btn_deposit'], TEXTS['en']['btn_deposit']]:
        # ដូរស្ថានភាពទៅជា "រង់ចាំការវាយបញ្ចូលទឹកប្រាក់"
        user_states[chat_id] = 'WAITING_AMOUNT'
        bot.send_message(chat_id, TEXTS[lang]['deposit_ask_amount'], parse_mode="HTML")
        
    elif text in [TEXTS['km']['btn_lang'], TEXTS['en']['btn_lang']]:
        user_states[chat_id] = None
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🇰🇭 ខ្មែរ", callback_data="lang_km"),
                   InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
        bot.send_message(chat_id, TEXTS[lang]['choose_lang'], reply_markup=markup)
    
    # 2. ប្រសិនបើ User កំពុងស្ថិតក្នុងវគ្គវាយបញ្ចូលទឹកប្រាក់
    elif user_states.get(chat_id) == 'WAITING_AMOUNT':
        try:
            # ព្យាយាមបម្លែងអត្ថបទទៅជាលេខ (អនុញ្ញាតទាំងលេខគត់ និងទសភាគ)
            amount = float(text)
            if amount <= 0:
                raise ValueError
                
            # បើលេខត្រឹមត្រូវ
            bot.send_message(chat_id, TEXTS[lang]['deposit_generating'])
            
            # ប្តូរស្ថានភាពទៅជា "រង់ចាំការផ្ញើរូបភាព"
            user_states[chat_id] = 'WAITING_RECEIPT'
            
            # ផ្ញើ KHQR រូបភាព
            caption_text = TEXTS[lang]['deposit_qr_caption'].format(amount=f"{amount:.2f}")
            bot.send_photo(chat_id, KHQR_IMAGE_URL, caption=caption_text, parse_mode="HTML")
            
        except ValueError:
            # បើវាយខុសពីលេខ ឬវាយអក្សរ
            bot.send_message(chat_id, TEXTS[lang]['deposit_invalid_amount'])
            
    else:
        bot.send_message(chat_id, TEXTS[lang]['invalid'])

# ចាប់យក Inline Buttons (ដូរភាសា និង ហាងសេវា)
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_callbacks(call):
    chat_id = call.message.chat.id
    lang = user_languages.get(chat_id, 'km')
    
    if call.data.startswith('lang_'):
        user_languages[chat_id] = 'km' if call.data == 'lang_km' else 'en'
        lang = user_languages[chat_id]
        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, TEXTS[lang]['lang_changed'])
        send_main_menu(chat_id, call.from_user.first_name)
    elif call.data in ['shop_roblox', 'shop_ml']:
        bot.answer_callback_query(call.id, "មុខងារនេះនឹងមកដល់ឆាប់ៗ!" if lang == 'km' else "Coming soon!")

if __name__ == "__main__":
    print("Bot កំពុងដំណើរការ...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
