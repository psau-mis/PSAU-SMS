# Part of eSMIS App. See LICENSE file for full copyright and licensing details.
{
    "name": "eSMIS Cashier Management",
    "category": "eSMIS",
    "version": "16.0.0.0.1",
    "sequence": 1,
    "author": "Pith Technologies",
    "website": "https://pithtech.net",
    "license": "LGPL-3",
    "development_status": "Production/Stable",
    "maintainers": ["gonzalesedwin1123","michaelgonzales"],
    "depends": ["web", "base", "esmis_base", "esmis_enrollment", "esmis_curriculum", "esmis_campus"],

    "data": [
        "security/esmis_cashier_security.xml",
        "security/ir.model.access.csv",
        # "data/employee_position_data.xml",
        "data/fee_data.xml",
        "data/invoice_sequence_data.xml",
        "views/menu_view.xml",
        # "views/cashiers_view.xml",
        "views/cashier_view.xml",
        "views/esmis_coa.xml",
        "views/fees_view.xml",
        "views/fees_types_view.xml",
        "views/enrollment_view.xml",
        "views/course_view.xml",
        "views/student_ledger.xml",
        "views/assessment.xml",
        "views/scholarship_maintenance.xml",
        "wizards/set_or_wizard.xml",
        "reports/paper_format.xml",
        "reports/certificate_of_registration.xml",
        "reports/bulk_cor.xml",
        "reports/or_report.xml",
        "wizards/mode_of_payment.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'esmis_cashier/static/src/xml/widget_view.xml',
            'esmis_cashier/static/src/js/widget.js',
        ],
    },
    "demo": [],
    "images": [],
    "application": False,
    "installable": True,
    "auto_install": False,
}
