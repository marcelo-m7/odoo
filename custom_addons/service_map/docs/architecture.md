Architecture Overview
=====================

This document describes the high‑level architecture of the ServiceMap backend.  The goal
is to present a modular and extensible design that follows Odoo development
conventions and can evolve into a full operational ecosystem for local service
providers and their clients.

## High‑Level Design

The ServiceMap backend is implemented as a single Odoo addon (`service_map`) that
acts as the **core operational system** for the marketplace.  It provides:

* **Data models** representing providers, categories, services, service requests,
  reviews, favourites, payments and messages.  These models extend Odoo’s ORM
  (`models.Model`) and integrate with standard models such as `res.partner` for
  contact information.
* **API controllers** exposing REST‑style endpoints under `/api/…` to allow a
  mobile application (or other clients) to consume the data.  Controllers use
  Odoo’s `http.Controller` infrastructure and return JSON responses.
* **Security configuration** defining groups, access control lists (ACLs) and
  record rules to ensure that data is accessed only by authorised users.
* **Services layer** (currently just a placeholder) for encapsulating business
  logic that does not belong in the models or controllers.  This separation
  facilitates unit testing and reuse.

The module can be installed on a stock Odoo instance.  No existing models
are duplicated; instead, the new models link to Odoo’s base models (e.g.
`res.partner`) via Many2one relationships.  This design makes it easy to
integrate later with Odoo’s CRM, invoicing and accounting apps.

## Components

### Data Models

| Model                    | Purpose                                                               |
|--------------------------|-----------------------------------------------------------------------|
| `service_map.provider`   | Represents a service provider (autonomous professional or business).  |
| `service_map.category`   | Hierarchical taxonomy of service categories.                          |
| `service_map.service`    | Individual service offered by a provider.                             |
| `service_map.request`    | A service request (order) placed by a client.                         |
| `service_map.review`     | Rating and comment left after service completion.                     |
| `service_map.favorite`   | Bookmark linking a client to a provider.                              |
| `service_map.payment`    | Payment information for a request.                                    |
| `service_map.message`    | Simple chat message tied to a request (placeholder).                  |

These models live in `service_map/models/` and are declared in separate Python
files for clarity.  Each model defines its fields, relationships and a few
placeholders for business methods (e.g. computing ratings or transitioning
states).  Models inherit from `mail.thread` and/or `mail.activity.mixin` where
appropriate to enable chatter and activities.

### API Controllers

Controllers in `service_map/controllers/api.py` expose endpoints such as:

* `POST /api/auth/login` – authenticate a user and return a token (placeholder).
* `GET /api/providers` – list providers.  Accepts optional filters.
* `GET /api/providers/nearby` – list providers near a location (to be
  implemented using geolocation logic).
* `GET /api/services` – list services with optional filters.
* `POST /api/orders/create` – create a service request.

Each route is annotated with comments describing expected request payloads and
responses.  The controllers currently return minimal JSON structures; actual
implementation will need to handle authentication, parameter validation and
error management.

### Security

The `security/` directory contains:

* `ir.model.access.csv` – Basic ACL definitions granting read/write/create
  permissions to users and administrators.  These entries should be refined
  according to your business rules.  Each line references an `ir.model`
  record which is automatically created by Odoo when you install the module.
* `service_map_security.xml` – Example groups (`Service Provider` and `Service
  Client`) and a placeholder for record rules.  Record rules allow you to
  restrict access to records based on the owner (e.g. a provider should only
  see their own services and requests).  Additional rules can be added here
  during implementation.

### Services Layer

A `services/` package is included for business logic that does not belong in
models or controllers.  For example, you might implement a service to
calculate distances between coordinates, to integrate with a payment gateway or
to manage the order workflow.  Keeping such logic in separate classes makes
unit testing easier and prevents bloating the models.

## Extensibility

The blueprint is designed to be extended:

1. **New models** can be added in the `models/` directory, imported through
   `models/__init__.py` and referenced in the manifest.  Always extend
   existing Odoo models via inheritance when appropriate (e.g. to add fields to
   `res.partner`).
2. **API routes** can be added by defining new methods on the controller class
   or by creating additional controller classes.  Use `auth='user'` for
   authenticated endpoints.
3. **Business logic** can be moved from controllers into the services layer to
   maintain separation of concerns.
4. **Views** (tree, form, kanban, etc.) can be defined in `views/*.xml` if you
   intend to manage data through the Odoo web UI.  They are omitted here but
   the manifest includes a placeholder for a views file.
5. **Integrations** with payments or geolocation can be added by creating
   services and hooking them into the existing models/controllers.  Keep
   external integrations loosely coupled to facilitate maintenance.

## Future Evolution

In later iterations you can evolve this module into a full
“super‑app” backend by:

* Integrating with Odoo’s **accounting** and **invoicing** modules to generate
  invoices and manage payments.
* Extending `res.partner` to store MEI/Recibos Verdes information.
* Implementing a **CRM dashboard** for service providers using Odoo’s
  activities and pipelines.
* Adding **analytics dashboards** via Odoo’s reporting tools.
* Implementing **notifications** (email or push) using the `mail` module.
