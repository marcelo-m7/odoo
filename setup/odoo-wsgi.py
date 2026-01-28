# WSGI Handler sample configuration file.
#
# Change the appropriate settings below, in order to provide the parameters
# that would normally be passed in the command-line.
# (at least conf['addons_path'])
#
# For generic wsgi handlers a global application is defined.
# For uwsgi this should work:
#   $ uwsgi_python --http :9090 --pythonpath . --wsgi-file odoo-wsgi.py
#
# For gunicorn additional globals need to be defined in the Gunicorn section.
# Then the following command should run:
#   $ gunicorn odoo.http:root --pythonpath . -c odoo-wsgi.py

from dotenv import load_dotenv
import os
from odoo.http import root as application  # noqa: F401
from odoo.tools import config as conf  # noqa: F401

# ----------------------------------------------------------
# Common
# ----------------------------------------------------------

# Load environment variables from a .env file
load_dotenv()

# Path to the Odoo Addons repository (comma-separated for
# multiple locations)
conf['addons_path'] = './odoo/addons,./addons, ./custom_addons' 

# DB via .env.local / env vars
conf["db_host"] = os.getenv("ODOO_DB_HOST", os.getenv("DB_HOST", "127.0.0.1"))
conf["db_port"] = int(os.getenv("ODOO_DB_PORT", os.getenv("DB_PORT", "5432")))
conf["db_user"] = os.getenv("ODOO_DB_USER", os.getenv("DB_USER", "odoo"))
conf["db_password"] = os.getenv("ODOO_DB_PASSWORD", os.getenv("DB_PASSWORD", ""))

# opcional: se você quiser travar num database específico
db_name = os.getenv("ODOO_DB_NAME", os.getenv("DB_NAME"))
if db_name:
    conf["db_name"] = db_name

# ----------------------------------------------------------
# Initializing the server
# ----------------------------------------------------------

application.initialize()

# ----------------------------------------------------------
# Gunicorn
# ----------------------------------------------------------
# Standard port is 8069
bind = '127.0.0.1:8069'
pidfile = '.gunicorn.pid'
workers = 4
timeout = 240
max_requests = 2000
