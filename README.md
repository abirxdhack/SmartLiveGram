<h1 align="center">SmartLiveGram Telegram Bot</h1>
<p align="center">
  <a href="https://github.com/abirxdhack/SmartLiveGram/stargazers"><img src="https://img.shields.io/github/stars/abirxdhack/SmartLiveGram?color=blue&style=flat" alt="GitHub Repo stars"></a>
  <a href="https://github.com/abirxdhack/SmartLiveGram/issues"><img src="https://img.shields.io/github/issues/abirxdhack/SmartLiveGram" alt="GitHub issues"></a>
  <a href="https://github.com/abirxdhack/SmartLiveGram/pulls"><img src="https://img.shields.io/github/issues-pr/abirxdhack/SmartLiveGram" alt="GitHub pull requests"></a>
  <a href="https://github.com/abirxdhack/SmartLiveGram/graphs/contributors"><img src="https://img.shields.io/github/contributors/abirxdhack/SmartLiveGram?style=flat" alt="GitHub contributors"></a>
  <a href="https://github.com/abirxdhack/SmartLiveGram/network/members"><img src="https://img.shields.io/github/forks/abirxdhack/SmartLiveGram?style=flat" alt="GitHub forks"></a>
</p>
<p align="center">
  <em>SmartLiveGram: an advanced Telegram feedback bot built with Telethon and MongoDB, designed for seamless user-to-owner messaging, broadcasting, group support, and moderation.</em>
</p>
<hr>

## ✨ Features

* 📩 **Feedback Forwarding**: All user private messages are forwarded to the owner and linked groups instantly.
* 🔁 **Owner Reply**: Owner replies to forwarded messages are sent back to the original user automatically.
* 👥 **Group Support**: Bot forwards messages to groups it's added in and allows admins to reply to users from there.
* 🕵️ **Anonymous Admin Support**: Anonymous group admins can reply and their replies are delivered to the user.
* 🚫 **Ban / Unban System**: Owner can ban or unban users with instant notification.
* 📢 **Broadcast**: Send a message to all users and groups at once with a detailed delivery report.
* 📊 **Statistics**: View daily, weekly, monthly, yearly, and total user and group metrics.
* 👋 **Welcome Message**: Users get a personalized welcome on `/start` with an inline button.
* 🛡️ **Ignore List**: Silently ignore specific user IDs without any response.
* 🗄️ **MongoDB Persistence**: All users, groups, bans, and activity are stored persistently.
* 📝 **Advanced Logging**: Rotating file logs with stdout output for easy monitoring.

## Requirements

Before you begin, ensure you have met the following requirements:

- Python 3.10 or higher.
- A Telegram bot token (you can get one from [@BotFather](https://t.me/BotFather) on Telegram).
- API ID and Hash: You can get these by creating an application on [my.telegram.org](https://my.telegram.org).
- A MongoDB connection URL from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (free tier available).

## Installation

To install required libraries run the following command:

```bash
pip install -r requirements.txt
```

## Configuration

1. Open the `config.py` file in your favorite text editor.
2. Replace the placeholders with your actual values:
   - **`API_ID`**: Your API ID from [my.telegram.org](https://my.telegram.org).
   - **`API_HASH`**: Your API Hash from [my.telegram.org](https://my.telegram.org).
   - **`BOT_TOKEN`**: The token you obtained from [@BotFather](https://t.me/BotFather).
   - **`OWNER_ID`**: Your Telegram account ID (integer).
   - **`MONGO_URL`**: Your MongoDB connection string from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

## Deploy the Bot

```sh
git clone https://github.com/abirxdhack/SmartLiveGram
cd SmartLiveGram
pip install -r requirements.txt
python3 main.py
```

## How It Works

1. **Start the Bot**: Send the `/start` command to the bot to register and receive a welcome message.
2. **Send a Message**: Any message sent to the bot is forwarded to the owner's PM and all linked groups.
3. **Owner Replies**: The owner replies to a forwarded message and it is delivered back to the original user.
4. **Group Admins Reply**: Admins (including anonymous admins) in linked groups can also reply to forwarded messages.
5. **Moderation**:
   - `/ban <user_id>` — Ban a user from messaging the bot.
   - `/unban <user_id>` — Unban a user.
6. **Broadcast**: Reply to any message and send `/send` to broadcast it to all users and groups.
7. **Statistics**: Send `/stats` to see a full usage report with user and group metrics.

✨ **Note**: If you found this repo helpful, please fork and star it. Also, feel free to share with proper credit!

## Author

- Name: Abir
- Telegram: [@ISmartCoder](https://t.me/ISmartCoder)
- Updates Channel: [@TheSmartProgrammers](https://t.me/TheSmartProgrammers)

Feel free to reach out if you have any questions or feedback.