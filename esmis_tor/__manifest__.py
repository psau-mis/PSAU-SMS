# -- coding: utf-8 --
{
    'name': 'eSMIS TOR',
    'version': '16.0.1.0.0',
    'summary': '',
    'description': """

        """,
    'category': 'Website',
    'author': "NexBridgetech Inc.",
    'company': 'NexBridgetech Inc.',
    'maintainer': 'NexBridgetech Inc.',
    'website': "https://nexbridgetech.com/",
    'depends' : ['base', 'esmis_base', 'esmis_curriculum', 'contacts'],
    'data': [
        # 'security/ir.model.access.csv',
        'reports/paper_format.xml',
        'reports/transcript_of_record.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
