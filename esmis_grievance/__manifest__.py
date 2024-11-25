# -- coding: utf-8 --
{
    'name': 'eSMIS Grievance',
    'version': '16.0.1.0.0',
    'summary': 'Create and Manage Grievance',
    'description': """
        Create and Manage Grievance.
        """,
    'category': 'Uncategorized',
    'author': "NexBridgetech Inc.",
    'company': 'NexBridgetech Inc.',
    'maintainer': 'NexBridgetech Inc.',
    'website': "https://nexbridgetech.com/",
    'depends': [
        'base', 'esmis_base', 'esmis_parent', 'esmis_enrollment',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/grievance_view.xml',

        # data
        'data/grievance_record_sequence.xml',

        #wizard
        'wizards/grievance_taken_action.xml',
    ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}

