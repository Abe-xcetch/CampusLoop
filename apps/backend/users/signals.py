from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User


@receiver(post_save, sender=User)
def create_user_reputation_profile(sender, instance, created, **kwargs):
    if created:
        from reputation.models import ReputationScore

        ReputationScore.objects.get_or_create(user=instance)
