# DiscordData
#### Video Demo: [DiscordData | CS50X Final Project](https://youtu.be/cd4T5sMcKbA)
#### Description: Simple discord bot that captures the information like server id, name, icon, owner, creation date, as well as a number of messages and number of members for each day. And represent that information in the form of chart on the website.

## `app.py`
`app.py` is a simple web server with only one path. If get argument 'server' is given, flask will render a page with statistics of given server id. Called stats page. If no 'server' argument is given or the given id is not in the database, flask will render a home page with a list of all available servers.

The home page is just a grid of all available servers. There are displayed icon (if server has one), name, ownership, and the date of creating the server as well as a button to see more details, which will take you to the stats page with id of the server you choose.

The stats page loads all information we have on the given server id, icon *if server has one*, name, ownership, and the date of creating the server as well as the number of sent messages and the number of members in the server for every day. Those two pieces of information are represented with charts. For making charts we use Chart.js (a free JavaScript library for making HTML-based charts).

## Database
The database has 2 tables. One is called 'servers' and another one is called 'data'. Servers table has id, name, icon, owner, created column. While data table has server_id, date, msg_count, member_count.

There are 3 indexes. On column id, server_id and the last one on date. Those three columns are used for querying that's why they have indexes.

## `bot.py`
`bot.py` is a simple discord bot that gets basic information about the server that he joins.
Information like id, name, ownership, icon and date of creation. Because most of this information can be changed except id and date of creation bot has `!update` command that's gonna update all information. After that bot will send a simple message to the channel where the command was entered to notify user that information has been updated.

When a new message is sent to text channel of server that bot is on, that message gets captured and using timestamp from the message, bot checks in the database (data table) to see if  there is row with server id of server where message is sent and date of when the message is sent. If there is row get current msg_count and increment by 1. If there is no row create one with msg_count = 1.

At the same time bot is getting number of members in the server message is sent in and update previously mentioned row. This allows us to track the number of server members for each day.

# Certain design choices
## `bot.py` from line 42 to line 50
This might need to be atomic. But doing that bot will probably become much slower for high speed performance like we need when trying to capture every message.