import requests
import websocket
import threading
import json
import time
import logging
from .config import MATTERMOST_URL, MATTERMOST_TOKEN, MATTERMOST_BOTNAME

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
        self.bot_id = None
        self.ws_client = WebSocketClient(self)
        self.message_listeners = []

    def connect(self):
        # Initialize and connect WebSocket client
        self.ws_client.add_message_listener(self.handle_websocket_event)
        self.ws_client.connect()
        logger.info("MattermostClient connected.")

    def handle_websocket_event(self, event_data):
        """
        Handles incoming WebSocket events and notifies listeners based on event type.
        :param event_data: The JSON-decoded event data from WebSocket.
        """
        event = event_data.get('event')
        if event == 'posted':
            self.notify_listeners(event_data)
        # Handle other event types as needed

    def notify_listeners(self, data):
        for listener in self.message_listeners:
            listener(data)

    def add_message_listener(self, callback):
        """
        Adds a listener for incoming messages.
        :param callback: Function to handle incoming messages.
        """
        self.message_listeners.append(callback)

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

    def get_file_info(self, file_id):
        response = requests.get(f"{self.url}/api/v4/files/{file_id}/info", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get file info: {response.status_code} - {response.text}")
            return None

    def download_file(self, file_id):
        response = requests.get(f"{self.url}/api/v4/files/{file_id}", headers=self.headers)
        if response.status_code == 200:
            file_path = f"/tmp/{file_id}"
            with open(file_path, 'wb') as f:
               f.write(response.content)
            logger.debug(f"File downloaded successfully to {file_path}.")
            return file_path
        else:
            logger.error(f"Failed to download file: {response.status_code} - {response.text}")
            return None

    def upload_file(self, channel_id, file_bytes, filename, mime_type='application/octet-stream'):
        """
        Uploads a file to a specified Mattermost channel.

        :param channel_id: ID of the channel where the file will be uploaded.
        :param file_bytes: Binary content of the file.
        :param filename: Name of the file.
        :param mime_type: MIME type of the file.
        :return: file_id if successful, None otherwise.
        """
        upload_url = f"{self.url}/api/v4/files"
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        files = {
            'files': (filename, file_bytes, mime_type)
        }
        data = {
            'channel_id': channel_id
        }

        logger.debug(f"Uploading file {filename} to channel {channel_id}.")
        try:
            response = requests.post(upload_url, headers=headers, files=files, data=data)
            if response.status_code == 201:
                json_response = response.json()
                file_infos = json_response.get('file_infos')
                file_id = file_infos[0].get('id')
                logger.debug(f"File uploaded successfully with ID: {file_id}")
                return file_id
            else:
                logger.error(f"Failed to upload file: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Exception during file upload: {e}")
            return None

    def close(self):
        """
        Closes the WebSocket connection and performs any necessary cleanup.
        """
        self.ws_client.close()
        logger.info("MattermostClient closed.")

class WebSocketClient:
    def __init__(self, mattermost_client):
        self.mm_client = mattermost_client
        self.message_listeners = []
        self.ws = None
        self.ws_thread = None
        self.reconnect_delay = 5  # seconds

    def connect(self):
        # Get bot ID first
        self.mm_client.bot_id = self.mm_client.get_me().get('id')
        if not self.mm_client.bot_id:
            logger.error("Failed to get bot ID. Check your token and permissions.")
            return

        # Establish WebSocket connection
        api_url = self.mm_client.url.replace('https', 'wss').replace('http', 'ws') + '/api/v4/websocket'
        logger.info(f"Connecting to Mattermost WebSocket at {api_url}")
        headers = [
            f"Authorization: Bearer {self.mm_client.token}"
        ]
        self.ws = websocket.WebSocketApp(
            api_url,
            header=headers,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.ws_thread.start()
        # Wait for connection establishment
        time.sleep(1)
        logger.info("WebSocket connection thread started.")

    def on_open(self, ws):
        logger.info("WebSocket connection opened.")

    def on_message(self, ws, message):
        try:
            event_data = json.loads(message)
            logger.debug(f"Received WebSocket message: {event_data}")
            for listener in self.message_listeners:
                listener(event_data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode WebSocket message: {e}")

    def on_error(self, ws, error):
        logger.error(f"WebSocket encountered error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.info(f"WebSocket connection closed. Code: {close_status_code}, Message: {close_msg}")
        logger.info(f"Attempting to reconnect in {self.reconnect_delay} seconds...")
        time.sleep(self.reconnect_delay)
        self.connect()

    def add_message_listener(self, callback):
        """
        Adds a listener for incoming WebSocket messages.
        :param callback: Function to handle incoming messages.
        """
        self.message_listeners.append(callback)

    def close(self):
        if self.ws:
            self.ws.close()
            self.ws_thread.join()
            logger.info("WebSocket connection closed and thread joined.")