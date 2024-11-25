# -- coding: utf-8 --
{
    'name': 'eSMIS Faculty Evaluation',
    'version': '16.0.1.0.0',
    'summary': 'Faculty Evaluation Module for Student Portal',
    'description': """
        Assess Faculty through Student answering questionnaires
    """,
    'category': 'Human Resources/Evaluation',
    'author': "NexBridgetech inc.",
    'company': 'NexBridgetech inc.',
    'maintainer': 'NexBridgetech inc.',
    'website': "https://nexbridgetech.com/",
    'depends': [
        'base', 'esmis_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/evaluation_question_data.xml',
        'data/question_ratings_data.xml',
        'views/faculty_evaluation.xml',
        'views/evaluation_question.xml',
        'views/question_ratings.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}