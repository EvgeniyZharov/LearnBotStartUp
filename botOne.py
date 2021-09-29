from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import random
from config import API_ONE, FileJsonName, elements
import jsonWork
import preparationTask

# Buttons for bot
kbOne = types.ReplyKeyboardMarkup()
for line in elements:
    btn = types.KeyboardButton(text=line.split()[0])
    kbOne.add(btn)


def getButtons(words):
    kb = types.ReplyKeyboardMarkup()
    for elem in words:
        btn = types.KeyboardButton(text=elem)
        kb.add(btn)
    return kb



def addForBtn(wordList, newWords):
    while len(wordList) < 5 and len(wordList) != len(newWords):
        word = random.choice(newWords)
        if word not in wordList:
            wordList.append(word)

    return random.sample(wordList, len(wordList))


bot = Bot(token=API_ONE)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):

    if str(message.from_user.id) not in str(jsonWork.openFile(FileJsonName)["users"]):
        name = "NameUntitled"
        if message.from_user.username:
            name = message.from_user.username
        elif message.from_user.first_name:
            if message.from_user.last_name:
                name = f"{message.from_user.first_name} {message.from_user.last_name}"
            else:
                name = message.from_user.first_name
        if jsonWork.addNew(FileJsonName, message.from_user.id, name):
            await message.reply(f"Привет!\nТеперь ты участник удивительной программы.")
    else:
        await message.reply("Привет! Ты уже есть в базе.", reply_markup=kbOne)


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):

    # await message.reply("Напиши м(не что-нибудь, и я отпрпавлю этот текст тебе в ответ!")
    await bot.send_message(message.from_user.id, '\n'.join(elements))


@dp.message_handler(commands=["words"])
async def changeStatusTask(message: types.Message):
    try:
        # get dict
        taskWords = jsonWork.getDict(FileJsonName, str(message.from_user.id))

        # get list of russian words
        words = [elem for elem in taskWords]

        if len(words) < 2:
            await bot.send_message(message.from_user.id, "У вас очень маленький словарь. Добавьте еще слов.")
        else:
            # change status for user
            jsonWork.changeTask(FileJsonName, str(message.from_user.id), "words")
            # get first word from dict
            firstWord = random.choice(words)

            # get list of words translate for buttons
            listWord = list()
            wordsForButton = list()
            for word in words:
                listWord.append(taskWords[word])
            wordsForButton.append(taskWords[firstWord])
            # adding true word in list for buttons
            # wordsForButton = [elem for elem in taskWords[firstWord]]
            # get whole list words
            wordsForBtn = addForBtn(wordsForButton, listWord)
            # create keyboard
            kb = getButtons(wordsForBtn)

            # save first word for user
            jsonWork.lastWord(FileJsonName, str(message.from_user.id), firstWord)

            # adding button with var start
            kb.add(types.KeyboardButton(text="/start"))

            # message for user
            await message.reply(f"Статус упражнения изменем на изучение слов. Первое слово:\n\n{firstWord}",
                                reply_markup=kb)
    except Exception:
        await message.reply("На сегодня выбрано другое задание.")


@dp.message_handler(commands=["wordsVers"])
async def words(msg: types.Message):
    try:
        # import words from dict user
        taskWords = jsonWork.getDict(FileJsonName, str(msg.from_user.id))

        # change position for words

        words = [elem for elem in taskWords]

        if len(words) < 2:
            await bot.send_message(msg.from_user.id, "У вас очень маленький словарь. Добавьте еще слов.")
        else:
            jsonWork.changeTask(FileJsonName, str(msg.from_user.id), "wordsVers")
            newTask = dict()
            allWords = list()
            for word in words:
                nWord = taskWords[word]
                newTask[nWord] = word
                allWords.append(nWord)

            # get first word for user
            firstWord = random.choice(allWords)

            # get list of words translate for buttons
            listWord = list()
            for word in allWords:
                listWord.append(newTask[word])
            # adding true word in list for buttons
            wordsForButton = [newTask[firstWord]]
            # get whole list words
            wordsForBtn = addForBtn(wordsForButton, listWord)
            # create keyboard
            kb = getButtons(wordsForBtn)
            kb.add(types.KeyboardButton(text="/start"))

            jsonWork.lastWord(FileJsonName, str(msg.from_user.id), firstWord)

            # message for user
            await msg.reply(f"Статус упражнения изменем на изучение слов. Первое слово:\n\n{firstWord}",
                                reply_markup=kb)
    except Exception:
        await msg.reply("На сегодня выбрано другое задание.")


