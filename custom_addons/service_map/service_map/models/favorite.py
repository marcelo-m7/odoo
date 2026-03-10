"""Favourite provider model.

Allows a client to bookmark a provider for quick access later.
"""

from odoo import models, fields


class ServiceFavorite(models.Model):
    _name = 'service_map.favorite'
    _description = 'Service Favourite'

    client_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        ondelete='cascade',
    )
    provider_id = fields.Many2one(
        'service_map.provider',
        string='Provider',
        required=True,
        ondelete='cascade',
    )

    _sql_constraints = [
        ('client_provider_unique', 'unique(client_id, provider_id)', 'This provider is already in your favourites.'),
    ]