Development Guidelines
======================

The ServiceMap backend blueprint follows Odoo development conventions.
Adhering to these guidelines will help maintain code quality and ease future
maintenance.

## General Principles

1. **Modular design** – Break features into separate models, controllers and
   services where possible.  Do not put all logic in a single file.
2. **Reuse core models** – Extend existing Odoo models via `_inherit`
   when adding fields to `res.partner`, `mail.message`, etc.  Only create
   entirely new models when necessary.
3. **Avoid business logic in controllers** – Controllers should validate
   input and delegate to models or services for processing.  This pattern
   makes your code easier to test and reuse (e.g. via RPC or cron jobs).
4. **Use the ORM** – Always access the database through Odoo’s ORM
   (search, browse, write) instead of raw SQL when possible.  The ORM
   automatically handles permissions and caching.
5. **Internationalisation** – Wrap user‑facing strings in `_()` so they
   can be translated.  Declare `translate=True` on Char fields where
   appropriate.
6. **Security first** – Define ACLs and record rules early.  Do not
   expose endpoints or fields without considering who should have access.

## Coding Standards

* Follow PEP 8 for Python code (indentation, naming conventions).  Odoo uses
  snake_case for variables and methods.
* Name models using `service_map.<entity>` and provide `_description` for
  clarity.
* Use meaningful XML IDs (e.g. `service_map.group_service_provider`) for
  records in data files.  IDs must be unique within the module.
* Keep controllers thin.  Return JSON via Python dictionaries; Odoo will
  serialise them automatically for `type='json'` routes.
* Document your API endpoints with comments describing expected inputs and
  outputs.  Consider using `pydantic` or custom validation for complex
  payloads.

## Extending the Blueprint

* **Authentication** – Implement authentication using Odoo’s session
  mechanism or JWT tokens.  You may store tokens in `ir.config_parameter`
  or in a dedicated model.
* **Geolocation** – To implement the `/api/providers/nearby` endpoint,
  extend the provider model with latitude/longitude fields and use a
  geospatial library in the services layer to compute distances.
* **Payments** – Integrate with a payment provider (e.g. Stripe, Adyen)
  by implementing a service that creates payment sessions and updates
  `service_map.payment` records accordingly.  Use Odoo’s accounting
  features for invoicing when appropriate.
* **Scheduling** – Add models for provider availability and scheduling
  constraints, and expose endpoints for clients to pick time slots.
* **Dashboards** – Build custom views and dashboards in the `views/`
  directory using Odoo’s XML view architecture.  Use `@api.model` methods
  to provide calculated fields.

## Testing

Write unit tests for your models and services using Odoo’s testing framework.
Tests reside in a `tests/` directory at the module root.  The blueprint
doesn’t include tests, but adding them early will help catch regressions.

## Contributions

If multiple developers work on this module, set up a version control
workflow (e.g. Git branching and pull requests) and code review process.
Document any additional conventions in this folder.
