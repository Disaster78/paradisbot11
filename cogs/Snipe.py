from discord import Embed, Colour
from discord.ext import commands

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.max_snipe_count = 10  # Set your desired maximum limit here
        self.deleted_messages = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # Store the deleted message
        channel_id = message.channel.id
        self.deleted_messages.setdefault(channel_id, []).insert(0, message)
        # Keep only the last N deleted messages (adjust as needed)
        self.deleted_messages[channel_id] = self.deleted_messages[channel_id][:self.max_snipe_count]

    @commands.command(name='snipe',description="View the last deleted messages.", usage=".snipe ({number of messages}, limit=10)")
    async def snipe_command(self, ctx, count: int = 1):
        channel_id = ctx.channel.id

        # Check if the specified count exceeds the maximum limit
        if count > self.max_snipe_count:
            await ctx.send(f"Error: You can snipe up to {self.max_snipe_count} messages at a time.")
            return

        # Check if there are deleted messages in the channel
        if channel_id in self.deleted_messages:
            sniped_messages = self.deleted_messages[channel_id][:count]

            # Use nextcord.Colour.random() for a random color
            embed_color = Colour.random()

            # Create an embed with the sniped messages details
            combined_content = "\n".join([f"**{m.author.name}:** {m.content}" for m in sniped_messages])
          
            embed = Embed(
                title=f'Sniped Messages ({len(sniped_messages)})',
                color=embed_color,
                description=combined_content,
            ) 
  
           # Combine the content of the deleted messages
            
 
            # Add a field with the combined content
    

            # Add a timestamp to the embed
            embed.timestamp = ctx.message.created_at

            # Set the author to the bot with a random color for the avatar
            if sniped_messages and sniped_messages[0].author:
                author_avatar_url = sniped_messages[0].author.avatar.url if sniped_messages[0].author.avatar else str(sniped_messages[0].author.default_avatar.url)
                embed.set_author(name=sniped_messages[0].author.name, icon_url=author_avatar_url)
            else:
                embed.set_author(name=self.bot.user.name)

            # Set a footer with the channel name
            embed.set_footer(text=f'In #{ctx.channel.name}')

            # Send the embed
            await ctx.send(embed=embed)

        else:
            await ctx.send('No recently deleted messages to snipe')

def setup(bot):
    bot.add_cog(Snipe(bot))
