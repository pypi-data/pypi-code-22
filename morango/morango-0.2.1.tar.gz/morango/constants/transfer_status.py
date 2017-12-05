"""
This module contains constants representing the possible stages of a transfer session.
"""
from django.utils.translation import ugettext_lazy as _

QUEUING = "queuing"
PUSHING_PULLING = ""
COMPLETED = "completed"
ERROR = "error"

choices = (
    (QUEUING, _("Queuing")),
    (PUSHING_PULLING, _("")),
    (COMPLETED, _("Completed")),
    (ERROR, _("Error")),
)
