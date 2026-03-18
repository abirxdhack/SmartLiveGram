# SmartLiveGram Bot (Telethon Edition)

![SmartLiveGram Banner](https://img.shields.io/badge/SmartLiveGram-Advanced%20Feedback%20Bot-8A2BE2?style=for-the-badge&logo=telegram&logoColor=white)
[![Updates Channel](https://img.shields.io/badge/Updates-Channel-FF69B4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/TheSmartProgrammers)
[![Owner](https://img.shields.io/badge/Owner-%40ISmartCoder-FFD700?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/ISmartCoder)
[![Python Version](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-00BFFF?style=flat&logo=opensource&logoColor=white)](LICENSE)

SmartLiveGram is a full-featured Telegram feedback bot — a complete Telethon rewrite of the original Pyrogram version. Powered by Telethon and MongoDB Motor with full async support, group relay, anonymous admin detection, and advanced broadcast analytics.

---

## Features

- **Seamless Feedback Forwarding** — Users send messages (text, media, files) in private chats. All messages are forwarded to the owner's PM and simultaneously to every registered group.
- **Group Relay** — When added to a group by the owner, the bot forwards all user PMs into that group as well, enabling multi-channel monitoring.
- **Group Welcome Message** — Bot instantly sends a welcome message when added to any group.
- **Admin Reply Routing** — Owner and group admins can reply to forwarded messages; the reply is delivered back to the original user's PM automatically.
- **Anonymous Admin Support** — Uses MTProto `GetParticipantsRequest` with `ChannelParticipantsAdmins` filter to detect anonymous admins by `admin_rights.anonymous`. Anonymous admin replies are correctly routed without exposing identity.
- **User Ban/Unban System** — `/ban <user_id>` and `/unban <user_id>` with instant notifications to both owner and the affected user.
- **Smart Broadcast** — `/send` (reply to any message) broadcasts to all registered users and all registered groups separately, with full delivery analytics.
- **Detailed Statistics** — `/stats` with daily, weekly, monthly, annual active user counts plus total users and total groups, with inline button.
- **Custom Welcome Experience** — Personalized `/start` message with inline Updates Channel button.
- **Ignore List** — Silently skip specific user IDs via `IGNORE` config.
- **Persistent MongoDB Storage** — Users, groups, bans, and last-active timestamps all tracked in MongoDB. Groups persist across restarts.
- **Advanced Logging** — Rotating file logs (`botlog.txt`, 50 MB, 10 backups) plus stdout. Telethon internals silenced to ERROR level.
- **Customizable Ban Reply** — Set `BAN_REPLY` in `config.py`.
- **Owner Command Isolation** — `/stats` and `/send` are intercepted before the forwarding pipeline so they are never echoed back to the owner as forwarded messages.
- **Clean Shutdown** — `KeyboardInterrupt` (Ctrl+C) is caught at the top level outside `asyncio.run()`, producing a clean exit log instead of a traceback.

---

## Project Structure

```
SmartLiveGram/
├── utils/
│   ├── logging_setup.py      # Rotating file + stdout logger
│   └── __init__.py
├── core/
│   ├── mongo.py              # Async MongoDB — users, groups, bans, stats
│   └── __init__.py
├── modules/
│   ├── listen.py             # PM forwarding, owner commands, group reply routing, anon admin
│   ├── status.py             # /stats, /send broadcast with analytics
│   ├── group.py              # ChatAction join handler, GROUP_CHAT_IDS shared state
│   └── __init__.py
├── app.py                    # TelegramClient (Irene) initialisation
├── main.py                   # Entry point, handler wiring, clean shutdown
├── config.py                 # All credentials and settings
├── requirements.txt
└── README.md
```

---

## Configuration

Edit `config.py`:

| Variable | Required | Description |
|----------|----------|-------------|
| `API_ID` | ✅ | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | ✅ | Telegram API Hash |
| `BOT_TOKEN` | ✅ | Bot token from [@BotFather](https://t.me/BotFather) |
| `OWNER_ID` | ✅ | Your Telegram user ID (integer) |
| `MONGO_URL` | ✅ | MongoDB connection string (Atlas or self-hosted) |
| `IGNORE` | ❌ | List of user IDs to silently ignore (default `[]`) |
| `BAN_REPLY` | ❌ | Message sent to banned users |

---

## Installation

```bash
git clone <repo>
cd SmartLiveGram
pip install -r requirements.txt
```

Edit `config.py`, then:

```bash
python3 main.py
```

---

## Owner Commands

| Command | Description |
|---------|-------------|
| `/stats` | Bot usage report — active users, groups, totals, with inline button |
| `/send` | Broadcast (reply to any message) to all users and groups |
| `/ban <user_id>` | Ban a user — notifies user and confirms to owner |
| `/unban <user_id>` | Unban a user — notifies user and confirms to owner |

> All commands work only in the owner's private chat with the bot.

---

## Stats Output Example

```
🤖 Bot Usage Report:
━━━━━━━━━━━━━━━━━━━
 User Engagements:
- Daily Starts: 30
- Weekly Starts: 345
- Monthly Starts: 881
- Annual Starts: 881
━━━━━━━━━━━━━━━━━━━
📈 Total Metrics:
- Total Groups: 73
- Users Registered: 982
```

## Broadcast Output Example

```
Smart Broadcast Successful ✅
━━━━━━━━━━━━━━━━━━━
To Users: 81 Users
Blocked Users: 163 Users
To Groups: 4 Groups
Failed Groups: 3 Groups
Total Chats: 85 Chats
━━━━━━━━━━━━━━━━━━━
Smooth Telecast → Activated ✅
```

---

## VPS Deployment

```bash
# Install dependencies
sudo apt update && sudo apt install python3 python3-pip git tmux -y
git clone <repo> && cd SmartLiveGram
pip3 install -r requirements.txt

# Run in persistent tmux session
tmux new -s smartlivegram
python3 main.py
# Detach: Ctrl+B then D
# Reattach: tmux attach -t smartlivegram
```

---

## Changelog

### v2.3.0 — `feat: isolate owner commands from forwarding pipeline`
- `/stats` and `/send` are now intercepted before the message forwarding logic in `listen.py` so they are never echoed to the owner as forwarded messages
- Added `OWNER_COMMANDS` tuple for clean extensibility

### v2.2.0 — `feat: add anonymous admin reply routing via MTProto participant inspection`
- Anonymous admin messages (where `sender_id` is `None` and `from_id` is `PeerChannel`/`PeerChat`) are now detected via `_sender_is_anonymous()`
- `_chat_has_anonymous_admins()` uses `iter_participants` with `ChannelParticipantsAdmins` filter and inspects `admin_rights.anonymous` on each participant
- Anonymous admin replies to forwarded messages are routed to the original user's PM

### v2.1.0 — `feat: broadcast groups separately with per-type delivery analytics`
- `/send` now broadcasts to users and groups as separate loops
- Result message shows `To Users`, `Blocked Users`, `To Groups`, `Failed Groups`, `Total Chats`
- `send_broadcast()` returns 5-tuple instead of 3-tuple

### v2.0.0 — `feat: add group relay, group persistence, and group reply routing`
- Bot forwards all incoming user PMs to registered groups simultaneously
- `GROUP_MSG_MAP` tracks forwarded group message IDs for reply routing
- Group admins (named) can reply to forwarded messages in the group; reply is delivered to original user
- `GROUP_CHAT_IDS` shared state lives in `group.py` and imported by `listen.py` — single source of truth
- `ChatAction` handler detects bot being added to a group and sends welcome message

### v1.3.0 — `feat: persist groups to MongoDB and include in stats`
- `mongo.py` gains `add_group()`, `get_all_groups()`, and `total_groups` in `get_stats()`
- `group.py` calls `add_group()` on join so groups survive bot restarts
- `get_all_users()` now explicitly filters `is_group: false`

### v1.2.0 — `feat: redesign /stats and broadcast output format`
- `/stats` shows 🤖 Bot Usage Report with daily/weekly/monthly/annual/total/groups breakdown and inline More Info button
- Broadcast result shows Smart Broadcast Successful with per-type counts

### v1.1.1 — `fix: resolve KeyboardInterrupt traceback on Ctrl+C`
- Moved `try/except KeyboardInterrupt` outside `asyncio.run()` in `main.py` — asyncio re-raises after the loop stops so inner catches were too late

### v1.1.0 — `fix: unify GROUP_CHAT_IDS to single shared set`
- Previous version had `GROUP_CHAT_IDS` defined in both `config.py` and `group.py` as separate objects — `listen.py` was reading the always-empty config one
- Canonical set now lives in `group.py`; `listen.py` imports it directly

### v1.0.1 — `fix: hardcode database name to resolve Motor ConfigurationError`
- `get_default_database()` raises `ConfigurationError` when Atlas URL has no path-based DB name
- Replaced with `mongo_client["SmartLiveGram"]` — explicit and reliable

### v1.0.0 — `feat: full rewrite from Pyrogram to Telethon`
- Replaced `pyrofork` + `asyncio` (redundant stdlib dep) with `telethon` + `tgcrypto`
- `snigdha` client renamed to `Irene`
- `filters.private & filters.incoming` replaced with `events.NewMessage(incoming=True, func=lambda e: e.is_private)`
- `message.forward()` replaced with `Irene.forward_messages()`
- `message.copy()` replaced with `Irene.send_message(entity, message_object)`
- `InlineKeyboardMarkup` + `InlineKeyboardButton` replaced with `Button.url()`
- `Client(workers=1000)` replaced with Telethon's async event loop (no manual worker config needed)
- Fixed original bug: `update_last_active()` now actually called on every forwarded message
- Fixed original bug: DB name now hardcoded — no fragile `appName` URL parsing

---

## Credits

- **Owner**: [@ISmartCoder](https://t.me/ISmartCoder)
- **Framework**: [Telethon](https://github.com/LonamiWebs/Telethon)
- **Inspiration**: [@LivegramBot](https://t.me/LivegramBot)
- **Updates**: [t.me/TheSmartProgrammers](https://t.me/TheSmartProgrammers)