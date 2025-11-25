
import json

from odoo import http
from odoo.http import request

class PropertyApi(http.Controller):
    @http.route("/v1/property", methods=["POST"], type="http", auth='none', csrf=False)
    def post_property(self):
        # Recieving the data:
        args = request.httprequest.data.decode()  # get json data
        vals = json.loads(args)  # convert json data to dictionary
        print(vals)

        # make creation we used sudo() to create as a superuser
        res = request.env['property'].sudo().create(vals)

        # sending response:
        if res:
            return request.make_json_response({
                "message":"property has been created successfully"
            },status=200)