import requests
import websocket
import threading
import json
import time
import logging
from config import MATTERMOST_URL, MATTERMOST_TOKEN, MATTERMOST_BOTNAME

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MattermostClient:
    def __init__(self):
        self.url = MATTERMOST_URL.rstrip('/')
        self.token = MATTERMOST_TOKEN
        self.botname = MATTERMOST_BOTNAME
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.ws = None
        self.ws_thread = None
        self.message_listeners = []
        self.bot_id = None

    def connect(self):
        # Get bot ID first
        self.bot_id = self.get_me().get('id')
        if not self.bot_id:
            logger.error("Failed to get bot ID. Check your token and permissions.")
            return

        # Establish WebSocket connection
        api_url = self.url + '/api/v4/websocket'
        params = {
            'token': self.token
        }
        ws_url = api_url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
        logger.info(f"Connecting to Mattermost WebSocket at {ws_url}")
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()
        # Wait for connection establishment
        time.sleep(1)
        logger.info("Connected to Mattermost WebSocket.")

    def post_message(self, channel_id, message, root_id=None, file_ids=None, props=None):
        """
        Sends a message to a specified Mattermost channel.
        :param channel_id: ID of the channel.
        :param message: The message text.
        :param root_id: (Optional) ID of the root post for threaded messages.
        :param file_ids: (Optional) List of file IDs to attach.
        :param props: (Optional) Additional properties for the post.
        :return: JSON response from Mattermost.
        """
        payload = {
            'channel_id': channel_id,
            'message': message
        }
        if root_id:
            payload['root_id'] = root_id
        if file_ids:
            payload['file_ids'] = file_ids
        if props:
            payload['props'] = props

        logger.debug(f"Sending payload: {json.dumps(payload, indent=2)}")
        response = requests.post(f"{self.url}/api/v4/posts", headers=self.headers, json=payload)
        if response.status_code == 201:
            logger.debug(f"Message posted successfully to channel {channel_id}.")
            return response.json()
        else:
            logger.error(f"Failed to post message: {response.status_code} - {response.text}")
            return None

    def get_users(self):
        """
        Retrieves the list of users.
        :return: JSON response with users details.
        """
        response = requests.get(f"{self.url}/api/v4/users", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get the list of users: {response.status_code} - {response.text}")
            return None

    def get_user(self, user_id):
        """
        Retrieves user information by user ID.
        :param user_id: The Mattermost user ID.
        :return: JSON response with user details.
        """
        response = requests.get(f"{self.url}/api/v4/users/{user_id}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get user {user_id}: {response.status_code} - {response.text}")
            return None

    def get_me(self):
        """
        Retrieves information about the bot itself.
        :return: JSON response with bot user details.
        """
        response = requests.get(f"{self.url}/api/v4/users/me", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get bot user info: {response.status_code} - {response.text}")
            return None

    def get_direct_channel_id(self, user_id):
        bot_id = self.get_me().get('id')
        logger.debug(f"Bot ID: {bot_id}")
        logger.debug(f"Target User ID: {user_id}")

        if not bot_id or not user_id:
            logger.error("One of the user IDs is invalid.")
            return None

        # Send payload as a JSON array
        payload = [bot_id, user_id]
        logger.debug(f"Payload being sent: {json.dumps(payload)}")

        response = requests.post(f"{self.url}/api/v4/channels/direct", headers=self.headers, json=payload)
        logger.debug(f"Direct channel response: {response.status_code} - {response.text}")

        if response.status_code in [200, 201]:
            channel = response.json()
            logger.debug(f"Direct channel created with ID: {channel['id']}")
            return channel['id']
        else:
            logger.error(f"Failed to get/create direct channel: {response.status_code} - {response.text}")
            return None

class WebSocketClient:
    def __init__(self, mattermost_client):
        self.mm_client = mattermost_client
        self.listeners = []

    def connect(self):
        self.mm_client.connect()

    def add_message_listener(self, callback):
        """
        Adds a listener for incoming messages.
        :param callback: Function to handle incoming messages.
        """
        self.mm_client.add_message_listener(callback)

    def post_message(self, channel_id, message, root_id=None, file_ids=None, props=None):
        """
        Sends a message via the Mattermost client.
        """
        self.mm_client.post_message(channel_id, message, root_id, file_ids, props)

    def get_user(self, user_id):
        return self.mm_client.get_user(user_id)

    def get_me(self):
        return self.mm_client.get_me()

    def get_direct_channel_id(self, user_id):
        return self.mm_client.get_direct_channel_id(user_id)

    def close(self):
        if self.mm_client.ws:
            self.mm_client.ws.close()