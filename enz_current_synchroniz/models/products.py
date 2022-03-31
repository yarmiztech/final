# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
# from datetime import datetime
# from datetime import date
# import time
# import fcntl
# import socket
# import struct
# import macpath
# from uuid import getnode as get_mac
# from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.constrains('name', 'categ_id','type','parent_id','default_code','l10n_in_hsn_code','purchase_ok','sale_ok','grouped','invoice_policy')
    def constraint_pin_code(self):
        import xmlrpc.client
        synch = self.env['synch.configuration'].search([('activate', '=', True)])
        if synch:
            url = synch.server
            db = synch.db
            username = synch.username
            password = synch.password
            # password = "YEZPR#ADM@786"
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            area_id = models.execute_kw(db, uid, password, 'product.template', 'search_read',
                                        [[['basic_synch_product', '=', self.id], ['name', '=', self.name]]],
                                        {'fields': ['name', 'id', 'l10n_in_hsn_code']})
            categ_id = models.execute_kw(db, uid, password, 'product.category', 'search_read',
                                        [[['name', '=', self.categ_id.name]]],
                                        {'fields': ['name', 'id']})
            parent_id = models.execute_kw(db, uid, password, 'product.template', 'search_read',
                                        [[['name', '=', self.parent_id.name],['grouped', '=', True]]],
                                        {'fields': ['name', 'id']})
            uom_id = models.execute_kw(db, uid, password, 'uom.uom', 'search_read',
                                                    [[['name', '=', self.uom_id.name]]],
                                                    {'fields': ['name', 'id']})
            tax_id = models.execute_kw(db, uid, password, 'account.tax', 'search_read',
                                                    [[['name', '=', self.taxes_id.name]]],
                                                    {'fields': ['name', 'id']})
            if parent_id:
                parent_id = parent_id[0]['id']
            else:
                parent_id = False
            if categ_id:
                categ_id = categ_id[0]['id']
            else:
                categ_id =False
            if tax_id:
                tax_id = tax_id[0]['id']
            else:
                tax_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'product.template', 'create',
                                            [{
                                                'name': self.name,
                                                'l10n_in_hsn_code': self.l10n_in_hsn_code,
                                                'basic_synch_product': str(self.id),
                                                # 'categ_id':categ_id[0]['id'],
                                                'categ_id':categ_id,
                                                'type':self.type,
                                                'default_code':self.default_code,
                                                # 'parent_id':parent_id[0]['id'] or False,
                                                'parent_id':parent_id,
                                                'purchase_ok':self.purchase_ok or False,
                                                'sale_ok':self.sale_ok or False,
                                                'grouped':self.grouped or False,
                                                # 'company_ids':
                                                'uom_id':uom_id[0]['id'],
                                                'list_price':self.list_price,
                                                'taxes_id': [tax_id],
                                                # 'taxes_id':tax_id[0]['id'],

                                                # 'invoice_policy':self.invoice_policy

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'product.template', 'write', [[area_id[0]['id']],
                                                                                         {
                                                                                             'name': self.name,
                                                                                             'l10n_in_hsn_code': self.l10n_in_hsn_code,
                                                                                             'basic_synch_product': str(
                                                                                                 self.id),
                                                                                             # 'categ_id': categ_id['0'][
                                                                                             #     'id'],
                                                                                             'categ_id': categ_id,
                                                                                             'type': self.type,
                                                                                             'default_code': self.default_code,
                                                                                             # 'parent_id': parent_id[0][
                                                                                             #     'id'],
                                                                                             'parent_id':parent_id,
                                                                                             'purchase_ok': self.purchase_ok or False,
                                                                                             'sale_ok': self.sale_ok or False,
                                                                                             'grouped': self.grouped or False,
                                                                                             # 'company_ids':
                                                                                             'uom_id': uom_id[0]['id'],
                                                                                             'list_price': self.list_price,
                                                                                             # 'taxes_id': tax_id[0][
                                                                                             #     'id'],
                                                                                             'taxes_id':[tax_id],
                                                                                             # 'invoice_policy': self.invoice_policy

                                                                                         }])
            return
