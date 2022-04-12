from telegram import InlineKeyboardButton,InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater,CommandHandler, CallbackQueryHandler,ConversationHandler,MessageHandler, Filters
from db_helper import DBHelper

from kun import kun_bugun


from datetime import datetime,timedelta

import pytz

TOKEN='5265017422:AAFVy7An3OvUR_UCx5dAjkrbVt8ErOwGLDI'
DB_NAME='ramazon.sqlite'



BTN_TODAY='⌛️ Bugun'
BTN_TOMORROW='⏳ Ertaga'
BTN_MONTH="📅 To'liq taqvim"
BTN_REGION='🇺🇿 Mintaqani o\'zgartirish'
BTN_DUA='🤲 Duo'
# RESTART1="Muommo yuzaga kelganda ➡️ /start ⬅️ bo\'limini bosing."
RESTART='/start'

main_buttons=ReplyKeyboardMarkup([
    [RESTART],[BTN_TODAY],[BTN_TOMORROW,BTN_MONTH],[BTN_REGION],[BTN_DUA]
], resize_keyboard=True)

STATE_REGION=1
STATE_CALENDAR=2
user_region=dict()
db=DBHelper(DB_NAME)

def regions_buttons():
    regions=db.get_regions()
    buttons=[]
    tmp=[]
    for region in regions:
        tmp.append(InlineKeyboardButton(region['name'],callback_data=region['id']))
        if len(tmp)==2:
            buttons.append(tmp)
            tmp=[]
    return buttons

def start(update, context):
    user=update.message.from_user
    user_region[user.id]=None
    buttons=regions_buttons()
    
    update.message.reply_html("Assalomu alaykum <b>{} {}!</b>\n \n<b>Ramazon oyi muborak bo'lsin</b>".format(user.first_name, user.last_name))
    update.message.reply_html("Sizga qaysi mintaqa bo'yicha ma'lumot berayin.", reply_markup=InlineKeyboardMarkup(buttons))
    return STATE_REGION

def inline_callback(update,context):
    query=update.callback_query
    user_id=query.from_user.id
    user_region[user_id]=int(query.data)
    query.message.delete()
    
    region_id=user_region[user_id]
    region=db.get_region(region_id)
    
    query.message.reply_html(text="<b>Ramazon taqvimi</b> 2️⃣0️⃣2️⃣2️⃣\n \n<b>{} vaqti bo'yicha</b> \n \nQuyidagilardan birini tanlang 👇".format(region['name']),reply_markup=main_buttons)
    return STATE_CALENDAR

def restart1():
    pass

# def restart(update, context):
#     user=update.message.from_user
#     user_region[user.id]=None
#     buttons=regions_buttons()
    
#     update.message.reply_html("Assalomu alaykum <b>{} {}!</b>\n \n<b>Ramazon oyi muborak bo'lsin</b>".format(user.first_name, user.last_name))
#     update.message.reply_html("Sizga qaysi mintaqa bo'yicha ma'lumot berayin.", reply_markup=InlineKeyboardMarkup(buttons))
#     return STATE_REGION

# def inline_callback(update,context):
#     query=update.callback_query
#     user_id=query.from_user.id
#     user_region[user_id]=int(query.data)
#     query.message.delete()
    
#     region_id=user_region[user_id]
#     region=db.get_region(region_id)
    
#     query.message.reply_html(text="<b>Ramazon taqvimi</b> 2️⃣0️⃣2️⃣2️⃣\n \n<b>{} vaqti bo'yicha</b> \n \nQuyidagilardan birini tanlang 👇".format(region['name']),reply_markup=main_buttons)
#     return STATE_CALENDAR


def calendar_today(update,context):
    user_id=update.message.from_user.id
    if not user_region[user_id]:
        return STATE_REGION
    region_id=user_region[user_id]
    region=db.get_region(region_id)
    
    time_zone = pytz.timezone('Asia/Tashkent')
    today=str(datetime.now(time_zone))[:10]
    # print(today)
    # print(kun_bugun())
    # vaqt=kun_bugun()
    # print(vaqt)
    if today=='2022-03-28' or today=='2022-03-29' or today=='2022-03-30' or today=='2022-03-31' or today=='2022-04-01':
        # print('false')
        update.message.reply_html("<b>Ramazon</b> oyi <b>2-aprel</b>dan boshlanadi.\n \nRamazon oyi boshlangunga qadar bu <b>Telegram bot</b>ni do\'stlaringizga jo\'natib qo\'yishingizni so\'rab qolaman.\n \nRamazon oyi 2-apreldan boshlanadi, shu bilan birga 1-aprel kunidan boshlab ⏳ <b>Ertaga</b> va 📅 <b>To\'liq taqvim</b> bo\'limlari ishlashni boshlaydi")
    else:
        # print('true')
        
        calendar=db.get_calendar_by_region(region_id,today)
        photo_path='images/img/{}.png'.format(calendar['id'])
        xabar="<b>Ramazon 2022</b> \n \n<b>{}</b> vaqti\n \nSana: <b>{} {}</b>\n \nSaharlik: <b>{}</b>\nIftorlik: <b>{}</b>".format(region['name'], calendar['sana'], calendar['hafta_kuni'], calendar['saharlik'],calendar['iftorlik']  )
        update.message.reply_photo( photo=open(photo_path, 'rb'),caption=xabar, parse_mode='HTML',reply_markup=main_buttons)
    

