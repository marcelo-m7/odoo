"""Message model.

Represents a simple chat message tied to a service request.  This is a
placeholder; in a full implementation you might leverage Odoo's built‑in
messaging framework or integrate with a realtime chat service.
"""

from odoo import models, fields


class ServiceMessage(models.Model):
    _name = 'service_map.message'
    _description = 'Service Message'
    _order = 'create_date'

    request_id = fields.Many2one(
        'service_map.request',
        string='Request',
        required=True,
        ondelete='cascade',
    )
    author_id = fields.Many2one(
        'res.partner',
        string='Author',
        required=True,
        ondelete='cascade',
    )
    body = fields.Text(required=True)