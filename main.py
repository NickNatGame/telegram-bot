import telebot
import webbrowser
import sqlite3
from yt import video_find

bot = telebot.TeleBot("7509749067:AAGYFN_QgDQ9q3ivLRvV2IVmsGFETFXmOYI")

def save_user(message):
    name = message.text.strip()                                                                        

    conn = sqlite3.connect("users.sql") 
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO users (link, pass) VALUES ('%s','%s')" % (name, message.from_user.id))
    conn.commit()

    cursor.close()
    conn.close()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Список Видео", callback_data="vid"))
    markup.add(telebot.types.InlineKeyboardButton("Добавить еще", callback_data="add"))
    markup.add(telebot.types.InlineKeyboardButton("Найти все видео", callback_data="find_all"))
    bot.send_message(message.chat.id,"ы", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "vid":
        show_all_users(call)
    if call.data == "vid_del":
        clear_users_table(call)
    if call.data == "add":
       one_more(call)
    if call.data == "find_all":
        yt_videos(call)
def yt_videos(call):
    c = video_find(call)
    for i in c:
        bot.send_message(call.message.chat.id,i)
def clear_users_table(call):
    conn = sqlite3.connect("users.sql")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users')
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(call.message.chat.id,"Таблица очищена")
def show_all_users(call):
    conn = sqlite3.connect("users.sql") 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    inf = ""
    for el in users:
        inf += f"link: {el[1]}\nPass: {el[2]}\n\n"
    cursor.close()
    conn.close()
    bot.send_message(call.message.chat.id,inf)
def one_more(call):
    bot.send_message(call.message.chat.id,"Введите название видео, которое хотите добавить")
    bot.register_next_step_handler(call.message, save_user)

@bot.message_handler(commands = ['start'])
def main(message):
    conn = sqlite3.connect("users.sql")
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, link varchar(50),pass varchar(50))')
    
    conn.commit()

    cursor.close()
    conn.close()
    bot.send_message(message.chat.id,"Введите название видео, которое хотите добавить")
    bot.register_next_step_handler(message, save_user)

bot.polling(non_stop=True)