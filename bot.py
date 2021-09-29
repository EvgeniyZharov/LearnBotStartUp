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
    while len(wordList) < 5 or len(wordList) == newWords:
        word = random.choice(newWords)
        if word not in wordList:
            wordList.append(word)

    return random.sample(wordList, len(wordList))


bot = Bot(token=API_ONE)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):

    if str(message.from_user.id) not in str(jsonWork.openFile(FileJsonName)["users"]):
        if jsonWork.addNew(FileJsonName, message.from_user.id):
            await message.reply(f"Привет!\nТеперь ты участник удивительной программы по французскому языку.")
    else:
        await message.reply("Привет! Ты уже есть в базе.", reply_markup=kbOne)


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):

    # await message.reply("Напиши м(не что-нибудь, и я отпрпавлю этот текст тебе в ответ!")
    await bot.send_message(message.from_user.id, '\n'.join(elements))


# @dp.message_handler(commands=["words"])
# async def changeStatusTask(message: types.Message):
#     try:
#         # get dict
#         taskWords = jsonWork.getDict(FileJsonName, str(message.from_user.id))
#         # change status for user
#         jsonWork.changeTask(FileJsonName, str(message.from_user.id), "words")
#         # get list of russian words
#         words = [elem for elem in taskWords]
#         # get first word from dict
#         firstWord = random.choice(words)
#
#         # get list of words translate for buttons
#         listWord = list()
#         for word in words:
#             listWord.append(taskWords[word])
#         # adding true word in list for buttons
#         wordsForButton = [taskWords[firstWord]]
#         # get whole list words
#         wordsForBtn = addForBtn(wordsForButton, listWord)
#         # create keyboard
#         kb = getButtons(wordsForBtn)
#
#         # save first word for user
#         jsonWork.lastWord(FileJsonName, str(message.from_user.id), firstWord)
#
#         # adding button with var start
#         kb.add(types.KeyboardButton(text="/start"))
#
#         # message for user
#         await message.reply(f"Статус упражнения изменем на изучение слов. Первое слово:\n\n{firstWord}",
#                             reply_markup=kb)
#     except Exception:
#         await message.reply("На сегодня выбрано другое задание.")


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
                print('change')

            # get list of words translate for buttons
            listWord = list()
            for word in words:
                listWord.append(taskWords[word])
            # adding true word in list for buttons
            wordsForButton = [taskWords[newWord]]
            # get whole list words
            wordsForBtn = addForBtn(wordsForButton, listWord)
            # create keyboard
            kb = getButtons(wordsForBtn)

            if msg.text.lower() == trueWord:
                jsonWork.lastWord(FileJsonName, str(msg.from_user.id), newWord)
                jsonWork.achievement(FileJsonName, str(msg.from_user.id), 5)
                await msg.reply(f"Правильно!\nСледующее слово: {newWord}", reply_markup=kb)
            else:
                jsonWork.lastWord(FileJsonName, str(msg.from_user.id), newWord)
                await msg.reply(f"Неправильно!\n\n{trueWord.upper()}\n\nСледующее слово: {newWord}", reply_markup=kb)
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
                await msg.reply(f"Слово {msg.text} успешно удалено.")
            else:
                await msg.reply("Слово не удалено, произошла ошибка.")
        else:
            await bot.send_message(msg.from_user.id, msg.text)
    else:
        jsonWork.addNew(FileJsonName, userID)
        await bot.send_message(msg.from_user.id, "Я добавил Вас в базу учеников.")


if __name__ == '__main__':
    print('o')
    executor.start_polling(dp)