def calendar_tomorrow(update,context):
    user_id=update.message.from_user.id
    if not user_region[user_id]:
        return STATE_REGION
    region_id=user_region[user_id]
    region=db.get_region(region_id)
    
    time_zone = pytz.timezone('Asia/Tashkent')
    today1=str(datetime.now(time_zone))[:10]
    today2=str(datetime.now(time_zone)+timedelta(days=1))
    print(today2)
    today=str(datetime.now(time_zone)+timedelta(days=1))[:10]
    if today1=='2022-03-28' or today1=='2022-03-29' or today1=='2022-03-30' or today1=='2022-03-31':
        # print('false')
        update.message.reply_html("<b>Ramazon</b> oyi <b>2-aprel</b>dan boshlanadi.\n \nRamazon oyi boshlangunga qadar bu <b>Telegram bot</b>ni do\'stlaringizga jo\'natib qo\'yishingizni so\'rab qolaman.\n \nRamazon oyi 2-apreldan boshlanadi, shu bilan birga 1-aprel kunidan boshlab ⏳ <b>Ertaga</b> va 📅 <b>To\'liq taqvim</b> bo\'limlari ishlashni boshlaydi")
    else:
        # print('true')
        calendar=db.get_calendar_by_region(region_id,today)
        photo_path='images/img/{}.png'.format(calendar['id'])
        xabar="<b>Ramazon 2022</b> \n \n<b>{}</b> vaqti\n \nSana: <b>{} {}</b>\n \nSaharlik: <b>{}</b>\nIftorlik: <b>{}</b>".format(region['name'], calendar['sana'], calendar['hafta_kuni'], calendar['saharlik'],calendar['iftorlik']  )
        update.message.reply_photo( photo=open(photo_path, 'rb'),caption=xabar, parse_mode='HTML',reply_markup=main_buttons)
    

def calendar_month(update,context):
    user_id=update.message.from_user.id
    if not user_region[user_id]:
        return STATE_REGION
    region_id=user_region[user_id]
    region=db.get_region(region_id)
    
    time_zone = pytz.timezone('Asia/Tashkent')
    today=str(datetime.now(time_zone))[:10]
    calendar=db.get_calendar_by_region(region_id,today)
    if today=='2022-03-28' or today=='2022-03-29' or today=='2022-03-30' or today=='2022-03-31':
        # print('false')
        update.message.reply_html("<b>Ramazon</b> oyi <b>2-aprel</b>dan boshlanadi.\n \nRamazon oyi boshlangunga qadar bu <b>Telegram bot</b>ni do\'stlaringizga jo\'natib qo\'yishingizni so\'rab qolaman.\n \nRamazon oyi 2-apreldan boshlanadi, shu bilan birga 1-aprel kunidan boshlab ⏳ <b>Ertaga</b>  va 📅 <b>To\'liq taqvim</b> bo\'limlari ishlashni boshlaydi")
    else:
        # print('true')
        photo_path='images/taqvim_oylik/{}.png'.format(region['id'])
        xabar="<b>Ramazon 2022</b> \n \n<b>{}</b> vaqti".format(region['name'])
        update.message.reply_photo( photo=open(photo_path, 'rb'),caption=xabar, parse_mode='HTML',reply_markup=main_buttons)
    

def select_region(update,context):
     buttons=regions_buttons()
     update.message.reply_text("Sizga qaysi mintaqa bo'yicha ma'lumot berayin.", reply_markup=InlineKeyboardMarkup(buttons))
     return STATE_REGION

def select_dua(update,context):
    update.message.reply_photo(photo=open('images/duo.png','rb'))

def main():
    # Updterni o'rnatib olamiz
    updater = Updater(TOKEN,use_context=True)
    
    # dispatcher eventlarini aniqlash uchun
    dispatcher=updater.dispatcher
    
    #  start komandasini ushlab qolish
    # dispatcher.add_handler(CommandHandler('start', start))
    
    # dispatcher.add_handler(CallbackQueryHandler(inline_callback))
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start' , start)],
        states={
            STATE_REGION:[
                CallbackQueryHandler(inline_callback),
                # MessageHandler(Filters.regex('^('+RESTART+')$'),start),
                MessageHandler(Filters.regex('^('+BTN_TODAY+')$'),calendar_today),
                MessageHandler(Filters.regex('^('+BTN_TOMORROW+')$'),calendar_tomorrow),
                MessageHandler(Filters.regex('^('+BTN_MONTH+')$'),calendar_month),
                MessageHandler(Filters.regex('^('+BTN_REGION+')$'),select_region),
                MessageHandler(Filters.regex('^('+BTN_DUA+')$'),select_dua)
                
                ],
            STATE_CALENDAR:[
                # MessageHandler(Filters.regex('^('+RESTART+')$'),start),
                MessageHandler(Filters.regex('^('+BTN_TODAY+')$'),calendar_today),
                MessageHandler(Filters.regex('^('+BTN_TOMORROW+')$'),calendar_tomorrow),
                MessageHandler(Filters.regex('^('+BTN_MONTH+')$'),calendar_month),
                MessageHandler(Filters.regex('^('+BTN_REGION+')$'),select_region),
                MessageHandler(Filters.regex('^('+BTN_DUA+')$'),select_dua)
                
            ],
        },
        fallbacks=[CommandHandler('start', start)]
    )
    
    dispatcher.add_handler(conv_handler)
    
    updater.start_polling()
    updater.idle()
    
main()