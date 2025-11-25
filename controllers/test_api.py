from pickle import FALSE

from odoo import http


class TestApi(http.Controller):

    @http.route("/api/test", methods=["GET"], type="http", auth='none', csrf=FALSE)
    def test_endpoint(self):
        print('inside test endpoint method')
