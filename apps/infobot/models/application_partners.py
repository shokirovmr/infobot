from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.infobot.choices import StatusChoices
from apps.shared.models import AbstractBaseModel


class ApplicationPartner(AbstractBaseModel):
    full_name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    phone = models.CharField(max_length=255, verbose_name=_("Phone"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    message = models.TextField(verbose_name=_("Message"), blank=True, null=True)
    status = models.CharField(
        choices=StatusChoices.choices, default=StatusChoices.PENDING, max_length=30
    )

    def __str__(self):
        return self.full_name if self.full_name else self.phone

    class Meta:
        verbose_name = _("Application Partner")
        verbose_name_plural = _("Application Partners")
