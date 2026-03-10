ServiceMap Backend Blueprint
===========================

This repository contains a **blueprint** for the backend of a local services marketplace.  
The goal of this blueprint is to provide a solid starting point for building an Odoo‑based back‑end that
powers a mobile application where clients can discover nearby service providers, request services,
schedule work and handle payments.  

> **Note:**
> This code is intentionally incomplete.  It defines the structure, models, controllers and
> supporting files that you would expect in a production Odoo module, but it leaves out
> implementation details such as authentication, detailed business logic and full UI views.

## Contents

The blueprint is organised as follows:

- `service_map` – The core Odoo addon providing models, controllers and services.
- `docs/` – Technical documentation explaining the architecture, API and development guidelines.
- `docker-compose.yaml` – Example configuration for running Odoo with this addon and its
  dependencies (optional, included here as a reference).

To install and extend this module, consult the documentation in `docs/`.