import os
import requests
from pyrogram import Client
from pyrogram.enums import ParseMode

async def sm_cmd(client, message, args):
    if not args:
        return await message.edit("<emoji id=5775887550262546277>❗️</emoji> <b>Usage: .sm [query]</b>")

    query = " ".join(args)
    temp_file = f"temp_{message.id}.mp3"
    
    try:
        await message.edit(f"<blockquote><emoji id=5891211339170326418>⌛️</emoji> <b>Searching...</b></blockquote>")
        
        results = await client.get_inline_bot_results("lybot", query)
        
        if not results or not results.results:
            return await message.edit(f"<emoji id=5778527486270770928>❌</emoji> <b>Not found</b>")

        result = results.results[0]
        audio_url = None
        if hasattr(result, "content") and hasattr(result.content, "url"):
            audio_url = result.content.url
        elif hasattr(result, "send_message"):
            audio_url = result.send_message.text

        if not audio_url:
            return await message.edit(f"<emoji id=5778527486270770928>❌</emoji> <b>Direct link not found</b>")

        await message.edit(f"<blockquote><emoji id=5899757765743615694>⬇️</emoji> <b>Downloading...</b></blockquote>")
        response = requests.get(audio_url, stream=True)
        with open(temp_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        await client.send_audio(
            chat_id=message.chat.id,
            audio=temp_file,
            reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None
        )
        
        await message.delete()

    except Exception as e:
        await message.edit(f"<emoji id=5778527486270770928>❌</emoji> <b>Error:</b> <code>{str(e)}</code>")
    
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def register(app, commands, module_name):
    commands["sm"] = {"func": sm_cmd, "module": module_name}
