# -- coding: utf-8 --
{
    'name': 'eSMIS Parents',
    'version': '16.0.1.0.0',
    'summary': 'Create an Manage Parents users',
    'description': """
        Create an Manage Parents users.
        """,
    'category': 'Uncategorized',
    'author': "NexBridgetech Inc.",
    'company': 'NexBridgetech Inc.',
    'maintainer': 'NexBridgetech Inc.',
    'website': "https://nexbridgetech.com/",
    'depends': [
        'base', 'esmis_base',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/parent_views.xml',
        'views/res_user_view.xml',
        'views/res_partner_view.xml',
    ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}

