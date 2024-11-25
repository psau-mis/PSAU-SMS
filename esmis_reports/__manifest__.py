# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'eSMIS: Reports Management',
    'version' : '1.1',
    'summary': 'Esmis Reports',
    'sequence': 1,
    'description': """
        Reports Module for eSMIS
    """,
    'category': 'Reports Management',
    'depends' : ['esmis_base', 'esmis_curriculum', 'esmis_enrollment', 'esmis_cashier', 'report_xlsx'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',   
        'report/paper_format.xml',
        'report/report.xml',
        'report/student_certificate.xml',
        'report/student_free_tuition_certificate.xml',
        'report/student_transfer_certificate.xml',
        'report/collection_report_by_payor_pdf.xml',
        'report/collection_report_by_payer_pdf.xml',
        'report/collection_report_by_fund_pdf.xml',
        'report/collection_report_by_account_pdf.xml',
        'report/collection_report_by_subaccount_pdf.xml',
        'report/report_of_collection_pdf.xml',
        'wizard/cor_collections_wiz.xml',
        'wizard/collection_by_payer.xml',
        'wizard/collection_by_fund.xml',
        'wizard/collection_by_account.xml',
        'wizard/collection_by_payor.xml',
        'wizard/report_of_collection.xml',
        'wizard/collection_by_subaccount.xml',
        
        


          
        
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'author':"NexBridge Technologies Inc."
}
