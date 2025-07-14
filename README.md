# SmartLiveGram Bot 

![SmartLiveGram Banner](https://img.shields.io/badge/SmartLiveGram-Advanced%20Feedback%20Bot-8A2BE2?style=for-the-badge&logo=telegram&logoColor=white)  
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/abirxdhack/SmartLiveGram)  
[![Updates Channel](https://img.shields.io/badge/Updates-Channel-FF69B4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/TheSmartProgrammers)  
[![Owner](https://img.shields.io/badge/Owner-%40ISmartCoder-FFD700?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/ISmartCoder)  
[![Python Version](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-00BFFF?style=flat&logo=opensource&logoColor=white)](LICENSE)

✨ **SmartLiveGram** is a sophisticated Telegram feedback bot engineered for seamless user-owner interactions. Inspired by the official [@LivegramBot](https://t.me/LivegramBot), we've cloned and enhanced its core functionalities to deliver a robust, performant solution. Powered by Pyrogram and MongoDB, it excels in private messaging, user management, broadcasting, and analytics. This project is proudly owned and maintained by [@ISmartCoder](https://t.me/ISmartCoder).

🔮 Ideal for developers, communities, and enterprises seeking an efficient feedback ecosystem on Telegram.

## 🌟 Features

- **Seamless Feedback Forwarding** 📩: Users send messages (text, media, or files) in private chats, which are forwarded to the owner. Replies from the owner are routed back effortlessly.
- **User Ban/Unban System** 🚫: Command-based moderation (`/ban <user_id>` or `/unban <user_id>`) with custom notifications for banned users.
- **Broadcast Capabilities** 📢: Effortlessly send messages or forwards to all users via `/send` (reply to a message). Includes delivery tracking for successes, blocks, and totals.
- **Comprehensive Statistics** 📊: Access detailed user activity insights with `/stats`, covering daily, weekly, monthly, yearly, and total metrics.
- **Custom Welcome Experience** 👋: Personalized `/start` message with Markdown formatting and inline buttons (e.g., updates channel link).
- **Ignore List** 🛡️: Optionally ignore specific users to filter out unwanted interactions.
- **Persistent Database** 🗄️: MongoDB-backed storage for bans, user stats, and activity tracking.
- **High Scalability** ⚡: Configured for up to 1000 workers to handle high-volume traffic.
- **Advanced Logging** 📝: Granular logs for monitoring, debugging, and operational insights.
- **Customizable Responses** 💬: Tailor ban messages and error replies to fit your branding.
- **Privacy-Focused** 🔒: Secure handling of API credentials and user data, with forward mapping to protect identities.

## 🗂️ Project Structure

The repository is organized modularly for clarity and maintainability:

```
SmartLiveGram/
├── utils/                # Utility functions and logging
│   ├── logging_setup.py  # Custom logging configuration
│   └── __init__.py       # Package initializer
├── core/                 # Core logic and database handlers
│   ├── mongo.py          # MongoDB operations for users and stats
│   └── __init__.py       # Package initializer
├── modules/              # Feature modules for handlers
│   ├── listen.py         # Incoming message processing and forwarding
│   └── status.py         # Stats, broadcast, and status commands
├── app.py                # Bot client initialization
├── main.py               # Main entry point to run the bot
├── config.py             # Environment variables and configurations
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## 📋 Requirements

- **Python**: 3.12 or higher 🐍
- **Telegram API Credentials**: Obtain API_ID, API_HASH, and BOT_TOKEN from [my.telegram.org](https://my.telegram.org/apps)
- **MongoDB**: A connection URL from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (free tier available) or a local instance
- **Owner ID**: Your Telegram user ID for admin access

Dependencies are specified in `requirements.txt`, including Pyrogram for Telegram interactions.

## ⚙️ Configuration

All settings are managed in `config.py`. Below is an explanation of each variable:

### Mandatory Variables (Required for the Bot to Function)
- `API_ID`: Your Telegram API ID (integer). *Essential for authenticating the bot client.*
- `API_HASH`: Your Telegram API hash (string). *Pairs with API_ID for secure access.*
- `BOT_TOKEN`: The bot's token from [@BotFather](https://t.me/BotFather). *Required to operate as a bot.*
- `OWNER_ID`: Your Telegram user ID (integer). *Defines the admin for commands like /stats, /send, /ban.*
- `MONGO_URL`: MongoDB connection string (e.g., `mongodb+srv://user:pass@cluster.mongodb.net/db`). *Stores user data, bans, and stats persistently.*

### Non-Mandatory Variables (Optional with Defaults)
- `IGNORE`: List of user IDs to ignore (e.g., `[]`). *Default: Empty list. Use to skip processing for specific users.*
- `REPLY_TARGET`: Dictionary for custom reply mappings (e.g., `{}`). *Default: Empty dict. Currently unused but available for extensions.*
- `BAN_REPLY`: Custom message for banned users (string, e.g., `"**Sorry You're Banned Forever ❌**"`). *Default provided. Customize for branded responses.*

Edit `config.py` directly or use environment variables for security in production.

## 🚀 Installation & Deployment

### Local Development Setup 🔧

1. Clone the repository:
   ```
   git clone https://github.com/abirxdhack/SmartLiveGram.git
   cd SmartLiveGram
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure `config.py` as detailed above.

4. Run the bot:
   ```
   python main.py
   ```
   Monitor logs for successful startup.

### VPS Deployment Guide 🌐

For always-on hosting, deploy on a VPS (e.g., Ubuntu via AWS, DigitalOcean, or Linode). Use `tmux` or `screen` to run in the background.

#### Prerequisites
- SSH into your VPS.
- Install essentials:
  ```
  sudo apt update && sudo apt install python3 python3-pip git tmux screen -y
  ```

#### Deployment Steps
1. Clone and prepare:
   ```
   git clone https://github.com/abirxdhack/SmartLiveGram.git
   cd SmartLiveGram
   pip3 install -r requirements.txt
   ```
   Edit `config.py` (use `nano config.py`).

2. **Using tmux** (Ideal for session management and multiplexing) 🔄:
   - Create a session:
     ```
     tmux new -s smartlivegram
     ```
   - Start the bot:
     ```
     python3 main.py
     ```
   - Detach: `Ctrl + B` then `D`.
   - Reattach: `tmux attach -t smartlivegram`.
   - Terminate: `tmux kill-session -t smartlivegram`.

3. **Using screen** (Simple for detached processes) 🖥️:
   - Create a session:
     ```
     screen -S smartlivegram
     ```
   - Start the bot:
     ```
     python3 main.py
     ```
   - Detach: `Ctrl + A` then `D`.
   - Reattach: `screen -r smartlivegram`.
   - Exit: `Ctrl + A` then `K`.

4. **MongoDB Integration**:
   - Create a free Atlas cluster.
   - Whitelist your VPS IP in MongoDB settings.
   - Update `MONGO_URL` in `config.py`.

5. **Best Practices**:
   - Use a virtual environment: `python3 -m venv venv && source venv/bin/activate`.
   - Monitor with `tail -f nohup.out` if using `nohup`.
   - For auto-restarts, explore systemd services.

## 🔍 Usage Guide

- **User Side**: Send `/start` for a welcome message. Any subsequent private messages forward to the owner.
- **Owner Commands** (Private chat with bot):
  - `/stats`: Display user activity statistics.
  - `/send`: Broadcast by replying to a message.
  - `/ban <user_id>`: Ban a user (reply to their forwarded message or specify ID).
  - `/unban <user_id>`: Unban a user.
- Logs track all events; check console or files for details.

## 🤝 Contributing

We welcome contributions! Fork the repo, create a branch, and submit a pull request. Adhere to Python PEP 8 style. Add tests and document changes. Report issues via GitHub.

## 📜 License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 💎 Credits & Acknowledgments

- **Owner**: [@ISmartCoder](https://t.me/ISmartCoder) 🔱
- **Inspiration**: Cloned from the official [@LivegramBot](https://t.me/LivegramBot) 🌈
- **Framework**: Built with [Pyrogram](https://docs.pyrogram.org/) and community libraries.

Stay updated via our [Updates Channel](https://t.me/TheSmartProgrammers)! 🚀