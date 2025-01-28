
# Simple Discord Bot  

A simple yet powerful Discord bot designed to enhance your server experience with useful features, fun commands, and advanced Spotify integration.  

## Main Features  
- **Music:** Control Spotify playback and play local files.  
- **Moderation:** Essential tools to manage your server efficiently.  
- **Fun Commands:** Engage your members with games and interactive features.  
- **Logs and Automation:** Track events and automate common tasks.  

---

## Installation  

Before you start, make sure to install the following dependencies and tools:  

### 1. Install Python Libraries  

The bot requires some Python libraries to run properly. You can install them by running the following command in your terminal:  

```bash
pip install discord.py aiohttp spotipy yt-dlp python-dotenv
```

#### Libraries:  
- `discord.py`: The library for interacting with Discord’s API.  
- `aiohttp`: Used for asynchronous HTTP requests.  
- `spotipy`: The Spotify API wrapper to interact with Spotify for playing music.  
- `yt-dlp`: A tool to download and stream audio from YouTube (used for music playback).  
- `python-dotenv`: Used to load environment variables from a `.env` file.  

### 2. Install FFMpeg  

The bot uses **FFmpeg** to handle audio streaming and music playback. Follow these steps to install it:  

#### Windows:
1. Download FFmpeg from the official website: [FFmpeg Windows Builds](https://ffmpeg.org/download.html#build-windows).  
2. Extract the files and move them to a folder (e.g., `C:\ffmpeg`).  
3. Add the FFmpeg bin directory to your system’s PATH variable:
   - Right-click on "This PC" and select "Properties".  
   - Click "Advanced system settings", then click "Environment Variables".  
   - Under "System variables", find the "Path" variable, select it, and click "Edit".  
   - Add the path to the `bin` folder (e.g., `C:\ffmpeg\bin`) to the list, and click "OK".  

#### Linux (Ubuntu/Debian):  
Run the following command in your terminal to install FFmpeg:  
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS:  
Use Homebrew to install FFmpeg:  
```bash
brew install ffmpeg
```

Once FFmpeg is installed, you can verify the installation by running:  
```bash
ffmpeg -version
```

If FFmpeg is properly installed, it will show you the version information.

---

### 3. Set Up the `.env` File  

The bot uses environment variables to store sensitive information like your bot token and Spotify credentials. Create a `.env` file in the root of your project folder and add the following lines:  

```env
TOKEN=your_discord_bot_token
STAFF_ROLE_ID=your_staff_role_id
LOG_CHANNEL_ID=your_log_channel_id
FOOTER_TEXT=your_footer_text
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

Replace the placeholder values with your own:

- `TOKEN`: Your Discord bot token, which you can get by creating a bot on the [Discord Developer Portal](https://discord.com/developers/applications).  
- `STAFF_ROLE_ID`: The role ID for your staff members.  
- `LOG_CHANNEL_ID`: The ID of the channel where logs will be sent.  
- `FOOTER_TEXT`: The custom footer text for the bot's embeds.  
- `SPOTIFY_CLIENT_ID`: Your Spotify Client ID (get it by creating an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)).  
- `SPOTIFY_CLIENT_SECRET`: Your Spotify Client Secret (found on the same dashboard).

---

### 4. Run the Bot  

After installing the dependencies and configuring your `.env` file, you can start the bot by running the following command in your terminal:  

```bash
python main.py
```

The bot should now be up and running, ready to use on your Discord server!  

---

## Available Commands  

### 🎵 **Music Commands**  
Commands to manage music playback:  
- `!join` - Join the user’s voice channel.  
- `!leave` - Leave the current voice channel.  
- `!play <query>` - Play a song searched on Spotify and add it to the queue.  
- `!skip` - Skip the current song.  
- `!queue` - Show the current song queue.  
- `!clear` - Clear the song queue.  
- `!pause` - Pause the current song.  
- `!resume` - Resume the paused song.  
- `!stop` - Stop the current song.  
- `!setvolume <volume>` - Adjust the bot's volume (from 1 to 100).  
- `!song <query>` - Display information about a song on Spotify.  
- `!localplay <query>` - Play a local song.  

> **Note:** To use the `!localplay` command, place the song file in the same directory as the bot's `main.py` file and restart the bot.  

---

### 🛠️ **Admin Commands**  
Commands to help manage and customize your server:  
- `!ping` - Display the bot's latency.  
- `!pex <member> <role>` - Add a role to a member.  
- `!depex <member> <role>` - Remove a role from a member.  
- `!annuncio <message>` - Send an announcement.  
- `!status <status>` - Change the bot's status.  
- `!say <message>` - Make the bot say a message.  
- `!console` - Send a test message to the console.  
- `!getstatus` - Show the bot's current status.  
- `!setstatus <status>` - Set the bot's status.  
- `!getstatuses` - Show all available bot statuses.  
- `!to_mod <message>` - Send an anonymous message to the moderators' channel.  
- `!userinfo <member>` - Display information about a user.  
- `!serverinfo` - Display server information.  
- `!botinfo` - Display bot information.  

---

### 🎮 **Fun Commands**  
Commands to entertain and engage your server members:  
- `!skin` - Display a Minecraft player's skin.  
- `!rps` - Play Rock, Paper, Scissors.  
- `!music` - Show the list of music commands.  

---

## Contributing  
Contributions are welcome! Fork the repository, create a feature branch, and submit a pull request.  


---  
Made with ❤️ by [Gecky](https://www.geckydev.me)    