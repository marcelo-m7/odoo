"""Service provider model.

Represents a professional or business offering services through the
ServiceMap platform.  Providers link to `res.partner` for contact
information and can offer multiple services.
"""

from odoo import models, fields, api


class ServiceProvider(models.Model):
    _name = 'service_map.provider'
    _description = 'Service Provider'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        ondelete='cascade',
        help='Link to the partner record containing contact details.',
    )
    category_ids = fields.Many2many(
        'service_map.category',
        string='Categories',
        help='Categories of services offered by this provider.',
    )
    service_ids = fields.One2many(
        'service_map.service',
        'provider_id',
        string='Services',
    )
    rating = fields.Float(
        string='Average Rating',
        compute='_compute_rating',
        store=True,
        help='Average rating computed from completed requests.',
    )
    is_active = fields.Boolean(default=True, tracking=True)

    latitude = fields.Float(string='Latitude', help='Geographic coordinate (degrees).')
    longitude = fields.Float(string='Longitude', help='Geographic coordinate (degrees).')

    @api.depends('service_ids.review_ids.rating')
    def _compute_rating(self):
        """Compute the provider's average rating across all reviews."""
        for provider in self:
            ratings = provider.mapped('service_ids.review_ids.rating')
            provider.rating = sum(ratings) / len(ratings) if ratings else 0.0