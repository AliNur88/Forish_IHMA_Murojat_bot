from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes,
    ConversationHandler, CallbackQueryHandler
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
from telegram.ext import Application
TOKEN = os.environ.get("BOT_TOKEN")  # "BOT_TOKEN" o‘zgartuvchi nomi
app = Application.builder().token(TOKEN).build()

def get_main_menu(user_id):
    if user_id == ADMIN_ID:
        # Admin uchun hech qanday tugma bo‘lmaydi, lekin /start qo‘lda yoziladi
        return ReplyKeyboardMarkup([['/start']], resize_keyboard=True)
    else:
        return ReplyKeyboardMarkup(
            [['Murojat', 'Taklif'], ['/start']],
            resize_keyboard=True
        )

# Bosqichlar
CHOOSING_TYPE, CHOOSING_MAHALLA, GET_FULLNAME, GET_ADDRESS, GET_BIRTHDATE, GET_PASSPORT, GET_JSHSHIR, GET_PHONE, GET_MESSAGE = range(9)

# Admin Telegram ID
ADMIN_ID = 7011996073

# Mahalla ro‘yxati (25 ta)
MAHALLALAR = [
    "Ilonli", "Garasha", "Oqtom", "Egizbuloq", "Nurak", "Osmonsoy", "Uchquloch", "Xonbandi",
    "Darboza", "Qizilqum", "Istiqlol", "Do'stlik", "Uxum", "Bog'don", "O'zbekiston", "Qarobdol",
    "Narvon", "Mustaqillik", "M. Orolov", "Uchma", "Oybek", "Sayyod", "Oqtepa", "Amur Temur", "Qulba"
]

def build_mahalla_buttons():
    buttons = []
    row = []
    for i, name in enumerate(MAHALLALAR, start=1):
        row.append(InlineKeyboardButton(text=name, callback_data=f"mahalla_{name}"))
        if i % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "username yo‘q"
    
    if user_id != ADMIN_ID:
        await update.message.reply_text(
            "📌Assalom alaykum xurmadli fuqaro \n Forish tuman 'INSON' ijtimoiy xizmatlar markazi \n murojaatlar botiga xush kelibsiz!\n"
            "Iltimos, quyidagilardan birini tanlang 'Murojat' yoki 'Taklif' :",
            reply_markup=get_main_menu(user_id)
        )
        return CHOOSING_TYPE
    else:
        await update.message.reply_text(
            f"🛠 Siz administrator hisobisiz. \n Fuqarolarning murojaatlari shu yerga keladi.",
            reply_markup=get_main_menu(user_id)
        )
        return ConversationHandler.END


async def choose_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["type"] = update.message.text
    await update.message.reply_text("Ayni vaqtda yashab turgan Mahallangizni tanlang:", reply_markup=build_mahalla_buttons())
    return CHOOSING_MAHALLA

async def mahalla_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    mahalla_nomi = query.data.replace("mahalla_", "")
    context.user_data["mahalla"] = mahalla_nomi
    await query.message.edit_text(f"✅ Mahalla: {mahalla_nomi}\n\nIltimos, F.I.SH gizni kiriting:\n ❌ to'liq va to'g'ri kiritilganligiga e'tiborli bo'ling! \n Namuna: Aliyev Vali Ali o'g'li")
    return GET_FULLNAME

async def get_fullname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["fullname"] = update.message.text
    await update.message.reply_text("Yashash manzilingizni kiriting:\n ❌ to'liq va to'g'ri kiritilganligiga e'tiborli bo'ling! \n Namuna: Forish tumani Garasha MFY Garasha qishlog'i Garasha ko'chasi 18-uy")
    return GET_ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.message.text
    await update.message.reply_text("Tug‘ilgan yilingizni kiriting:\n ❌ to'liq va to'g'ri kiritilganligiga e'tiborli bo'ling!\n Namuna: 01.01.2000-yil")
    return GET_BIRTHDATE

async def get_birthdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["birthdate"] = update.message.text
    await update.message.reply_text("Passport seriya va raqamingizni kiriting:\n ❌ to'liq va to'g'ri kiritilganligiga e'tiborli bo'ling!\n Namuna: AB123456")
    return GET_PASSPORT

async def get_passport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["passport"] = update.message.text
    await update.message.reply_text("JSHSHIR raqamingizni kiriting (faqat raqam):\n ❌ to'liq va to'g'ri kiritilganligiga e'tiborli bo'ling! \n Namuna: 14 xonali raqam")
    return GET_JSHSHIR

async def get_jshshir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text.isdigit():
        await update.message.reply_text("❗ Iltimos, faqat raqam kiriting:")
        return GET_JSHSHIR
    context.user_data["jshshir"] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting (faqat raqam):\n ❌ to'liq va to'g'ri kiritilganligiga e'tiborli bo'ling!\n 99-897-644-88-87")
    return GET_PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text.isdigit():
        await update.message.reply_text("❗ Iltimos, faqat raqam kiriting:")
        return GET_PHONE
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Endi murojaatingizni yozing:\n ❌ To'liq va to'g'ri kiritilganligiga e'tiborli bo'ling!")
    return GET_MESSAGE

async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["message"] = update.message.text

    user = update.effective_user
    username = f"@{user.username}" if user.username else "(username yo'q)"

    msg = f"""📝 Yangi {context.user_data['type']} keldi:
👤 Ism Familiya Otasining ismi: {context.user_data['fullname']}
🏘 Mahalla: {context.user_data['mahalla']}
📍 Manzil: {context.user_data['address']}
🎂 Tug‘ilgan yil: {context.user_data['birthdate']}
🆔 Passport: {context.user_data['passport']}
🔢 JSHSHIR: {context.user_data['jshshir']}
📞 Telefon: {context.user_data['phone']}
✉️ Murojaat: {context.user_data['message']}
👤 Foydalanuvchi: {username}
"""

    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    await update.message.reply_text("✅ Murojaatingiz qabul qilindi. Rahmat! \n Botdan qaytadan foydalanish uchun /start knopkasini bosing")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.")
    return ConversationHandler.END



conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSING_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_type)],
        CHOOSING_MAHALLA: [CallbackQueryHandler(mahalla_callback)],
        GET_FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fullname)],
        GET_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
        GET_BIRTHDATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birthdate)],
        GET_PASSPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_passport)],
        GET_JSHSHIR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_jshshir)],
        GET_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        GET_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_message)],
    },
    fallbacks=[CommandHandler('start', start)],
)

app.add_handler(conv_handler)
app.run_polling()
