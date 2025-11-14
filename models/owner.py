from pkg_resources import require

from odoo import models,fields,api


class Owner(models.Model):
    _name="owner"

    name = fields.Char(required='1')
    phone = fields.Char()
    address = fields.Char()

    # One2many ===> it is preferable to start with many to one fields to use as inverse_name in the one2many field attributes
    property_ids = fields.One2many('property','owner_id')