"""REST API controllers for the ServiceMap module.

All endpoints defined here return JSON responses.  Authentication,
validation and error handling are kept minimal to serve as a starting
point for further development.
"""

from odoo import http
from odoo.http import request


class ServiceMapController(http.Controller):
    """Public API for the ServiceMap platform."""

    # ---------------------------------------------------------------------
    # Authentication
    # ---------------------------------------------------------------------

    @http.route('/api/auth/login', type='json', auth='public', methods=['POST'], csrf=False)
    def api_login(self, **kwargs):
        """Authenticate a user and return a token.

        Expected JSON payload:
        {
          "login": "user@example.com",
          "password": "secret"
        }

        Returns a dictionary with a token on success or an error message on
        failure.  The implementation of token generation and password
        verification is left as an exercise.
        """
        login = kwargs.get('login')
        password = kwargs.get('password')
        if not login or not password:
            return {'error': 'Missing credentials'}
        # TODO: validate credentials, generate token
        return {'status': 'success', 'token': 'dummy-token'}

    # ---------------------------------------------------------------------
    # Providers
    # ---------------------------------------------------------------------

    @http.route('/api/providers', type='json', auth='public', methods=['GET'], csrf=False)
    def api_providers(self, **params):
        """Return a list of service providers.

        Accepts optional filters such as category_id or name.  Returns a
        simplified structure containing provider id, name and rating.
        """
        domain = []
        category_id = params.get('category_id')
        if category_id:
            domain.append(('category_ids', 'in', int(category_id)))
        name = params.get('name')
        if name:
            domain.append(('partner_id.name', 'ilike', name))
        providers = request.env['service_map.provider'].sudo().search(domain)
        data = []
        for prov in providers:
            data.append({
                'id': prov.id,
                'name': prov.partner_id.name,
                'rating': prov.rating,
            })
        return {'providers': data}

    @http.route('/api/providers/nearby', type='json', auth='public', methods=['GET'], csrf=False)
    def api_providers_nearby(self, **params):
        """Return providers near a given location.

        Parameters:
        - latitude (float, required)
        - longitude (float, required)
        - radius_km (float, optional, default 10)
        - category_id (int, optional)

        Implementation of distance calculation belongs in the services
        layer; this controller simply collects the parameters and returns
        an empty list as a placeholder.
        """
        try:
            lat = float(params.get('latitude'))
            lon = float(params.get('longitude'))
        except (TypeError, ValueError):
            return {'error': 'latitude and longitude are required'}
        radius_km = float(params.get('radius_km', 10))
        category_id = params.get('category_id')
        # TODO: call a service to compute nearby providers
        providers = []
        return {'providers': providers}

    # ---------------------------------------------------------------------
    # Services
    # ---------------------------------------------------------------------

    @http.route('/api/services', type='json', auth='public', methods=['GET'], csrf=False)
    def api_services(self, **params):
        """Return a list of services.

        Optional filters:
        - category_id
        - provider_id
        """
        domain = []
        category_id = params.get('category_id')
        if category_id:
            domain.append(('category_id', '=', int(category_id)))
        provider_id = params.get('provider_id')
        if provider_id:
            domain.append(('provider_id', '=', int(provider_id)))
        services = request.env['service_map.service'].sudo().search(domain)
        data = []
        for serv in services:
            data.append({
                'id': serv.id,
                'name': serv.name,
                'provider_id': serv.provider_id.id,
                'category_id': serv.category_id.id,
                'price': serv.price,
                'price_unit': serv.price_unit,
            })
        return {'services': data}

    # ---------------------------------------------------------------------
    # Orders
    # ---------------------------------------------------------------------

    @http.route('/api/orders/create', type='json', auth='user', methods=['POST'], csrf=False)
    def api_order_create(self, **params):
        """Create a new service request.

        Expected JSON keys:
        - service_id
        - provider_id
        - scheduled_date (optional)
        - description (optional)
        - location { latitude, longitude } (optional)
        """
        required_fields = ['service_id', 'provider_id']
        for field in required_fields:
            if field not in params:
                return {'error': f'{field} is required'}
        client_partner = request.env.user.partner_id
        values = {
            'service_id': int(params['service_id']),
            'provider_id': int(params['provider_id']),
            'client_id': client_partner.id,
            'description': params.get('description'),
        }
        if params.get('scheduled_date'):
            values['scheduled_date'] = params['scheduled_date']
        location = params.get('location')
        if isinstance(location, dict):
            values['location_latitude'] = location.get('latitude')
            values['location_longitude'] = location.get('longitude')
        request_record = request.env['service_map.request'].sudo().create(values)
        return {'status': 'created', 'request_id': request_record.id}