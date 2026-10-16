import telebot
import os
import sqlite3
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ទាញយក Token ពី Environment Variable (BOT_TOKEN) នៅក្នុង Railway
TOKEN = os.getenv('BOT_TOKEN') 
bot = telebot.TeleBot(TOKEN)

# លេខ ID គណនី Telegram របស់អ្នកសម្រាប់ធ្វើជា Admin
ADMIN_ID = 8929688085

# ==========================================
# ១. បង្កើតនិងភ្ជាប់ទៅ Database (SQLite)
# ==========================================
conn = sqlite3.connect('customers.db', check_same_thread=False)
cursor = conn.cursor()

# បង្កើតតារាង (Table) សម្រាប់រក្សាទុកទិន្នន័យអតិថិជន
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        first_name TEXT,
        username TEXT,
        balance REAL DEFAULT 0.0
    )
''')
conn.commit()

# ==========================================
# ២. មុខងារសម្រាប់ពេលមានអ្នកចុច /start
# ==========================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    
    # បញ្ចូលទិន្នន័យទៅក្នុង Database ប្រសិនបើគាត់ជាសមាជិកថ្មី
    cursor.execute('INSERT OR IGNORE INTO users (chat_id, first_name, username) VALUES (?, ?, ?)', 
                   (chat_id, first_name, username))
    conn.commit()

    # បង្កើតផ្ទាំងប៊ូតុងគោល (Main Menu)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton('👨🏻‍💻 គណនី')
    btn2 = KeyboardButton('🎥 ហាងរឿង')
    btn3 = KeyboardButton('🛍️ បញ្ជូលប្រាក់')
    btn4 = KeyboardButton('🛠️ ភាសា')
    
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    
    bot.send_message(
        chat_id, 
        f"សួស្តី {first_name}! សូមស្វាគមន៍មកកាន់ Bot របស់យើង។\nសូមជ្រើសរើសជម្រើសណាមួយខាងក្រោម៖", 
        reply_markup=markup
    )

# ==========================================
# ៣. មុខងារសម្រាប់ Admin (/admin)
# ==========================================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    # ឆែកមើលថាតើអ្នកដែលវាយ /admin នេះពិតជា Admin មែនឬអត់
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ អ្នកមិនមានសិទ្ធិប្រើប្រាស់មុខងារនេះទេ។")
        return
    
    msg = bot.send_message(
        message.chat.id, 
        "🛠️ <b>Admin Panel</b>\n\nសូមវាយបញ្ចូលសារដែលអ្នកចង់ប្រកាស (Broadcast) ទៅកាន់សមាជិកទាំងអស់៖\n<i>(ឬវាយ /cancel ដើម្បីបោះបង់)</i>",
        parse_mode="HTML"
    )
    # ចាំចាប់យកសារបន្ទាប់ដែល Admin វាយបញ្ចូល
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "✅ ប្រតិបត្តិការត្រូវបានបោះបង់។")
        return
        
    # ទាញយក chat_id ទាំងអស់ពី Database ដើម្បីផ្ញើសារទៅ
    cursor.execute('SELECT chat_id FROM users')
    users = cursor.fetchall()
    
    success_count = 0
    fail_count = 0
    
    bot.send_message(message.chat.id, "⏳ កំពុងដំណើរការផ្ញើសារ...")
    
    for user in users:
        user_id = user[0]
        try:
            bot.send_message(user_id, f"📢 <b>សេចក្តីប្រកាសពី Admin:</b>\n\n{message.text}", parse_mode="HTML")
            success_count += 1
        except Exception:
            # លោតចូលទីនេះប្រសិនបើ User នោះបាន Block Bot របស់យើង
            fail_count += 1
            
    # រាយការណ៍លទ្ធផលត្រលប់មក Admin វិញ
    bot.send_message(
        message.chat.id, 
        f"✅ <b>ការប្រកាសបានបញ្ចប់!</b>\n\n- ផ្ញើបានជោគជ័យ៖ {success_count} នាក់\n- ផ្ញើមិនចេញ (Blocked)៖ {fail_count} នាក់",
        parse_mode="HTML"
    )

# ==========================================
# ៤. មុខងារឆ្លើយតបប៊ូតុងធម្មតា
# ==========================================
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text
    chat_id = message.chat.id
    
    if text == '👨🏻‍💻 គណនី':
        # ទាញយកទឹកប្រាក់ពី Database
        cursor.execute('SELECT balance FROM users WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()
        balance = result[0] if result else 0.0
        
        bot.send_message(chat_id, f"👤 ឈ្មោះ៖ {message.from_user.first_name}\n💰 ទឹកប្រាក់ក្នុងគណនី៖ ${balance}")
        
    elif text == '🎥 ហាងរឿង':
        bot.send_message(chat_id, "សូមស្វាគមន៍មកកាន់ហាងរឿង! 🎬 សូមជ្រើសរើសរឿងដែលអ្នកចង់មើល។")
        
    elif text == '🛍️ បញ្ជូលប្រាក់':
        bot.send_message(chat_id, "សូមជ្រើសរើសវិធីសាស្ត្របង់ប្រាក់ (ABA, ACLEDA, វីង...)។ 💸")
        
    elif text == '🛠️ ភាសា':
        # បង្ហាញជម្រើសតែភាសាខ្មែរមួយគត់
        inline_markup = InlineKeyboardMarkup()
        btn_kh = InlineKeyboardButton('🇰🇭 ខ្មែរ', callback_data='lang_kh')
        inline_markup.row(btn_kh)
        
        bot.send_message(chat_id, "បច្ចុប្បន្នប្រព័ន្ធគាំទ្រតែភាសាខ្មែរទេ 👇", reply_markup=inline_markup)
        
    else:
        bot.send_message(chat_id, "សូមអភ័យទោស ខ្ញុំមិនយល់ទេ។ សូមជ្រើសរើសប៊ូតុងខាងក្រោម។")

# ==========================================
# ៥. មុខងារពេលចុចប៊ូតុង Inline (ខ្មែរ)
# ==========================================
@bot.callback_query_handler(func=lambda call: True)
def handle_language_selection(call):
    chat_id = call.message.chat.id
    
    if call.data == 'lang_kh':
        bot.answer_callback_query(call.id) # លុបសញ្ញា Loading លើប៊ូតុង
        bot.send_message(chat_id, "✅ អ្នកកំពុងប្រើប្រាស់ ភាសាខ្មែរ។")

# ដំណើរការ Bot អោយដើររហូត
if __name__ == "__main__":
    print("Bot កំពុងដំណើរការ...")
    bot.polling(none_stop=True)
