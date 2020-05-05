from django.db import models
from rules.contrib.models import RulesModelBase, RulesModelMixin

class BaseModel(RulesModelMixin, models.Model, metaclass=RulesModelBase):
    created     = models.DateTimeField(auto_now_add=True)

    class Meta():
        abstract = True
