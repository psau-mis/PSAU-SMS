# -- coding: utf-8 --
{
    'name': 'eSMIS Website',
    'version': '16.0.1.0.0',
    'summary': 'PSAU Website Module',
    'description': """ """,
    'category': 'Website/PSAU Website',
    'author': "NexBridgetech inc.",
    'company': 'NexBridgetech inc.',
    'maintainer': 'NexBridgetech inc.',
    'website': "https://nexbridgetech.com/",
    'depends': [
        'base', 'esmis_base', 'esmis_admission', 'website', 'esmis_website_admission',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/admission_template.xml',
        

        # form templates for testing
        'views/admission_setup_template.xml',
        'views/form_templates/undergraduate_new_student.xml',

        #
        'views/admission_form_partials/instruction_note.xml',

        #
        'views/admission_form_template/admission_admission_type.xml',
        'views/admission_form_template/admission_applicant_type.xml',
        'views/admission_form_template/admission_registration_new.xml',

        #
        'views/qweb_inherit.xml',
    ],
    "assets": {
        'web.assets_frontend': [
            # 'esmis_website/static/src/js/admission.js',

            # for testing
            'esmis_website/static/src/js/admission_set_up.js',
            'esmis_website/static/src/js/contact_mail_validation.js',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
