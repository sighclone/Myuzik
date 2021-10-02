import os
import discord
import urllib
import re
import time
import subprocess
import youtube_dl
from discord.ext import commands
from keepalive import keepalive


# Global variable declarations

global thevc
global play_mode
global current_song

# specifying what the command prefix is + print when bot loads all dependencies and is online

client = commands.Bot(command_prefix="!")
@client.event
async def on_ready():
  print("Bot is now online")


# A command to check if the bot (by itself) is responsive

@client.command(name="check",pass_contect=True)
async def check(ctx):
  await ctx.send("I am online and responsive!")


# This command makes the bot join the VC of the user who uses the command

@client.command(name="join",pass_context=True)
async def join(ctx):
  if(ctx.author.voice):
    await ctx.send("Attempting to join your VC");
    try:
      channel = ctx.message.author.voice.channel
      await channel.connect()
      await ctx.send("I have joined")
      global thevc
      thevc = ctx.message.author.voice.channel
    except:
      await ctx.send("Attempt failed, I am possibly in another VC")
  else:
    await ctx.send("You need to join a VC first, then I follow")


# This command makes the bot leave the VC it is in

@client.command(name="leave",pass_context=True)
async def leave(ctx):
  global thevc
  if(ctx.voice_client and ctx.message.author.voice.channel==thevc):
    await ctx.guild.voice_client.disconnect()
    await ctx.send("See you next time!")
    thevc = ""
  elif(ctx.voice_client and ctx.message.author.voice.channel!=thevc):
    await ctx.send("I'm in a VC which you aren't in, you don't have the permission to make me leave it!")
  else:
    await ctx.send("Leave what? The server? bruh, shut up")


# the play command, plays the requested song

@client.command(name="play", pass_context=True)
async def play(ctx,url):
  ctx.voice_client.stop()
  ffmpeg_options={"before_options":"-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5","options":'-vn',}
  ydl_options={"format":"bestaudio/best"}
  vc = ctx.voice_client

  # first it will try to see if the given query is a direct url, if it is, it will play it directly

  try:
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
      info = ydl.extract_info(url,download=False)
      url2=info["formats"][0]["url"]
      source = await discord.FFmpegOpusAudio.from_probe(url2,**ffmpeg_options)
      play_mode = "link"
      global current_song
      current_song = source
      vc.play(source)
      
      # if it is not a url, then it will read it as plain text and search the text on youtube
      # then it will get the link of the top result on youtube, use the link for the same procedure as above

  except:
    query = str(ctx.message.content.lower())
    query = query[6:]
    await ctx.channel.send("Your requested audio is `" + query + "`")
    indirect_query=query.replace(" ", "+")
    ytquery = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + indirect_query)
    video_ids = re.findall(r"watch\?v=(\S{11})", ytquery.read().decode())
    link="https://youtu.be/" + str(video_ids[0])
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
      info = ydl.extract_info(link,download=False)
      url2=info["formats"][0]["url"]
      source = await discord.FFmpegOpusAudio.from_probe(url2,**ffmpeg_options)
      play_mode = "search"
      vc.play(source)
        
"""
@client.command(name = "loop", pass_ctx=True)
async def loop(ctx):
  global play_mode
  if play_mode == "link":
    while True:
      client.command(play())
"""
# pause the song

@client.command(pass_context=True)
async def pause(ctx):
  if ctx.voice_client.is_playing():
    await ctx.voice_client.pause()
  else:
    await ctx.send("Pause what? Your life? A song needs to be playing in the first place")


# resume playing the song

@client.command(pass_context=True)
async def resume(ctx):
  if not (ctx.voice_client.is_playing()):
    try:
      await ctx.voice_client.resume()
    except:
      pass
  else:
    await ctx.send("The song is already playing!")


# stops playing the song and also removes it from the queue

@client.command(pass_context=True)
async def stop(ctx):
  ctx.voice_client.stop()


# potential alternative format can be:
# @client.command(name="yt", pass_context=True)
# and so on...
# this message just searches for the query, gets top result link and just shows the link in chat

# this code is removed for now
@client.command(name = "yt", pass_context=True)
async def yt(ctx):
    query = str(ctx.message.content.lower()[4:])
    await ctx.channel.send("Your requested YouTube link is `" + query + "`")
    indirect_query = query.replace(" ", "+")
    ytquery = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + indirect_query)
    video_ids = re.findall(r"watch\?v=(\S{11})", ytquery.read().decode())
    link="https://youtu.be/" + str(video_ids[0])
    await ctx.channel.send(link) #old one exact


keepalive()


# misc

client.run(os.getenv('token'))
players={}


# end