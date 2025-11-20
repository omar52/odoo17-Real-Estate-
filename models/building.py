from email.policy import default
from odoo import models, fields


class Building(models.Model):
    _name = 'building'

    # Display name to the Building Record when created, in tracking in chutter
    _description = 'Building Record'

    # odoo support Multiple inheritence to inherit  Chatter, to add tracking of any field i add attr of tracking=1
    _inherit = ['mail.thread','mail.activity.mixin']
    # _rec_name = 'code'   # is automatically assigned to name unless you assign it



    #fields:
    no = fields.Integer()
    code = fields.Char()
    description =fields.Text()
    name = fields.Char()
    active = fields.Boolean(default=True)

