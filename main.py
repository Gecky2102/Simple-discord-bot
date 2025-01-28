import discord
from discord.ext import commands
import random
import aiohttp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp as youtube_dl
from dotenv import load_dotenv
import os

# Carica il file .env
load_dotenv()

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# COSE IMPORTANTI, RUOLI ETC ETC
STAFF_ROLE_ID = int(os.getenv("STAFF_ROLE_ID"))
CANALE_PEX_DEPEX_ID = int(os.getenv("CANALE_PEX_DEPEX_ID"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))
FOOTER_TEXT = os.getenv("FOOTER_TEXT")
HANGMAN_CHANNEL_ID = int(os.getenv("HANGMAN_CHANNEL_ID"))
TO_MOD_CHANNEL_ID = int(os.getenv("TO_MOD_CHANNEL_ID"))
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
API_KEY = os.getenv("API_KEY")

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents=intents)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

#COMANDO CON LISTA E OPZIONI DI OGNI COMANDO
@bot.command(name='my_help')
async def my_help(ctx):
    embed = discord.Embed(title="Comandi disponibili", color=discord.Color.green())
    embed.add_field(name="!skin", value="Mostra la skin di un giocatore Minecraft", inline=False)
    embed.add_field(name="!rps", value="Gioca a sasso, carta, forbice", inline=False)
    embed.add_field(name="!music", value="Mostra i comandi per la musica", inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game('⚒️Manuntenzione⚒️'))
    print(f'✅ Il bot è online! Connesso come {bot.user}')
    await bot.tree.sync()
    try:
        with open('th.jpeg', 'rb') as image:
            data = image.read()
            await bot.user.edit(avatar=data)
            print("✅ Avatar impostato con successo!")
    except FileNotFoundError:
        print("❌ Immagine dell'avatar non trovata.")
    except discord.HTTPException as e:
        print(f"❌ Errore durante l'aggiornamento dell'avatar: {e}")

