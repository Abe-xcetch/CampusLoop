from django.db.models.signals import post_save
from django.dispatch import receiver
from core.users.infrastructure.orm_models import User, ReputationScore


@receiver(post_save, sender=User)
def create_user_reputation_profile(sender, instance, created, **kwargs):
    """
    Automatically instantiates a ReputationScore record for every newly synced user.
    """
    if created:
        ReputationScore.objects.get_or_create(user=instance)
