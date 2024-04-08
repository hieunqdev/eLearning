{
    'name': "advanced_elearning",
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly

    'depends': ['base', 'survey', 'website_slides'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/s_slide_channel.xml',
        'views/s_survey_question.xml',
        'views/s_survey_survey.xml',
        'views/s_survey_templates.xml',
        'views/s_survey_user_input.xml',
        'views/s_survey_question_views.xml',
        'views/s_survey_survey_views.xml'
    ],
    'assets': {
        'advanced_elearning.survey_page_fill_inherit': [
            'advanced_elearning/static/src/js/survey_templates_dashboard.js',
            'advanced_elearning/static/src/js/s_survey_form.js'
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'css': ['static/src/css/survey_templates_dashboard.css'],
}
