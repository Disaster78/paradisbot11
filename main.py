import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

keep_alive()

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot.remove_command("help")
token = os.environ['TOKEN']

cogs = ["cogs.basic", "cogs.Snipe", "cogs.help", "cogs.moderation", "cogs.WelcomeCog"] 

@bot.event
async def on_ready():
    print("The bot is ready!")
    print("Loading cogs . . .")
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(cog + " was loaded.")
        except Exception as e:
            print(e)

@bot.event
async def on_message(message):
    if bot.user.mention in message.content:
        await message.reply("Hello Pookie")
    await bot.process_commands(message)


    
bot.run(token)
