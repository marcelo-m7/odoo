"""Aggregate model initialisation.

Import each model so that Odoo can register them on module load.
"""

from . import service_provider
from . import service_category
from . import service
from . import service_request
from . import review
from . import favorite
from . import payment
from . import message