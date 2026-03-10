"""Service category model.

Defines a hierarchical taxonomy of service categories.  Categories can
be nested (e.g. "Home Repair" → "Plumbing" → "Leak Fix").
"""

from odoo import models, fields


class ServiceCategory(models.Model):
    _name = 'service_map.category'
    _description = 'Service Category'
    _order = 'name'

    name = fields.Char(required=True, translate=True)
    parent_id = fields.Many2one(
        'service_map.category',
        string='Parent Category',
        ondelete='restrict',
    )
    child_ids = fields.One2many(
        'service_map.category',
        'parent_id',
        string='Child Categories',
    )
    service_ids = fields.One2many(
        'service_map.service',
        'category_id',
        string='Services',
    )

    _sql_constraints = [
        ('name_unique', 'unique(name, parent_id)', 'Category names must be unique per level.'),
    ]