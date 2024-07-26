from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Contact(AbstractBaseModel):
    name = models.CharField(_("Name"), max_length=255)
    email = models.EmailField(_("Email"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=255)
    phone2 = models.CharField(_("Phone2"), max_length=255)
    message = models.TextField(_("Message"))
    address = models.CharField(_("Address"), max_length=255)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return self.name
