import discord
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

ai = Groq(api_key=GROQ_KEY)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!ask '):
        question = message.content[5:]
        await message.channel.send("Thinking... 🤔")
        response = ai.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
        for i in range(0, len(answer), 1900):
            await message.channel.send(answer[i:i+1900])

client.run(TOKEN)