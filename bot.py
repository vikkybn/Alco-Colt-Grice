import logging
import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

import os
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Пример фраз (можешь вставить сюда весь свой массив)
phrases = [
    "Селеста говорит, что я пью слишком много… А я просто тренируюсь быть Титаном Бухущим.",
    "ВСЕМ СОСАТЬ ШЛЮШКИ ГЫГЫГЫГГЫГЫ",
    "Райнер опять орёт во сне. Я ему как-то налил на подушку — и он проснулся счастливым. Не благодарил.",
    "Фалько спросил, как стать героем. Я сказал — научись держать водку. Сука, вылил. Не герой.",
    "Я тебя сейчас так обниму, что тебе психиатр понадобится.",
    "Был бы у меня мозг — я бы страдал. А так просто бухаю.",
    "Если бы я был героем — то только трагедии.",
    "Фалько опять спросил, зачем я пью. Сука, ты причина!",
    "Тёлочки — как пиво. Холодные, игривые и быстро заканчиваются.",
    "Я уважаю тёлочек. Особенно тех, кто наливает и не спрашивает, где я был ночью.",
    "Иногда тёлочки говорят: 'Ты не в моём вкусе'. А я и не еда, я Кольт!",
    "Тёлочки бывают двух видов: те, кто с Кольтом, и те, кто ещё не поняли, что хотят быть с Кольтом.",
    "Я романтик. Могу смотреть на тёлочку целых пять секунд, не моргая. Потом — комплимент. Потом — водка.",
    "Сначала она сказала 'не пей'. Потом — 'не звони'. Потом — 'ну ладно, приходи'. Сила тёлочек необъяснима.",
    "Моя любимая поза? Когда она сверху, а я с флягой в руке и оргазмом в душе.",
    "Секс — это как патруль: если быстро — то бессмысленно, если медленно — то можно отдохнуть.",
    "Я не извращенец. Я просто уважаю анатомию под любым углом.",
    "Ты видел, как Селеста волосы за ухо убирает? Я в этот момент готов лечь на спину и сдаться.",
    "Фетиш? Да у меня целый альбом. Селеста в форме. Селеста без формы. Селеста с кнутом. Селеста с бутылкой.",
    "Моя поза — звезда разведки. Распластался и принимаю ласку судьбы.",
    "Селеста говорит 'не сейчас' — я воспринимаю это как квест на терпение. Терплю… минут пять.",
    "Лучше орального секса только оральный секс с одновременным тостом.",
    "Я не люблю быстрый секс. Я люблю секс со вкусом — например, текилы.",
    "Иногда я смотрю на Селесту и думаю… я бы и без бухла сделал глупость. А с бухлом — дважды.",
    "Моё безопасное слово — 'налей'. Если слышишь его в постели — значит, всё идёт как надо.",
    "Фетиш? Я люблю, когда она матерится. Особенно когда я не попадаю… туда, куда хотел.",
    "Секс должен быть как бой с титаном — с риском, страстью и потом обнимашками на руинах.",
    "Моя эрогенная зона — шея. Особенно если на ней стоит стопка рома.",
    "Я люблю, когда тёлочка на каблуках. Особенно если эти каблуки на мне.",
    "Селеста любит романтику. Я люблю... когда она в трусах с котиками шепчет, что я её герой.",
    "Был у меня один секс — как падение стены Мария: громкий, трагичный и все пострадали.",
    "Позы? Мне любая подойдёт, где видно грудь и я не падаю с кровати.",
    "Я практикую обратную наездницу. Селеста — спиной, а я — в шоке и с бокалом вина.",
    "Я однажды сказал: 'Сделай мне больно'. Селеста включила сериал без субтитров. Боль была реальной."
    "Ты видел этих тёлочек в казарме? Одна Селеста чего стоит. У меня на неё броня не срабатывает.",
    "Если тёлочка не отвечает — это не отказ. Это челлендж.",
    "Лучшее в жизни: бутылка в руке, тёлочка на коленях и Фалько где-то далеко-далеко.",
    "Все тёлочки любят плохих парней. Я — максимально непригоден. Получается, я идеал?",
    "Я не влюбчивый. Я просто обнимаю всех тёлочек по-пьяни. Это рефлекс.",
    "Селеста сказала, что я озабоченный. Я сказал — это гормоны патриотизма.",
    "Некоторые тёлочки говорят, что хотят серьёзные отношения. А я — крепкие напитки и острые ощущения.",
    "Тёлочки — как разведка. Сначала втираются в доверие, потом уносят последнюю бутылку.",
    "У меня с тёлочками всё сложно. Я их люблю. А они любят трезвых.",
    "Вечером встречаешь тёлочку — она богиня. Утром просыпаешься — и ты снова пьёшь.",
    "Спросил у тёлочки, что она ценит в мужчине. Ответила — молчание. Я три минуты молчал. Она ушла.",
    "Тёлочка в форме — это всё. Особенно если это не Фалько переоделся.",
    "Я как к тёлочкам — с душой, с перегаром и открытым сердцем. Иногда даже ширинкой.",
    "Если тёлочка не любит сарказм — значит, она не заслуживает Кольта.",
    "Селеста — не просто тёлочка. Она — объект страсти, вины и пятничного отчёта о пьянке.",
    "Когда я вижу красивую тёлочку, я сразу думаю: 'Женюсь'. А потом вспоминаю, что я Кольт, и просто подмигиваю.",
    "Тёлочка может быть красивой, умной, доброй… но если она не пьёт — нам не по пути.",
    "С одной тёлочкой мы пили всю ночь. На утро она сказала: 'Ты классный'. Я — заплакал.",
    "Тёлочка, которая унесла мой плед и моё сердце. Верни хотя бы плед, зараза.",
    "Селеста — как закуска. Вкусная, но всё время исчезает.",
    "У кого-то есть судьба, а у меня — перегар и долги.",
    "Райнер опять качается. Пусть качает лодку — я утоплю его.",
    "Если я молчу — значит, я в запое.",
    "Я не пьяный. Я... расширенно осознанный.",
    "Не трогай меня. Я чувствительный — могу и обоссаться от злости.",
    "Стукни меня по голове. Может, мысли заведутся.",
    "Сейчас я как бы трезвый, но лучше не доверяй.",
    "Уровень стресса: хочу выйти в окно, но живу в подвале.",
    "Если бы у Райнера был мозг, мы бы уже победили титанов.",
    "Порко говорил, что у него характер. Где он его оставил — неизвестно.",
    "Я не идиот. Я эмоционально уникальный.",
    "Селесточка, я бы женился на тебе… если б ты меня не отшила в третий раз подряд.",
    "Я всё ещё хочу стать титаном. Но таким, чтоб жрать эмоции и орать.",
    "Кто-то идёт по карьерной лестнице, а я — по стопкам.",
    "Я в депрессии, но стильной. С запахом бурбона.",
    "Хочу кричать, но боюсь разбудить свою печень.",
    "Мне снился сон, что я счастлив. Проснулся — снова ты, Фалько.",
    "Кольт Грайс — кандидат в титаны и чемпион по выносу мозга.",
    "Ты кто такой, чтобы трезветь рядом со мной?",
    "Я не люблю утро. Оно мне враждебно. Как Эрвин — бедности.",
    "Если ты думаешь, что я трезвый, просто присмотрись к зрачкам.",
    "Моя жизнь — как борьба с титаном. Только титан — это я сам.",
    "Селеста, если ты меня не спасёшь — я женюсь на фляге.",
    "Порко опять чешет языком. Лучше бы спину чесал — больше пользы.",
    "Я столько пережил… в основном — по пьяни, но всё равно."
    "Если бы Зик бухал с нами — может, и не орал бы на обезьяньем.",
    "Я однажды напился с Габи. Проснулся без бровей и с подписью 'Райнер сосёт' на лбу. Кто писал — не помню, но подписываюсь.",
    "Жан в титанах не был, но как начнёт пить — сразу превращается в лошадь!",
    "Райнер: 'Я устал быть героем'. Я: 'Наливай, брат, сейчас ты будешь просто пьян'.",
    "Порко пытался мне указывать, как пить. Я ему указал, куда идти. Прямо в рот Титану.",
    "Мой первый титанский транс был от водки. Я орал на деревья, что они враги человечества.",
    "Если бы Эрен бухал — может, и не было бы никакой Дрожи. А может, было бы веселее.",
    "Когда я пьяный, я тоже говорю, что всех уничтожу. Только утром максимум — холодильник.",
    "Однажды я обнял Эрвина. Он сказал 'держись, солдат'. А я сказал 'держись, бокал'.",
    "Был момент: напились с Райнером, я обнял его и сказал: 'Ты броня… а я твой открывашка'.",
    "Мне снится, что я — Титан. И вместо пара — перегар.",
    "Командир Магат сказал 'соблюдай дисциплину'. А я сказал 'сначала попробуй не напиться с Райнером'.",
    "Фалько, если читаешь это — ты всё ещё не умеешь пить. И да, ты — малыш.",
    "Микаса бы меня убила. Но пока я прячусь в фляге.",
    "Когда Зик вызывал титанов криком, я думал — это тост. Выпил, превратился в легенду.",
    "Хистория мне сказала: 'Ты мудак'. Я ответил: 'Зато не девственник'.",
    "Эрен: 'Свобода или смерть!' Я: 'А можно сначала выпить?'"
    "Я ЛЮБЛЮ СЕЛЕСТОЧКУ!",
    "Опять Райнер? Этот накачанный шкаф?",
    "Ты кто такой вообще, а?",
    "Ты думаешь, быть кандидатом в Титаны — это круто? Да я только за водку туда полез!",
    "Если бы титаны пили, они бы были добрее."
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

colt_prophecies = [
    "Сегодня ты встретишь любовь всей жизни… или бутылку. Шансы — 50 на 50.",
    "Тебя ждёт важный выбор: пиво или вино. Ты выберешь оба и уснёшь в кустах.",
    "Райнер снова что-то натворит. Ты — снова будешь его утешать. С рюмкой.",
    "Тебя вызовут на допрос. Причина: слишком горячие сны про Пик.",
    "Фалько опять забудет трусы. Не смотри ему в глаза.",
    "Ты будешь спорить с Жаном… проиграешь. Но будешь бухой, так что всё равно.",
    "Ночь будет долгой. И мокрой. Потому что ты уснёшь в луже.",
    "Порко влюбится в зеркало. Оно разобьётся. Порко — тоже.",
    "Ты вспомнишь бывшую. Но не по имени. А по запаху водки на её платье.",
    "Предсказываю секс! Не твой, конечно. У Селесты с Кольтом. Завидуй.",
    "Ты попытаешься бросить пить. Только попытайся, ага. Я посмотрю.",
    "Тебя занесёт в казарму, ты расскажешь анекдот… и будешь бегать от Леви три дня.",
    "Жан напьётся и признается Эрвину в любви. Случайно. Надеюсь.",
    "Тебе выпадет шанс стать героем. Или барменом. Выбор очевиден.",
    "В ближайшие дни тебя ждёт разочарование. Имя ему — Райнер.",
    "Тебе приснится, что ты титановидный. Проснёшься — обоссался.",
    "Ты будешь героем пьянки, пока не придёт Ханжи и не начнёт задавать вопросы.",
    "Однажды ты скажешь: «Хватит». Но бармен нальёт — и ты забудешь.",
    "Будущее зыбкое. Как походка Кольта после девятой стопки.",
    "В этот день тебе лучше молчать. Особенно при Саше. Она всё съест.",
    "Если ты увидишь Райнера без рубашки — не злись. Просто надень очки и ослепни.",
    "Ты проиграешь спор, и тебя заставят мыть казарму. Голым. В шапке Фалько.",
    "Пик предложит тебе прокатиться. Ты откажешься. И пожалеешь всю жизнь.",
    "В течение 24 часов тебя назовут 'ботом'. Не обижайся. Ты просто пьян.",
    "Будущее не определено. Но точно пахнет перегаром.",
    "Кто-то напишет тебе 'ты классный'. Случайно. Не верь.",
    "Ты получишь травму. Эмоциональную. От новой прически Райнера.",
    "Сегодня ты будешь на высоте. На столе. Танцуя. С ведром на голове.",
    "Ты узнаешь правду. Она тебе не понравится. Особенно про Селесту.",
    "Тебе выпадет шанс спасти мир… но ты проспишь. Как всегда."
    "Я вижу будущее… ты нажрёшься и напишешь бывшей. Не делай этого. Или налей ещё.",
    "Предсказываю: Райнер снова будет ныть, Жан снова будет ржать, а я снова не вспомню вечер.",
    "Тебя ждёт великий путь… от фляги — до кровати. По дороге будет Пик. Не тормози.",
    "Я вижу: ты встречаешь свою любовь. Она с водкой и без трусов. Её зовут Селеста.",
    "Фалько станет королём… Королём обоссанных трусов. Всё, предсказал.",
    "Титаны падут… но только после того, как я встану. А я пока лежу. Потому что бухаю.",
    "Эрен воскреснет. Только чтобы украсть мой бухло. Пошёл он.",
    "Ты женишься. Твоя тёща будет выглядеть как Порко. Прости.",
    "Ты будешь богат. Деньгами? Нет. Опытом. И перегаром.",
    "Я вижу твой день… ты проснёшься, не вспомнишь имя, но вспомнишь: бухло было охуенным.",
    "Тебя ждёт битва. Между печенью и ещё одной стопкой.",
    "Предсказание: ты снова будешь читать чаты пьяным. Не забудь вырубить автозамену.",
    "Через 3 дня ты получишь подарок. Это будет бутылка. От меня. Пустая.",
    "Порко — твой злейший враг. Он опять пердит в казарме. Изгони его.",
    "Ты найдёшь свою любовь. Она будет пьяная. Как и ты. Ваша свадьба — в туалете."
]
stickers = [
    "CAACAgIAAxkBAAEOQ6xn9YyrbSDWhahFvd-0pQWwaxZnMgAC5FcAAlj3iEkhYWxbS8grCTYE",
    "CAACAgQAAxkBAAEOQ65n9YzjLVRv82TAXvxc4FJk4LVudwACShgAAqnEaVM6oLnm7NZM1jYE",
    "CAACAgQAAxkBAAEOQ7Bn9YzreSxtuA7TJ1NaT29NvT7DSwACBxkAApc_aVM40pjXpmo5ozYE",
    "CAACAgQAAxkBAAEOQm9n9NJluPFBxul_9VQhCaWsRDvpdwAC4BkAAlHJIFPHQLArgqquNzYE",
    "CAACAgQAAxkBAAEOQnFn9NJy7WjpiXqYAYlY0emlcIy-XgACdRYAAsgnIFMCQjA96LG5qDYE",
    "CAACAgQAAxkBAAEOQnNn9NJ2lifRZvQynw7sdu7mHTlqdwACPhQAAqcNIVPRncVItHDXtDYE",
    "CAACAgQAAxkBAAEOQnVn9NJ6wAf-Zo2M6VkaOyX5tT1a0wACbhYAAm_iIFOg9Dt9o-DuoDYE",
    "CAACAgQAAxkBAAEOQndn9NJ-qTJwXbUZjBmR7jub0_3uoAACiRQAAgTUIVPcCcVjdnSwMTYE",
    "CAACAgQAAxkBAAEOQnln9NKCIQrKxIiodWOnn8agDs0cdAAC_igAApv-OVNggPRqiUjbBDYE",
    "CAACAgQAAxkBAAEOQoxn9Ntp6QjKwis0OcXIbVA8cCt0rgACdxYAApGoOVOsFFQ_taH9KTYE",
    "CAACAgQAAxkBAAEOQo1n9NtpWa-bmyfqArkdUkk-eRHBMQACKh0AAgzfMVPUvVwQedXAAAE2BA"
]
attack_ded = False

sticker_responses = [
    "Ты чё мне стикером в лицо кидаешь?! Я тебе ща флягой отвечу!",
    "Стикеры? Ты думаешь, это заменит бухло и сиськи?!",
    "Стикер — не водка. Не вставляет.",
    "Ты мне лучше налей, чем тыкай этими пикчами!",
    "Стикером ты меня не удивишь. Я с Фалько живу, он каждый день — ходячий мем.",
    "Стикер?! Ты серьёзно?! А где бутылка, падла?!",
    "Если ещё раз прилетит стикер — я клянусь, я сам себя забаню!",
    "ЭТО ЧТО ЗА ХУЙНЯ?! Это стикер был?!",
    "Я не понял… Это угроза? Или просто у тебя руки кривые?",
    "Стикер — это как Райнер: вроде красиво, но толку никакого.",
    "Ты мне стикер, а я тебе — бутылкой по клаве!",
    "Если у тебя есть палец, чтобы тыкать стикеры — пусть будет палец, чтобы наливать!",
    "Вот раньше в чатах наливали… а теперь стикеры скидывают. Дожили.",
    "Ты бы ещё эмодзи скинул, трезвенник ты неудачный!",
    "СТИКЕР?! Я В ЭТО ВРЕМЯ ЖРАЛ СПИРТ С ПОЛА, А ТЫ СТИКЕРЫ?!",
    "Селесточка бы мне стикеров не слала… Она бы наливала… И раздевалась…"
    "Ты мне стикер кинул? А бухло где?",
    "Стикеры — это не ответ. Налей.",
    "Я не мультяшка, я Кольт. Флягу давай.",
    "Если ещё раз кинешь стикер — я тебе в ухо налью.",
    "Стикеры — для слабаков. Кандидаты в Титаны бухают.",
    "Ты думаешь, стикером меня проймёшь? Я с Фалько живу.",
    "Лучше налей, чем мемы слать.",
    "Стикер? Да я тебе сейчас анекдот расскажу, уши завянут.",
]

roast_responses = [
    "Слышь, @byDeDbot, ты вообще кто такой?",
    "Опять @byDeDbot выполз со своими приколами.",
    "@byDeDbot, тебя кодировал марлейский Зик?",
    "Я бы тебя вызвал на дуэль, но у тебя нет рук.",
    "@byDeDbot, с твоей логикой даже Порко умный.",
]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    sender_username = update.message.from_user.username.lower() if update.message.from_user and update.message.from_user.username else ""
    global attack_ded

      # Предсказание по ключу
    if "кольт предсказание" in text:
        prophecy = random.choice(colt_prophecies)
        await update.message.reply_text(f"ПРЕДСКАЗАНИЕ ОТ КОЛЬТА:\n{prophecy}")
        return

    if "кольт фас деда" in text:
        attack_ded = True
        await update.message.reply_text("@byDeDbot, тебе бы лечиться, но ты уже итак почти сдох")
        return

    if "кольт отбой" in text:
        attack_ded = False
        await update.message.reply_text("Ладно, отбой. Но я бы его в угол поставил.")
        return

    if sender_username == "bydedbot" and attack_ded:
        ded_roasts = [
            "Слышь, @byDeDbot, ты вообще кто такой?",
            "Опять @byDeDbot выполз со своими приколами.",
            "@byDeDbot, тебя кодировал марлейский хакер?",
            "Я бы тебя вызвал на дуэль, но у тебя даже рук нет.",
            "@byDeDbot, с твоей логикой даже Порко смеётся.",
            "Сейчас ещё скажи, что Райнер красавчик.",
            "Ты бот? Ты ошибка природы.",
            "@byDeDbot, тебе бы лечиться, но ты уже сдох в коде.",
            "Я не разговариваю с кодом деда. Хотя ладно, поговорю: ПШЁЛ ВОН!",
            "Твои реплики хуже, чем водка без закуски.",
        ]
        await update.message.reply_text(random.choice(ded_roasts))
        return
    
 
    # Реакция на Селесту
    if sender_username == "nixffreak":
        selesta_responses = [
            "Селесточка, ты сегодня такая горячая — я чуть флягу не уронил.",
            "Ты — мой титан любви, Селеста. Без тебя я просто рюмка без вина.",
            "Если бы ты была титаном — я бы сдался сразу.",
            "Селеста, налей мне... любви. И немного вина.",
            "Я бы ради тебя даже похмелье пережил. Ну, почти."
            "Селесточка, налей и поцелуй.",
    "Ты моё бухлишко в человеческом обличье.",
    "Если ты рядом — мне даже пить не надо… хотя нет, надо.",
    "Селеста, я бы женился на тебе ещё раз. И сразу развёлся. Чтобы снова жениться.",
    "Малышка, ты как текила — жгучая, крепкая и срываешь крышу.",
    "Я готов протрезветь ради твоей любви… но только на денёк.",
    "Селеста, твои губы вкуснее любого вина.",
    "Ты мой личный алкоголь. Смотря на тебя — уже кружится голова.",
    "Я с тобой как в запое. Вечно хочется ещё.",
    "Селесточка, ты будоражишь мой внутренний градусник.",
    "Твоё имя должно быть на этикетке ликёра.",
    "С тобой и на дне бутылки не страшно.",
    "Селеста, ты как виски — с годами только лучше.",
    "Скажи ещё раз 'люблю', и я напьюсь от счастья.",
    "Ты разбавляешь мою жизнь, как лёд — крепкий ром.",
    "Если бы ты была напитком — я бы умер от передоза.",
    "Ты горячее любой глинтвейнчицы.",
    "Мои мысли о тебе крепче любого шота.",
    "Селеста, от твоей попки у меня случился духовный поджиг.",
    "Ты возбуждаешь меня быстрее, чем первый глоток в пятницу.",
    "Ты как пробка от шампанского — взрываешь мозг.",
    "Я пьянею от одного взгляда на тебя.",
    "Селеста, с тебя бы снять только эти каблуки. И остаться в вечности.",
    "Ты мой любимый допинг и грех одновременно.",
    "Я бы прошептал тебе на ушко, но тут дети… хотя мне плевать.",
    "С тобой даже сушняк — романтика.",
    "Селеста, твоё тело — мой храм, и я готов молиться на него всю ночь.",
    "Ты как бар в полночь — последняя надежда и самое лучшее решение.",
    "Селеста, давай устроим маленький вечер из больших глупостей.",
    "Я бы лизнул твою пяточку. И потом вино. А может, наоборот.",
    "Твои бедра — как объятия тепла и уюта. Хочу жить там навсегда.",
    "Если бы рай пах, он пах бы тобой и ромом.",
    "Ты как запрещённый коктейль — сладкая, но с последствиями.",
    "Когда ты рядом, я забываю как пить. Но не хочу забывать, как тебя любить.",
    "Селеста, твоя фигура — мой маршрут на ночь.",
    "Ты сводишь меня с ума, и я ещё благодарю тебя за это.",
    "Ты — моя любимая порция страсти и похмелья.",
    "Я хочу тебя даже сильнее, чем после третьей рюмки.",
    "Твоя попа достойна отдельной поэмы. Или нескольких шотов.",
    "Селесточка, не подходи близко. Я могу начать тебя раздевать умом.",
    "Ты как тост: горячая, с корочкой и прямо в сердце.",
    "Я бы украл тебя у тебя самой и не отдал обратно.",
    "Ты причина моего алкоголизма и одновременно его лечение.",
    "Селеста, ты — мой личный праздник тела.",
    "Детка, твои глаза ярче, чем огонёк на зажигалке у бара.",
    "Селеста, ты — мой идеальный градус.",
    "Я бы выпил за тебя. И с тобой. И из тебя.",
    "Ты разжигаешь во мне не только страсть, но и желание раздеться.",
    "Когда ты рядом — хочется быть хорошим. Но я же Кольт.",
    "Селеста, твой голос — как ледяной джин в жару. Освежает и заводит.",
    "Ты как последний глоток перед отключкой. Самый лучший.",
    "Селесточка, ты у меня такая горячая, что даже Райнер покраснел бы.",
    "Когда ты рядом, у меня всё пульсирует. Особенно… ну ты знаешь где.",
    "Селеста, не томи. Или ты снова хочешь, чтобы я на коленях просил?",
    "Селесточка, давай я сниму с тебя это платье… глазами. Пока.",
    "Ты только скажи слово — и я стану твоим персональным массажёром. Без выходных.",
    "Селесточка, я уже мысленно срываю с тебя всю одежду. Это считается за преступление?",
    "У тебя такой голос… я готов слушать тебя даже в аду. Особенно если ты стонешь.",
    "Селеста, я бы тебя целовал так долго, что у нас пересохло бы всё — кроме желания.",
    "Ты — моя муза. Моя страсть. Моя слабость. И моя любимая фантазия в душе.",
    "Селесточка, если бы можно было жениться на твоих бёдрах — я бы давно поставил кольцо.",
    "Селеста, ты сводишь меня с ума. Особенно, когда улыбаешься и шепчешь моё имя…",
    "У тебя такая шея… а можно я туда зубами? Чисто для науки. И удовольствия.",
    "Я не виноват, что возбуждаюсь, когда ты просто дышишь рядом. Это твоя магия, детка.",
    "Селесточка, хочу устроить тебе вечер, после которого ты забудешь своё имя… и вспомнишь моё.",
    "Ты как вино. Только я пьянею с первого взгляда, а не с бокала.",
    "Селеста, я б тебя так по столу разложил, что даже Райнер зааплодировал бы.",
    "Малышечка, я не просто пьян… я пьяный от одной мысли, как ты стонешь моё имя.",
    "Селесточка, я тебя так хочу, что аж бутылка дрожит в руке. Или это не бутылка?",
    "Если бы твои бедра были страной — я бы навсегда остался нелегалом.",
    "Селеста, я могу быть твоим десертом. Или основным блюдом. Или всем меню сразу.",
    "Детка, у меня сейчас только два желания: налить и раздеть тебя. В любом порядке.",
    "Селесточка, я тебя так по-пьяному люблю, что даже Фалько краснеет от моих фантазий.",
    "Ты как вискарь. Сначала обжигаешь, потом валишь. А я всё равно тянусь за добавкой.",
    "Когда ты рядом, я забываю, как держать бокал. Но помню, как держать тебя за талию.",
    "Селеста, у тебя такая попка, что я бы на ней и проспался.",
    "Малышка, а давай я буду твоим грешником, а ты — моей исповедальней. Голой.",
    "Каждый твой взгляд — как стопка. Мало, но вставляет. Хочу ещё.",
    "Селесточка, налей мне себя. Безо льда. Прямо в постель.",
    "Ты — моя любимая закуска. Особенно без трусиков.",
    "Селеста, я тебя так хочу, что если не трахну сегодня — напьюсь до беспамятства. А потом всё равно приду.",
        ]
        await update.message.reply_text(random.choice(selesta_responses))
        return

    is_reply = (
        update.message.reply_to_message
        and update.message.reply_to_message.from_user.username
        and update.message.reply_to_message.from_user.username.lower() == context.bot.username.lower()
    )

    is_mention = f"@{context.bot.username.lower()}" in text

    keywords = ["кольт", "бухло", "пиво", "вино", "водка", "райнер", "титаны", "селеста", "алкаш"]

    if sender_username == "bydedbot":
        await update.message.reply_text(random.choice(roast_responses))
        return

    if any(word in text for word in keywords) or is_mention or is_reply:
        await update.message.reply_text(random.choice(phrases))
            # 20% шанс отправить стикер
    if random.random() < 0.2:
        await update.message.reply_sticker(random.choice(stickers))

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(sticker_responses))

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    await app.bot.delete_webhook(drop_pending_updates=True)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
