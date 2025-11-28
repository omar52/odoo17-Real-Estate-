from ast import literal_eval
from odoo import http
from odoo.http import request
import io
import xlsxwriter


class XlsxPropertyReport(http.Controller):
    @http.route('/property/excel/report/<string:property_ids>', type='http', auth='user')
    def download_property_excel_report(self,property_ids):

        # 1- literal_eval convert the string of '[1, 2, 3, 4]' to list
        # 2- browse takes input of A single ID or list of IDs, unlike the search metho which needs search domain []
        property_ids = request.env['property'].browse(literal_eval(property_ids))
        print(property_ids)
        # means you are creating an in-memory binary stream (like a file, but it exists only in memory) using Python’s io module
        output = io.BytesIO()
        # is creating a new Excel workbook in memory using the XlsxWriter library,
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # Create new sheet and naming it
        worksheet = workbook.add_worksheet('Peroperties')

        # Add format
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        string_format = workbook.add_format({'bold': True,  'border': 1, 'align': 'center'})
        price_format = workbook.add_format({'num_format': '$##,##00.00',  'border': 1, 'align': 'center'})

        # add header titles:
        headers = ['Name', 'Postcode', 'Selling Price', 'Garden']

        # Write  headers to the worksheet
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        # Add Data to the sheet
        for idx, property in enumerate(property_ids):

            worksheet.write(idx+1, 0, property.name,string_format)
            worksheet.write(idx+1, 1, property.postcode,string_format)
            worksheet.write(idx+1, 2, property.selling_price,price_format)
            worksheet.write(idx+1, 3, 'Yes' if property.garden else 'No',string_format)



        # If you try to read from output before .close(), it may be incomplete or corrupted
        workbook.close()

        # Reading from output now (for sending over HTTP, saving, etc.) will start from the beginning of the file.
        # Without .seek(0), a read operation would return nothing because the cursor is at the end.
        output.seek(0)



        file_name = 'Property Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition',f'attachment; filename={file_name}')
            ]
        )