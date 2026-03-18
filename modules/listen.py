from telethon import events, Button
from telethon.tl.types import (
    User,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    PeerChannel,
    PeerChat,
)
from telethon.tl.functions.channels import GetParticipantRequest
from utils import LOGGER
from core import banned_users
from config import OWNER_ID, IGNORE, BAN_REPLY
from modules.group import GROUP_CHAT_IDS

FORWARDED_MAP = {}
GROUP_MSG_MAP = {}

OWNER_COMMANDS = ("/stats", "/send")


async def _is_named_admin_or_owner(Irene, chat_id, user_id):
    if user_id == OWNER_ID:
        return True
    try:
        participant = await Irene(GetParticipantRequest(chat_id, user_id))
        return isinstance(
            participant.participant,
            (ChannelParticipantAdmin, ChannelParticipantCreator)
        )
    except Exception as e:
        LOGGER.error(f"Admin check failed for {user_id} in {chat_id}: {e}")
        return False


async def _chat_has_anonymous_admins(Irene, chat_id):
    try:
        async for user in Irene.iter_participants(
            chat_id, filter=ChannelParticipantsAdmins
        ):
            participant = getattr(user, "participant", None)
            if participant is None:
                continue
            admin_rights = getattr(participant, "admin_rights", None)
            if admin_rights is None:
                continue
            if getattr(admin_rights, "anonymous", False):
                return True
        return False
    except Exception as e:
        LOGGER.error(f"Anonymous admin check failed for {chat_id}: {e}")
        return False


def _sender_is_anonymous(event):
    if event.sender_id is not None:
        return False
    from_id = getattr(event.message, "from_id", None)
    if from_id is None:
        return True
    if isinstance(from_id, (PeerChannel, PeerChat)):
        return True
    return False


