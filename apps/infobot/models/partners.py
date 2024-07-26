from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Partner(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    logo = models.ImageField(upload_to="partners/", verbose_name=_("Logo"))

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")

    def __str__(self):
        return self.name
