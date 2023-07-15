from discord.ext import commands
from random import randint
from time import sleep
from flask import Flask
from dotenv import load_dotenv
import discord
import threading
import os

load_dotenv('.env')

key = os.getenv('KEY')

CHANNEL = 1122405068487000154  # channel bot talks in

intents = discord.Intents().default()
intents.message_content = True #set's basic permissions

people = 0
permPeople = 0
indexGlobal = 0
bullet = 0
listOfPeople = []

bot = commands.Bot(command_prefix="!", intents=intents)
discord.Permissions(add_reactions=True, kick_members=True, send_messages=True)  # sets all the bot's permissions

app = Flask(__name__)

@app.route("/")
def index():
  return open("index.html", "r").read()

async def roll(auth):
  global bullet
  global indexGlobal
  global people
  global listOfPeople

  if auth != listOfPeople[indexGlobal]:
    return

  channelClass = bot.get_channel(CHANNEL)
  bullet = randint(1, people)
  sleep(0.5)
  if bullet == listOfPeople[indexGlobal+1]:
    try:
      await listOfPeople[indexGlobal].kick(reason="get russiad")
    except:
      await channelClass.send("I can't kick you, pretend to be kicked.")
    listOfPeople.pop(indexGlobal+1)
    listOfPeople.pop(indexGlobal)
    people -= 1
    sleep(0.5)
  else:
    await channelClass.send(f"Saved, with a bullet of {bullet}")
  if people == int((3/5)*permPeople):
    await channelClass.send("-----------------------------------")
    await channelClass.send("The winners are, ")
    for i in range(0, len(listOfPeople)+1):
      if i % 2 != 0:
        continue
      try:
          await channelClass.send(listOfPeople[i].global_name)
      except:
        await channelClass.send(listOfPeople[i].name)
    people = 0
    return
  if (indexGlobal+2) > people:
    indexGlobal == 0
  else:
    indexGlobal += 2

  name = listOfPeople[indexGlobal].global_name
  if name == None:
    name = listOfPeople[indexGlobal].name
  mes = await channelClass.send(f"{name}, roll or shoot?")
  await mes.add_reaction("🍀")
  await mes.add_reaction("🔫")


async def shoot(auth):
  global bullet
  global indexGlobal
  global people
  global listOfPeople

  if auth != listOfPeople[indexGlobal]:
    return

  channelClass = bot.get_channel(CHANNEL)
  sleep(0.5)
  if bullet == listOfPeople[indexGlobal+1]:
    try:
      await listOfPeople[indexGlobal].kick(reason="get russiad")
    except:
      await channelClass.send("I can't kick you, pretend to be kicked.")
    listOfPeople.pop(indexGlobal+1)
    listOfPeople.pop(indexGlobal)
    people -= 1
    sleep(0.5)
  else:
    await channelClass.send(f"Saved, with a bullet of {bullet}")
  if people == int((3/5)*permPeople):
    await channelClass.send("-----------------------------------")
    await channelClass.send("It looks like the limit has been reached. До свидания!")
    people = 0
    return
  if (indexGlobal+2) > people:
    indexGlobal == 0
  else:
    indexGlobal += 2

  name = listOfPeople[indexGlobal].global_name
  if name == None:
    name = listOfPeople[indexGlobal].name
  mes = await channelClass.send(f"{name}, roll or shoot?")
  await mes.add_reaction("🍀")
  await mes.add_reaction("🔫")

async def beginGame():
  global listOfPeople
  global people
  global permPeople
  global indexGlobal
  global bullet

  nums = []
  channelClass = bot.get_channel(CHANNEL)
  if people <= 1:
    await channelClass.send("Too litle people, извини")
    return
  await channelClass.send("-----------------------------------")
  await channelClass.send("If you don\'t know who I am, then maybe your best course would be to tread lightly")  
  sleep(1)

  permPeople = people

  for i in range(0, people*2):
    if i % 2 == 0:
      continue
    randomInt = randint(1, people)
    while True:
      if randomInt in nums:
        randomInt = randint(1, people)
      else:
        break
      sleep(0.1)
    nums.append(randomInt)
    listOfPeople.insert(i, randomInt)
  
  await channelClass.send("The numbers are, ")
  await channelClass.send("-----------------------------------")
  sleep(2)
  for j in range(0, people+1):
    if j % 2 != 0:
      continue
    try:
      await channelClass.send(listOfPeople[j].global_name + " : " + str(listOfPeople[j+1]))
    except:
      await channelClass.send(listOfPeople[j].name + " : " + str(listOfPeople[j+1]))
  await channelClass.send("-----------------------------------")
  sleep(3)
  await channelClass.send("Let us begin")
  sleep(1)
  await channelClass.send(" # insert banning gun rolling noises here # ")
  
  bullet = randint(1, people)

  sleep(0.2)

  await channelClass.send(f"{listOfPeople[indexGlobal].global_name}, roll or shoot?")
  mes = await channelClass.send("🍀 is roll, 🔫 is shoot")
  await mes.add_reaction("🍀")
  await mes.add_reaction("🔫")


@bot.event
async def on_ready():
  print("ready to become strongest bot")
  channel = bot.get_channel(CHANNEL)
  await channel.send("Здравствуйте! I shall be your russian roulete bot.")

@bot.listen("on_reaction_add")
async def on_reaction_add(reac, user):
  global people
  global listOfPeople

  channel = bot.get_channel(CHANNEL)
  if reac.message.author != bot.user :
    return
  if user == bot.user:
    return
  if reac.emoji == "✅" :
    people += 1
    listOfPeople.append(user)
  if reac.emoji == "⭕" :
    await beginGame()
  if reac.emoji == "🍀" :
    if people <= int((3/5)*permPeople):
      await channel.send("извини, the game hasn't started.")
      return
    await roll(user)
  if reac.emoji == "🔫" :
    if people <= int((3/5)*permPeople):
      await channel.send("извини, the game hasn't started.")
      return
    await shoot(user)
  
@bot.command()
async def start(ctx):
  if ctx.channel != bot.get_channel(1122405068487000154):
    return
  await ctx.send("Press checkmark to join in, and the circle to start")
  mes = await ctx.send("Be warned, players who loose get kicked")
  await mes.add_reaction("✅")
  await mes.add_reaction("⭕")

def startWeb():
  port = os.getenv('PORT', 3000)
  app.run(host="0.0.0.0", port=port)

x = threading.Thread(target=startWeb, args=())
x.start()
bot.run(key)