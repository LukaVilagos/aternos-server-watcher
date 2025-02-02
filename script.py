import asyncio
import os

import discord
from dotenv import load_dotenv
from mcstatus import JavaServer

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_IP = os.getenv("SERVER_IP")
PORT = int(os.getenv("SERVER_PORT"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_status = None  # Track the last known status

async def check_server():
    global last_status
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    
    while not client.is_closed():
        try:
            server = JavaServer.lookup(f"{SERVER_IP}:{PORT}")
            status = server.status()
            is_online = True
        except:
            is_online = False

        if last_status is None:
            last_status = is_online  # Initialize first status

        if is_online and last_status is False:
            await channel.send("🔵 The Minecraft server is **ONLINE**! Join now! 🎮")
        elif not is_online and last_status is True:
            await channel.send("🔴 The Minecraft server is **OFFLINE**! 🚫")

        last_status = is_online
        await asyncio.sleep(30)  # Check every 30 seconds

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(check_server())

client.run(TOKEN)
