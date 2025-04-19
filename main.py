import discord
from discord.ext import commands
from discord import app_commands

from match import Match
from player import Player
from bet import Bet

players = []
matches = []
bets = []

class Client(commands.Bot):
########################################################################################################################
    #Function that runs on the startup of the bot
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        Player.load_players_from_csv(players)
        Match.load_matches_from_csv(matches, players)
        Bet.load_bets_from_csv(bets, matches, players)

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
    player = Player(name.name, faction, tv, coins)
    player.save_to_csv(players)
    await interaction.response.send_message(f'{name}\'s {faction} team added to player list')
########################################################################################################################
@client.tree.command(name='add_win', description='Add a win to the players record', guild=GUILD_ID)
async def add_win(interaction: discord.Interaction):
    players_names = []
    for player in players:
        players_names.append(player.name)
    if interaction.user.name in players_names:
        players[players_names.index(interaction.user.name)].add_win()
        await interaction.response.send_message(f'Congrats on your win, {interaction.user.name}!')
    else:
        await interaction.response.send_message(f'{interaction.user.name} is not a registered coach')
    Player.update_csv(players)
########################################################################################################################
@client.tree.command(name='add_loss', description='Add a loss to the players record', guild=GUILD_ID)
async def add_loss(interaction: discord.Interaction):
    players_names = []
    for player in players:
        players_names.append(player.name)
    if interaction.user.name in players_names:
        players[players_names.index(interaction.user.name)].add_loss()
        await interaction.response.send_message(f'Sorry for your loss, {interaction.user.name}!')
    else:
        await interaction.response.send_message(f'{interaction.user.name} is not a registered coach')
    Player.update_csv(players)
########################################################################################################################
@client.tree.command(name='add_draw', description='Add a draw to the players record', guild=GUILD_ID)
async def add_draw(interaction: discord.Interaction):
    players_names = []
    for player in players:
        players_names.append(player.name)
    if interaction.user.name in players_names:
        players[players_names.index(interaction.user.name)].add_draw()
        await interaction.response.send_message(f'It was an even match, {interaction.user.name}!')
    else:
        await interaction.response.send_message(f'{interaction.user.name} is not a registered coach')
    Player.update_csv(players)
########################################################################################################################
@client.tree.command(name='show_players', description='Shows all added players', guild=GUILD_ID)
async def show_players(interaction: discord.Interaction):
    Player.load_players_from_csv(players)
    embeds = []
    for player in players:
        embed = discord.Embed(title=player.name.title(), description=f'Faction: {player.faction.title()}')
        embed.add_field(name='Team Value:', value=player.TV)
        embed.add_field(name='Coins:', value=player.coins)
        embed.add_field(name='W/D/L:', value=f'{player.wins}/{player.draws}/{player.losses}')
        embeds.append(embed)
    await interaction.response.send_message(embeds=embeds)
########################################################################################################################
async def player_autocomplete(interaction: discord.Interaction,current: str,) -> list[app_commands.Choice[str]]:
    player_names = [player.name for player in players]
    return [
        app_commands.Choice(name=player, value=player)
        for player in player_names if current.lower() in player.lower()
    ]

async def match_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    pending_matches = [match.match_name for match in matches]
    return [
        app_commands.Choice(name=match, value=match)
    for match in pending_matches if current.lower() in match.lower()]

async def parlay_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    match = interaction.namespace.match
    match_obj = next((m for m in matches if m.match_name == match), None)
    if not match_obj:
        return []

    player_names = [match_obj.home_player.name, match_obj.away_player.name]
    return [
        app_commands.Choice(name=player, value=player)
        for player in player_names if current.lower() in player.lower()
    ]
########################################################################################################################
@client.tree.command(name='add_match', description='Add match to the tournament', guild=GUILD_ID)
@app_commands.autocomplete(home_player=player_autocomplete, away_player=player_autocomplete)
async def add_match(interaction: discord.Interaction, home_player: str, away_player: str):
    home_player_obj = next((player for player in players if player.name == home_player), None)
    away_player_obj = next((player for player in players if player.name == away_player), None)

    if home_player_obj and away_player_obj:
        temp_match = Match(home_player_obj, away_player_obj)
        temp_match.save_to_csv(matches)
        matches.append(temp_match)
        await interaction.response.send_message(f'{home_player_obj.name} vs {away_player_obj.name} added to matches')
    else:
        if not home_player_obj:
            await interaction.response.send_message(f'{home_player} is not a registered coach')
        if not away_player_obj:
            await interaction.response.send_message(f'{away_player} is not a registered coach')
########################################################################################################################
@client.tree.command(name='show_matches', description='Shows added matches', guild=GUILD_ID)
async def show_matches(interaction: discord.Interaction):
    Match.load_matches_from_csv(matches,players)
    embeds = []
    for match in matches:
        embed = discord.Embed(title=f'{match.home_player.name} vs {match.away_player.name}',
                              description=f'{match.home_player.faction} vs {match.away_player.faction}')
        embeds.append(embed)
    await interaction.response.send_message(embeds=embeds)
########################################################################################################################
#Used to clear the entire message history of the text channel
@client.tree.command(name='purge_chat', description='Clears message history (must be admin)', guild=GUILD_ID)
async def purge_chat(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        if interaction.permissions.administrator:
            # Purge messages in the channel
            deleted = await interaction.channel.purge(limit=None)
            await interaction.followup.send(f"Successfully deleted {len(deleted)} messages.", ephemeral=True)
        else:
            await interaction.followup.send(f"Only administrators have permission to purge messages in this channel.")

    except discord.Forbidden:
        await interaction.followup.send("I don't have permission to delete messages in this channel.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)
########################################################################################################################
@client.tree.command(name='place_bet', description='Place a bet on the desired match', guild=GUILD_ID)
@app_commands.autocomplete(match=match_autocomplete, parlay=parlay_autocomplete)
async def place_bet(interaction: discord.Interaction, match: str, parlay: str, amount: int):
    match_obj = next((m for m in matches if m.match_name == match), None)
    if not match_obj:
        await interaction.response.send_message(f'Match {match} does not exist')
        return

    if parlay not in [match_obj.home_player.name, match_obj.away_player.name]:
        await interaction.response.send_message(f'Parlay {parlay} is not a valid parlay')
        return

    temp_bet = Bet(match_obj, parlay, amount, interaction.user)
    temp_bet.save_to_csv(bets)

    await interaction.response.send_message(f'{interaction.user} placed a {amount} gold bet on {parlay} in \'{match_obj.match_name}\'')
########################################################################################################################
@client.tree.command(name='show_bets', description='Shows the bets for a specified match', guild=GUILD_ID)
@app_commands.autocomplete(match=match_autocomplete)
async def show_bets(interaction: discord.Interaction, match: str):
    Match.load_matches_from_csv(matches,players)
    Bet.load_bets_from_csv(bets,matches,players)
    embeds = []
    for bet in bets:
        if bet.match_name == match:
            embed = discord.Embed(title=f'{match}',
                              description=f'{bet.gambler} - {bet.wager} on {bet.parlay.name}')
        embeds.append(embed)
    if embeds:
        await interaction.response.send_message(embeds=embeds)
    else:
        await interaction.response.send_message('No bets found')
########################################################################################################################
client.run('MTM1ODk2MDk4NTY2MjI5MjExMg.GMIq8J.Dn4fTHERIXtEAFabwfXdvo-tZqmIj3Yh9wlL9U')