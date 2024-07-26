from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class StatusChoices(TextChoices):
    PENDING = "Pending", _("Pending")
    APPROVED = "Approved", _("Approved")
    REJECTED = "Rejected", _("Rejected")
    CANCELLED = "Cancelled", _("Cancelled")
