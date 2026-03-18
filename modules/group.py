from telethon import events
from utils import LOGGER
from config import OWNER_ID

GROUP_CHAT_IDS = set()


async def is_admin_or_owner(Irene, chat_id, user_id):
    if user_id == OWNER_ID:
        return True
    try:
        from telethon.tl.functions.channels import GetParticipantRequest
        from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
        participant = await Irene(GetParticipantRequest(chat_id, user_id))
        return isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
    except Exception:
        return False


def setup_group_handler(Irene):

    @Irene.on(events.ChatAction())
    async def on_chat_action(event):
        try:
            if not event.user_added and not event.user_joined:
                return
            me = await Irene.get_me()
            user_ids = getattr(event, "_user_ids", None) or []
            if me.id not in user_ids:
                return
            chat_id = event.chat_id
            GROUP_CHAT_IDS.add(chat_id)
            from core import banned_users
            await banned_users.add_group(chat_id)
            await Irene.send_message(chat_id, "**Thank you for adding me to this group!**")
            LOGGER.info(f"Bot added to group {chat_id}")
        except Exception as e:
            LOGGER.error(f"ChatAction error: {e}")

    LOGGER.info("Group handlers setup successfully!")