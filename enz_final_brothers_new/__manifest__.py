# -*- coding: utf-8 -*-
{
    'name': "Brothers Final",
    'author':
        'YARMIZ',
    'summary': """
This module will help to assign the targets to sales persons
""",

    'description': """
        Long description of module's purpose
    """,
    'website': "",
    'category': 'base',
    'version': '12.0',
    'depends': ['base','account',"stock","Inters_company_transfer","sale","contacts","ezp_estimate","ezp_cash_collection","boraq_company_branches","budget_report_multi","enz_mc_owner","inventory_sale_purchase","enz_multi_updations","brothers_sales_return"],
    "images": ['static/description/icon.png'],
    'data': [
        'views/amount_withdraw.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
