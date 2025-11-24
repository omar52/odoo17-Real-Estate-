from pkg_resources import require

from odoo import models,fields,api


class AccountMove(models.Model):
    _inherit="account.move"


    def account_do_something(self):
        print(self,'inside the account_do_something')

