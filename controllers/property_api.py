import json
import math
from urllib.parse import parse_qs

from PIL.ImageChops import offset

from odoo import http
from odoo.http import request


def valid_response(data, status,pagination_info):
    response_body = {
        'message': 'successful',
        'data': data,
    }
    if pagination_info:
        response_body['pagination_info']=pagination_info
    return request.make_json_response(response_body, status=status)


def invalid_response(error, status):
    response_body = {
        'message': 'Failed',
        'error': error,
    }
    return request.make_json_response(response_body, status=status)


class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth='none', csrf=False)
    def post_property(self):
        # Recieving the data:
        args = request.httprequest.data.decode()  # get json data
        vals = json.loads(args)  # convert json data to dictionary
        # print(vals)

        # validate:
        if not vals.get('name'):
            return invalid_response("Property name is required!!", status=400)
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
                return invalid_response(error, status=400)

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
            if not property_id:
                return invalid_response("ID is not existed")
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
            return invalid_response(error, status=400)

    # Get / Read
    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth='none', csrf=False)
    def get_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return invalid_response('ID does not exist!', status=400)
            else:
                return valid_response({
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
            if not property_id:
                return invalid_response("Id is not Existed", status=400)

            else:
                property_id.unlink()
                return request.make_json_response({
                    "message": "Property Has been Deleted Successfully"
                })
        except Exception as error:
            return invalid_response(error, status=400)

    # Get all records
    @http.route("/v1/properties", methods=["GET"], type="http", auth='none', csrf=False)
    def get_all_property(self):
        try:
            # recieving params
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            offset = 0
            limit = 0
            if params:
                if params.get('limit'):
                    limit = (params.get('limit')[0])
                    print(limit)
                if params.get('page'):
                    page = int(params.get('page')[0])
                    offset = ((page - 1) * int(limit))
                    print(offset)
            if params.get('state'):
                property_domain += [("state", "=", params.get('state')[0])]
                property_ids = request.env['property'].sudo().search(property_domain)
                print(property_ids)
                if not property_ids:
                    return invalid_response(f"There are no records with the entered state = {params.get('state')[0]}",
                                            status=400)
                else:
                    return valid_response([{
                        "id": property.id,
                        "name": property.name,
                        "postcode": property.postcode,
                        "bedrooms": property.bedrooms,
                    } for property in property_ids], status=201)
            else:
                # offset takes (INT) and must equals to the record number previous to the one you want to show while limit takes (STR)
                property_ids = request.env['property'].sudo().search([], offset=offset, limit=limit, order='id desc')
                print(property_ids)
                property_count = request.env['property'].sudo().search_count([])
                print(property_count)
                pages_num = math.ceil(property_count / int(limit))
                if page <= pages_num:
                    if not property_ids:
                        return invalid_response(f"There are no records in this table", status=400)

                    else:
                        return valid_response([{
                            "id": property_id.id,
                            "name": property_id.name,
                            "postcode": property_id.postcode,
                            "bedrooms": property_id.bedrooms,
                        } for property_id in property_ids], pagination_info={
                            'page': page if page else 1,
                            'limit': limit,
                            'pages':pages_num,
                            'record':property_count,

                        }, status=201)
                else:
                    return invalid_response(
                        f'The page number you want to display is out of pages range:{pages_num} pages', status=400)

        except Exception as error:
            return invalid_response(error, status=400)
