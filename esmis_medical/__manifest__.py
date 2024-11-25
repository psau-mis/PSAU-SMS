# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'eSMIS: Medical Management',
    'version' : '1.1',
    'summary': 'Esmis Medical',
    'sequence': 1,
    'description': """
        Medical Module for eSMIS
    """,
    'category': 'School Management',
    'depends' : ['base', 'esmis_base', 'esmis_website_portal'],
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        # 'views/menu_view.xml',   
        # 'views/esmis_maintenance.xml',
        # 'wizard/esmis_health_services_logbook_wiz.xml',
        # 'views/esmis_health_services.xml',
        # 'views/esmis_psau_ambulance_logbook.xml',
        # 'views/esmis_medical_health_summary.xml',
        # 'views/esmis_medical_health_record.xml',
        # 'views/esmis_psau_consultation.xml',
        # 'views/esmis_medical_cert.xml',
        # 'views/esmis_rx_pad.xml',
        # 'views/esmis_dental.xml',
        # 'views/esmis_dental_recommendation.xml',
        # 'views/esmis_dental_certificate.xml',
        #  'views/esmis_hwc_attendance_log.xml',
        # 'views/esmis_health_checklist.xml',
        # 'views/esmis_hwc_membership_log.xml',
        # 'views/esmis_cash_remittance.xml',
        # 'views/esmis_credit_remittance.xml',
        # 'views/esmis_covid_1a.xml',
        # 'views/esmis_covid_1b.xml',
        # 'views/esmis_medical_covid_vaccination.xml',
        # 'views/esmis_wfh_req.xml',
        # 'views/esmis_psau_clearance.xml',
        # 'views/esmis_procedures.xml',

        'views/portal_medical_template/inherit_partner_form_view.xml'

          
        
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'author':"NexBridge Technologies Inc."
}
