from odoo.http import request

# validation method:
def check_existence_of_the_name(name):
    # adding Validation layer
    if not name:
        return request.make_json_response({
            "message": 'Name is required',
        }, status=400)
    return None