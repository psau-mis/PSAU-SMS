# -- coding: utf-8 --
{
    'name': 'eSMIS Website Portal',
    'version': '16.0.1.0.0',
    'summary': 'Website Portal Frontend module for Student Portal',
    'description': """
        Website Portal Frontend module for Student Portal.
        """,
    'category': 'Website',
    'author': "NexBridgetech inc.",
    'company': 'NexBridgetech inc.',
    'maintainer': 'NexBridgetech inc.',
    'website': "https://nexbridgetech.com/",
    'depends': [
        'base', 'base_address_extended', 'mail', 'web', 'website', 'portal', 'contacts', 'mail', 'esmis_base', 'esmis_admission', 'esmis_grading_management', 'esmis_grievance'
    ],
    'data': [
        'security/ir.model.access.csv',
        #template(inherit default template from portal module)
        'views/inherit_portal_layout_template.xml',
        'views/inherit_web_layout_template.xml',

        #data
        'data/website_portal_data.xml',
        'data/inherit_email_notif_layout.xml',

        #student portal xml templates design
        'views/student_qweb_templates/student_dashboard.xml',
        'views/student_qweb_templates/subject_enrolled.xml',
        'views/student_qweb_templates/student_grades.xml',
        'views/student_qweb_templates/student_medical.xml',
        'views/student_qweb_templates/student_info.xml',
        'views/student_qweb_templates/student_enrollment.xml',
        'views/student_qweb_templates/faculty_evaluation.xml',
        'views/student_qweb_templates/student_grievance.xml',

        #parent portal xml templates
        'views/parent_qweb_templates/parent_child_list.xml',
        'views/parent_qweb_templates/parent_child_records.xml',
        # inner child records
        'views/parent_qweb_templates/child_info.xml',
        'views/parent_qweb_templates/child_grades.xml',
        'views/parent_qweb_templates/child_subjects.xml',
        'views/parent_qweb_templates/child_grievances.xml',

        #layout
        'views/portal_main_layout.xml',
        'views/student_portal_layout.xml',
        'views/parent_portal_layout.xml',
        'reports/certificate_portal_grades.xml',
    ],
    "assets": {
        'web.assets_frontend': [
            'esmis_website_portal/static/src/css/student_portal.css',
            'esmis_website_portal/static/src/css/faculty_evaluation.css',
            'esmis_website_portal/static/src/css/parent_portal.css',
            
            # dependencies for multi-step from wizard for enrollment
            'esmis_website_portal/static/src/plugins/jquery-smartwizard-master/dist/css/smart_wizard_all.min.css',
            'esmis_website_portal/static/src/plugins/jquery-smartwizard-master/dist/js/jquery.smartWizard.min.js',
            'esmis_website_portal/static/js/multi_step.js',

            'esmis_website_portal/static/js/student_grade.js',
            'esmis_website_portal/static/js/student_subject.js',
            'esmis_website_portal/static/js/student_grievance.js',

            'esmis_website_portal/static/js/security_portal.js',
            'esmis_website_portal/static/js/auth_signup.js',

            'esmis_website_portal/static/js/parent_child_subjects.js',
            'esmis_website_portal/static/js/parent_child_grades.js',
            'esmis_website_portal/static/js/parent_grievance.js',

            #PWA related
            'esmis_website_portal/static/lib/idb-keyval/idb-keyval.js'
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
