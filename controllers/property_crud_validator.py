from odoo.http import request


# validation method:
def check_existence_of_the_record(property_id):
    # adding Validation layer
    if not property_id:
        return request.make_json_response({
            "message": 'there is no record with the entered id',
        }, status=400)
    return None

def check_existence_of_the_records(property_ids):
    # adding Validation layer
    if not property_ids:
        return request.make_json_response({
            "message": 'there are no records in this model',
        }, status=400)
    return None

# Creation method:
def check_existence_of_the_name(name):
    # adding Validation layer
    if not name:
        return request.make_json_response({
            "message": 'Name is required',
        }, status=400)
    return None
