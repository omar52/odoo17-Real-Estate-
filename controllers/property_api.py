import json
from odoo import http
from odoo.http import request
from .property_validator import check_existence_of_the_name


class PropertyApi(http.Controller):



    @http.route("/v1/property", methods=["POST"], type="http", auth='none', csrf=False)
    def post_property(self):
        # Recieving the data:
        args = request.httprequest.data.decode()  # get json data
        vals = json.loads(args)  # convert json data to dictionary
        # print(vals)

        # validate:
        error = check_existence_of_the_name(vals.get('name'))
        if error:
            return error
        else:

            # handling any error from creation operation using try except
            try:
                # make creation we used sudo() to create as a superuser
                res = request.env['property'].sudo().create(vals)

                # sending response: status code :
                # 1- 200 : general success
                # 2- 201 : Creation process success
                if res:
                    return request.make_json_response({
                        "message": "property has been created successfully",
                        "id": res.id,
                        "name": res.name,
                    }, status=201)
            except Exception as error:
                return request.make_json_response({
                    "message": error,
                }, status=400)

    # post using json ==> 3rd party application should use only json formate data sending with the request.
    @http.route("/v1/property/json", methods=["POST"], type="json", auth='none', csrf=False)
    def post_property_json(self):
        # Recieving the data:
        args = request.httprequest.data.decode()  # get json data
        vals = json.loads(args)  # convert json data to dictionary
        print(vals)

        # make creation we used sudo() to create as a superuser
        res = request.env['property'].sudo().create(vals)
        # sending response:
        if res:
            # what i return will be assigned to the key "result" in jsn response , i can not control the status it is always 200.
            # json reponse has fixed contruction, i can only add to the "result" key
            return [{
                "message": "property has been created successfully from json "
            }]
        return None
