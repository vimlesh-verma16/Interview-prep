"""
Functional Requirements (FR):

1. User Management
   - Register and login users
   - Manage user profile (username, avatar, status)

2. One-to-One Chat
   - Send and receive messages in real-time
   - Support text, image, video, file, emoji messages
   - Show read/unread status
   - Show online/offline status

3. Group Chat
   - Create, join, and leave groups
   - Group admins can add or remove members
   - Messages broadcasted to all group members
   - Support mentions using @username

4. Message Delivery Guarantees
   - Messages must be delivered reliably with acknowledgment and retries
   - Maintain message order per conversation
   - Prevent duplicate messages

5. Presence and Typing Indicators
   - Show when a user is online
   - Show typing indicators (e.g., "user is typing...")
   - Last seen timestamps

6. Notifications
   - Push notifications for new messages
   - Support mute chat and "Do Not Disturb" mode

7. Search
   - Search messages by keyword
   - Search users or groups by name

8. Message History
   - Store and retrieve message history
   - Support pagination or infinite scroll in chat

9. Media Handling
   - Upload, download, and preview media
   - Generate thumbnails, compress files

10. Security
    - End-to-end encryption (optional)
    - Support disappearing/expiring messages
    - Authentication and authorization

11. Admin Features (Optional)
    - Report and block users
    - Moderate group chats
    - Access logs (for enterprise/internal tools)
"""

# Real-Time Chat Application LLD in Python (Simplified OOP + Typing)

from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime


# -------------------- User Management --------------------
class User:
    def __init__(self, username: str, password_hash: str, avatar_url: str = ""):
        self.id: UUID = uuid4()
        self.username = username
        self.password_hash = password_hash
        self.avatar_url = avatar_url
        self.status = "offline"  # online/offline
        self.last_seen: Optional[datetime] = None

    def update_status(self, status: str):
        self.status = status
        self.last_seen = datetime.now()


# -------------------- Conversations --------------------
class Conversation:
    def __init__(self, is_group: bool = False, group_name: Optional[str] = None):
        self.id: UUID = uuid4()
        self.is_group = is_group
        self.group_name = group_name
        self.participants: List[UUID] = []
        self.group_admins: List[UUID] = []

    def add_user(self, user_id: UUID, is_admin: bool = False):
        if user_id not in self.participants:
            self.participants.append(user_id)
            if is_admin:
                self.group_admins.append(user_id)

    def remove_user(self, user_id: UUID):
        if user_id in self.participants:
            self.participants.remove(user_id)
        if user_id in self.group_admins:
            self.group_admins.remove(user_id)


# -------------------- Messages --------------------
class Message:
    def __init__(
        self,
        sender_id: UUID,
        conversation_id: UUID,
        content: str,
        message_type: str = "text",
        media_url: Optional[str] = None,
        mentions: Optional[List[UUID]] = None,
    ):
        self.id: UUID = uuid4()
        self.sender_id = sender_id
        self.conversation_id = conversation_id
        self.content = content
        self.media_url = media_url
        self.message_type = message_type  # text, image, video, file, emoji
        self.timestamp = datetime.now()
        self.status = "sent"  # sent, delivered, read
        self.mentions = mentions or []


# -------------------- Typing Indicator --------------------
class TypingIndicator:
    def __init__(self, user_id: UUID, conversation_id: UUID):
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.is_typing = False


# -------------------- Notification --------------------
class Notification:
    def __init__(self, user_id: UUID):
        self.user_id = user_id
        self.message_ids: List[UUID] = []
        self.is_muted = False
        self.do_not_disturb = False

    def notify(self, message_id: UUID):
        if not self.is_muted and not self.do_not_disturb:
            self.message_ids.append(message_id)


# -------------------- Media --------------------
class Media:
    def __init__(
        self,
        message_id: UUID,
        media_type: str,
        file_path: str,
        thumbnail_url: Optional[str] = None,
    ):
        self.id: UUID = uuid4()
        self.message_id = message_id
        self.media_type = media_type
        self.file_path = file_path
        self.thumbnail_url = thumbnail_url
        self.uploaded_at = datetime.now()


# -------------------- Admin Tools --------------------
class Admin:
    def __init__(self):
        self.blocked_users: List[UUID] = []
        self.reported_users: List[UUID] = []

    def block_user(self, user_id: UUID):
        if user_id not in self.blocked_users:
            self.blocked_users.append(user_id)

    def report_user(self, user_id: UUID):
        if user_id not in self.reported_users:
            self.reported_users.append(user_id)


# -------------------- Example Usage --------------------
if __name__ == "__main__":
    # Create users
    alice = User("alice", "hashed_pwd_123")
    bob = User("bob", "hashed_pwd_456")

    # Create one-to-one conversation
    convo = Conversation()
    convo.add_user(alice.id)
    convo.add_user(bob.id)

    # Alice sends a message
    message = Message(sender_id=alice.id, conversation_id=convo.id, content="Hi Bob!")

    # Bob is typing
    typing = TypingIndicator(user_id=bob.id, conversation_id=convo.id)
    typing.is_typing = True

    # Notification example
    notif = Notification(user_id=bob.id)
    notif.notify(message.id)

    # Admin blocks a user
    admin = Admin()
    admin.block_user(bob.id)

    print("Conversation ID:", convo.id)
    print("Message content:", message.content)
    print("Typing status:", typing.is_typing)
    print("Notifications:", notif.message_ids)
    print("Blocked users:", admin.blocked_users)
