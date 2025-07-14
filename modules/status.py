#Copyright @ISmartCoder
#Updates Channel https://t.me/TheSmartProgrammers
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from utils import LOGGER
from core import banned_users
from config import OWNER_ID
from datetime import datetime

async def send_broadcast(client: Client, message: Message):
    users = await banned_users.get_all_users()
    total_chats = 0
    blocked_users = 0
    successful = 0

    for user in users:
        user_id = user["user_id"]
        total_chats += 1
        if user.get("banned", False):
            blocked_users += 1
            continue
        try:
            await client.forward_messages(user_id, OWNER_ID, message.id, disable_notification=True)
            successful += 1
        except Exception as e:
            LOGGER.error(f"Failed to send broadcast to {user_id}: {e}")
            blocked_users += 1

    return successful, blocked_users, total_chats

def setup_status_handler(snigdha: Client):
    @snigdha.on_message(filters.command("stats") & filters.user(OWNER_ID))
    async def stats_command(client: Client, message: Message):
        stats = await banned_users.get_stats()
        stats_message = (
            "**SmartGram Status Report**\n"
            "------------------------\n"
            "User Activity Overview:\n"
            f"- Last 24 Hours: {stats['day']} active users\n"
            f"- Last 7 Days: {stats['week']} active users\n"
            f"- Last 30 Days: {stats['month']} active users\n"
            f"- Last 365 Days: {stats['year']} active users\n"
            f"- Total Users: {stats['total']}\n"
            "------------------------\n"
            f"Total SmartGram Users: {stats['total']}"
        )
        await message.reply(stats_message, parse_mode=ParseMode.MARKDOWN)
        LOGGER.info("Stats command executed by owner")

    @snigdha.on_message(filters.command("send") & filters.user(OWNER_ID) & ~filters.reply)
    async def broadcast_no_reply(client: Client, message: Message):
        await message.reply("**Please reply to a message to broadcast**", parse_mode=ParseMode.MARKDOWN)
        LOGGER.info("Broadcast command used without reply by owner")

    @snigdha.on_message(filters.command("send") & filters.user(OWNER_ID) & filters.reply)
    async def broadcast_command(client: Client, message: Message):
        temp_msg = await message.reply("**Processing Broadcast to Users**", parse_mode=ParseMode.MARKDOWN)
        broadcast_msg = message.reply_to_message

        if not broadcast_msg:
            await temp_msg.edit("**Please reply to a message to broadcast**", parse_mode=ParseMode.MARKDOWN)
            return

        successful, blocked, total = await send_broadcast(client, broadcast_msg)
        result_msg = (
            "**Broadcast Summary**\n"
            "--------------------\n"
            f"- Messages Delivered: {successful} users\n"
            f"- Blocked Users: {blocked}\n"
            f"- Total Attempts: {total}\n"
            "--------------------\n"
            "Broadcast Completed"
        )
        await temp_msg.edit(result_msg, parse_mode=ParseMode.MARKDOWN)
        LOGGER.info(f"Broadcast completed: {successful} successful, {blocked} blocked, {total} total chats")

    LOGGER.info("Status handlers setup successfully! ")