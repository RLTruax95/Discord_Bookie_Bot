import discord
from discord.ext import commands
from discord import app_commands

from match import Match
from player import Player

players = []
matches = []

class Client(commands.Bot):
########################################################################################################################
    #Function that runs on the startup of the bot
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

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
#Has the bot respond with a hello message. Keeping for example
@client.tree.command(name='hello', description='Bot says Hello', guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello!')
########################################################################################################################
@client.tree.command(name='add_player', description='Add player to the tournament', guild=GUILD_ID)
async def add_player(interaction: discord.Interaction, name: discord.Member, faction: str, tv: int, coins: int):
    players.append(Player(name, faction, tv, coins))
    await interaction.response.send_message(f'{name}\'s {faction} team added to player list')
########################################################################################################################
@client.tree.command(name='show_players', description='Shows all added players', guild=GUILD_ID)
async def show_players(interaction: discord.Interaction):
    temp_str = ''
    for player in players:
        temp_str = temp_str + f'{player.name}: {player.faction} \n'
    await interaction.response.send_message(temp_str)
########################################################################################################################
@client.tree.command(name='add_match', description='Add match to the tournament', guild=GUILD_ID)
async def add_match(interaction: discord.Interaction, home_player: discord.Member, away_player: discord.Member):
    matches.append(Match(home_player, away_player))
    await interaction.response.send_message(f'{home_player.name.title()} vs {away_player.name.title()} Added')
########################################################################################################################
@client.tree.command(name='show_matches', description='Shows added matches', guild=GUILD_ID)
async def show_matches(interaction: discord.Interaction):
    temp_str = 'Home vs Away\n'
    for match in matches:
        temp_str = temp_str + f'{match.home_player} vs {match.away_player} \n'
    await interaction.response.send_message(temp_str)
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