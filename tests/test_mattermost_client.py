import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mattermost_client import MattermostClient
import logging

logging.basicConfig(level=logging.DEBUG)

def test_mattermost_client():
    mm_client = MattermostClient()

    # Test get_me
    me = mm_client.get_me()
    if me:
        print("Bot User Info:", me)
    else:
        print("Failed to get bot user info. Check your token and permissions.")
        return

    # # Fetch other users
    users = mm_client.get_users()
    if not users:
        print("Failed to retrieve users.")
        return

    # Exclude the bot user
    # if user is not me and user doesn't include a key called 'is_bot'
    other_users = [user for user in users if (user['id'] != me['id']) and (user.get('is_bot') is None)]
    if not other_users:
        print("No other users found to create a direct channel with.")
        return

    other_user_id = other_users[0]['id']
    user_info = mm_client.get_user(other_user_id)
    if user_info:
        print("Other User Info:", user_info)
    else:
        print("Failed to get other user info.")
        return

    # Test direct channel
    direct_channel_id = mm_client.get_direct_channel_id(other_user_id)
    if direct_channel_id:
        print("Direct Channel ID:", direct_channel_id)
    else:
        print("Failed to get direct channel ID.")
        return

    # Test posting a message
    response = mm_client.post_message(
        channel_id=direct_channel_id,
        message="Hello from the Mattermost client!",
        root_id=None,
        file_ids=None,
        props=None
    )
    if response:
        print("Post Message Response:", response)
    else:
        print("Failed to post message.")

if __name__ == "__main__":
    test_mattermost_client()