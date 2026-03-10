"""Service model.

Represents a single service offering by a provider.  A provider can offer
multiple services; each service belongs to exactly one category.
"""

from odoo import models, fields


class Service(models.Model):
    _name = 'service_map.service'
    _description = 'Service'

    name = fields.Char(required=True)
    provider_id = fields.Many2one(
        'service_map.provider',
        string='Provider',
        required=True,
        ondelete='cascade',
    )
    category_id = fields.Many2one(
        'service_map.category',
        string='Category',
        required=True,
        ondelete='restrict',
    )
    description = fields.Text()
    price = fields.Float(help='Base price or hourly rate.')
    price_unit = fields.Selection(
        [
            ('fixed', 'Fixed'),
            ('hour', 'Per Hour'),
            ('quote', 'Per Quote'),
        ],
        default='quote',
    )
    is_active = fields.Boolean(default=True)
    request_ids = fields.One2many(
        'service_map.request',
        'service_id',
        string='Requests',
    )
    review_ids = fields.One2many(
        'service_map.review',
        'service_id',
        string='Reviews',
    )