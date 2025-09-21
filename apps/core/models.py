from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampedModel(models.Model):
    """
    Abstract base model with created and modified timestamps
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
