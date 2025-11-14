from email.policy import default

from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    name = fields.Char(required="1",default='New',size=20)
    description = fields.Text()
    postcode = fields.Char(required="1")
    date_availability = fields.Date()
    expected_price = fields.Float(digits=(0,5))
    selling_price = fields.Float(digits=(0,5))
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    # the first value is what stored in data base, the second one appears to the user
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West'),
    ],default='north')

    # Many2one relation Field
    # as it is many to one from property ---> naming convention ---> owner_id ,,,,,,if it one to many or many to many---> owner_ids
    owner_id = fields.Many2one('owner')

    # Many2one relation Field
    tag_ids = fields.Many2many('tag')


    # Data Base constrains and validation
    _sql_constraints = [
        ('unique_name','unique("name")','Property name is existed!')
    ]


    # for only integer values as 0 is already one of them
    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please enter valid number of bedrooms')


    # # Overriding create function
    # @api.model_create_multi
    # def create(self,vals):
    #     res = super(Property,self).create(vals)
    #     # logic
    #     print('inside create function')
    #     return res

    # Overriding research function
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property,self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     # logic
    #     print('inside search function')
    #     return res

    # # Overriding write function
    # def write(self, vals):
    #     res = super(Property,self).write(vals)
    #     # logic
    #     print('inside write model')
    #     return res

    # #Overriding delete function
    # def unlink(self):
    #     res = super(Property,self).unlink()
    #     # logic
    #     print('inside unlink model')
    #     return res


