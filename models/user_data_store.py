from models.user_settings import UserSettings

# Global dict to store users (RAM içinde geçici)
user_store = {}

def get_or_create_user(user_id: int) -> UserSettings:
    """
    Returns existing user settings or creates new one if not found
    """
    if user_id not in user_store:
        user_store[user_id] = UserSettings(user_id)
    return user_store[user_id]

def get_all_users() -> list:
    """
    Returns all user objects
    """
    return list(user_store.values())

def get_all_user_ids() -> list:
    """
    Returns all user IDs (int)
    """
    return list(user_store.keys())
