from core.users.domain.models import UserDomainEntity
from core.users.infrastructure.repositories import UserRepositoryInterface


class RegisterUserUseCase:
    """
    Application Use Case executing User Profile synchronization
    upon initial Firebase Auth verification.
    """
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, user_id: str, email: str, first_name: str, last_name: str) -> UserDomainEntity:
        # Check if user already exists
        existing_user = self.user_repository.get_by_id(user_id)
        if existing_user:
            return existing_user

        # Create new domain aggregate
        new_user = UserDomainEntity(
            id=user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_verified=False # Initial registration is pending email confirmation
        )

        # Enforce validation
        new_user.validate_strathmore_email()

        # Persist through repository
        self.user_repository.save(new_user)
        return new_user
