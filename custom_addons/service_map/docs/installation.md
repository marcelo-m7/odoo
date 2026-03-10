Installation Guide
==================

This guide explains how to install the `service_map` addon on an Odoo
instance and how to run it using the provided Docker configuration.  The
instructions assume familiarity with Odoo administration and access to an
environment where you can run Docker containers.

## Prerequisites

* **Odoo 16 or 17/18/19** – The module is designed for recent Odoo versions.
  Adjust the base image in `docker-compose.yaml` if necessary.
* **Python 3.10+** – Required if running Odoo directly on your host.
* **PostgreSQL** – Odoo’s database backend.

## Installation Using Docker

1. Clone or download this blueprint repository.
2. Copy the `service_map` addon into the Odoo addons path.  When using
   the provided `docker-compose.yaml`, the `extra-addons` volume will be
   populated automatically.
3. Run the containers:

   ```shell
   docker compose up -d
   ```

4. Once Odoo is running, log in to the Odoo web UI with an administrator
   account.
5. Activate developer mode and update the app list (Apps → Update Apps List).
6. Search for **Service Map** and install the module.

## Manual Installation

If you prefer not to use Docker:

1. Ensure that Odoo and PostgreSQL are installed and configured on your host.
2. Copy the `service_map` directory into your Odoo addons path (e.g.
   `/odoo/custom-addons/service_map`).
3. Update your Odoo configuration file (`addons_path`) to include the
   directory where you placed the addon.
4. Restart Odoo.
5. Activate developer mode, update the app list, search for **Service Map**
   and install it.

## Next Steps

After installation you can start exploring the data models using the Odoo
backend (Settings → Technical → Database Structure → Models) and test the API
endpoints using a tool such as Postman.  The module currently provides
skeleton functionality; you will need to implement authentication, business
logic and UI views to make the platform production ready.
