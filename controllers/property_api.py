import json
import math
from urllib.parse import parse_qs

from PIL.ImageChops import offset

from odoo import http
from odoo.addons.test_impex.tests.test_load import values
from odoo.http import request


def valid_response(data, status, pagination_info=None):
    response_body = {
        'message': 'successful',
        'data': data,
    }
    if pagination_info:
        response_body['pagination_info'] = pagination_info
    return request.make_json_response(response_body, status=status)


def invalid_response(error, status):
    response_body = {
        'message': 'Failed',
        'error': error,
    }
    return request.make_json_response(response_body, status=status)


class PropertyApi(http.Controller):

    # @http.route("/v1/property", methods=["POST"], type="http", auth='none', csrf=False)
    # def post_property(self):
    #     # Recieving the data:
    #     args = request.httprequest.data.decode()  # get json data
    #     vals = json.loads(args)  # convert json data to dictionary
    #     # print(vals)
    #
    #     # validate:
    #     if not vals.get('name'):
    #         return invalid_response("Property name is required!!", status=400)
    #     else:
    #
    #         # handling any error from creation operation using try except
    #         try:
    #             # make creation we used sudo() to create as a superuser
    #             res = request.env['property'].sudo().create(vals)
    #
    #             # sending response: status code :
    #             # 1- 200 : general success
    #             # 2- 201 : Creation process success
    #             if res:
    #                 return request.make_json_response({
    #                     "message": "property has been created successfully",
    #                     "id": res.id,
    #                     "name": res.name,
    #                 }, status=201)
    #         except Exception as error:
    #             return (invalid_response(error, status=400)

    # Using sql queries instead of ORM method for POST
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
                cols = ', '.join(vals.keys())  # ==> name , postcode, ...
                values = ', '.join(['%s'] * len(vals))  # ==> '%s', '%s', '%s', ...
                cr = request.env.cr
                query = f""" INSERT INTO property ({cols}) VALUES ({values}) RETURNING id ,name ,postcode """
                cr.execute(query, tuple(vals.values()))
                res = cr.fetchone()
                print(res)
                if res:
                    return request.make_json_response({
                        "message": "property has been created successfully",
                        "id": res[0],
                        "name": res[1],
                        "postcode": res[2],
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
            # Parse params
            params = parse_qs(request.httprequest.query_string.decode("utf-8"))

            # Extract parameters safely
            limit = int(params.get("limit", [0])[0]) if params.get("limit") else 0
            page = int(params.get("page", [1])[0]) if params.get("page") else None
            state = params.get("state", [None])[0]

            # CASE 1: State filtering
            domain = []
            if state:
                domain.append(("state", "=", state))

            # Count records before pagination
            record_count = request.env["property"].sudo().search_count(domain)

            if record_count == 0:
                return invalid_response("No records found for this request.", status=400)

            # CASE 2: Pagination logic
            offset = 0
            if page and limit:
                offset = (page - 1) * limit

            # CASE 3: Search with or without pagination
            property_ids = request.env["property"].sudo().search(
                domain,
                offset=offset,
                limit=limit if limit else None,
                order="id desc"
            )

            if not property_ids:
                return invalid_response("No records found for the requested page.", status=400)

            # Format response data
            data = [{
                "id": p.id,
                "name": p.name,
                "postcode": p.postcode,
                "bedrooms": p.bedrooms,
            } for p in property_ids]

            # CASE 4: If no pagination → return simple result
            if not limit:
                return valid_response(data, status=200)

            # CASE 5: If pagination → return pagination info
            total_pages = math.ceil(record_count / limit)

            # Invalid page check
            if page > total_pages:
                return invalid_response(
                    f"Page {page} is out of range. Total pages = {total_pages}.",
                    status=400
                )

            return valid_response(
                data,
                pagination_info={
                    "page": page,
                    "limit": limit,
                    "pages": total_pages,
                    "records": record_count,
                },
                status=200
            )

        except Exception as error:
            return invalid_response(str(error), status=400)
