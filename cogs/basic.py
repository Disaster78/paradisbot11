import discord
from discord.ext import commands

class Basic(commands.Cog, name="basic"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="serverinfo", description="Shows info about the server.", usage=".serverinfo")
    async def serverinfo(self, ctx):
        staff_roles = ("Founder", "Head Administrator", "Trial Admin", "Moderators", "Trial Mod")
        embed2 = discord.Embed(timestamp=ctx.message.created_at, color=ctx.author.color)
        embed2.add_field(name='Name', value=f"{ctx.guild.name}", inline=False)
        embed2.add_field(name='Owner', value=f'{ctx.guild.owner.mention}', inline=False)
        embed2.add_field(name='Verification Level', value=str(ctx.guild.verification_level), inline=False)
        embed2.add_field(name='Highest role', value=ctx.guild.roles[-2], inline=False)
        embed2.add_field(name='Contributers:', value="None")
        for r in staff_roles:
            role = discord.utils.get(ctx.guild.roles, name=r)
            if role:
                members = '\n'.join([member.name for member in role.members])
                embed2.add_field(name=f'{r}', value=members, inline=False)

        embed2.add_field(name='Number of roles',value=str(len(ctx.guild.roles)), inline=False)
        embed2.add_field(name='Number Of Members', value=ctx.guild.member_count, inline=False)
        embed2.add_field(name= 'Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
        embed2.set_thumbnail(url= ctx.guild.icon.url)
        embed2.set_author(name =ctx.author.name, icon_url=ctx.author.avatar.url)
        embed2.set_footer(text =self.bot.user.name,  icon_url=ctx.message.author.avatar.url)
        await ctx.send(embed=embed2)

    @commands.command(name="userinfo", description="Shows information about a user.", usage=".userinfo [mention]")
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
            roles = [role for role in ctx.author.roles]
        else:
            roles = [role for role in member.roles]
        embed = discord.Embed(title=f"{member}", colour=member.colour, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.set_author(name="User Info: ")
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="User Name:",value=member.display_name, inline=False)
        embed.add_field(name="Discriminator:",value=member.discriminator, inline=False)
        embed.add_field(name="Current Status:", value=str(member.status).title(), inline=False)
        embed.add_field(name="Current Activity:", value=f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}" if member.activity is not None else "None", inline=False)
        embed.add_field(name="Created At:", value=member.created_at.strftime("%a, %d, %B, %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name="Joined At:", value=member.joined_at.strftime("%a, %d, %B, %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name=f"Roles [{len(roles)}]", value=" **|** ".join([role.mention for role in roles]), inline=False)
        embed.add_field(name="Top Role:", value=member.top_role, inline=False)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.add_field(name="Bot?:", value=member.bot, inline=False)
        await ctx.send(embed=embed)
        return

    @commands.command(name="avatar", aliases=["av"], description="Shows the avatar of a user.", usage=".avatar [mention]")
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"{member}'s Avatar", colour=member.colour, timestamp=ctx.message.created_at)
        embed.set_image(url=member.avatar.url)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="ping", description="Check the bot's latency.", usage=".ping")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")
    @commands.command(name= "support", description="Get the link to the bot's support server.", usage=".support")
    async def support(self, ctx):
        embed = discord.Embed(title="Support Server", colour=discord.Colour.random(), timestamp=ctx.message.created_at)
        embed.add_field(name="Support Server:", value="[Click Here](https://discord.com/invite/38Zj8AZAMM)", inline=False)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)     

def setup(bot):
    bot.add_cog(Basic(bot))
