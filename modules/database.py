# ─── database.py ─── SmartyMS-Uploader ───────────────────────────────────────
# Handles: auth users (with nickname + timing) & all users (for broadcast)
# Storage: MongoDB (persistent across restarts)
# ─────────────────────────────────────────────────────────────────────────────

import os
from datetime import datetime, timedelta
from pymongo import MongoClient

# ── MongoDB Connection ────────────────────────────────────────────────────────

MONGO_URL = os.environ.get(
    "MONGO_URL",
    "mongodb+srv://m49606145_db_user:Th15V5nu9utMejwO@cluster0.g11tftt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

_client = MongoClient(MONGO_URL)
_db = _client["SmartyMS"]

auth_col     = _db["auth_users"]
users_col    = _db["all_users"]
channels_col = _db["channels"]


# ── Duration parser ───────────────────────────────────────────────────────────

def parse_duration(duration_str: str):
    """
    Parse strings like: '01 week', '2 months', '3 years', '7 days'
    Returns timedelta or None on failure.
    """
    parts = duration_str.strip().lower().split()
    if len(parts) < 2:
        return None
    try:
        num = int(parts[0])
    except ValueError:
        return None
    unit = parts[1].rstrip("s")   # normalize: weeks→week, months→month, etc.

    if unit in ("day",):
        return timedelta(days=num)
    elif unit in ("week",):
        return timedelta(weeks=num)
    elif unit in ("month",):
        return timedelta(days=num * 30)
    elif unit in ("year",):
        return timedelta(days=num * 365)
    return None


# ── Auth users ────────────────────────────────────────────────────────────────

def add_auth_user(user_id: int, duration_str: str, nickname: str):
    """
    Add / update an authorized user.
    Returns (expires_datetime, None) on success or (None, error_string).
    """
    td = parse_duration(duration_str)
    if td is None:
        return None, (
            "Invalid duration format.\n"
            "Use: `/addauth <id> <num> <week/day/month/year> <nickname>`\n"
            "Example: `/addauth 123456 01 week Mahira`"
        )

    now = datetime.now()
    expires = now + td

    auth_col.update_one(
        {"user_id": user_id},
        {"$set": {
            "user_id": user_id,
            "nickname": nickname,
            "granted_at": now.strftime("%Y-%m-%d %H:%M:%S"),
            "expires_at": expires.strftime("%Y-%m-%d %H:%M:%S"),
        }},
        upsert=True
    )
    return expires, None


def remove_auth_user(user_id: int):
    """Remove user from auth DB. Returns True if existed."""
    result = auth_col.delete_one({"user_id": user_id})
    return result.deleted_count > 0


def get_auth_user(user_id: int):
    """Returns user dict {nickname, granted_at, expires_at} or None."""
    doc = auth_col.find_one({"user_id": user_id}, {"_id": 0})
    if doc:
        return {
            "nickname": doc.get("nickname"),
            "granted_at": doc.get("granted_at"),
            "expires_at": doc.get("expires_at"),
        }
    return None


def get_all_auth_users():
    """Returns full auth dict {user_id_str: {...}} — same shape as old JSON."""
    result = {}
    for doc in auth_col.find({}, {"_id": 0}):
        result[str(doc["user_id"])] = {
            "nickname": doc.get("nickname"),
            "granted_at": doc.get("granted_at"),
            "expires_at": doc.get("expires_at"),
        }
    return result


def is_authorized(user_id: int):
    """True if user exists in DB AND subscription has not expired."""
    info = get_auth_user(user_id)
    if not info:
        return False
    try:
        expires = datetime.strptime(info["expires_at"], "%Y-%m-%d %H:%M:%S")
        return datetime.now() < expires
    except Exception:
        return False


def get_auth_user_ids():
    """Returns list of currently valid (non-expired) user IDs."""
    now = datetime.now()
    valid = []
    for doc in auth_col.find({}, {"_id": 0, "user_id": 1, "expires_at": 1}):
        try:
            expires = datetime.strptime(doc["expires_at"], "%Y-%m-%d %H:%M:%S")
            if now < expires:
                valid.append(int(doc["user_id"]))
        except Exception:
            pass
    return valid


# ── All-users registry (for broadcast) ───────────────────────────────────────

def register_user(user_id: int):
    """Track every user who interacts with the bot (for broadcast)."""
    users_col.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )


def get_all_user_ids():
    """Returns list of all user IDs ever seen by the bot."""
    return [doc["user_id"] for doc in users_col.find({}, {"_id": 0, "user_id": 1})]


# ── Allowed Channels / Groups ─────────────────────────────────────────────────

def add_channel(chat_id: int):
    """Add a channel/group to the allowed list."""
    channels_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id}},
        upsert=True
    )

def remove_channel(chat_id: int):
    """Remove a channel/group. Returns True if existed."""
    result = channels_col.delete_one({"chat_id": chat_id})
    return result.deleted_count > 0

def is_allowed_chat(chat_id: int):
    """True if this chat_id is in the allowed channels list."""
    return channels_col.find_one({"chat_id": chat_id}) is not None

def get_all_channels():
    """Returns list of allowed channel/group IDs."""
    return [doc["chat_id"] for doc in channels_col.find({}, {"_id": 0, "chat_id": 1})]
