from odoo.http import request

# validation method:
def check_existence_of_the_record(property_id):
    # adding Validation layer
    if not property_id:
        return request.make_json_response({
            "message": 'there is no record with the entered id',
        }, status=400)
    return None