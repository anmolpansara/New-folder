from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    ACTIVE = "active", _("Active")
    PENDING = "pending", _("Pending")
    DEACTIVE = "deactive", _("Deactive")


class UserRoleChoices(models.IntegerChoices):
    ADMIN = 1, _("Admin")
    SUPPORT = 2, _("Support")
    CLIENT = 3, _("Client")


class QueryTypeChoice(models.IntegerChoices):
    INSTALLATION = 1, _("Installation")
    SERVICE = 2, ("Service")
    SPARES = 3, ("Spares")
    SALES_INQUIRY = 4, ("Sales_inquiry")
    OTHERS = 5, ("Others")


class PriorityChoice(models.TextChoices):
    LOW = "low", ("Low")
    MEDIUM = "medium", ("Medium")
    HIGH = "high", ("High")
