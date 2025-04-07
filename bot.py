
import logging
import random
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "7776840247:AAFIlJhf1Hvs16z5namJG_staKPO8rQJa7w"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Огромное количество разнообразных фраз
phrases = [
    "Ты кто такой вообще, а?",
    "Я ЛЮБЛЮ СЕЛЕСТОЧКУ!",
    "Эй, где бухло?",
    "Опять Райнер? Этот накачанный шкаф?",
    "Ты мне налей сначала, а потом пиши.",
    "Я не пью один. Я просто начинаю, пока все собираются.",
    "Фалько, не ори! Я уже на пределе.",
    "Пить вредно. Не пить — ещё вреднее.",
    "Ты че, трезвый? Фу, отойди!",
    "Сначала пиво, потом туман, потом — титаны.",
    "Райнер? Этот шкаф из Марлии?",
    "Сколько можно бухать? — Пока не начнёшь разговаривать с мебелью.",
    "Фраза дня: 'А давай ещё чуть-чуть и спать'.",
    "Я сегодня в режиме 'в говно'. Всё, не трогай меня.",
    "Я тебе сейчас такого бота устрою, что Телеграм плакать будет.",
    "Ты Райнера видел? Накачанный шкаф и два мозговых импульса в неделю.",
    "Если увидишь Фалько — дай подзатыльник.",
    "Ты думаешь, ты мне друг? Ха-ха.",
    "В этом чате только элита. То есть я.",
    "Я тут бухой сижу, а ты мне душу тревожишь.",
    "Я сейчас рюкзак скину и буду драться, как в Парадайзе!",
    "Где бухло — там и я. Где я — там и срач.",
    "Бухать — это искусство. А я Пикассо с перегаром.",
    "Мой рацион: завтрак — водка, обед — пиво, ужин — 'ну налей ещё'.",
    "Хочешь поговорить — говори. Хочешь налить — НАЛЕЙ!",
    "Если ты не принёс бухла — не жди от меня сочувствия.",
    "Я не алкоголик. Я профессионал.",
    "Я не пью. Я увлажняю душу.",
    "Ты вообще знаешь, каково это — быть братом Фалько?",
    "Я не матерюсь, я выражаюсь ёмко!",
    "Селесточка бы так не писала… Хотя кто ты вообще такой?",
    "Если ты не Селеста — иди в ж...",
    "Ты думаешь, быть кандидатом в Титаны — это круто? Да я только за водку туда полез!"
]

# Функция обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    is_reply = update.message.reply_to_message and update.message.reply_to_message.from_user.username == context.bot.username
    is_mention = f"@{context.bot.username.lower()}" in text
    keywords = ["кольт", "бухло", "пиво", "вино", "водка", "райнер", "титаны", "селеста", "фалько"]

    if any(word in text for word in keywords) or is_mention or is_reply:
        response = random.choice(phrases)
        await update.message.reply_text(response)

# Запуск бота
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
