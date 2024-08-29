{
    'name': 'Tritel Requisition Module',
    'author': 'Kevins Code',
    'license': 'LGPL-3',
    'version': '17.0.1.1',
    'category':'Tritel',
    'summary': 'Manage Tritel Requests within TRM path',
    'description': 'Module to manage Tritel employee requests.',
    'depends':['mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/view_tritel_request.xml',
        'views/action_tritel_requests.xml',
        'views/menu.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    }