@dp.message_handler(commands=["text"])
async def changeStatusTask(message: types.Message):
    try:
        taskTexts = jsonWork.getTexts(FileJsonName, str(message.from_user.id))
        if taskTexts:
            jsonWork.changeTask(FileJsonName, str(message.from_user.id), "text")
            firstText = random.choice([elem for elem in taskTexts])
            jsonWork.lastText(FileJsonName, str(message.from_user.id), firstText)
            await message.reply(f"Статус упражнения изменем на повторение текта. Первый текст:\n\n{firstText}")
        else:
            await bot.send_message(message.from_user.id, "У Вас не записано текстов.")
    except Exception:
        await message.reply("На сегодня выбрано другое задание.")


@dp.message_handler(commands=["break"])
async def breakStatus(message: types.Message):
    jsonWork.changeTask(FileJsonName, str(message.from_user.id), "None")
    jsonWork.helpInfoUser(FileJsonName, str(message.from_user.id), '')
    await message.reply("Режим изменен на: Базовый.")


@dp.message_handler(commands=["newWords"])
async def newWords(message: types.Message):
    jsonWork.changeTask(FileJsonName, str(message.from_user.id), "newWords")
    await message.reply("Режим изменен: Вы можете добавить новые слова (перевод.слово)")


@dp.message_handler(commands=["delWord"])
async def delword(msg: types.Message):
    dictWords = jsonWork.getDict(FileJsonName, str(msg.from_user.id))
    kb = types.ReplyKeyboardMarkup()
    jsonWork.changeTask(FileJsonName, str(msg.from_user.id), "delWord")
    for elem in [word for word in dictWords]:
        btn = types.KeyboardButton(text=elem)
        kb.add(btn)
    kb.add(types.KeyboardButton(text="/start"))
    await msg.reply("Выберите слово, чтобы удалить.", reply_markup=kb)


@dp.message_handler(commands=["myDict"])
async def myDict(msg: types.message):
    await msg.reply("Сейчас подготовлю Ваш словарь.")
    userDict = jsonWork.getDict(FileJsonName, str(msg.from_user.id))
    if userDict:
        text = ''
        for elem in userDict:
            text += f"{elem} - {userDict[elem]}\n"
        await bot.send_message(msg.from_user.id, text)

    else:
        await bot.send_message(msg.from_user.id, "Ваш словарь пуст.")


@dp.message_handler(commands=["newText"])
async def newText(message: types.Message):
    jsonWork.changeTask(FileJsonName, str(message.from_user.id), "newText")
    await message.reply("Режим изменен: Вы можете добавить новые слова (перевод ,. текст)")


@dp.message_handler(commands=["myTexts"])
async def myTexts(msg: types.Message):
    await msg.reply("Сейчас подготовлю Ваши тексты.")
    userTexts = jsonWork.getTexts(FileJsonName, str(msg.from_user.id))
    if userTexts:
        text = ''
        for elem in userTexts:
            text += f"{elem} --- {userTexts[elem]}\n"


        await bot.send_message(msg.from_user.id, text)

        await bot.send_message(msg.from_user.id, "У Вас не записано текстов.")
    else:
        await bot.send_message(msg.from_user.id, "У Вас не записано текстов.")


@dp.message_handler(commands=["myScore"])
async def score(msg: types.Message):
    await msg.reply(f"Ваши очки: {jsonWork.openFile(FileJsonName)['users'][str(msg.from_user.id)]['exp']}")


@dp.message_handler(commands=["check"])
async def check(message: types.Message):
    context = jsonWork.openFile(FileJsonName)
    if context and str(message.from_user.id) == "961023982":
        await message.reply(context)
    else:
        await message.reply("ERROR")


@dp.message_handler(commands=["rating"])
async def rating(msg: types.Message):
    await msg.reply("Составляем рейтинг участников")
    rating = jsonWork.getRating(FileJsonName)
    if rating:
        await bot.send_message(msg.from_user.id, f"Данные о пользователях\n\n{rating}")


@dp.message_handler(commands=["check"])
async def check(msg: types.Message):
    text = 'h: '
    if msg.from_user.last_name:
        text += msg.from_user.last_name
    await bot.send_message("961023982", text)


@dp.message_handler(commands=["hesoyam"])
async def func(msg: types.Message):
    if str(msg.from_user.id) == "961023982":
        await msg.reply("Okey, I listenning you.")
        jsonWork.changeTask(FileJsonName, str(msg.from_user.id), "CreateNewDict")
    else:
        await msg.reply("Команда не распознана.")

@dp.message_handler(commands=["bigDict"])
async def add(msg: types.Message):
    try:
        jsonWork.changeTask(FileJsonName, str(msg.from_user.id), "connectBigDict")
        kb = types.ReplyKeyboardMarkup()
        for elem in jsonWork.openFile(FileJsonName)["lang"]:
            btn = types.KeyboardButton(text=elem)
            kb.add(btn)
        kb.add(types.KeyboardButton(text="/start"))
        await msg.reply("Выберите язык для изучения.", reply_markup=kb)
    except:
        await msg.reply("Произошла ошибка.")


