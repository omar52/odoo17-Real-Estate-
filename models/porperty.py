from email.policy import default
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.populate import compute


class Property(models.Model):
    _name = 'property'

    # Display name to the Property when created, in tracking in chutter
    _description = 'Property'

    # odoo support Multiple inheritence to inherit  Chatter, to add tracking of any field i add attr of tracking=1
    _inherit = ['mail.thread','mail.activity.mixin']

    ref = fields.Char(default='New', readonly=1)
    name = fields.Char(required=1, default='New', size=20)
    description = fields.Text()
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    # Automated action
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    # expected_price = fields.Float(digits=(0,5))
    # selling_price = fields.Float(digits=(0,5))
    expected_price = fields.Float()
    selling_price = fields.Float()

    # computed (derived) field ==> is not stored in DB automatically.
    # used generally if i will compute the value before setting it.
    diff = fields.Float(compute='_compute_diff')
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)

    # the first value is what stored in data base, the second one appears to the user
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='north')

    # Many2one relation Field
    # as it is many to one from property ---> naming convention ---> owner_id ,,,,,,if it one to many or many to many---> owner_ids
    owner_id = fields.Many2one('owner')

    # Many2one relation Field
    tag_ids = fields.Many2many('tag')

    #related Fields ===> are not stored in DB Automatically, it needs 'store' attribute ===> store=1
    # related field type must be the same as the one related to. Char()==Char()
    owner_address = fields.Char(related='owner_id.address',readonly=0)
    owner_phone = fields.Char(related='owner_id.phone',readonly=0)

    # work flow ====> add state to the property
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft',tracking=1)


    line_ids = fields.One2many('property.line','property_id')

    ################################################## Start Actions for State #####################################################
    # add actions buttons
    def action_draft(self):
        for rec in self:
            print('inside draft action')
            rec.state = 'draft'
            # rec.write({
            #     'state':'draft'
            # })

    def action_pending(self):
        for rec in self:
            print('inside pending action')
            rec.state = 'pending'
            # rec.write({
            #     'state':'pending'
            # })

    def action_sold(self):
        for rec in self:
            print('inside sold action')
            rec.state = 'sold'
            # rec.write({
            #     'state':'sold'
            # })

    def action_colsed(self):
        for rec in self:
            print('inside closed action')
            rec.state = 'closed'
            # rec.write({
            #     'state':'sold'
            # })
    # self has only the property, it does not carry any record which is irreasonable as my logic will be applied on these records
    def check_expected_selling_date(self):
        property_id = self.search([])
        for rec in property_id:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                if rec.state == 'draft' or rec.state == 'pending':
                    rec.is_late = True


    # Env can be used to catch user Data & company & context & cursor & [model====> most important call to any method in side the model]
    def action(self):
        # print(self.env.user)          #Return  Record of user-- any field can ce accessed by dot notation
        # print(self.env.uid)           #Return id of user
        # print(self.env.company.name)  #Return company of user -- any field can be accessed by dot notation
        # print(self.env.context)       #Return context
        # print(self.env.cr)            #Return Cursor
        # print(self.env['owner'])        # Return model name
        # print(self.env['owner'].create({
        #     'name': 'Ahmed Ezzat',
        #     'phone':'01000101001'
        # }))            #create an instance (record of the model)
        # print(self.env['owner'].search([])) # Search for
        ...



    ################################################## End Actions for State #####################################################

    ################################################## Start _sql_constraints #####################################################
    # Data Base constrains and validation
    _sql_constraints = [
        ('unique_name', 'unique("name")', 'Property name is existed!')
    ]

    ################################################## End _sql_constraints #####################################################

    ################################################## Start Decorators #####################################################
    # can pass all fields in the same model + the realtional field with other models
    # is a real  record, we can  apply crud operation on it
    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print('inside _compute_diff method')
            rec.diff = rec.expected_price - rec.selling_price


    # can pass all fields in the same model only (views fields)
    # return a pesudo  record, we can not apply crud operation on it we can use dot notation or method called update
    # application ==> warnining ===> it does not prevent me from recording in DB
    @api.onchange('expected_price', 'owner_id.phone')
    def _onchange_expected_price(self):
        for rec in self:
            print('inside _onchange_expected_price method')
            return {
                'warning': {
                    'title': 'warning',
                    'message': 'negative value',
                    'type': 'notification'
                }
            }

    ######Start logic Tier Validation #####################################################
    # for only integer values as 0 is already one of them
    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please enter valid number of bedrooms')
    ##### End logic Tier Validation #####################################################

    ################################################## End Decorators #####################################################

    ################################################## start Overrriding functions #####################################################
    # # Overriding create function ==> to handle the sequence Vid(50)
    # @api.model_create_multi
    @api.model
    def create(self,vals):
        res = super(Property,self).create(vals)
        # logic
        if res.ref =='New':
            print('condtion is working')
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
            # print('inside create function')
        return res


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



    ################################################## end Overrriding functions #####################################################




class PropertyLine(models.Model):
    _name = 'property.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')