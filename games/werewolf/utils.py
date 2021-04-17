import time
import asyncio
async def establish_chat(client,players, description, chat_time=60):
    start = time.time()
    for player in players:
        await player.get_discord_member().send('**' + description + '**')
    while time.time() - start <= chat_time:
        def check(msg):
            for player in players:
                if player.get_discord_member() == msg.author:
                    return True
            return False

        try:
            timeout = chat_time - (time.time() - start)
            message = await client.wait_for('message', timeout=timeout, check=check)
        except asyncio.TimeoutError:
            pass
        else:
            for player in players:
                if player.get_discord_member() != message.author:
                    await player.get_discord_member().send(f'**{message.author.name}:** {message.content}')
    for player in players:
        await player.get_discord_member().send(f'**O chat acabou**')