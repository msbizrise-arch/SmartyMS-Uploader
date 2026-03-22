# ─── database.py ─── SmartyMS-Uploader ───────────────────────────────────────
# Handles: auth users (with nickname + timing) & all users (for broadcast)
# Storage: JSON file (persists on disk inside Docker container)
# ─────────────────────────────────────────────────────────────────────────────

import json
import os
from datetime import datetime, timedelta

_DIR = os.path.dirname(__file__)
AUTH_DB_FILE = os.path.join(_DIR, "MSauth_db.json")
ALL_USERS_FILE = os.path.join(_DIR, "MSall_users.json")


# ── Internal helpers ──────────────────────────────────────────────────────────

def _load(path):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def _save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


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

    data = _load(AUTH_DB_FILE)
    now = datetime.now()
    expires = now + td

    data[str(user_id)] = {
        "nickname": nickname,
        "granted_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "expires_at": expires.strftime("%Y-%m-%d %H:%M:%S"),
    }
    _save(AUTH_DB_FILE, data)
    return expires, None


def remove_auth_user(user_id: int):
    """Remove user from auth DB. Returns True if existed."""
    data = _load(AUTH_DB_FILE)
    key = str(user_id)
    if key in data:
        del data[key]
        _save(AUTH_DB_FILE, data)
        return True
    return False


def get_auth_user(user_id: int):
    """Returns user dict {nickname, granted_at, expires_at} or None."""
    return _load(AUTH_DB_FILE).get(str(user_id))


def get_all_auth_users():
    """Returns full auth dict {user_id_str: {...}}."""
    return _load(AUTH_DB_FILE)


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
    data = _load(AUTH_DB_FILE)
    now = datetime.now()
    valid = []
    for uid_str, info in data.items():
        try:
            expires = datetime.strptime(info["expires_at"], "%Y-%m-%d %H:%M:%S")
            if now < expires:
                valid.append(int(uid_str))
        except Exception:
            pass
    return valid


# ── All-users registry (for broadcast) ───────────────────────────────────────

def register_user(user_id: int):
    """Track every user who interacts with the bot (for broadcast)."""
    data = _load(ALL_USERS_FILE)
    data[str(user_id)] = True
    _save(ALL_USERS_FILE, data)


def get_all_user_ids():
    """Returns list of all user IDs ever seen by the bot."""
    return [int(k) for k in _load(ALL_USERS_FILE).keys()]


# ── Allowed Channels / Groups ─────────────────────────────────────────────────

CHANNELS_DB_FILE = os.path.join(_DIR, "MSchannels_db.json")

def add_channel(chat_id: int):
    """Add a channel/group to the allowed list."""
    data = _load(CHANNELS_DB_FILE)
    data[str(chat_id)] = True
    _save(CHANNELS_DB_FILE, data)

def remove_channel(chat_id: int):
    """Remove a channel/group. Returns True if existed."""
    data = _load(CHANNELS_DB_FILE)
    key = str(chat_id)
    if key in data:
        del data[key]
        _save(CHANNELS_DB_FILE, data)
        return True
    return False

def is_allowed_chat(chat_id: int):
    """True if this chat_id is in the allowed channels list."""
    return str(chat_id) in _load(CHANNELS_DB_FILE)

def get_all_channels():
    """Returns list of allowed channel/group IDs."""
    return [int(k) for k in _load(CHANNELS_DB_FILE).keys()]