def setup_listen_handler(Irene):

    @Irene.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def forward_private_message(event):
        try:
            sender = await event.get_sender()
            if not isinstance(sender, User):
                return

            user_id = sender.id
            text = event.raw_text or "<non-text message>"
            LOGGER.info(f"Message received from {user_id}: {text}")

            if text.strip() == "/start":
                await banned_users.add_user(user_id)
                first = sender.first_name or ""
                last = sender.last_name or ""
                user_name = (first + " " + last).strip() or "User"
                welcome_msg = (
                    f"**Hi {user_name}! Welcome To This Bot**\n"
                    f"**━━━━━━━━━━━━━━━━━━━━━━**\n"
                    f"**SmartGram: The ultimate toolkit on Telegram, offering best feedback bot features including private users.**\n"
                    f"**━━━━━━━━━━━━━━━━━━━━━━**\n"
                    f"**Don't forget to [Join Here](http://t.me/TheSmartDev) for updates!**"
                )
                await Irene.send_message(
                    user_id,
                    welcome_msg,
                    buttons=[[Button.url("Updates Channel", "https://t.me/TheSmartProgrammers")]],
                    link_preview=False
                )
                LOGGER.info(f"Sent welcome message to user {user_id}")
                return

            if await banned_users.is_banned(user_id):
                await Irene.send_message(user_id, f"**{BAN_REPLY}**")
                LOGGER.info(f"Ignored banned user {user_id}")
                return

            if user_id in IGNORE:
                LOGGER.info(f"Ignored user {user_id}")
                return

            if user_id == OWNER_ID:
                raw = text.strip()
                if any(raw == cmd or raw.startswith(cmd + " ") for cmd in OWNER_COMMANDS):
                    LOGGER.info(f"Owner used command {raw!r} — skipping forward")
                    return

                reply_msg = await event.get_reply_message()
                replied_msg_id = reply_msg.id if reply_msg else None
                target_user_id = FORWARDED_MAP.get(replied_msg_id) if replied_msg_id else None

                if target_user_id is None and reply_msg and reply_msg.sender_id == OWNER_ID:
                    target_user_id = OWNER_ID

                if text.startswith("/ban"):
                    parts = text.split()
                    if len(parts) > 1:
                        try:
                            target_user_id = int(parts[1])
                        except ValueError:
                            await Irene.send_message(OWNER_ID, "**Invalid user ID.**")
                            return
                    elif target_user_id is None:
                        await Irene.send_message(OWNER_ID, "**Please reply to a forwarded message or provide a user ID.**")
                        return
                    if target_user_id == OWNER_ID:
                        await Irene.send_message(OWNER_ID, "**You Can't Ban Bot Owner**")
                        return
                    await banned_users.ban_user(target_user_id)
                    await Irene.send_message(OWNER_ID, f"**User {target_user_id} has been banned.**")
                    try:
                        await Irene.send_message(target_user_id, f"**{BAN_REPLY}**")
                        LOGGER.info(f"Sent ban notification to user {target_user_id}")
                    except Exception as e:
                        LOGGER.error(f"Failed to notify user {target_user_id} of ban: {e}")
                    return

                elif text.startswith("/unban"):
                    parts = text.split()
                    if len(parts) > 1:
                        try:
                            target_user_id = int(parts[1])
                        except ValueError:
                            await Irene.send_message(OWNER_ID, "**Invalid user ID.**")
                            return
                    elif target_user_id is None:
                        await Irene.send_message(OWNER_ID, "**Please reply to a forwarded message or provide a user ID.**")
                        return
                    if target_user_id == OWNER_ID:
                        await Irene.send_message(OWNER_ID, "**Lol Why To Unban He Is Already Bot Owner**")
                        return
                    await banned_users.unban_user(target_user_id)
                    await Irene.send_message(OWNER_ID, f"**User {target_user_id} has been unbanned.**")
                    try:
                        await Irene.send_message(target_user_id, "**Good News, You're Unbanned Now**")
                        LOGGER.info(f"Sent unban notification to user {target_user_id}")
                    except Exception as e:
                        LOGGER.error(f"Failed to notify user {target_user_id} of unban: {e}")
                    return

                elif target_user_id:
                    try:
                        await Irene.send_message(target_user_id, event.message)
                        LOGGER.info(f"Sent owner PM reply to user {target_user_id}")
                    except Exception as e:
                        LOGGER.error(f"Error sending PM reply to user {target_user_id}: {e}")
                        await Irene.send_message(OWNER_ID, "**❌ Sorry, action not allowed.**")
                    return

            try:
                fwd = await Irene.forward_messages(OWNER_ID, event.message, silent=True)
                if isinstance(fwd, list):
                    fwd = fwd[0]
                FORWARDED_MAP[fwd.id] = user_id
                await banned_users.update_last_active(user_id)
                LOGGER.info(f"✅ Forwarded to owner {OWNER_ID} from {user_id}")
                LOGGER.info(f"User ID: {user_id}, Message ID: {event.message.id}")

                for group_id in list(GROUP_CHAT_IDS):
                    try:
                        group_fwd = await Irene.forward_messages(group_id, event.message, silent=True)
                        if isinstance(group_fwd, list):
                            group_fwd = group_fwd[0]
                        GROUP_MSG_MAP[group_fwd.id] = user_id
                        LOGGER.info(f"✅ Also forwarded to group {group_id} from {user_id}")
                    except Exception as e:
                        LOGGER.error(f"Failed to forward to group {group_id}: {e}")

            except Exception as e:
                LOGGER.error(f"❌ Forwarding failed: {e}")
                await Irene.send_message(user_id, "**Sorry Failed To Send To Owner❌**")

        except Exception as e:
            LOGGER.error(f"Unhandled error in forward_private_message: {e}")

    @Irene.on(events.NewMessage(incoming=True, func=lambda e: e.is_group or e.is_channel))
    async def handle_group_message(event):
        try:
            chat_id = event.chat_id
            if chat_id not in GROUP_CHAT_IDS:
                return

            if not event.is_reply:
                return

            reply_msg = await event.get_reply_message()
            if not reply_msg:
                return

            target_user_id = GROUP_MSG_MAP.get(reply_msg.id)
            if target_user_id is None:
                return

            is_privileged = False

            if _sender_is_anonymous(event):
                LOGGER.info(f"Anonymous admin reply detected in group {chat_id}")
                is_privileged = await _chat_has_anonymous_admins(Irene, chat_id)
                if is_privileged:
                    LOGGER.info(f"Confirmed: group {chat_id} has anonymous admins — allowing reply")
                else:
                    LOGGER.info(f"No anonymous admins found in {chat_id} — ignoring")
                    return
            else:
                sender = await event.get_sender()
                if not isinstance(sender, User):
                    return
                user_id = sender.id
                is_privileged = await _is_named_admin_or_owner(Irene, chat_id, user_id)
                if not is_privileged:
                    return
                LOGGER.info(f"Named admin/owner {user_id} reply in group {chat_id}")

            try:
                await Irene.send_message(target_user_id, event.message)
                LOGGER.info(f"✅ Group reply delivered to user {target_user_id}")
            except Exception as e:
                LOGGER.error(f"Failed to deliver group reply to {target_user_id}: {e}")
                try:
                    await Irene.send_message(chat_id, "**❌ Failed to deliver reply to user.**")
                except Exception:
                    pass

        except Exception as e:
            LOGGER.error(f"Unhandled error in handle_group_message: {e}")

    LOGGER.info("Listen handlers setup successfully!")