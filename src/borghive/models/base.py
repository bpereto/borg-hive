from django.db import models


class BaseModel(models.Model):
    """base model for all borghive models"""

    created = models.DateTimeField(auto_now_add=True)

    class Meta():
        abstract = True
