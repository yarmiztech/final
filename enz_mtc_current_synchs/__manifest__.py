# -*- coding: utf-8 -*-
{
    'name': 'Current MTC synchronius',
    'version': '1.0',
    'summary': 'FLEET',
    'sequence': -100,
    'description': """Local""",
    'category': '',
    'website': 'https://enzapps.com',
    'license': 'LGPL-3',
    'depends': ['base','sale','account','transportation','fleet','stock','enz_current_synch','mtc_cashbook','vehicle_allocate','enz_petroleum','hr','transportation_posting','mtc_access_update'],
    'images': [],
    'data': [
        'security/ir.model.access.csv',

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
