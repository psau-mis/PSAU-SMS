# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'eSMIS: Campus Management',
    'version' : '1.1',
    'summary': 'Esmis Campus',
    'sequence': 1,
    'description': """
        Campus Module for eSMIS
    """,
    'category': 'School Management',
    'depends' : ['base', 'esmis_base'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',   
        'views/esmis_campus.xml',
        'views/esmis_building.xml',
        'views/esmis_room.xml',
        

          
        
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'author':"NexBridge Technologies Inc."
}
