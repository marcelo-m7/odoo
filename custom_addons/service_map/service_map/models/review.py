"""Service review model.

Stores a rating and optional comment left by a client after a request
has been completed.
"""

from odoo import models, fields


class ServiceReview(models.Model):
    _name = 'service_map.review'
    _description = 'Service Review'
    _order = 'create_date desc'

    request_id = fields.Many2one(
        'service_map.request',
        string='Request',
        required=True,
        ondelete='cascade',
    )
    client_id = fields.Many2one(
        'res.partner',
        string='Client',
        related='request_id.client_id',
        store=True,
        readonly=True,
    )
    provider_id = fields.Many2one(
        'service_map.provider',
        string='Provider',
        related='request_id.provider_id',
        store=True,
        readonly=True,
    )
    service_id = fields.Many2one(
        'service_map.service',
        string='Service',
        related='request_id.service_id',
        store=True,
        readonly=True,
    )
    rating = fields.Integer(required=True, help='Rating from 1 (worst) to 5 (best).')
    comment = fields.Text()