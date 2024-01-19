import nextcord
from nextcord.ext import commands

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Give the user the "Quarantine" role when they join
        quarantine_role = nextcord.utils.get(member.guild.roles, name="Quarantine")
        await member.add_roles(quarantine_role)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Check if the "Quarantine" role is in before.roles and not in after.roles,
        # and if the "Member" role is in after.roles
        quarantine_role = nextcord.utils.get(after.guild.roles, name="Quarantine")
        member_role = nextcord.utils.get(after.roles, id=1197243265532043304)

        if quarantine_role in before.roles and quarantine_role not in after.roles and member_role in after.roles:
            # The user has been verified and received the "Member" role
            channel = after.guild.get_channel(1197217821533413447)  # Replace with your channel ID
            embed = nextcord.Embed(
                title=f"Welcome {after.mention}!",
                description=f"Thanks for verifying and joining {after.guild.name}! Please check <#1197217992002523196> and <#1197218991215743046>",
                colour=nextcord.Colour.random(),
                timestamp=after.joined_at,
            )

            if after.avatar is None:
                embed.set_thumbnail(url=after.default_avatar.url)
            else:
                embed.set_thumbnail(url=after.avatar.url)

            embed.set_footer(text=f"Member Count: {len(after.guild.members)}")

            await channel.send(f"{after.mention}",embed=embed)

def setup(bot):
    bot.add_cog(WelcomeCog(bot))
