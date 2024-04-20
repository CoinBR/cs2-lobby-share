import discord
import asyncio

intents = discord.Intents.default()
intents.messages = True

async def send_msg_async(token, channel_id, msg):
    client = discord.Client(intents=intents)

    async def on_ready():
        print("Discord Bot is ready.")
        channel = client.get_channel(int(channel_id))  # Convert to int to avoid issues
        if channel is None:
            print(f"Channel with ID {channel_id} not found.")
        else: 
            await channel.send(msg)
        await client.close()
        
    client.event(on_ready)
    
    try:
        await client.start(token)
    finally:
        await client.close()  

def send_msg(token, channel_id, msg):
    asyncio.run(send_msg_async(token, channel_id, msg))
