from odoo import fields
from odoo.tests.common import TransactionCase



class TestProperty(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()

        self.property_01_record = self.env['property'].create({
            'ref': 'PRT1000',
            'name': 'property 1000',
            'description': 'description property 1000',
            'postcode': '1010',
            'date_availability': fields.Date.today(),
            'bedrooms': 10,
            'expected_price': 10000,
        })
    # we must add the db_name in the odoo.config file
    def test_01_property_values(self):
        property_id = self.property_01_record

        self.assertRecordValues(property_id, [{
            'ref': 'PRT1000',
            'name': 'property 1000',
            'description': 'description property 1000',
            'postcode': '1010',
            'date_availability': fields.Date.today(),
            'bedrooms': 10,
            'expected_price': 10000,
        }])
