# -- coding: utf-8 --
{
    'name': 'eSMIS Website Admission',
    'version': '16.0.1.0.0',
    'summary': 'Add functionality to website admission',
    'description': """
        Add functionality to website admission.
        """,
    'category': 'Website',
    'author': "NexBridgetech inc.",
    'company': 'NexBridgetech inc.',
    'maintainer': 'NexBridgetech inc.',
    'website': "https://nexbridgetech.com/",
    'depends': [
        'base', 'base_address_extended', 'web', 'website', 'contacts', 'mail', 'esmis_base', 'esmis_admission', 'portal'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/website_menu.xml',
        'data/data.xml',
        'views/esmis_res_barangay.xml',
        'views/esmis_admission.xml',
        'views/qweb_templates/admission_registration_web.xml',
        'views/qweb_templates/admission_input_groups.xml',
        # 'views/qweb_templates/esmis_admission_website_templates.xml',
        'views/qweb_templates/esmis_admission_update_documents.xml',
        'views/qweb_templates/esmis_admission_certification.xml',
        'views/qweb_templates/admission_snippets.xml',
        'wizards/admission_document_to_resend_wiz.xml',
    ],
    "assets": {
        'web.assets_frontend': [
            'esmis_website_admission/static/src/js/*.js',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
