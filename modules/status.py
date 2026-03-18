from telethon import events, Button
from utils import LOGGER
from core import banned_users
from config import OWNER_ID
from modules.group import GROUP_CHAT_IDS


async def send_broadcast(Irene, broadcast_msg):
    users = await banned_users.get_all_users()
    groups = await banned_users.get_all_groups()

    total_users = 0
    blocked_users = 0
    successful_users = 0
    total_groups = 0
    successful_groups = 0
    failed_groups = 0

    for user in users:
        user_id = user["user_id"]
        total_users += 1
        if user.get("banned", False):
            blocked_users += 1
            continue
        try:
            await Irene.forward_messages(user_id, broadcast_msg, silent=True)
            successful_users += 1
        except Exception as e:
            LOGGER.error(f"Failed broadcast to user {user_id}: {e}")
            blocked_users += 1

    for group in groups:
        group_id = group["user_id"]
        total_groups += 1
        try:
            await Irene.forward_messages(group_id, broadcast_msg, silent=True)
            successful_groups += 1
        except Exception as e:
            LOGGER.error(f"Failed broadcast to group {group_id}: {e}")
            failed_groups += 1

    total_chats = total_users + total_groups
    return successful_users, blocked_users, successful_groups, failed_groups, total_chats


def setup_status_handler(Irene):

    @Irene.on(events.NewMessage(
        incoming=True,
        pattern="/stats",
        from_users=OWNER_ID
    ))
    async def stats_command(event):
        stats = await banned_users.get_stats()
        stats_message = (
            "**🤖 Bot Usage Report:**\n"
            "**━━━━━━━━━━━━━━━━━━━**\n"
            "** User Engagements:**\n"
            f"- Daily Starts: {stats['day']} \n"
            f"- Weekly Starts: {stats['week']} \n"
            f"- Monthly Starts: {stats['month']} \n"
            f"- Annual Starts: {stats['year']} \n"
            "**━━━━━━━━━━━━━━━━━━━**\n"
            "**📈 Total Metrics:**\n"
            f"- Total Groups: {stats['total_groups']}\n"
            f"- Users Registered: {stats['total']}"
        )
        await event.reply(
            stats_message,
            buttons=[[Button.url("More Info", "https://t.me/abirxdhackz")]]
        )
        LOGGER.info("Stats command executed by owner")

    @Irene.on(events.NewMessage(
        incoming=True,
        pattern="/send",
        from_users=OWNER_ID,
        func=lambda e: not e.is_reply
    ))
    async def broadcast_no_reply(event):
        await event.reply("**Please reply to a message to broadcast**")
        LOGGER.info("Broadcast command used without reply by owner")

    @Irene.on(events.NewMessage(
        incoming=True,
        pattern="/send",
        from_users=OWNER_ID,
        func=lambda e: e.is_reply
    ))
    async def broadcast_command(event):
        temp_msg = await event.reply("**Processing Broadcast to Users**")
        broadcast_msg = await event.get_reply_message()

        if not broadcast_msg:
            await temp_msg.edit("**Please reply to a message to broadcast**")
            return

        successful_users, blocked_users, successful_groups, failed_groups, total_chats = await send_broadcast(Irene, broadcast_msg)

        result_msg = (
            "**Smart Broadcast Successful ✅**\n"
            "**━━━━━━━━━━━━━━━━━━━**\n"
            f"To Users: {successful_users} Users\n"
            f"Blocked Users: {blocked_users} Users\n"
            f"To Groups: {successful_groups} Groups\n"
            f"Failed Groups: {failed_groups} Groups\n"
            f"Total Chats: {total_chats} Chats\n"
            "**━━━━━━━━━━━━━━━━━━━**\n"
            "**Smooth Telecast → Activated ✅**"
        )
        await temp_msg.edit(result_msg)
        LOGGER.info(
            f"Broadcast completed: {successful_users} users, {blocked_users} blocked, "
            f"{successful_groups} groups, {failed_groups} failed groups, {total_chats} total"
        )

    LOGGER.info("Status handlers setup successfully!")