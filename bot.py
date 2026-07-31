import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ---------------------------------------------------------
# تنظیمات - این دو مقدار رو باید از متغیرهای محیطی بگیری
# TELEGRAM_TOKEN از @BotFather
# GEMINI_API_KEY از https://aistudio.google.com/app/apikey (رایگان)
# ---------------------------------------------------------
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

logging.basicConfig(level=logging.INFO)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


def ask_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"خطا در تولید محتوا: {e}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "سلام! من دستیار تولید محتوای حوزه‌ی ادیت هستم.\n\n"
        "دستورات:\n"
        "/script <موضوع> - ساخت اسکریپت ریلز با هوک قوی\n"
        "/caption <موضوع> - ساخت کپشن و هشتگ\n"
        "/idea - ۵ ایده محتوایی تازه در حوزه‌ی ادیت\n"
    )
    await update.message.reply_text(text)


async def script_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)
    if not topic:
        await update.message.reply_text("لطفاً موضوع رو هم بنویس، مثلاً:\n/script قبل و بعد ادیت رنگ")
        return
    await update.message.reply_text("در حال نوشتن اسکریپت...")
    prompt = (
        f"یک اسکریپت ریلز اینستاگرام کمتر از ۳۰ ثانیه درباره‌ی '{topic}' "
        "در حوزه‌ی ادیت ویدیو/عکس بنویس. باید یک هوک جسورانه و کنجکاوی‌برانگیز در ۲ ثانیه اول "
        "داشته باشد، ریتم سریع، یک جمله‌ی محرک ریپلی، و یک CTA غیرمستقیم در پایان. "
        "به زبان فارسی و با ساختار تایم‌بندی‌شده بنویس."
    )
    result = ask_gemini(prompt)
    await update.message.reply_text(result)


async def caption_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)
    if not topic:
        await update.message.reply_text("لطفاً موضوع رو هم بنویس، مثلاً:\n/caption ترنسفورمیشن AI")
        return
    await update.message.reply_text("در حال نوشتن کپشن...")
    prompt = (
        f"برای یک پست اینستاگرام در حوزه‌ی ادیت ویدیو/عکس با موضوع '{topic}' "
        "یک کپشن کوتاه جذاب به فارسی به همراه یک سوال باز برای افزایش کامنت، "
        "و ۸ هشتگ مرتبط (ترکیبی از هشتگ‌های داغ و نیچ) بنویس."
    )
    result = ask_gemini(prompt)
    await update.message.reply_text(result)


async def idea_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در حال فکر کردن به ایده‌ها...")
    prompt = (
        "۵ ایده محتوایی تازه و پرتعامل برای پیج اینستاگرامی در حوزه‌ی "
        "آموزش ادیت ویدیو و عکس پیشنهاد بده. برای هر ایده یک هوک کوتاه هم بنویس. به فارسی."
    )
    result = ask_gemini(prompt)
    await update.message.reply_text(result)


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        raise RuntimeError("TELEGRAM_TOKEN و GEMINI_API_KEY باید تنظیم شده باشند.")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("script", script_cmd))
    app.add_handler(CommandHandler("caption", caption_cmd))
    app.add_handler(CommandHandler("idea", idea_cmd))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
