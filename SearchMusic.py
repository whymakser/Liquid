import os
from pyrogram import Client
from pyrogram.enums import ParseMode

async def sm_cmd(client, message, args):
    if not args:
        return await message.edit("<emoji id=5775887550262546277>❗️</emoji> <b>Usage: .sm [query]</b>")

    query = " ".join(args)
    try:
        await message.edit(f"<blockquote><emoji id=5891211339170326418>⌛️</emoji> <b>Searching for:</b> <code>{query}</code></blockquote>")
        
        results = await client.get_inline_bot_results("lybot", query)
        
        if not results or not results.results:
            return await message.edit(f"<emoji id=5778527486270770928>❌</emoji> <b>No results found for</b> <code>{query}</code>")

        await client.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=results.query_id,
            result_id=results.results[0].id,
            reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None
        )
        
        await message.delete()
        
    except Exception as e:
        await message.edit(f"<emoji id=5778527486270770928>❌</emoji> <b>Error:</b> <code>{str(e)}</code>")

def register(app, commands, module_name):
    commands["sm"] = {"func": sm_cmd, "module": module_name}