@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 Pong!", description=f"Latency: {latency}ms", color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def pex(ctx, member: discord.Member, role: discord.Role, *, reason: str = "Nessun motivo fornito"):
    await member.add_roles(role, reason=reason)

    embed = discord.Embed(title="Nuovo pex!", description=f"{member.mention} ha ottenuto il ruolo {role.mention}\nMotivo: {reason}", color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    channel = bot.get_channel(CANALE_PEX_DEPEX_ID)
    await channel.send(embed=embed)
    await ctx.message.delete()

@bot.command()
async def depex(ctx, member: discord.Member, role: discord.Role, *, reason: str = "Nessun motivo fornito"):
    await member.remove_roles(role, reason=reason)

    embed = discord.Embed(title="Depex!", description=f"{member.mention} ha perso il ruolo {role.mention}\nMotivo: {reason}", color=discord.Color.red())
    embed.set_footer(text=FOOTER_TEXT)
    channel = bot.get_channel(CANALE_PEX_DEPEX_ID)
    await channel.send(embed=embed)
    await ctx.message.delete()

    @pex.error
    async def pex_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Errore", description="Non hai i permessi necessari per eseguire questo comando.", color=discord.Color.red())
            embed.set_footer(text=FOOTER_TEXT)
            await ctx.send(embed=embed)
    
    @depex.error
    async def depex_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Errore", description="Non hai i permessi necessari per eseguire questo comando.", color=discord.Color.red())
            embed.set_footer(text=FOOTER_TEXT)
            await ctx.send(embed=embed)
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def annuncio(ctx, *, message):
    embed = discord.Embed(title="📢 Annuncio", description=message, color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)
    await ctx.message.delete()
@bot.event
async def on_message_delete(message):
    embed = discord.Embed(title="Messaggio eliminato", description=f"Autore: {message.author.mention}\nContenuto: {message.content}", color=discord.Color.red())
    embed.set_footer(text=FOOTER_TEXT)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    embed = discord.Embed(title="Messaggio modificato", description=f"Autore: {before.author.mention}\nMessaggio prima: {before.content}\nMessaggio dopo: {after.content}", color=discord.Color.orange())
    embed.set_footer(text=FOOTER_TEXT)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    if before.nick != after.nick:
        embed = discord.Embed(title="Nickname cambiato", description=f"Utente: {before.mention}\nNickname prima: {before.nick}\nNickname dopo: {after.nick}", color=discord.Color.orange())
        embed.set_footer(text=FOOTER_TEXT)
        channel = bot.get_channel(LOG_CHANNEL_ID)
        await channel.send(embed=embed)
    if before.roles != after.roles:
        if len(before.roles) < len(after.roles):
            for role in after.roles:
                if role not in before.roles:
                    embed = discord.Embed(title="Ruolo aggiunto", description=f"Utente: {before.mention}\nRuolo: {role.mention}", color=discord.Color.green())
                    embed.set_footer(text=FOOTER_TEXT)
                    channel = bot.get_channel(LOG_CHANNEL_ID)
                    await channel.send(embed=embed)
        else:
            for role in before.roles:
                if role not in after.roles:
                    embed = discord.Embed(title="Ruolo rimosso", description=f"Utente: {before.mention}\nRuolo: {role.mention}", color=discord.Color.red())
                    embed.set_footer(text=FOOTER_TEXT)
                    channel = bot.get_channel(LOG_CHANNEL_ID)
                    await channel.send(embed=embed)

@bot.event
async def on_guild_channel_create(channel):
    embed = discord.Embed(title="Canale creato", description=f"Nome: {channel.name}\nTipo: {channel.type}", color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_delete(channel):
    embed = discord.Embed(title="Canale eliminato", description=f"Nome: {channel.name}\nTipo: {channel.type}", color=discord.Color.red())
    embed.set_footer(text=FOOTER_TEXT)
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_update(before, after):
    if before.name != after.name:
        embed = discord.Embed(title="Nome canale modificato", description=f"Nome prima: {before.name}\nNome dopo: {after.name}", color=discord.Color.orange())
        embed.set_footer(text=FOOTER_TEXT)
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        await log_channel.send(embed=embed)
    if before.permissions != after.permissions:
        embed = discord.Embed(title="Permessi canale modificati", description=f"Canale: {before.name}", color=discord.Color.orange())
        embed.set_footer(text=FOOTER_TEXT)
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        await log_channel.send(embed=embed)
async def on_guild_emojis_update(guild, before, after):
    if before != after:
        embed = discord.Embed(title="Emoji aggiunta/rimossa", description=f"Emoji prima: {before}\nEmoji dopo: {after}", color=discord.Color.orange())
        channel = bot.get_channel(LOG_CHANNEL_ID)
        await channel.send(embed=embed)
async def on_guild_emojis_update(guild, before, after):
    if before != after:
        embed = discord.Embed(title="Emoji aggiunta/rimossa", description=f"Emoji prima: {before}\nEmoji dopo: {after}", color=discord.Color.orange())
        channel = bot.get_channel(LOG_CHANNEL_ID)
        await channel.send(embed=embed)
@bot.event
async def on_member_ban(guild, user):
    embed = discord.Embed(title="Utente bannato", description=f"Utente: {user.mention}", color=discord.Color.red())
    embed.set_footer(text=FOOTER_TEXT)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(embed=embed)
    embed.set_footer(text=FOOTER_TEXT)
@bot.event
async def on_member_unban(guild, user):
    embed = discord.Embed(title="Utente sbannato", description=f"Utente: {user.mention}", color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(embed=embed)
    embed = discord.Embed(title="Utente sbannato", description=f"Utente: {user.mention}", color=discord.Color.green())
@bot.event
async def on_member_timeout(member, timeout):
    embed = discord.Embed(title="Utente timeout", description=f"Utente: {member.mention}", color=discord.Color.red())
@bot.event
async def on_member_timeout(member, timeout):
    embed = discord.Embed(title="Utente timeout", description=f"Utente: {member.mention}", color=discord.Color.red())
    embed.set_footer(text=FOOTER_TEXT)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(embed=embed)

@bot.event
async def on_member_untimeout(member, timeout):
    embed = discord.Embed(title="Utente untimeout", description=f"Utente: {member.mention}", color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(embed=embed)

@bot.event
async def on_member_role_add(member, role):
    embed = discord.Embed(title="Ruolo aggiunto", description=f"Utente: {member.mention}\nRuolo: {role.mention}", color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(embed=embed)

@bot.event
async def on_member_role_remove(member, role):
    embed = discord.Embed(title="Ruolo rimosso", description=f"Utente: {member.mention}\nRuolo: {role.mention}", color=discord.Color.red())
    embed.set_footer(text=FOOTER_TEXT)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(embed=embed)

#FINE COMANDI DI LOG

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Errore", description="Comando non trovato.", color=discord.Color.red())
        embed.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=embed)

#COMANDO PER CAMBIARE LO STATO DEL BOT
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def status(ctx, *, status):
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(status))
    embed = discord.Embed(title="Stato cambiato", description=f"Nuovo stato: {status}", color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

#COMANDO SAY
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def say(ctx, *, message):
    await ctx.send(message)
    await ctx.message.delete()

#COMANDO PER INVIARE UN MESSAGGIO DI TEST NELLA CONSOLE
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def console(ctx):
    print("Test effettuato con successo!")
    embed = discord.Embed(title="Console", description="Messaggio effettuato con successo!", color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

#COMANDO PER IMPOSTARE LO STATO DEL BOT
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def setstatus(ctx, status: str):
    statuses = {
        "online": discord.Status.online,
        "offline": discord.Status.offline,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd
    }
    if status.lower() in statuses:
        await bot.change_presence(status=statuses[status.lower()])
        embed = discord.Embed(title="Stato cambiato", description=f"Nuovo stato: {status}", color=discord.Color.green())
    else:
        embed = discord.Embed(title="Errore", description="Stato non valido. Usa uno di questi: online, offline, idle, dnd.", color=discord.Color.red())
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

#COMANDO PER OTTENERE GLI STATI DISPONIBILI DEL BOT
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def getstatuses(ctx):
    statuses = ["online", "offline", "idle", "dnd"]
    embed = discord.Embed(title="Stati disponibili", description=", ".join(statuses), color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

#COMANDO TO MOD PER INVIARE UN MESSAGGIO IN MODALITA ANONIMA A UN CANALE SPECIFICO
@bot.command()
async def to_mod(ctx, *, message):
    embed = discord.Embed(title="Nuovo messaggio", description=message, color=discord.Color.green())
    embed.set_footer(text=FOOTER_TEXT)
    channel = bot.get_channel(TO_MOD_CHANNEL_ID)
    await channel.send(embed=embed)
    await ctx.message.delete()

#COMANDO PER OTTENERE LA SKIN DI UN GIOCATORE MINECRAFT
@bot.command()
async def skin(ctx, username):
    embed = discord.Embed(title=f"Skin di {username}", color=discord.Color.green())
    embed.set_image(url=f"https://minotar.net/armor/body/{username}/100.png")
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)


#SASSO CARTA FORBICE
@bot.command()
async def rps(ctx, choice):
    choices = ["sasso", "carta", "forbice"]
    if choice.lower() in choices:
        bot_choice = random.choice(choices)
        if choice.lower() == bot_choice:
            embed = discord.Embed(title="Pareggio", description=f"Tu hai scelto {choice}, io ho scelto {bot_choice}", color=discord.Color.orange())
        elif choice.lower() == "sasso" and bot_choice == "forbice":
            embed = discord.Embed(title="Hai vinto!", description=f"Tu hai scelto {choice}, io ho scelto {bot_choice}", color=discord.Color.green())
        elif choice.lower() == "carta" and bot_choice == "sasso":
            embed = discord.Embed(title="Hai vinto!", description=f"Tu hai scelto {choice}, io ho scelto {bot_choice}", color=discord.Color.green())
        elif choice.lower() == "forbice" and bot_choice == "carta":
            embed = discord.Embed(title="Hai vinto!", description=f"Tu hai scelto {choice}, io ho scelto {bot_choice}", color=discord.Color.green())
        else:
            embed = discord.Embed(title="Hai perso!", description=f"Tu hai scelto {choice}, io ho scelto {bot_choice}", color=discord.Color.red())
    else:
        embed = discord.Embed(title="Errore", description="Scelta non valida. Usa una di queste: sasso, carta, forbice.", color=discord.Color.red())
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

#COMANDO PER IMPOSTARE LA FOTO DEL PROFILO DEL BOT
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def setavatar(ctx, url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    await bot.user.edit(avatar=data)
                    embed = discord.Embed(title="Avatar cambiato", description="Nuovo avatar impostato con successo!", color=discord.Color.green())
                else:
                    embed = discord.Embed(title="Errore", description="Errore durante il download dell'immagine.", color=discord.Color.red())
    except aiohttp.ClientError as e:
        embed = discord.Embed(title="Errore", description=f"Errore durante il download dell'immagine: {e}", color=discord.Color.red())
    except discord.HTTPException as e:
        embed = discord.Embed(title="Errore", description=f"Errore durante l'aggiornamento dell'avatar: {e}", color=discord.Color.red())
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

#COMANDO PER FAR ENTRARE IL BOT NEL CANALE VOCALE DELL'UTENTE
@bot.command()
async def join(ctx):
    """Unisciti al canale vocale dell'utente"""
    try:
        if ctx.author.voice:  # Controlla se l'utente è in un canale vocale
            channel = ctx.author.voice.channel
            if ctx.voice_client:  # Controlla se il bot è già connesso a un canale
                await ctx.voice_client.move_to(channel)
            else:
                await channel.connect()
            await ctx.send(f"✅ Sono entrato nel canale vocale: {channel.mention}")
        else:
            await ctx.send("❌ Non sei in un canale vocale! Unisciti prima a un canale.")
    except discord.ClientException as e:
        await ctx.send(f"❌ Errore: {e}")
    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")

#COMANDO PER FAR USCIRE IL BOT DAL CANALE VOCALE
@bot.command()
async def leave(ctx):
    """Lascia il canale vocale"""
    try:
        if ctx.voice_client:  # Controlla se il bot è in un canale vocale
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Ho lasciato il canale vocale!")
        else:
            await ctx.send("❌ Non sono in nessun canale vocale!")
    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")

#COMANDO PER RIPRODURRE UNA CANZONE DA SPOTIFY
@bot.command()
async def play(ctx, *, query):
    """Riproduci una canzone cercata su Spotify e aggiungila alla coda"""
    try:
        if not ctx.voice_client:
            await ctx.invoke(join)
        results = sp.search(q=query, type="track", limit=1)
        if not results['tracks']['items']:
            await ctx.send("❌ Nessuna canzone trovata su Spotify!")
            return

        track = results['tracks']['items'][0]
        track_url = track['external_urls']['spotify']
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        await ctx.send(f"🎶 Aggiunto alla coda: {track_name} di {artist_name} ({track_url})")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            search_query = f"{track_name} {artist_name} audio"
            info = ydl.extract_info(f"ytsearch:{search_query}", download=False)['entries'][0]
            url = info['url']
            song_title = info['title']
        if not hasattr(ctx.voice_client, 'queue'):
            ctx.voice_client.queue = []

        ctx.voice_client.queue.append({'title': song_title, 'url': url})

        if not ctx.voice_client.is_playing():
            async def play_next():
                if ctx.voice_client.queue:
                    next_song = ctx.voice_client.queue.pop(0)
                    song_url = next_song['url']
                    ctx.voice_client.play(discord.FFmpegPCMAudio(song_url), after=lambda e: bot.loop.create_task(play_next()))

            await play_next()

    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")

#COMANDO PER SALTARE LA CANZONE CORRENTE
@bot.command()
async def skip(ctx):
    """Salta la canzone corrente"""
    try:
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ Canzone saltata!")
        else:
            await ctx.send("❌ Non sto riproducendo nulla!")
    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")

#COMANDO PER MOSTRARE LA CODA DELLE CANZONI
@bot.command()
async def queue(ctx):
    """Mostra la coda delle canzoni"""
    try:
        if ctx.voice_client and ctx.voice_client.queue:
            queue = "\n".join([f"{i + 1}. {song['title']}" for i, song in enumerate(ctx.voice_client.queue)])
            embed = discord.Embed(title="Coda delle canzoni", description=queue, color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Non ci sono canzoni in coda!")
    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")


#COMANDO PER PULIRE LA CODA DELLE CANZONI
@bot.command()
async def clear(ctx):
    """Pulisci la coda delle canzoni"""
    try:
        if ctx.voice_client and ctx.voice_client.queue:
            ctx.voice_client.queue.clear()
            await ctx.send("🧹 Coda delle canzoni pulita!")
        else:
            await ctx.send("❌ Non ci sono canzoni in coda!")
    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")

#COMANDO PER METTERE IN PAUSA LA CANZONE CORRENTE
@bot.command()
async def pause(ctx):
    """Metti in pausa la canzone corrente"""
    try:
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Canzone in pausa!")
        else:
            await ctx.send("❌ Non sto riproducendo nulla!")
    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")

#COMANDO PER RIPRENDERE LA CANZONE IN PAUSA
@bot.command()
async def resume(ctx):
    """Riprendi la canzone in pausa"""
    try:
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Canzone ripresa!")
        else:
            await ctx.send("❌ Non sto riproducendo nulla o la canzone non è in pausa!")
    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")

#COMANDO PER STOPPARE LA CANZONE CORRENTE
@bot.command()
async def stop(ctx):
    """Ferma la canzone corrente"""
    try:
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏹️ Canzone fermata!")
        else:
            await ctx.send("❌ Non sto riproducendo nulla!")
    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")

#COMANDO PER IMPOSTARE IL VOLUME DEL BOT
@bot.command(name='setvolume')
async def setvolume(ctx, volume: int):
    """Imposta il volume del bot (da 1 a 100)"""
    try:
        if ctx.voice_client:
            if 1 <= volume <= 100:
                volume_normalized = volume / 100.0
                if ctx.voice_client.is_playing():
                    if not isinstance(ctx.voice_client.source, discord.PCMVolumeTransformer):
                        ctx.voice_client.source = discord.PCMVolumeTransformer(ctx.voice_client.source)
                    ctx.voice_client.source.volume = volume_normalized
                    await ctx.send(f"🔊 Volume impostato a {volume}%")
                else:
                    await ctx.send("❌ Nessuna canzone è attualmente in riproduzione!")
            else:
                await ctx.send("❌ Il volume deve essere un valore tra 1 e 100!")
        else:
            await ctx.send("❌ Non sono connesso a un canale vocale!")
    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")

#COMANDO !MUSIC PER MOSTRARE I COMANDI PER LA MUSICA
@bot.command()
async def music(ctx):
    embed = discord.Embed(title="Comandi per la musica", color=discord.Color.green())
    embed.add_field(name="!join", value="Unisciti al canale vocale dell'utente", inline=False)
    embed.add_field(name="!leave", value="Lascia il canale vocale", inline=False)
    embed.add_field(name="!play <query>", value="Riproduci una canzone cercata su Spotify e aggiungila alla coda", inline=False)
    embed.add_field(name="!skip", value="Salta la canzone corrente", inline=False)
    embed.add_field(name="!queue", value="Mostra la coda delle canzoni", inline=False)
    embed.add_field(name="!clear", value="Pulisci la coda delle canzoni", inline=False)
    embed.add_field(name="!pause", value="Metti in pausa la canzone corrente", inline=False)
    embed.add_field(name="!resume", value="Riprendi la canzone in pausa", inline=False)
    embed.add_field(name="!stop", value="Ferma la canzone corrente", inline=False)
    embed.add_field(name="!setvolume <volume>", value="Imposta il volume del bot (da 1 a 100)", inline=False)
    embed.add_field(name="!song <query>", value="Mostra le informazioni di una canzone su Spotify", inline=False)
    embed.add_field(name="!localplay <query>", value="Riproduci una canzone locale", inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

#COMANDO !ADMIN PER VEDERE I COMANDI PER GLI AMMINISTRATORI
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def admin_help(ctx):
    embed = discord.Embed(title="Comandi per gli amministratori", color=discord.Color.green())
    embed.add_field(name="!ping", value="Mostra la latenza del bot", inline=False)
    embed.add_field(name="!pex <member> <role>", value="Aggiunge un ruolo a un membro", inline=False)
    embed.add_field(name="!depex <member> <role>", value="Rimuove un ruolo a un membro", inline=False)
    embed.add_field(name="!annuncio <message>", value="Invia un annuncio", inline=False)
    embed.add_field(name="!status <status>", value="Cambia lo stato del bot", inline=False)
    embed.add_field(name="!say <message>", value="Fai dire al bot un messaggio", inline=False)
    embed.add_field(name="!console", value="Invia un messaggio di test nella console", inline=False)
    embed.add_field(name="!getstatus", value="Mostra lo stato attuale del bot", inline=False)
    embed.add_field(name="!setstatus <status>", value="Imposta lo stato del bot", inline=False)
    embed.add_field(name="!getstatuses", value="Mostra gli stati disponibili del bot", inline=False)
    embed.add_field(name="!to_mod <message>", value="Invia un messaggio in modalità anonima al canale dei moderatori", inline=False)
    embed.add_field(name="!userinfo <member>", value="Mostra le informazioni di un utente", inline=False)
    embed.add_field(name="!serverinfo", value="Mostra le informazioni del server", inline=False)
    embed.add_field(name="!botinfo", value="Mostra le informazioni del bot", inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)


#COMANDO PER VEDERE LE INFORMAZIONI DI UNA CANZONE
@bot.command()
async def song(ctx, *, query):
    """Mostra le informazioni di una canzone su Spotify"""
    try:
        results = sp.search(q=query, type="track", limit=1)
        if not results['tracks']['items']:
            await ctx.send("❌ Nessuna canzone trovata su Spotify!")
            return

        track = results['tracks']['items'][0]
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        album_name = track['album']['name']
        album_image = track['album']['images'][0]['url']
        track_url = track['external_urls']['spotify']

        embed = discord.Embed(title=track_name, description=f"Artista: {artist_name}\nAlbum: {album_name}\n[Ascolta su Spotify]({track_url})", color=discord.Color.green())
        embed.set_image(url=album_image)
        embed.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")

#COMANDO PER VEDERE LE INFORMAZIONI DI UN UTENTE
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def userinfo(ctx, member: discord.Member):
    """Mostra le informazioni di un utente"""
    embed = discord.Embed(title=f"Informazioni di {member}", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Nickname", value=member.display_name, inline=False)
    embed.add_field(name="Creato il", value=member.created_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=False)
    embed.add_field(name="Entrato il", value=member.joined_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=False)
    embed.add_field(name="Ruoli", value=", ".join([role.mention for role in member.roles if role.name != "@everyone"]), inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

#COMANDO PER VEDERE LE INFORMAZIONI DEL SERVER
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def serverinfo(ctx):
    """Mostra le informazioni del server"""
    embed = discord.Embed(title=f"Informazioni di {ctx.guild.name}", color=discord.Color.green())
    embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.add_field(name="ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Proprietario", value=ctx.guild.owner.mention, inline=False)
    embed.add_field(name="Creato il", value=ctx.guild.created_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=False)
    embed.add_field(name="Membri", value=ctx.guild.member_count, inline=False)
    embed.add_field(name="Canali di testo", value=len(ctx.guild.text_channels), inline=False)
    embed.add_field(name="Canali vocali", value=len(ctx.guild.voice_channels), inline=False)
    embed.add_field(name="Ruoli", value=len(ctx.guild.roles), inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

#COMANDO PER VEDERE LE INFORMAZIONI DEL BOT
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def botinfo(ctx):
    """Mostra le informazioni del bot"""
    embed = discord.Embed(title=f"Informazioni di {bot.user.name}", color=discord.Color.green())
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.add_field(name="ID", value=bot.user.id, inline=False)
    embed.add_field(name="Creato il", value=bot.user.created_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=False)
    embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=False)
    embed.add_field(name="Server connessi", value=len(bot.guilds), inline=False)
    embed.add_field(name="Comandi", value=len(bot.commands), inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

#COMANDO !localplay per riprodurre un file audio locale
@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def localplay(ctx, *, filename):
    """Riproduci un file audio locale"""
    try:
        if not ctx.voice_client:
            await ctx.invoke(join)
        if not os.path.isfile(filename):
            await ctx.send("❌ File non trovato!")
            return

        if not hasattr(ctx.voice_client, 'queue'):
            ctx.voice_client.queue = []

        ctx.voice_client.queue.append({'title': filename, 'url': filename})

        if not ctx.voice_client.is_playing():
            async def play_next():
                if ctx.voice_client.queue:
                    next_song = ctx.voice_client.queue.pop(0)
                    song_url = next_song['url']
                    ctx.voice_client.play(discord.FFmpegPCMAudio(song_url), after=lambda e: bot.loop.create_task(play_next()))

            await play_next()
    except Exception as e:
        await ctx.send(f"⚠️ Qualcosa è andato storto: {e}")








    







bot.run('BOT_TOKEN')
    