from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL
from datetime import datetime, timedelta
from utils import LOGGER

LOGGER.info("Creating Database Client From MONGO_URL")

try:
    mongo_client = AsyncIOMotorClient(MONGO_URL)
    db = mongo_client["SmartLiveGram"]
    LOGGER.info("Database Client Created Successfully!")
except Exception as e:
    LOGGER.error(f"Database Client Create Error: {e}")
    raise


class BannedUsers:
    def __init__(self):
        self.users = db["users_db"]

    async def add_user(self, user_id: int):
        await self.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "user_id": user_id,
                    "banned": False,
                    "last_active": datetime.utcnow(),
                    "is_group": False
                }
            },
            upsert=True
        )

    async def add_group(self, chat_id: int):
        await self.users.update_one(
            {"user_id": chat_id},
            {
                "$set": {
                    "user_id": chat_id,
                    "banned": False,
                    "last_active": datetime.utcnow(),
                    "is_group": True
                }
            },
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
        return await self.users.find({"is_group": False}).to_list(None)

    async def get_all_groups(self):
        return await self.users.find({"is_group": True}).to_list(None)

    async def update_last_active(self, user_id: int):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"last_active": datetime.utcnow(), "is_group": False}},
            upsert=True
        )

    async def get_stats(self):
        now = datetime.utcnow()
        stats = {
            "day": await self.users.count_documents({
                "is_group": False,
                "last_active": {"$gte": now - timedelta(days=1)}
            }),
            "week": await self.users.count_documents({
                "is_group": False,
                "last_active": {"$gte": now - timedelta(days=7)}
            }),
            "month": await self.users.count_documents({
                "is_group": False,
                "last_active": {"$gte": now - timedelta(days=30)}
            }),
            "year": await self.users.count_documents({
                "is_group": False,
                "last_active": {"$gte": now - timedelta(days=365)}
            }),
            "total": await self.users.count_documents({"is_group": False}),
            "total_groups": await self.users.count_documents({"is_group": True})
        }
        return stats


banned_users = BannedUsers()