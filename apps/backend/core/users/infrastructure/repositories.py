from abc import ABC, abstractmethod
from typing import Optional
from core.users.domain.models import UserDomainEntity
from core.users.infrastructure.orm_models import User as ORMUser


class UserRepositoryInterface(ABC):
    """
    Abstract Port defining core database mutations and queries
    for the User aggregate. Decoupled from Django ORM.
    """
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[UserDomainEntity]:
        pass

    @abstractmethod
    def save(self, user: UserDomainEntity) -> None:
        pass


class DjangoUserRepository(UserRepositoryInterface):
    """
    Concrete Adapter implementing persistence using Django ORM.
    """
    def _to_domain(self, orm_user: ORMUser) -> UserDomainEntity:
        return UserDomainEntity(
            id=orm_user.id,
            email=orm_user.email,
            first_name=orm_user.first_name,
            last_name=orm_user.last_name,
            role=orm_user.role,
            is_verified=orm_user.is_verified,
            is_active=orm_user.is_active,
            avatar_url=orm_user.avatar_url,
            phone_number=orm_user.phone_number,
            created_at=orm_user.created_at,
            updated_at=orm_user.updated_at
        )

    def get_by_id(self, user_id: str) -> Optional[UserDomainEntity]:
        try:
            orm_user = ORMUser.objects.get(id=user_id)
            return self._to_domain(orm_user)
        except ORMUser.DoesNotExist:
            return None

    def save(self, user: UserDomainEntity) -> None:
        # Validate domain constraints before saving
        user.validate_strathmore_email()
        
        ORMUser.objects.update_or_create(
            id=user.id,
            defaults={
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "is_verified": user.is_verified,
                "is_active": user.is_active,
                "avatar_url": user.avatar_url,
                "phone_number": user.phone_number,
            }
        )
