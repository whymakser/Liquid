import os
from pyrogram import Client
from pyrogram.enums import ParseMode

async def sm_cmd(client, message, args):
    if not args:
        return await message.edit("<b>Введите название музыки.</b>")

    query = " ".join(args)
    try:
        await message.edit(f"<b>🔍 Ищу:</b> <code>{query}</code>")
        
        results = await client.get_inline_bot_results("lybot", query)
        
        if not results or not results.results:
            return await message.edit(f"<b>❌ Музыка <code>{query}</code> не найдена.</b>")

        await client.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=results.query_id,
            result_id=results.results[0].id,
            reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None
        )
        
        await message.delete()
        
    except Exception as e:
        await message.edit(f"<b>❌ Ошибка:</b> <code>{str(e)}</code>")

def register(app, commands, module_name):
    commands["sm"] = {"func": sm_cmd, "module": module_name}
