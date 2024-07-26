from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class CompanyInfo(AbstractBaseModel):
    name = models.CharField(max_length=200, verbose_name=_("Company Name"))
    address = models.CharField(max_length=200, verbose_name=_("Address"))
    phone = models.CharField(max_length=200, verbose_name=_("Phone"))
    email = models.EmailField(verbose_name=_("Email"))
    website = models.URLField(verbose_name=_("Website"))
    description = models.TextField(verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Company Info")
        verbose_name_plural = _("Company Info")

    def __str__(self):
        return self.name
