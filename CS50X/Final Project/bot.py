import discord
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Enable the intent for the Discord client
intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    # Print a message to the console when the bot is ready
    print("Bot is UP!")


@client.event
async def on_guild_join(guild):
    # Get the URL of the server's icon, if it has one
    if guild.icon:
        icon = guild.icon.url
    else:
        icon = ""

    # Check if the server is already in the database
    r = db.execute("SELECT * FROM servers WHERE id = ?", guild.id)

    # If the server is not in the database, insert a new row
    if len(r) == 0:
        db.execute("INSERT INTO servers (id, name, icon, owner, created) VALUES (?, ?, ?, ?, ?)", guild.id, guild.name, icon, guild.owner.name + "#" + guild.owner.discriminator, guild.created_at)

    # If the server is already in the database, update the existing row
    elif len(r) == 1:
        db.execute("UPDATE servers SET name = ?, icon = ?, owner = ? WHERE id = ?", guild.name, icon, guild.owner.name + "#" + guild.owner.discriminator, guild.id)


@client.event
async def on_message(message):
    # OVO MORA BITI ATOMIC
    # Get the current message count for the server and date
    r = db.execute("SELECT msg_count FROM data WHERE server_id = ? AND date = ?", message.guild.id, message.created_at.date())

    # If there are no rows in the database for the server and date, insert a new row
    if len(r) == 0:
        db.execute("INSERT INTO data (server_id, date, msg_count, member_count) VALUES (?, ?, 1, ?)", message.guild.id, message.created_at.date(), message.guild.member_count)

    # If there is a row in the database for the server and date, update the existing row
    else:
        db.execute("UPDATE data SET msg_count = ?, member_count = ? WHERE server_id = ? AND date = ?", r[0]["msg_count"] + 1, message.guild.member_count, message.guild.id, message.created_at.date())

    # Check if the message starts with a forward slash
    if message.content.startswith('!'):
        # Split the message into a list of words
        words = message.content.split()
        # Check if the first word is the command you want to trigger
        if words[0] == '!update':
            await on_guild_join(message.guild)
            # Send a message back to the user
            await message.channel.send("Server information updated!")


# Run the bot using your bot token
client.run('')
