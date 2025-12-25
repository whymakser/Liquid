import asyncio
from pyrogram.enums import ParseMode

# meta developer: @notdekma
# meta description: Module for massive delate messages
# meta version: 1.0

async def del_cmd(c, m, a):
    """Default Delete"""
    if m.reply_to_message:
        await m.reply_to_message.delete()
    await m.delete()

async def purge_cmd(c, m, a):
    """Default Purge"""
    if not m.reply_to_message:
        return await m.edit("<blockquote><emoji id=5775887550262546277>❗️</emoji> <b>Needed replay</b></blockquote>")
    
    chat_id = m.chat.id
    start_id = m.reply_to_message.id
    end_id = m.id
    
    message_ids = list(range(start_id, end_id + 1))
    
    for i in range(0, len(message_ids), 100):
        await c.delete_messages(chat_id, message_ids[i:i+100])
        await asyncio.sleep(0.3)

async def spurge_cmd(c, m, a):
    """Silent Purge"""
    if not m.reply_to_message:
        return await m.delete()
        
    chat_id = m.chat.id
    message_ids = list(range(m.reply_to_message.id, m.id + 1))
    
    for i in range(0, len(message_ids), 100):
        await c.delete_messages(chat_id, message_ids[i:i+100])
        await asyncio.sleep(0.2)

def register(app, commands, module_name):
    commands["del"] = {"func": del_cmd, "module": module_name}
    commands["purge"] = {"func": purge_cmd, "module": module_name}
    commands["spurge"] = {"func": spurge_cmd, "module": module_name}
