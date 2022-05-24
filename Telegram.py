import telebot
from telebot import types
import requests
import time

bot=telebot.TeleBot('5107993569:AAE7vtJ0iixBYo6jqlw1ImKNcTQ028RmLzw')


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("Начать")
markup.add(item1)

markup_null = types.ReplyKeyboardMarkup(resize_keyboard=True)


    
    



wrong_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]
@bot.message_handler(content_types=wrong_types)
def notype(message):
    bot.send_message(message.chat.id,'Пожалуйста, опишите ваш запроp текстом',reply_markup=markup_null)



@bot.message_handler(commands=['start'])
def welcome(message):
        str1="Здравствуйте, {0.first_name}. Я помогу вам выбрать нужный товар!Опишите то, чтобы вы хотели купить".format(message.from_user)
        bot.send_message(message.chat.id, str1,reply_markup=markup, parse_mode='html')
i=1  

@bot.message_handler(commands=['find'])       
def finding(message):
    global i
    i+=1
    ids[message.chat.id]=i
    
    str3='опишите товар, который вам нужен'
    bot.send_message(message.chat.id,str3, parse_mode='html')
    
@bot.message_handler(commands=['bug'])       
def bug_report(message):
    global find_bug  
    str4='опишите ошибку, которую вы нашли'
    bot.send_message(message.chat.id,str4, parse_mode='html')
    find_bug=True
    
find_bug=False        
@bot.message_handler(content_types=['text'])
def sending(message):
    global i
    global find_bug
    if find_bug:
        str5='спасибо за ваш отзыв. Мы расмотрим жалобу и исправим ошибку'
        bot.send_message(message.chat.id,str5, parse_mode='html')
        find_bug=False
        report_f=open('report.txt','w')
        report_f.write(str(message.chat.id)+' : '+message.text)
        report_f.close()
        return
    if message.chat.id in ids.keys():
        id_rec=ids[message.chat.id]
        if id_rec not in texts.keys():
            texts[id_rec]=message.text
        else:
            texts[id_rec]=texts[id_rec]+' '+message.text
      
        url="http://127.0.0.1:3000/api/teleg/"+str(message.chat.id)+'/'+str(id_rec)           
        requests.post(url,{"user_id":str(message.chat.id), "text":texts[id_rec].lower()})
        str2='ваш запрос отправлен в обработку, пожалуйста, подождите'
        bot.send_message(message.chat.id,str2, parse_mode='html')
        itog={'text':'bla bla bla'}
        while 'result' not in itog.keys():
            res = requests.get(url)
            itog = dict(res.json())
            time.sleep(3)
            
        if itog['result']!='':
            result=itog['result']
            bot.send_message(int(itog['user_id']),result, parse_mode='html')
            if ids[itog['user_id']] in texts.keys():
                del texts[ids[itog['user_id']]]
            if itog['user_id'] in ids.keys():
                del ids[itog['user_id']]
        else:
            markup_extra = types.ReplyKeyboardMarkup(resize_keyboard=True)
            extra_question=itog['extra_question']
            extra_values=itog['extra_values'].split(',')
            for j in extra_values:
                markup_extra.add(j)
            
            bot.send_message(int(itog['user_id']),extra_question,reply_markup=markup_extra, parse_mode='html')
       
    else:
        bot.send_message(message.chat.id,'пожалуйста используйте команду find для начала работы', parse_mode='html')
ids={}       
texts={}

bot.polling(none_stop=True)   





