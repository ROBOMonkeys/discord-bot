import discord
import asyncio
import json
import urllib.request
import urllib.parse
import database_manager as db

client = discord.Client()
me = None


def search(searchfor):
    query = urllib.parse.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.request.urlopen(url)
    search_results = search_response.read().decode("utf8")
    results = json.loads(search_results)
    data = results['responseData']
    hits = data['results']
    return hits[0]['url']


@client.async_event
def on_ready():
    print("Connected as " + client.user.name + "!")
    for s in client.servers:
        global me
        me = s.me


@client.async_event
def on_message(msg):
    if me in msg.mentions:
        msg_words = msg.content.split(" ")
        if msg_words[1] == "g" or \
           msg_words[1] == "google":
            gs = search(msg.content[(len(msg_words[1]) + len(msg_words[0]) + 1):])
            yield from client.send_message(msg.channel, "Top Google result:\n" + urllib.parse.unquote(gs))
        elif msg_words[1] == "grab":
            if len(msg_words) < 3:
                yield from client.send_message(msg.channel, "Please add a username")
            else:
                messages = yield from client.logs_from(me.server.default_channel)
                for m in messages:
                    if m.author.name == msg_words[2]:
                        db.add_quote(m.author.name, m.content)
                        break
                yield from client.send_message(msg.channel, "Grabbed!")
        elif msg_words[1] == "quote":
            num_quotes = 1
            if len(msg_words) < 3:
                yield from client.send_message(msg.channel, "Please add a username")
            else:
                if len(msg_words) == 4:
                    num_quotes = msg_words[3]
                yield from client.send_message(msg.channel, db.get_quote(msg_words[2], num_quotes))


@client.async_event
def on_voice_state_update(before, after):
    if after.voice_channel is not None:
        yield from client.send_message(after.server, after.name + " joined voice channel " + after.voice_channel.name)
    else:
        yield from client.send_message(after.server, after.name + " quit voice chatting")


client.run("zactepps@gmail.com", "justAsimpletest")
client.logout()
client.close()
