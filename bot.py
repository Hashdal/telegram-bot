import json

def openJson():
    try:
        file = open("dataBase.json", "r")
        content = json.load(file)
        file.close()
        return content
    except:
        file = open("dataBase.json", "w")
        file.write("{}")
        file.close
        return {}

def writeJson(dictionary: dict):
    jsonContent = json.dumps(dictionary)
    file = open("dataBase.json", "w")
    file.write(jsonContent)
    file.close()
    return True

def addEvent(eventName: str):
    content = openJson()
    for i in content:
        if i == eventName:
            return False
    content[eventName] = {'people': {}, 'transactions': {}}
    writeJson(content)
    return True

def findEvent(eventName):
    content = openJson()
    for i in content:
        if i == eventName:
            return True
    return False

def addPeopleNames(names: list, eventName: str) -> bool:
    content = openJson()
    for i in content:
        if i == eventName:
            for j in names:
                content[i]['people'][j] = 0
            writeJson(content)
            return True
    return False

def transaction(eventName: str, name: str, price: float, people: list):
    content = openJson()
    for i in content:
        if i == eventName:
            content[i]["transactions"][name] = {'price': price, 'buyer': people[0], 'people': people}
            perPerson = float(price)/len(people)
            for j in range(len(people)):
                for z in content[i]['people']:
                    if people[j] == z and j == 0:
                        content[i]['people'][people[j]] += float(price) - perPerson
                    if people[j] == z and j != 0:
                        content[i]['people'][people[j]] -= perPerson
            writeJson(content)
            return True
    writeJson(content)
    return False

def geteEventPeople(eventName):
    content = openJson()
    output = []
    for i in content:
        if i == eventName:
            for j in content[i]["people"]:
                output.append(j)
    return output

def checkingout(eventName, sender, getter, price):
    content = openJson()
    for i in content:
        if i == eventName:
            content[i]["people"][sender] += float(price)
            content[i]["people"][getter] -= float(price)
            writeJson(content)
            return True
    return False

def getPeople(eventName):
    content = openJson()
    output = []
    for i in content:
        if i == eventName:
            return content[i]["people"]
#----------------------------------------------------------------------------------

import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5858548522:AAGDyZ92d-GoiD6r947MunHbV1PAl37bmzs'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("salam!\nbaraye sakhtane rooydad az dastoore /startEvent estefade konid\n"
                        + "baraye entekhabe rooydad az /setActiveEvent estefade konid\n"
                        + "baraye ezafe kardane afrad az /addPeople estefade konid\n"
                        + "baraye ezafe kardane tarakonesh az /addTransaction estefade konid\n"
                        + "baraye tasvie hesab az /checkout estefade konid\n"
                        + "baraye daryaft ettela'at hesab az /showAccounts estefade konid"
                        + "baraye gereftane tamame ettele'at rooydad az /getEventInformation estefade konid\n"
                        + "**hengami ke rooydadi sakhte mishavad, fardi ozve an nist, pas avval pas az sakhte rooydad afrad ra be an ezafe konid!")

@dp.message_handler(commands=['startEvent'])
async def createEvent(message: types.Message):
    global state
    state = "startEvent"
    await message.answer("name rooydad ra vard konid:\n**dar name entekhabi az fasele estefade nakonid, mitavanid bejaye fasele az - estefadeh konid")

@dp.message_handler(commands=['addPeople'])
async def addPeople(message: types.Message):
    global state
    state = "addPeople"
    await message.answer("name afrad ra ba fasele vared konid.\n**deghat konid ke name har fard nabayad fasele dashte bashad, agar be fasele dar name har fard niaz dashtid az - estefade konid.")

def setterActiveEvent(eventName):
    global activeEvent
    activeEvent = eventName

@dp.message_handler(commands=['setActiveEvent'])
async def setActiveEvent(message: types.Message):
    global state
    state = "setActiveEvent"
    await message.answer("name event ra vared konid:")

@dp.message_handler(commands=['addTransaction'])
async def addTransaction(message: types.Message):
    global state
    state = "addTransaction"
    await message.answer("be tartib nam haye zir ra ba fasele vared konid, tavajoh konid az fasele dar nam ha nemitavanid estefade konid, agar lazem be estefade bood az - estefadeh konid\n"
                         +"kala gheymat kharidar farde1 farde2 ...\n"
                         +"name afrade rooydade faal:\n" + str(geteEventPeople(activeEvent)))

@dp.message_handler(commands=['checkout'])
async def checkout(message: types.Message):
    global state
    state = "checkout"
    await message.answer("be tartibe zir, mavarede zir ra vared konid:\npardakhtKonande girande mablagh")

@dp.message_handler(commands=['showAccounts'])
async def showAccounts(message: types.Message):
    try:
        content = getPeople(activeEvent)
        await message.answer(str(content))
    except:
        await message.answer("name rooydad ra tanzim nakardid!")

@dp.message_handler(commands=['getEventInformation'])
async def getEventInformaion(message: types.message):
    try:
        await message.answer(openJson()[activeEvent]["people"])
        await message.answer(openJson()[activeEvent]["transactions"])
    except:
        await message.answer("rooydadi ra entekhab nakardid!")

@dp.message_handler()
async def echo(message: types.Message):
    try:
        messageContent = message.text
        if state == "startEvent":
            if addEvent(messageContent):
                setterActiveEvent(messageContent)
                await message.reply("rooydad sakhte shod!")
            else:
                await message.reply("in rooydad ghablan estefade shode!")
        elif state == "setActiveEvent":
            eventName = message.text
            if findEvent(eventName):
                setterActiveEvent(eventName)
                await message.reply("rooydad be rooydade {} taghir yaft!".format(eventName))
            else:
                await message.reply("in rooydad ghablan sabt nashode! rooydade digari ra entekhab konid.")
        elif state == "addPeople":
            names = message.text.split(" ")
            if addPeopleNames(names, activeEvent):
                await message.reply("karbaran ezafe shodand!")
            else:
                await message.reply("name rooydad dorost vared nashode ya rooydad sakhte nashode.")
        elif state == "addTransaction":
            transactionContent = message.text.split(" ")
            if transaction(eventName=activeEvent, name=transactionContent[0], price=transactionContent[1], people=transactionContent[2:]):
                await message.reply("tarakonesh ezafe shod!")
            else:
                await message.reply("moshkeli pish amade, dobare emtehan konid!")
        elif state == "checkout":
            checkoutInfirmation = message.text.split(" ")
            if checkingout(activeEvent ,sender=checkoutInfirmation[0], getter=checkoutInfirmation[1], price=checkoutInfirmation[2]):
                await message.reply("tasvie hesab anjam shod!")
            else:
                await message.reply("name event ra entekhab najardid!")
        else:
            await message.reply("format ra dorost vared nakardid ya dastoori ra entekhab nakardid!")
    except:
        await message.reply("ebteda dastoori ra vared konid ya dastoor ra dorost vared konid!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)