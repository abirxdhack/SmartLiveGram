#Copyright @ISmartCoder
#Updates Channel https://:t.me/TheSmartProgrammers
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import urlparse, parse_qs
from config import MONGO_URL
from datetime import datetime, timedelta
from utils import LOGGER

LOGGER.info("Creating Database Client From MONGO_URL")

try:
    parsed = urlparse(MONGO_URL)
    query_params = parse_qs(parsed.query)
    db_name = query_params.get("appName", [None])[0]

    if not db_name:
        raise ValueError("No database name found in MONGO_URL (missing 'appName' query param)")

    mongo_client = AsyncIOMotorClient(MONGO_URL)
    db = mongo_client.get_database(db_name)
    LOGGER.info(f"Database Client Created Successfully!")
except Exception as e:
    LOGGER.error(f"Database Client Create Error: {e}")
    raise

class BannedUsers:
    def __init__(self):
        self.users = db["users_db"]

    async def add_user(self, user_id: int):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id, "banned": False, "last_active": datetime.utcnow(), "is_group": False}},
            upsert=True
        )

    async def ban_user(self, user_id: int):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"banned": True}},
            upsert=True
        )

    async def unban_user(self, user_id: int):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"banned": False}},
            upsert=True
        )

    async def is_banned(self, user_id: int) -> bool:
        user = await self.users.find_one({"user_id": user_id})
        return user.get("banned", False) if user else False

    async def get_all_users(self):
        return await self.users.find().to_list(None)

    async def update_last_active(self, user_id: int):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"last_active": datetime.utcnow(), "is_group": False}},
            upsert=True
        )

    async def get_stats(self):
        now = datetime.utcnow()
        stats = {
            "day": await self.users.count_documents({"is_group": False, "last_active": {"$gte": now - timedelta(days=1)}}),
            "week": await self.users.count_documents({"is_group": False, "last_active": {"$gte": now - timedelta(days=7)}}),
            "month": await self.users.count_documents({"is_group": False, "last_active": {"$gte": now - timedelta(days=30)}}),
            "year": await self.users.count_documents({"is_group": False, "last_active": {"$gte": now - timedelta(days=365)}}),
            "total": await self.users.count_documents({"is_group": False})
        }
        return stats

banned_users = BannedUsers()