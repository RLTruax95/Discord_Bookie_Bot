import discord
from discord.ext import commands
from discord import app_commands

from player import Player

players = []
matches = []

class Client(commands.Bot):
########################################################################################################################
    #Function that runs on the startup of the bot
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        Player.load_players_from_csv(players)

        try:
            #Used to synch the slash commands to the discord server
            guild = discord.Object(id=806414853749211186)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing command: {e}')
########################################################################################################################
    #Prints the posted message to the terminal and says 'hello' is the message starts with 'hello'
    async def on_message(self, message):
        print(f'{message.author} said: {message.content}')
        if message.author == self.user:
            return
        if message.content.startswith('hello'):
            await message.channel.send(f'Hello, {message.author}!')
########################################################################################################################
    #Has the bot send a message after a user posts reaction
    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send(f'You reacted, {user.name}!')
########################################################################################################################
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='!', intents=intents)

GUILD_ID = discord.Object(id = 806414853749211186)
########################################################################################################################
@client.tree.command(name='add_player', description='Add player to the tournament', guild=GUILD_ID)
async def add_player(interaction: discord.Interaction, name: discord.Member, faction: str, tv: int, coins: int):
    player = Player(name, faction, tv, coins)
    player.save_to_csv(players)
    await interaction.response.send_message(f'{name}\'s {faction} team added to player list')
########################################################################################################################
@client.tree.command(name='show_players', description='Shows all added players', guild=GUILD_ID)
async def show_players(interaction: discord.Interaction):
    Player.load_players_from_csv(players)
    print(f'{len(players)} players in list')
    embeds = []
    for player in players:
        embed = discord.Embed(title=player.name.title(), description=f'Faction: {player.faction.title()}')
        embed.add_field(name='Team Value:', value=player.TV)
        embed.add_field(name='Coins:', value=player.coins)
        embeds.append(embed)
    await interaction.response.send_message(embeds=embeds)
########################################################################################################################
# @client.tree.command(name='add_match', description='Add match to the tournament', guild=GUILD_ID)
# async def add_match(interaction: discord.Interaction, home_player: discord.Member, away_player: discord.Member):
#     matches.append(Match(home_player, away_player))
#     await interaction.response.send_message(f'{home_player.name.title()} vs {away_player.name.title()} Added')
########################################################################################################################
# @client.tree.command(name='show_matches', description='Shows added matches', guild=GUILD_ID)
# async def show_matches(interaction: discord.Interaction):
#     for match in matches:
#         embed = discord.Embed(title=f'{match.home_player.name} vs {match.away_player.name}',
#                               description=f'{match.home_player.faction} vs {match.away_player.faction}',
#                               thumbnail=match.home_player.avatar)
#         await interaction.response.send_message(embed=embed)
########################################################################################################################
#Used to clear the entire message history of the text channel
@client.tree.command(name='purge_chat', description='Clears message history', guild=GUILD_ID)
async def purge_chat(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        # Purge messages in the channel
        deleted = await interaction.channel.purge(limit=None)

        # Send an invisible (ephemeral) confirmation message
        await interaction.followup.send(f"Successfully deleted {len(deleted)} messages.", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("I don't have permission to delete messages in this channel.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)
########################################################################################################################
client.run('MTM1ODk2MDk4NTY2MjI5MjExMg.GMIq8J.Dn4fTHERIXtEAFabwfXdvo-tZqmIj3Yh9wlL9U')