import discord
from discord.ext import commands 
from pathlib import Path

BOT_TOKEN = "Token"


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.voice_states = True

path_songs = Path("Path to songs")
song_files = {file.name: file.resolve() for file in path_songs.iterdir() if file.is_file()}
bot = commands.Bot(command_prefix="!", intents=intents)

intros = {
    0  : "Songname.filetype" # member id as key and the file as value
}
sup_allowed_users = 0 # owner id, unless you want others to shutdown bot
@bot.event
async def on_voice_state_update(member,before,after):
    if before.channel and not after.channel:
        return
    voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
    if not voice_client:
        return
    for id in intros:
        if member.id == id:
            print("Found member")
            intro = intros.get(member.id)
            song_files = {file.name: file.resolve() for file in path_songs.iterdir() if file.is_file()}
            path_to_wav = str(song_files.get(intro))
            audio = discord.FFmpegPCMAudio(path_to_wav)
            voice_client.play(audio)

@bot.command()
async def shutdown(ctx):
    if ctx.author.id not in sup_allowed_users: 
        return 
    exit()


@bot.command()
async def join(ctx, *, message):
    channelid = int(message)
    channel = bot.get_channel(channelid)
    if channel:
        await channel.connect()
    else:
        print("did not find channel")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I am not in a voice channel :(")

@bot.command()
async def stop(ctx): 
    if not ctx.voice_client: 
        await ctx.send("I am not in a voice channel.")
        return
    ctx.voice_client.stop()
    await ctx.send("Stopped.")

bot.run(BOT_TOKEN)