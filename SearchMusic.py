import asyncio
from pyrogram import Client
from pyrogram.enums import ParseMode

async def sm_cmd(client, message, args):
    if not args:
        return await message.edit("<emoji id=5775887550262546277>❗️</emoji> <b>Usage: .sm [query]</b>")

    query = " ".join(args)
    try:
        await message.edit(f"<blockquote><emoji id=5891211339170326418>⌛️</emoji> <b>Searching...</b></blockquote>")
        
        await client.send_message("lybot", query)
        await asyncio.sleep(2)
        
        async for msg in client.get_chat_history("lybot", limit=1):
            if msg.reply_markup:
                await msg.click(0)
                await asyncio.sleep(2)
            else:
                return await message.edit("<emoji id=5778527486270770928>❌</emoji> <b>Not found</b>")

        audio_msg = None
        async for m in client.get_chat_history("lybot", limit=3):
            if m.audio:
                audio_msg = m
                break

        if audio_msg:
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id="lybot",
                message_id=audio_msg.id,
                caption="",
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None
            )
            await message.delete()
        else:
            await message.edit("<emoji id=5778527486270770928>❌</emoji> <b>Audio not found</b>")
                
    except Exception as e:
        await message.edit(f"<emoji id=5778527486270770928>❌</emoji> <b>Error:</b> <code>{str(e)}</code>")

def register(app, commands, module_name):
    commands["sm"] = {"func": sm_cmd, "module": module_name}
