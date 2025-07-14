#Copyright @ISmartCoder
#Updates Channel https://t.me/TheSmartProgrammers
import logging
from pyrogram import Client, filters
from pyrogram.types import (
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from pyrogram.enums import ParseMode
from utils import LOGGER
from core import banned_users
from config import OWNER_ID, IGNORE, BAN_REPLY

FORWARDED_MAP = {}

def setup_listen_handler(snigdha: Client):
    @snigdha.on_message(filters.private & filters.incoming & ~filters.command(["stats", "send"]))
    async def forward_private_message(client: Client, message: Message):
        user_id = message.from_user.id
        text = message.text or message.caption or "<non-text message>"
        LOGGER.info(f"Message received from {user_id}: {text}")

        if text == "/start":
            await banned_users.add_user(user_id)
            user_name = message.from_user.first_name or "User"
            if message.from_user.last_name:
                user_name += f" {message.from_user.last_name}"

            welcome_msg = (
                f"**Hi {user_name}! Welcome To This Bot**\n"
                f"**━━━━━━━━━━━━━━━━━━━━━━**\n"
                f"**SmartGram: The ultimate toolkit on Telegram, offering best feedback bot features including private users.**\n"
                f"**━━━━━━━━━━━━━━━━━━━━━━**\n"
                f"**Don't forget to [Join Here](http://t.me/TheSmartDev) for updates!**"
            )

            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Updates Channel", url="https://t.me/TheSmartProgrammers")
            ]])

            await client.send_message(
                user_id,
                welcome_msg.strip(), 
                reply_markup=keyboard, 
                parse_mode=ParseMode.MARKDOWN, 
                disable_web_page_preview=True
            )
            LOGGER.info(f"Sent welcome message to user {user_id}")
            return

        if await banned_users.is_banned(user_id):
            await client.send_message(user_id, f"**{BAN_REPLY}**", parse_mode=ParseMode.MARKDOWN)
            LOGGER.info(f"Ignored banned user {user_id}")
            return

        if user_id in IGNORE:
            LOGGER.info(f"Ignored user {user_id}")
            return

        if user_id == OWNER_ID:
            replied = message.reply_to_message.id if message.reply_to_message else None
            target_user_id = FORWARDED_MAP.get(replied) if replied else None
            if target_user_id is None and message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == OWNER_ID:
                target_user_id = OWNER_ID

            if message.text and message.text.startswith('/ban'):
                parts = message.text.split()
                if len(parts) > 1:
                    try:
                        target_user_id = int(parts[1])
                    except ValueError:
                        await client.send_message(OWNER_ID, "**Invalid user ID.**", parse_mode=ParseMode.MARKDOWN)
                        return
                elif target_user_id is None:
                    await client.send_message(OWNER_ID, "**Please reply to a forwarded message or provide a user ID.**", parse_mode=ParseMode.MARKDOWN)
                    return

                if target_user_id == OWNER_ID:
                    await client.send_message(OWNER_ID, "**You Can't Ban Bot Owner**", parse_mode=ParseMode.MARKDOWN)
                    return

                await banned_users.ban_user(target_user_id)
                await client.send_message(OWNER_ID, f"**User {target_user_id} has been banned.**", parse_mode=ParseMode.MARKDOWN)
                try:
                    await client.send_message(target_user_id, f"**{BAN_REPLY}**", parse_mode=ParseMode.MARKDOWN)
                    LOGGER.info(f"Sent ban notification to user {target_user_id}")
                except Exception as e:
                    LOGGER.error(f"Failed to notify user {target_user_id} of ban: {e}")
                return

            elif message.text and message.text.startswith('/unban'):
                parts = message.text.split()
                if len(parts) > 1:
                    try:
                        target_user_id = int(parts[1])
                    except ValueError:
                        await client.send_message(OWNER_ID, "**Invalid user ID.**", parse_mode=ParseMode.MARKDOWN)
                        return
                elif target_user_id is None:
                    await client.send_message(OWNER_ID, "**Please reply to a forwarded message or provide a user ID.**", parse_mode=ParseMode.MARKDOWN)
                    return

                if target_user_id == OWNER_ID:
                    await client.send_message(OWNER_ID, "**Lol Why To Unban He Is Already Bot Owner**", parse_mode=ParseMode.MARKDOWN)
                    return

                await banned_users.unban_user(target_user_id)
                await client.send_message(OWNER_ID, f"**User {target_user_id} has been unbanned.**", parse_mode=ParseMode.MARKDOWN)
                try:
                    await client.send_message(target_user_id, "**Good News, You're Unbanned Now**", parse_mode=ParseMode.MARKDOWN)
                    LOGGER.info(f"Sent unban notification to user {target_user_id}")
                except Exception as e:
                    LOGGER.error(f"Failed to notify user {target_user_id} of unban: {e}")
                return

            elif target_user_id:
                try:
                    await message.copy(target_user_id)
                    LOGGER.info(f"Sent owner reply to user {target_user_id}")
                except Exception as e:
                    LOGGER.error(f"Error sending reply to user {target_user_id}: {e}")
                    await client.send_message(OWNER_ID, "**❌ Sorry, action not allowed.**", parse_mode=ParseMode.MARKDOWN)
                return

        try:
            fwd = await message.forward(OWNER_ID, disable_notification=True)
            FORWARDED_MAP[fwd.id] = user_id
            LOGGER.info(f"✅ Forwarded to owner {OWNER_ID} from {user_id}")
            LOGGER.info(f"User ID: {user_id}, Message ID: {message.id}")
        except Exception as e:
            LOGGER.error(f"❌ Forwarding failed: {e}")
            await client.send_message(user_id, "**Sorry Failed To Send To Owner❌**", parse_mode=ParseMode.MARKDOWN)

    LOGGER.info("Listen handlers setup successfully! ")