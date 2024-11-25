# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'eSMIS: Grade Management',
    'version' : '1.1',
    'summary': 'Esmis Campus',
    'sequence': 1,
    'description': """
        Grade Module for eSMIS
    """,
    'category': 'Grade Management',
    'depends' : ['base', 'esmis_base', 'esmis_curriculum'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',   
        'views/esmis_grade_management.xml',
        'views/faculty_schedule.xml',
        'views/grade_equivalent.xml',
        'views/esmis_student.xml',
        "reports/paper_format.xml",
        # "reports/certificate_of_grades.xml",
        

          
        
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'author':"NexBridge Technologies Inc."
}
