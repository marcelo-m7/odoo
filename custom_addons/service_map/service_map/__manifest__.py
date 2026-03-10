{
    'name': 'Service Map',
    'summary': 'Local services marketplace backend',
    'version': '0.1',
    'description': """
Core backend for the ServiceMap platform.

This module provides data models, API controllers and security rules to
operate a marketplace where clients can discover nearby providers,
request services, schedule work and process payments.  It is designed to
be extended with additional functionality such as payment integration,
geolocation search, provider dashboards and CRM features.
""",
    'author': 'Your Company',
    'website': 'https://example.com',
    'category': 'Services',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/service_map_security.xml',
        'data/service_map_data.xml',
        # 'views/service_map_views.xml',  # Uncomment when you add views
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}