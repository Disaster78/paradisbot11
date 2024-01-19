import nextcord
from nextcord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", description="Shows available commands and their descriptions. Usage: `.help [command_name]`")
    async def help(self, ctx, *, command_name: str = None):
        if command_name:
            command = self.bot.get_command(command_name.lower())

            if not command:
                return await ctx.send(f"No information found for command `{command_name}`.")

            embed = nextcord.Embed(
                title=f"Command Help: `{command.name}`",
                description=command.description,
                color=nextcord.Colour.random()
            )
            embed.add_field(name="Usage", value=f"```{command.usage}```" if command.usage else "No usage information provided.")
            embed.set_thumbnail(url =ctx.guild.icon.url)
            embed.set_footer(text =f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                title="Commands Help",
                description="Shows available commands and their descriptions. Usage: `.help [command_name]`",
                color=nextcord.Colour.random()
            )

            commands_list = [f"`{command.name}`" for cog in self.bot.cogs.values() for command in cog.get_commands() if not command.hidden]
            if commands_list:
                embed.add_field(name="Commands", value=", ".join(commands_list), inline=False)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

            server_url=ctx.guild.icon.url
            embed.set_thumbnail(url=server_url)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
