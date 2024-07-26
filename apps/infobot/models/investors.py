from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Investor(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    logo = models.ImageField(upload_to="investors/", verbose_name=_("Logo"))

    class Meta:
        verbose_name = _("Investor")
        verbose_name_plural = _("Investors")

    def __str__(self):
        return self.name
