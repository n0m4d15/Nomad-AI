import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()

ping_word = ["bot", "Bot"]
ping_response = ["Aye?", "Hmm, Gonna make me suck your dick or something IDK?", "Gonna pretend I'm not here", "Why you bully me?"]

joke_word = ["lol", "LoL","lmao","LMAO","Lmao"]
joke_response = ["Real Funny Moment here", "Kekekeke", "Jeezos"]

sad_words = ["ffs","sad","feel bad" , "ded","sed", "unhappy", "oof", "kms", "fml", "angry", "miserable", "depressing","depressed","anxious","nervous"]
starter_encourage = ["Cheer up mate", "Yeah don't kill yourself over it", "You're gonna be fine", "Shit happens, right..?","You really wanna stress over things you can't win eh?"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)

def update_encourage(en_msg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(en_msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [en_msg]

def delete_encourage(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print("{0.user} has logged in . . .".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if msg.startswith("$hello"):
    await message.channel.send("Hey there")
  if msg.startswith("$inspire"):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encourage
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))
  
  if any(word in msg for word in ping_word):
    await message.channel.send(random.choice(ping_response))

  if any(word in msg for word in joke_word):
    await message.channel.send(random.choice(joke_response))

  if msg.startswith('$new'):
    en_msg = msg.split("$new ",1)[1]
    update_encourage(en_msg)
    await message.channel.send("Yeah, Got it.")

  if msg.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encourage(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)  

client.run(os.getenv('TOKEN'))



