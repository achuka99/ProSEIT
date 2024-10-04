# -*- coding: utf-8 -*-
{
    'name': "ProSEIT",

    'summary': "Professional Software Engineers and IT Practitioners (ProSEIT)",

    'description': """
    The Guild of Professional Software Engineers and IT Practitioners (ProSEIT) is a prestigious professional body that aims to promote professionalism, certified skills, high ethical standards, and innovation in Uganda's software and IT industry.
    """,

    'author': "Crystalline Wealth SMC",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
                'portal',    
                'mail',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/res_partner_category_data.xml',
        'views/proseit_job_portal_views.xml',
        'views/proseit_job_posting_views.xml',
        'views/proseit_project_views.xml',
        'views/proseit_project_portal_views.xml',
        'views/proseit_professional_registration.xml',
        'views/proseit_professional_portal.xml',
        'views/proseit_client_views.xml',
        'views/proseit_company_views.xml',
        'views/proseit_professional_views.xml',
        'views/proseit_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}

