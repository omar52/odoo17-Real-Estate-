{
    'name': "App One",
    'author': "Omar Abdelkarim",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base','sale','account','mail'],
    'data': [           # path within the application
        # order is very important
        #1- security
        'security/ir.model.access.csv',
        #2- data
        'data/sequence.xml',
        #3- views
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/buidling_view.xml',
        'views/property_history_view.xml',
        #4-Templates:
        'reports/property_report.xml',
    ],
    'assets':{
        'web.assets_backend':['app_one/static/src/css/property.css']
    },
    'application': True,
    'installable':True,
}