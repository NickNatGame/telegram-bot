from youtubesearchpython import VideosSearch
import sqlite3
import telebot

def video_find(call):
    conn = sqlite3.connect("users.sql") 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    all = []
    user_id = call.from_user.id
    for i in users:
        if i[2] == f"{user_id}":
            search = VideosSearch(i[1], limit = 1)
            result = search.result()
            video_link = result['result'][0]['link']
            all.append(video_link)
    return all