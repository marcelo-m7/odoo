"""Payment model.

Captures basic payment information for a request.  Real payment
integration should add additional fields and states as necessary.
"""

from odoo import models, fields


class ServicePayment(models.Model):
    _name = 'service_map.payment'
    _description = 'Service Payment'
    _inherit = ['mail.thread']

    request_id = fields.Many2one(
        'service_map.request',
        string='Request',
        required=True,
        ondelete='cascade',
    )
    amount = fields.Float(required=True)
    payment_date = fields.Datetime(default=fields.Datetime.now)
    transaction_reference = fields.Char(string='Transaction Reference')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ], default='pending')