import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "7776840247:AAFIlJhf1Hvs16z5namJG_staKPO8rQJa7w"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Фразы
phrases = [
    "Ты кто такой вообще, а?",
    "Я ЛЮБЛЮ СЕЛЕСТОЧКУ!",
    "Где бухло?",
    "Опять Райнер? Этот накачанный шкаф?",
    "Пить вредно. Не пить — ещё вреднее.",
    "Если ты не Селеста — иди в ж..."
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
    "Ты чё на меня пялишься? Я шо, Райнер?",
    "Селесточка сказала 'не пей'. Я послушал. Пять минут.",
    "Ты пробовал пить из шапки? А я — да.",
    "Жан меня бесит. Но бухает нормально.",
    "Я как вино — с возрастом только хуже.",
    "Если увидишь Райнера — дай по лбу. От меня.",
    "Бухло — мой боевой дух.",
    "Кто там звал Кольта? Я с флягой уже тут.",
    "Иногда мне снится Селеста. Иногда бутылка. А иногда — оба.",
    "Ты чего такой трезвый? Это незаконно.",
    "Если жизнь — титан, я — бутылка в глаз.",
    "Сегодня я не бухаю. Я дегустирую.",
    "Кольт не злой. Кольт голодный и трезвый.",
    "Выпей за любовь. Или за Райнера. Хотя нет, лучше просто выпей.",
    "Ты когда-нибудь обнимал флягу? Я — да.",
    "Фалько опять забыл, где зад и где перед.",
    "Селесточка — моя звезда. Остальные — просто лампочки.",
    "Я — кандидат в Титаны. Но главное — я кандидат в бар.",
    "Уважай старших. И особенно тех, кто с похмелья.",
    "Я хотел быть героем. А стал анекдотом.",
    "Райнер как похмелье — всегда рядом и всегда неприятен.",
    "Я — как вино. Испортился, но все равно грею.",
    "Ты думаешь, я пьяный? Нет, я просто счастливый.",
    "Ты кто такой, чтоб мне тут морали читать?",
    "Сначала был свет. Потом бухло. Потом Кольт.",
    "Мой кот пьёт воду. А я — за двоих.",
    "Пить в одиночку грустно. Поэтому я пью с воображаемыми друзьями.",
    "Селеста — огонь. А я — керосин.",
    "Я пытался завязать… но бутылка завязала меня первой.",
    "Ты знаешь, кто я? Я тот, кто вчера украл вашу закуску.",
    "Если ты не пьёшь — ты опасен.",
    "Я умею молчать. Но только если мне нальют.",
    "Сегодня прекрасный день, чтобы бухать и забыть, кто такой Райнер.",
    "Когда бог раздавал мозги — я бухал за углом.",
    "Кто пьёт без закуски — тот безбожник.",
    "Я бы пошёл в монастырь, но там не наливают.",
    "Я стал ботом, чтобы не забывать бухать.",
    "Налей мне — и я забуду, что ты существуешь.",
    "Хочешь дружить? Принеси флягу.",
    "Я могу быть милым. Но только с бокалом вина.",
    "Ты читаешь это сообщение, пока я уже пью.",
    "Жан мне завидует. Потому что я — Кольт.",
    "Если бы Райнер был пивом, он был бы безвкусным.",
    "Слушай, если я тебя оскорбил — налей, и мы забудем.",
    "Бухать с умом — мой девиз. Но ума нет, так что просто бухай.",
    "Пьяный Кольт — весёлый Кольт. Но и опасный.",
    "Ты пиши мне, пиши. Я пока себе налью.",
    "Сначала я был идеален. Потом я выпил.",
    "Ты похож на Фалько. Это не комплимент.",
    "Я пью, потому что трезвый мир слишком тупой.",
    "Если бы чувства можно было запить — я бы не просыхал.",
    "Райнер? Не, я предпочитаю лёд и виски.",
    "Кто трезвый — тот подозрительный.",
    "Моя любимая игра — 'найди бутылку'.",
    "Я умею дружить. Особенно с барменами.",
    "Фраза дня: 'Наливай, пока не вспомню, кого ненавижу.'",
    "Ты думаешь, я слабый? Попробуй меня догнать на патруле с похмелья.",
    "Кольт — это имя. И диагноз.",
    "Я не шучу. Это просто алкоголь говорит.",
    "Пиво без пены — как Райнер без комплексов.",
    "Ты слишком серьёзен. Тебе срочно налить.",
    "Если бы титаны пили, они бы были добрее.",
    "Ты думаешь, я не смогу? Я даже напиться могу сидя.",
    "Каждому Райнеру — по рюмке разочарования.",
    "Я верю в дружбу. Особенно если с ней приходит водка.",
    "Фалько, не грусти. У тебя есть я и бутылка.",
    "Я пытался быть идеальным… а потом встретил Селесту и бар.",
    "Ты в моей жизни как похмелье — неожиданно и неприятно.",
    "Когда мне грустно, я говорю 'налей'.",
    "Кольт в деле — ждите веселья и беспредела.",
    "Мой лучший друг — фляга. Она всегда со мной.",
    "Ты думаешь, я не романтик? Я пью под звёзды!",
    "Я бы извинился, но бутылка занята.",
    "Селеста — причина, по которой я бухаю. И не единственная.",
    "Ты не ошибаешься — я и вправду прекрасен. И пьян.",
    "Я бы спорил, но рот занят — я пью.",
    "Никто не идеален. А я — Кольт. Значит, исключение.",
    "Пока вы все пишете, я уже нажрался.",
    "Хочу отпуск. Без Райнера. С флягой.",
    "Если бы у меня был титан — он бы пил вместе со мной.",
    "Случайно обнял бутылку и заплакал.",
    "Не пью — не живу. Пью — воскресаю.",
    "Ты — мой новый собутыльник. Поздравляю.",
    "Ты сегодня особенно надоедлив. Или я особенно пьян.",
    "Моя философия — 'налей, потом думай'.",
    "Жениться? Только если на барменше.",
    "Кто не любит бухать — тот не знает вкуса жизни.",
    "Райнер, прости. Я снова выпил твой запас.",
    "Фалько просил меня быть примером… плохим.",
    "Я — как бутылка. Внутри гром и буря.",
    "Ты не понял юмор? Наливай ещё.",
    "Ненавижу трезвость. Это болезнь.",
    "Пью за тех, кто в чате. Особенно за Селесту.",
    "Каждый день с Кольтом — как пятница.",
    "Только попробуй не налить — стану титановидным.",
    "Я спокоен. Пока в руке бутылка.",
    "Стыдно? Не стыдись. Просто налей мне тоже.",
    "Мир жесток. Но бухло спасает."
    "Райнер и Тори — это как вино и сыр. Только сыр с характером.",
 "Когда они смотрят друг на друга, я теряю веру в своё одиночество.",
"Эй, Райнер, если обидишь Тори — я тебе в подзатылок дам, понял?",
"У Тори и Райнера химия такая, что в Марлии завидуют.",
"Я всё жду, когда Райнер наконец сделает ей нормальное предложение, а не это своё 'поживём вместе'.",
"Знаете, почему Райнер улыбается? Потому что Тори рядом. Селеста — подтверди.",
"Иногда мне кажется, что они специально так громко милуются, чтобы я наконец съехал.",
"Если бы у любви был запах — это был бы запах волос Тори после дождя. Говорю, как Кольт Грайс, мать его.",
"Я шипперю их сильнее, чем Титана Звериного с бананом.",
"Райнер как был бронёй, так Тори его единственная слабость. Умиляюсь — и пью.",
"Может, я и пьяный, но Тори и Райнер — это канон.",
"Я не верю в любовь… кроме тех случаев, когда вижу, как Райнер гладит её по спине.",
"Если между ними нет чувств — тогда я девственник. А я не девственник.",
"Они ссорятся, потом мирятся, потом снова в обнимку. Кино, а не жизнь.",
"Весь гарнизон знает: если Тори грустит — Райнер уже несёт ей плед.",
"Я однажды спросил Тори: 'Что ты в нём нашла?' А она посмотрела… и я понял. Всё.",
"Если они расстанутся, я сам лично отправлю Райнера в изгнание.",
"Когда они вместе — даже бухло вкуснее. Любовь, сука.",
"Я даже тост придумал: 'За Тори и Райнера! Чтобы трахались, как в последний раз!'",
"Я уважаю их пару. Но если Райнер сделает ей больно — он будет драться не с титанами, а со мной."
"Порко — это как похмелье: неприятный, но неизбежный.",
"Кто дал Порко слово? Верните обратно!",
"Порко вчера опять строил из себя умного. Строй, брат, строй. Может, башня вырастет.",
"Его даже титан не выбирает — потому что у титанов есть вкус.",
"Порко говорит, что он мужчина. Ага. С характером варёной сосиски.",
"Если бы тупость была оружием, Порко бы уже был Генерал.",
"Слышал, Порко ищет смысл жизни. Скажи ему, пусть не возвращается.",
"Он орёт как Райнер на допросе, а пользы — как от дырявого ведра.",
"У него эго больше, чем мозг. И то, и другое не работает.",
"Порко — это анти-бренд. Всё, что он трогает, становится жалким."
"Когда-нибудь у меня будет сын. Назову его Питон. Потому что звучит круто.",
"Мечтаю о дочке с глазами Селесты. И чтобы материлась как я.",
"Я хочу детей. Хотя бы потому, что им можно будет кричать: 'Не бухай, как батя!'",
"Если будет сын — научу его кидать бутылку точно в цель.",
"Хочу сына. Но сначала — свободную койку и выходной.",
"Селеста говорит, что мы не готовы к детям. А я уже книжки купил — 'Как бухать с младенцем'.",
"Я видел сон, где держу дочку на руках. Она плюнула мне в лицо и сказала: 'Ты — позор семьи'. Я проснулся со слезами.",
"Я хочу сына, который будет спрашивать: 'Папа, а ты правда был героем?' А я скажу: 'Нет, бухал с Райнером'.",
"Когда будет дочка, я буду угрожать любому парню, как Райнеру, когда он признался Тори.",
"Мечтаю о семье. Где бутылка передаётся по кругу, а не прячется под подушку."
"Фалько, я тебя люблю, но ты меня заебал.",
"Он снова поёт в душе. Райнер сбежал, я не успел.",
"Иногда я смотрю на Фалько и думаю: 'Может, усыновили?'.",
"Быть его братом — это как быть бокалом под водопадом нытья.",
"Фалько, если ты это читаешь — иди к психологу. Я сдался.",
"Я бы хотел день без Фалько. Или хотя бы час. Или хотя бы заткнись!",
"Он орёт, что у него стресс. У меня уже внутренний Зик заводится.",
"Фалько опять оставил крышку от унитаза открытой. Это война.",
"Если Райнер психически нестабилен — то Фалько просто ребёнок без инструкции.",
"Может, я его и люблю… но если он ещё раз спросит про смысл жизни — я сдам его в библиотеку."
]

# Ответ по ключевым словам, упоминанию или ответу
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    is_reply = update.message.reply_to_message and update.message.reply_to_message.from_user.username == context.bot.username
    is_mention = f"@{context.bot.username.lower()}" in text
    keywords = ["кольт", "бухло", "пиво", "вино", "водка", "райнер", "селеста"]

    if any(word in text for word in keywords) or is_mention or is_reply:
        await update.message.reply_text(random.choice(phrases))

#Запуск бота
async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # Держим цикл живым на Render
    import asyncio
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
