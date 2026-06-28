from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


class DomainValidationError(Exception):
    pass


@dataclass
class UserDomainEntity:
    """
    Pure Python Domain Entity for a User.
    Decoupled from Django ORM database mechanics.
    """
    id: str  # Firebase UID
    email: string
    first_name: string
    last_name: string
    role: str = "STUDENT"
    is_verified: bool = False
    is_active: bool = True
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def validate_strathmore_email(self):
        """
        Enforce Strathmore domain validation at the domain layer
        """
        valid_suffixes = ("@strathmore.edu", "@su.strathmore.edu", "@alumni.strathmore.edu")
        if not self.email.endswith(valid_suffixes):
            raise DomainValidationError("Only Strathmore email addresses are authorized.")

    def upgrade_to_admin(self):
        self.role = "ADMIN"
        self.updated_at = datetime.utcnow()

    def deactivate_account(self):
        self.is_active = False
        self.updated_at = datetime.utcnow()


@dataclass
class VerificationDomainEntity:
    id: str
    user_id: str
    is_email_verified: bool = False
    verified_at: Optional[datetime] = None
    verification_token: Optional[str] = None
    expires_at: Optional[datetime] = None
