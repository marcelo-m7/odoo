"""Service request / order model.

Represents a request made by a client for a specific service offered by a
provider.  Requests go through a state machine and can store location
coordinates for on‑site services.
"""

from odoo import models, fields, api, _


class ServiceRequest(models.Model):
    _name = 'service_map.request'
    _description = 'Service Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Request Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
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
    service_id = fields.Many2one(
        'service_map.service',
        string='Service',
        required=True,
        ondelete='cascade',
    )
    description = fields.Text()
    scheduled_date = fields.Datetime(string='Scheduled Date')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('accepted', 'Accepted'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        default='draft',
        tracking=True,
    )
    price_estimate = fields.Float(string='Estimated Price')
    price_final = fields.Float(string='Final Price')
    payment_id = fields.Many2one(
        'service_map.payment',
        string='Payment',
        ondelete='set null',
    )
    review_ids = fields.One2many(
        'service_map.review',
        'request_id',
        string='Reviews',
    )
    location_latitude = fields.Float(string='Latitude')
    location_longitude = fields.Float(string='Longitude')

    @api.model
    def create(self, vals):
        """Override create to assign a sequence to the request reference."""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('service_map.request') or _('New')
        return super().create(vals)

    # Placeholder for state transitions
    def action_accept(self):
        for record in self:
            record.state = 'accepted'
        return True

    def action_start(self):
        for record in self:
            record.state = 'in_progress'
        return True

    def action_done(self):
        for record in self:
            record.state = 'done'
        return True