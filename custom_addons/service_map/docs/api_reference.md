API Reference
=============

This document provides an overview of the REST‑style endpoints exposed by the
`service_map` addon.  Each endpoint is implemented in `service_map/controllers/api.py`.

> **Important:** The following definitions are provisional and
> intentionally simplified.  In a real implementation you should handle
> authentication, input validation, pagination, error handling and proper
> HTTP status codes.

## Authentication

Authentication is expected to be token‑based.  Clients should supply an
authentication token in the `Authorization` header for protected endpoints.
The `/api/auth/login` endpoint returns such a token.  Token generation and
verification must be implemented.

### `POST /api/auth/login`

Authenticate a user.

**Request body (JSON)**

```
{
  "login": "user@example.com",
  "password": "secret"
}
```

**Response (JSON)**

```
{
  "status": "success",
  "token": "..."
}
```

On failure, return an appropriate error message and status.

## Providers

### `GET /api/providers`

Return a list of providers.  Optional query parameters:

- `category_id`: Filter providers who offer services in this category.
- `name`: Search by provider name.

**Response**

```
{
  "providers": [
    {
      "id": 1,
      "name": "Jane Doe",
      "rating": 4.8
    },
    ...
  ]
}
```

### `GET /api/providers/nearby`

Return providers near a given location.  Query parameters:

- `latitude` (required)
- `longitude` (required)
- `radius_km` – search radius in kilometres (default 10)
- `category_id` – optional category filter

The backend should compute distances (e.g. via Haversine formula) and filter
providers accordingly.  Implementation belongs in the services layer.

**Response**

```
{
  "providers": [
    {
      "id": 2,
      "name": "Fix‑it Fast",
      "distance_km": 3.2,
      "rating": 4.5
    },
    ...
  ]
}
```

## Services

### `GET /api/services`

List services offered by providers.  Query parameters:

- `category_id` – filter by category
- `provider_id` – filter by provider

**Response**

```
{
  "services": [
    {
      "id": 10,
      "name": "Electrical Repair",
      "provider_id": 1,
      "category_id": 5,
      "price": 50.0,
      "price_unit": "hour"
    },
    ...
  ]
}
```

## Orders (Service Requests)

### `POST /api/orders/create`

Create a new service request.  Requires authentication.

**Request body (JSON)**

```
{
  "service_id": 10,
  "provider_id": 1,
  "scheduled_date": "2026-03-15T09:00:00Z",
  "description": "Fix my leaking tap",
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194
  }
}
```

**Response**

```
{
  "status": "created",
  "request_id": 42
}
```

### `GET /api/orders/<request_id>`

Retrieve the details of a specific request.  Only the client who created the
request or the assigned provider should be able to access it.  Security rules
must enforce this behaviour.

## Reviews

### `POST /api/reviews`

Create a review for a completed request.  Requires authentication.  Only the
client assigned to the request may create a review and only once per
request.

**Request body**

```
{
  "request_id": 42,
  "rating": 5,
  "comment": "Excellent work!"
}
```

**Response**

```
{
  "status": "success"
}
```

## Favourites

### `POST /api/favourites`

Add a provider to the client’s favourites list.

```
{
  "provider_id": 1
}
```

### `DELETE /api/favourites/<provider_id>`

Remove a favourite provider.

## Payments

Payment integration is intentionally left open.  A future implementation
should define endpoints such as:

* `POST /api/payments/create` – initiate a payment transaction for a request.
* `GET /api/payments/status` – check the status of a transaction.

Actual integration with a payment gateway should be encapsulated in the
services layer and leverage Odoo’s accounting features where appropriate.
