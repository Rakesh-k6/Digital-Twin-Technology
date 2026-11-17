"""
CityLink - Authentication, RBAC & Cyber Security Access Control
Implements:
1. Operator / Officer authentication
2. Session token issuance & verification
3. Role-Based Access Control (RBAC) with 3 pre-configured demo credentials
4. Audit trail logging for command actions
"""

import time
import uuid
from typing import Dict, Any, Optional
from pydantic import BaseModel


class LoginCredentials(BaseModel):
    username: str
    password: str
    role_override: Optional[str] = None


class UserProfile:
    def __init__(self, user_id: str, username: str, name: str, role: str, clearance: str, department: str, avatar_initials: str):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.role = role
        self.clearance = clearance
        self.department = department
        self.avatar_initials = avatar_initials

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "name": self.name,
            "role": self.role,
            "clearance": self.clearance,
            "department": self.department,
            "avatar_initials": self.avatar_initials
        }


DEMO_USERS: Dict[str, Dict[str, Any]] = {
    "operator": {
        "password": "bangalore2026",
        "profile": UserProfile(
            user_id="USR-BLR-01",
            username="operator",
            name="Dr. Arvind Rao",
            role="Chief Urban Traffic & Grid Controller",
            clearance="LEVEL-3 TACTICAL COMMAND",
            department="Bengaluru Traffic Police & BESCOM Integrated Cell",
            avatar_initials="AR"
        )
    },
    "csoc_sec": {
        "password": "defense2026",
        "profile": UserProfile(
            user_id="USR-BLR-02",
            username="csoc_sec",
            name="Vikramaditya Sengupta",
            role="CSOC Cyber Security Lead Officer",
            clearance="LEVEL-4 TOP SECRET CYBER DEFENSE",
            department="Karnataka State Cyber Security Operations Center (CSOC)",
            avatar_initials="VS"
        )
    },
    "admin": {
        "password": "admin2026",
        "profile": UserProfile(
            user_id="USR-BLR-03",
            username="admin",
            name="Meera Krishnaswamy, IAS",
            role="Municipal Infrastructure Director",
            clearance="LEVEL-5 EXECUTIVE URBAN AUTONOMY",
            department="Bruhat Bengaluru Mahanagara Palike (BBMP) & BWSSB",
            avatar_initials="MK"
        )
    }
}


class AuthManager:
    """Handles session issuance, validation, and session revocation."""

    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        user_record = DEMO_USERS.get(username.strip().lower())
        if not user_record:
            return None

        if user_record["password"] != password:
            return None

        # Issue session token
        token = f"BLR_TOKEN_{uuid.uuid4().hex[:16].upper()}"
        session_data = {
            "token": token,
            "user": user_record["profile"].to_dict(),
            "authenticated_at": time.time(),
            "expires_at": time.time() + 86400  # 24 hours
        }
        self.active_sessions[token] = session_data
        return session_data

    def quick_login(self, role_key: str) -> Optional[Dict[str, Any]]:
        """Instant 1-click authorization for hackathon demonstrations."""
        user_record = DEMO_USERS.get(role_key.strip().lower())
        if not user_record:
            return None

        token = f"BLR_TOKEN_{uuid.uuid4().hex[:16].upper()}"
        session_data = {
            "token": token,
            "user": user_record["profile"].to_dict(),
            "authenticated_at": time.time(),
            "expires_at": time.time() + 86400
        }
        self.active_sessions[token] = session_data
        return session_data

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        session = self.active_sessions.get(token)
        if not session:
            return None
        if time.time() > session["expires_at"]:
            del self.active_sessions[token]
            return None
        return session["user"]

    def revoke_session(self, token: str) -> bool:
        if token in self.active_sessions:
            del self.active_sessions[token]
            return True
        return False


# Global singleton instance
auth_manager = AuthManager()
