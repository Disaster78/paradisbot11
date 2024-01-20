import discord
from discord import app_commands
from discord.ext import commands
import os
from keep_alive import keep_alive
keep_alive()

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot.remove_command("help")
tree = app_commands.CommandTree(bot)
token = os.environ['TOKEN']

cogs = ["cogs.basic", "cogs.Snipe", "cogs.help", "cogs.moderation", "cogs.WelcomeCog"]  # Modify the cogs list to include the correct path to the basic.commands file

@bot.event
async def on_ready():
    print("The bot is ready!")
    print("Loading cogs . . .")
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print(cog + " was loaded.")
        except Exception as e:
            print(e)

@bot.event 
async def on_message(message):
    if bot.user.mention in message.content:
        await message.reply("Hello Pookie")
    await bot.process_commands(message)

class Buttons(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Ticket Support", style=discord.ButtonStyle.green, emoji="📧")
    async def teste3(self, button: discord.ui.Button, interaction: discord.Interaction):
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await interaction.guild.create_text_channel(f"Ticket-", overwrites=overwrites)
        channel_id = channel.id
        embed = discord.Embed(title="Ticket Support", description=f"Thank you for requesting help.\nState your problems or questions here and await a response.")
        await channel.send(embed=embed, view=Butts())
        await interaction.send(f"Ticket created <#{channel_id}>..", ephemeral=True)

class Butts(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="📧")
    async def teste(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.channel.delete()

    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.green, emoji="📧")
    async def teste2(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator and interaction.user is not None:
            embed = discord.Embed(title=f"Claimed Ticket", description=f"Your ticket will be handled by {interaction.user.mention}.")
            await interaction.send(embed=embed)
            interaction = await bot.wait_for("button_click", check=lambda inter: inter.custom_id == "teste2")

            async def button_callback(button_inter: discord.Interaction):
                Butts.disabled = True
            Butts.callback = button_callback
        else:
            embed = discord.Embed(title=f"You don't have the permissions for this!")
            await interaction.send(embed=embed, ephemeral=True)

@tree.command(name="ticket", description="Setup the ticket system!")
async def ticket(ctx: discord.Interaction):
    if ctx.user.guild_permissions.administrator and ctx.user is not None:
        embed = discord.Embed(description=f"Press the button below to create a Ticket!")
        await ctx.send(embed=embed, view=Buttons())
    else:
        embed = discord.Embed(title=f"You don't have the permissions for this!")
        await ctx.send(embed=embed, ephemeral=True)

bot.run(token)