@dp.message_handler()
async def main(msg: types.Message):
    userID = msg.from_user.id
    if str(userID) in jsonWork.openFile(FileJsonName)['users']:
        status = jsonWork.getStatusTask(FileJsonName, str(userID))

        if status == "words":
            taskWords = jsonWork.getDict(FileJsonName, str(msg.from_user.id))
            trueWord = taskWords[jsonWork.openFile(FileJsonName)["users"][str(msg.from_user.id)]["lastWord"]]
            words = [elem for elem in taskWords]

            newWord = random.choice(words)


            while (taskWords[newWord] == trueWord):
                newWord = random.choice(words)

            # get list of words translate for buttons
            wordsForButton = list()
            listWord = list()
            for word in words:
                listWord.append(taskWords[word])
            wordsForButton.append(taskWords[newWord])
            # get whole list words
            wordsForBtn = addForBtn(wordsForButton, listWord)
            # create keyboard
            kb = getButtons(wordsForBtn)
            kb.add(types.KeyboardButton(text="/start"))

            if msg.text.lower() == trueWord:
                jsonWork.lastWord(FileJsonName, str(msg.from_user.id), newWord)
                jsonWork.achievement(FileJsonName, str(msg.from_user.id), 5)
                await msg.reply(f"Правильно!\nСледующее слово: {newWord}", reply_markup=kb)
            else:
                jsonWork.lastWord(FileJsonName, str(msg.from_user.id), newWord)
                await msg.reply(f"Неправильно!\n\n{trueWord.upper()}\n\nСледующее слово: {newWord}", reply_markup=kb)

        elif status == "wordsVers":
            taskWords = jsonWork.getDict(FileJsonName, str(msg.from_user.id))
            words = [elem for elem in taskWords]

            newTask = dict()
            allWords = list()
            for word in words:
                nWord = taskWords[word]
                newTask[nWord] = word
                allWords.append(nWord)
            try:
                trueWord = newTask[jsonWork.openFile(FileJsonName)["users"][str(msg.from_user.id)]["lastWord"]]

                newWord = random.choice(allWords)


                while (newTask[newWord] == trueWord):
                    newWord = random.choice(allWords)

                # get list of words translate for buttons
                wordsForButton = list()
                listWord = list()
                for word in allWords:
                    listWord.append(newTask[word])
                wordsForButton.append(newTask[newWord])
                # get whole list words
                wordsForBtn = addForBtn(wordsForButton, listWord)
                # create keyboard
                kb = getButtons(wordsForBtn)
                kb.add(types.KeyboardButton(text="/start"))

                if msg.text.lower() == trueWord:
                    jsonWork.lastWord(FileJsonName, str(msg.from_user.id), newWord)
                    jsonWork.achievement(FileJsonName, str(msg.from_user.id), 5)
                    await msg.reply(f"Правильно!\nСледующее слово: {newWord}", reply_markup=kb)
                else:
                    jsonWork.lastWord(FileJsonName, str(msg.from_user.id), newWord)
                    await msg.reply(f"Неправильно!\n\n{trueWord.upper()}\n\nСледующее слово: {newWord}", reply_markup=kb)
            except Exception:
                await bot.send_message(msg.from_user.id, "Произошла ошибка.")

        elif status == "text":
            taskText = jsonWork.getTexts(FileJsonName, str(msg.from_user.id))
            userText = msg.text.lower()
            trueText = taskText[jsonWork.openFile(FileJsonName)["users"][str(msg.from_user.id)]["lastText"]]
            score, percent = preparationTask.checkTexts(userText, trueText)
            jsonWork.achievement(FileJsonName, str(msg.from_user.id), score)

            newText = random.choice([elem for elem in taskText])
            if (newText == trueText):
                newText = random.choice([elem for elem in taskText])

            jsonWork.lastText(FileJsonName, str(msg.from_user.id), newText)
            await msg.reply(f"Точность: {percent}%\n\nВот следующий текст:\n{newText}")
        elif status == "newWords":
            userWords = msg.text.lower()
            try:
                if jsonWork.addWords(FileJsonName, str(msg.from_user.id), userWords):
                    await msg.reply("Слова добавлены в словарь.")
                else:
                    await msg.reply("Некорректный ввод.\nПример правильного ввода: \"привет.hello\"")
            except Exception:
                await msg.reply("Произошла какая-то ошибка")
        elif status == "newText":
            userText = msg.text.lower()
            try:
                if jsonWork.addText(FileJsonName, str(msg.from_user.id), userText):
                    await msg.reply("Текст добавлен.")
                else:
                    await msg.reply("Некорректный ввод.\nПример правильного ввода:"
                                    " \"Привет, мой друг! ,. Bonjour mon ami!\"")
            except Exception:
                await msg.reply("Произошла какая-то ошибка")

        elif status == "delWord":
            if jsonWork.delWord(FileJsonName, str(msg.from_user.id), msg.text):
                dictWords = jsonWork.getDict(FileJsonName, str(msg.from_user.id))
                kb = types.ReplyKeyboardMarkup()
                jsonWork.changeTask(FileJsonName, str(msg.from_user.id), "delWord")
                for elem in [word for word in dictWords]:
                    btn = types.KeyboardButton(text=elem)
                    kb.add(btn)
                kb.add(types.KeyboardButton(text="/start"))
                await msg.reply(f"Слово {msg.text} успешно удалено.", reply_markup=kb)
            else:
                await msg.reply("Слово не удалено, произошла ошибка.")

        elif status == "connectBigDict":
            try:
                data = jsonWork.openFile(FileJsonName)["lang"]
                if msg.text in data:
                    kb = types.ReplyKeyboardMarkup()
                    for elem in data[msg.text]:
                        kb.add(types.KeyboardButton(text=elem))
                    kb.add(types.KeyboardButton(text="/start"))
                    jsonWork.helpInfoUser(FileJsonName, str(msg.from_user.id), msg.text)
                    jsonWork.changeTask(FileJsonName, str(msg.from_user.id), "connectToCategory")

                    await bot.send_message(msg.from_user.id, "Выберите категорию слов.",
                                           reply_markup=kb)
                else:
                    await msg.reply("Вы ввели несуществующий язык.")
            except:
                await msg.reply("Произошла ошибка 1.")

        elif status == "connectToCategory":
            try:
                data = jsonWork.openFile(FileJsonName)
                userHelpInfo = data["users"][str(msg.from_user.id)]["helpInfo"]
                if msg.text in data["lang"][userHelpInfo.split(';')[0]]:
                    kb = types.ReplyKeyboardMarkup()
                    text = ''
                    for elem in data["lang"][userHelpInfo.split(';')[0]][msg.text]:
                        text += f"{elem} - {data['lang'][userHelpInfo.split(';')[0]][msg.text][elem]}\n"
                        kb.add(types.KeyboardButton(text=elem))
                    kb.add(types.KeyboardButton(text="Назад"))
                    kb.add(types.KeyboardButton(text="/start"))

                    jsonWork.helpInfoUser(FileJsonName, str(msg.from_user.id), f"{userHelpInfo};{msg.text}")
                    jsonWork.changeTask(FileJsonName, str(msg.from_user.id), "choiseWords")
                    await bot.send_message(msg.from_user.id, "Вот слова, которые скоро можно будет добавить в свой словарь.", reply_markup=kb)
                    await bot.send_message(msg.from_user.id, text)

                else:
                    await msg.reply("Вы ввели некорректное название.")

            except:
                await msg.reply("Произошла ошибка 2.")

        elif status == "choiseWords":
            try:
                data = jsonWork.openFile(FileJsonName)
                userHelpInfo = data["users"][str(msg.from_user.id)]["helpInfo"]
                if msg.text.lower() == "назад":
                    try:
                        jsonWork.changeTask(FileJsonName, str(msg.from_user.id), "connectBigDict")
                        kb = types.ReplyKeyboardMarkup()
                        for elem in jsonWork.openFile(FileJsonName)["lang"]:
                            btn = types.KeyboardButton(text=elem)
                            kb.add(btn)
                        kb.add(types.KeyboardButton(text="/start"))
                        await msg.reply("Выберите язык для изучения.", reply_markup=kb)
                    except:
                        await msg.reply("Произошла ошибка.")
            except:
                await msg.reply("Произошла ошибка 3.")

        elif status == "CreateNewDict" and str(msg.from_user.id):
            if jsonWork.workWithDicts(FileJsonName, msg.text.split('\n')):
                await msg.reply("Данные загружены.")
            else:
                await msg.reply("error")



        else:
            await bot.send_message(msg.from_user.id, msg.text)
    else:

        name = "NameUntitled"
        if msg.from_user.username:
            name = msg.from_user.username
        elif msg.from_user.first_name:
            if msg.from_user.last_name:
                name = f"{msg.from_user.first_name} {msg.from_user.last_name}"
            else:
                name = msg.from_user.first_name
        jsonWork.addNew(FileJsonName, userID, name)
        await bot.send_message(msg.from_user.id, "Я добавил Вас в базу учеников.")


if __name__ == '__main__':
    print('ok')
    executor.start_polling(dp)
