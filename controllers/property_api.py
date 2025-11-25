import json
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request
from .property_crud_validator import check_existence_of_the_record, check_existence_of_the_name, \
    check_existence_of_the_records


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

    # update / write methos
    # it is allowed to send the id in the url
    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth='none', csrf=False)
    def update_property(self, property_id):

        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            error = check_existence_of_the_record(property_id)
            if error:
                return error
            else:
                args = request.httprequest.data.decode()  # get json data
                vals = json.loads(args)  # convert json data to dictionary
                property_id.write(vals)
                return request.make_json_response({
                    "message": "property has been updated successfully",
                    "id": property_id.id,
                    "name": property_id.name,
                }, status=201)

        except Exception as error:
            return request.make_json_response({
                "message": error,
            }, status=400)

    # Get / Read
    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth='none', csrf=False)
    def get_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            error = check_existence_of_the_record(property_id)
            if error:
                return error
            else:
                return request.make_json_response({
                    "message": "property is",
                    "id": property_id.id,
                    "name": property_id.name,
                    "postcode": property_id.postcode,
                    "bedrooms": property_id.bedrooms,
                }, status=201)
        except Exception as error:
            return request.make_json_response({
                "message": error
            })

    # Delete
    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth='none', csrf=False)
    def delete_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            error = check_existence_of_the_record(property_id)
            if error:
                return error
            else:
                property_id.unlink()
                return request.make_json_response({
                    "message": "Property Has been Deleted Successfully"
                })
        except Exception as error:
            return request.make_json_response({
                "message": error
            })

    # Get all records
    @http.route("/v1/properties", methods=["GET"], type="http", auth='none', csrf=False)
    def get_all_property(self):
        try:
            # recieving params
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            if params.get('state'):
                property_domain += [("state", "=", params.get('state')[0])]
                property_ids = request.env['property'].sudo().search(property_domain)
                error = check_existence_of_the_records(property_ids)
                if error:
                    return error
                else:
                    return request.make_json_response([{
                        "id": property.id,
                        "name": property.name,
                        "postcode": property.postcode,
                        "bedrooms": property.bedrooms,
                    } for property in property_ids], status=201)
            else:
                property_ids = request.env['property'].sudo().search([])
                error = check_existence_of_the_records(property_ids)
                if error:
                    return error
                else:
                    return request.make_json_response([{
                        "id": property.id,
                        "name": property.name,
                        "postcode": property.postcode,
                        "bedrooms": property.bedrooms,
                    } for property in property_ids], status=201)

        except Exception as error:
            return request.make_json_response({
                "message": error
            })
