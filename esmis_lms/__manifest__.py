# -- coding: utf-8 --
{
    'name': 'eSMIS LMS Extension',
    'version': '16.0.1.0.0',
    'summary': 'Feature Extension For eLearning Management System',
    'description': """
        Feature Extension For eLearning Management System.
        """,
    'category': 'Website',
    'author': "NexBridgetech inc.",
    'company': 'NexBridgetech inc.',
    'maintainer': 'NexBridgetech inc.',
    'website': "https://nexbridgetech.com/",
    'depends': [
        'base', 'esmis_base', 'website_slides', 'website_slides_survey', 'survey', 
        'contacts', 'esmis_website_portal', 'hr', 'survey_upload_file',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/teacher_security.xml',
        'views/inherit_survey_views.xml',
        'views/inherit_website_slides_views.xml',

        # /inherited_web_templates
        'views/inherited_web_templates/inherit_home_website_slides.xml',

        # /custom_web_templates
        'views/custom_web_templates/examination_result.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
