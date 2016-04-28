import discord
import asyncio
import json
import urllib.request
import urllib.parse

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



@client.async_event
def on_voice_state_update(before, after):
    if after.voice_channel is not None:
        yield from client.send_message(after.server, after.name + " joined voice channel " + after.voice_channel.name)
    else:
        yield from client.send_message(after.server, after.name + " quit voice chatting")


client.run("zactepps@gmail.com", "justAsimpletest")
client.logout()
client.close()
