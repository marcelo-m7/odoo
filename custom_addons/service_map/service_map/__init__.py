"""Initialize the service_map module.

This file imports subpackages so that Odoo registers the models and
controllers when the module is loaded.
"""

from . import models
from . import controllers
from . import services