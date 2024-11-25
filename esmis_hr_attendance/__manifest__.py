# -- coding: utf-8 --
{
    'name': 'PSAU Attendance',
    'version': '16.0.1.0.0',
    'summary': 'PSAU Attendance modification',
    'description': """
        
        """,
    'category': 'Generic Modules/Human Resources',
    'author': "NexBridgetech inc.",
    'company': 'NexBridgetech inc.',
    'maintainer': 'NexBridgetech inc.',
    'website': "https://nexbridgetech.com/",
    'depends': [
        'base', 'hr_attendance',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_attendance.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
