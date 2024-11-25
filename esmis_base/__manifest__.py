# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'eSMIS: Base',
    'version' : '1.1',
    'summary': 'Esmis Base',
    'sequence': 1,
    'description': """
        Core Module for eSMIS
    """,
    'category': 'School Management',
    'depends' : ['base', 'hr', 'mail'],
    'data': [
        'security/security.xml',
        'data/hr_job.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',   
        'views/esmis_signatories.xml',
        'views/esmis_iso_printouts.xml',
        'views/esmis_department.xml',
        'views/esmis_course.xml',
        'views/esmis_subjects.xml',
        'views/esmis_school_year.xml',
        'views/esmis_students.xml',
        'views/esmis_employee.xml',
        'views/esmis_lec_lab.xml',

          
        
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'author':"NexBridge Technologies Inc."
}
