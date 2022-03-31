# -*- coding: utf-8 -*-
{
    'name': 'CURRENT ESTIMATE SYNCHRONIZATION',
    'version': '1.0',
    'summary': 'POS',
    'sequence': -100,
    'description': """Local""",
    'category': '',
    'website': 'https://enzapps.com',
    'license': 'LGPL-3',
    'depends': ['base','sale','account','ezp_estimate','enzapps_eway_einvoices','enz_invoice_brother_round_custom','transportation','fleet','ezp_cash_collection','enz_brothers_dec','Inters_company_transfer','stock','enz_mc_owner',
                'opening_balance_customers','brothers_sales_return','salesperson_target','multi_purchase_discount','budget_report_multi','accounts_bankfee_statements'],
    'images': [],
    'data': [
        'security/ir.model.access.csv',
        'views/configuration.xml'

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
