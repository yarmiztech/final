import requests

from odoo import http
from odoo.http import request
from datetime import datetime
from num2words import num2words
import urllib.parse as urlparse
from urllib.parse import parse_qs
from odoo import models,fields,api





class ResSubPartner(models.Model):
    _inherit = 'sub.partner'


    @api.constrains('name','sub_part','partner','vat', 'ref_partner', 'site', 'state_id', 'country_id', 'b_to_b',)
    def constraint_partner(self):
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
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

                print(models)
                # partner_passenger_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                #                                      [[['basic_synch_partner', '=', self.id],['name', '=', self.name]]],
                #                                      {'fields': ['name', 'id', 'mobile']})
                # partner_passenger_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                #                                          [[['basic_synch_sub_partner', '=', self.id],
                #                                            ['name', '=', self.name]]],
                #                                          {'fields': ['name', 'id', 'mobile']})

                for all in self:
                    partner_passenger_id = models.execute_kw(db, uid, password, 'sub.partner', 'search_read',
                                                                             [[['name', '=', all.name]]],
                                                                             {'fields': ['name', 'id']})


                    if not partner_passenger_id:
                        partner = models.execute_kw(db, uid, password, 'sub.partner', 'create',
                                                    [{
                                                        'name': all.name,
                                                        # 'sale_estimate_line': self.sale_estimate_line.id,
                                                        # 'sub_partner': all.sub_partner.id,
                                                        # 'partner': all.partner.id,
                                                        'b_to_b':all.b_to_b or False,
                                                        'b_to_c':all.b_to_c  or False,
                                                        'vat':all.vat  or False,
                                                        'ref_partner':all.ref_partner or False,
                                                        'street': all.street or False,
                                                        'street2': all.street2 or False,
                                                        'site': all.site or False,
                                                        'b2b_company_name': all.b2b_company_name  or False,
                                                        'zip': all.zip  or False,
                                                        'city': all.city  or False,
                                                        'state_id': all.state_id.id,
                                                        'country_id': all.country_id.id,
                                                        'mobile': all.mobile or False,

                                                    }]
                                                    )
                        print(partner, 'partner')
                    else:
                        upd = models.execute_kw(db, uid, password, 'sub.partner', 'write', [[partner_passenger_id[0]['id']],
                                                                                            {
                                                                                                'name': all.name,
                                                                                                # 'sale_estimate_line': self.sale_estimate_line.id,
                                                                                                # 'sub_part': all.sub_part.id,
                                                                                                # 'partner': all.partner.id,
                                                                                                'b_to_b': all.b_to_b or False,
                                                                                                'b_to_c': all.b_to_c or False,
                                                                                                'vat': all.vat or False,
                                                                                                'ref_partner': all.ref_partner or False,
                                                                                                'street': all.street or False,
                                                                                                'street2': all.street2 or False,
                                                                                                'site': all.site or False,
                                                                                                'b2b_company_name': all.b2b_company_name or False,
                                                                                                'zip': all.zip or False,
                                                                                                'city': all.city or False,
                                                                                                'state_id': all.state_id.id,
                                                                                                'country_id': all.country_id.id,
                                                                                                'mobile': all.mobile or False,

                                                                                            }])
                        print(upd, 'upd')
                    return

class SaleEstimate(models.Model):
    _inherit = 'sale.estimate'


    #
    # @api.constrains('estimate_ids')
    # def estimate_ids_test(self):
    #     if self.est_order_id:
    #         import xmlrpc.client
    #         synch = self.env['synch.configuration'].search([('activate', '=', True)])
    #         if synch:
    #             if self:
    #                 url = synch.server
    #                 db = synch.db
    #                 username = synch.username
    #                 password = synch.password
    #                 common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    #                 uid = common.authenticate(db, username, password, {})
    #                 models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    #
    #                 estimate_order = models.execute_kw(db, uid, password, 'estimate.orders', 'search_read',
    #                                                          [[['basic_synch_order', '=', self.est_order_id.id]]],
    #                                                          {'fields': ['name', 'id']})
    #                 if estimate_order:
    #                     estimate_order = estimate_order[0]['id']
    #                 else:
    #                     estimate_order =False
    #                 estimate = models.execute_kw(db, uid, password, 'sale.estimate', 'search_read',
    #                                              [[['est_order_id', '=', estimate_order]]])
    #
    #                 if estimate:
    #                     estimate_ids = []
    #                     sub_list = []
    #                     for line in self.estimate_ids:
    #
    #                         for sub in line.sub_customers:
    #                             partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
    #                                                                 [[['basic_synch_partner', '=', self.partner_id.id]]],
    #                                                                 {'fields': ['name', 'id']})
    #                             if partner_pass_id:
    #                                 partner_pass_id = partner_pass_id[0]['id']
    #                             else:
    #                                 partner_pass_id =False
    #
    #                             partner_sub_id = models.execute_kw(db, uid, password, 'sub.partner', 'search_read',
    #                                                                [[['name', '=', sub.partner.name]]],
    #                                                                {'fields': ['name', 'id']})
    #                             if partner_sub_id:
    #                                 partner_sub_id = partner_sub_id[0]['id']
    #                             else:
    #                                 partner_sub_id =False
    #
    #                             sub_dict = (0, 0, {
    #                                 'sub_partner': partner_pass_id,
    #                                 'partner': partner_sub_id,
    #                                 'tax_ids': sub.tax_ids.ids,
    #                                 'quantity': sub.quantity,
    #                                 'amount': sub.amount,
    #                                 'excluded_value': sub.excluded_value,
    #                                 'vat': sub.vat or False,
    #                                 'b_to_b': sub.b_to_b or False,
    #                                 'site': sub.site or False,
    #                                 'b2b_company_name': sub.b2b_company_name or False,
    #                                 'street': sub.street or False,
    #                                 'street2': sub.street2 or False,
    #                                 'city': sub.city or False,
    #                                 'country_id': sub.country_id.id,
    #                                 'state_id': sub.state_id.id or False,
    #                                 'mobile': sub.mobile or False,
    #                                 'zip': sub.zip or False,
    #                                 'complete_address': sub.complete_address or False,
    #                             })
    #                             sub_list.append(sub_dict)
    #                         product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
    #                                                            [[['name', '=', line.product_id.name]]],
    #                                                            {'fields': ['name', 'id']})
    #
    #                         vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
    #                                                         [[['license_plate', '=', line.vahicle.license_plate]]],
    #                                                         {'fields': ['name', 'id']})
    #                         if vehicle_ser:
    #                             vehicle_ser = vehicle_ser[0]['id']
    #                         else:
    #                             vehicle_ser = False
    #
    #                         vehicle_simply = models.execute_kw(db, uid, password, 'vehicle.simply', 'search_read',
    #                                                            [[['vehi_reg', '=', line.vahicle_char.vehi_reg]]],
    #                                                            {'fields': ['name', 'id']})
    #                         if vehicle_simply:
    #                             vehicle_simply = vehicle_simply[0]['id']
    #                         else:
    #                             vehicle_simply = False
    #
    #                         product_main = (0, 0, {
    #                             'product_id': product_server[0]['id'],
    #                             'company_ids': line.company_ids.ids,
    #                             'branch_id': line.branch_id.id,
    #                             'product_uom': line.product_uom.id,
    #                             'tax_ids': line.tax_ids.ids,
    #                             'product_uom_qty': line.product_uom_qty,
    #                             'price_unit': line.price_unit,
    #                             'dippo_id': line.dippo_id.id,
    #                             'taluk': line.taluk.id,
    #                             'vahicle': vehicle_ser,
    #                             # 'vahicle_char':line.vahicle_char or False,
    #                             'vahicle_char': vehicle_simply,
    #                             'narration': line.narration,
    #                             'vahicle_expense': line.vahicle_expense,
    #                             'exp_inv_price': line.exp_inv_price,
    #                             'sub_customers': sub_list,
    #                         })
    #                         estimate_ids.append(product_main)
    #                     upd = models.execute_kw(db, uid, password, 'sale.estimate', 'write', [[estimate[0]['id']],
    #                                                                                           {
    #                                                                                               'estimate_ids': estimate_ids,
    #                                                                                           }])

    #
    # def action_approve(self):
    #     self.action_approve_server()



    def action_approve(self):
        # rec = super(SaleEstimate, self).action_approve()
        import xmlrpc.client
        synch = self.env['synch.configuration'].search([('activate', '=', True)])
        if synch:
            if self:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

                estimate = models.execute_kw(db, uid, password, 'sale.estimate', 'search_read',
                                                         [[['basic_synch_estimate', '=',self.id]]])

                # xmlrpc.execute_kw(db, uid, password, 'sale.estimate', 'action_approve', [56])
                upd = models.execute_kw(db, uid, password, 'sale.estimate', 'write', [[estimate[0]['id']],
                                                                                    {
                                                                                        'basic_synch_estimate_approve': True,
                                                                                    }])
        return super(SaleEstimate, self).action_approve()
        # return True


        # res = super(SaleEstimate, self).action_approve()
    def action_send_owner(self):
        # rec = super(SaleEstimate, self).action_approve()
        import xmlrpc.client
        synch = self.env['synch.configuration'].search([('activate', '=', True)])
        if synch:
            if self:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

                estimate = models.execute_kw(db, uid, password, 'sale.estimate', 'search_read',
                                                         [[['basic_synch_estimate', '=',self.id]]])

                # xmlrpc.execute_kw(db, uid, password, 'sale.estimate', 'action_approve', [56])
                upd = models.execute_kw(db, uid, password, 'sale.estimate', 'write', [[estimate[0]['id']],
                                                                                    {
                                                                                        'basic_synch_estimate_send_owner': True,
                                                                                    }])
        return super(SaleEstimate, self).action_send_owner()
        # return True


        # res = super(SaleEstimate, self).action_approve()
    def action_cancel(self):
        # rec = super(SaleEstimate, self).action_approve()
        import xmlrpc.client
        synch = self.env['synch.configuration'].search([('activate', '=', True)])
        if synch:
            if self:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

                estimate = models.execute_kw(db, uid, password, 'sale.estimate', 'search_read',
                                                         [[['basic_synch_estimate', '=',self.id]]])

                # xmlrpc.execute_kw(db, uid, password, 'sale.estimate', 'action_approve', [56])
                upd = models.execute_kw(db, uid, password, 'sale.estimate', 'write', [[estimate[0]['id']],
                                                                                    {
                                                                                        'basic_synch_estimate_cancel': True,
                                                                                    }])
        return super(SaleEstimate, self).action_cancel()
        # return True


        # res = super(SaleEstimate, self).action_approve()
    def action_send_approved(self):
        # rec = super(SaleEstimate, self).action_approve()
        import xmlrpc.client
        synch = self.env['synch.configuration'].search([('activate', '=', True)])
        if synch:
            if self:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

                estimate = models.execute_kw(db, uid, password, 'sale.estimate', 'search_read',
                                                         [[['basic_synch_estimate', '=',self.id]]])

                # xmlrpc.execute_kw(db, uid, password, 'sale.estimate', 'action_approve', [56])
                upd = models.execute_kw(db, uid, password, 'sale.estimate', 'write', [[estimate[0]['id']],
                                                                                    {
                                                                                        'basic_synch_estimate_approved': True,
                                                                                    }])
        return super(SaleEstimate, self).action_send_approved()
        # return True


        # res = super(SaleEstimate, self).action_approve()
    def action_send_rejected(self):
        # rec = super(SaleEstimate, self).action_approve()
        import xmlrpc.client
        synch = self.env['synch.configuration'].search([('activate', '=', True)])
        if synch:
            if self:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

                estimate = models.execute_kw(db, uid, password, 'sale.estimate', 'search_read',
                                                         [[['basic_synch_estimate', '=',self.id]]])

                # xmlrpc.execute_kw(db, uid, password, 'sale.estimate', 'action_approve', [56])
                upd = models.execute_kw(db, uid, password, 'sale.estimate', 'write', [[estimate[0]['id']],
                                                                                    {
                                                                                        'basic_synch_estimate_rejected': True,
                                                                                    }])
        return super(SaleEstimate, self).action_send_rejected()
        # return True


        # res = super(SaleEstimate, self).action_approve()




    @api.constrains('name','vat','estimate_ids','est_order_id')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            # if not self.est_order_id:
            if synch:
                    url = synch.server
                    db = synch.db
                    username = synch.username
                    password = synch.password
                    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                    uid = common.authenticate(db, username, password, {})
                    print('uid=', uid)
                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

                    print(models)

                    partner_passenger_id = models.execute_kw(db, uid, password, 'sale.estimate', 'search_read',
                                                         [[['basic_synch_estimate', '=', self.id]]],
                                                         {'fields': ['name', 'id']})
                    # partner_passenger_id = models.execute_kw(db, uid, password, 'sale.estimate', 'search_read',
                    #                                      [[['name', '=', self.name]]],
                    #                                      {'fields': ['name', 'id']})

                    partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                         [[['basic_synch_partner', '=', self.partner_id.id]]],
                                                         {'fields': ['name', 'id']})

                    estimate_ids = []
                    sub_list = []
                    user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                                [[['name', '=', self.user_id.name]]],
                                                {'fields': ['name', 'id']})

                    if user_id:
                        user_id = user_id[0]['id']
                    else:
                        user_id = False

                    for line in self.estimate_ids:
                        for sub in line.sub_customers:
                            partner_sub_id = models.execute_kw(db, uid, password, 'sub.partner', 'search_read',
                                                               [[['name', '=', sub.partner.name]]],
                                                               {'fields': ['name', 'id']})

                            sub_dict = (0, 0, {
                                'sub_partner': partner_pass_id[0]['id'],
                                'partner': partner_sub_id[0]['id'],
                                'tax_ids': sub.tax_ids.ids,
                                'quantity': sub.quantity,
                                'amount': sub.amount,
                                'excluded_value': sub.excluded_value,
                                'vat': sub.vat or False,
                                'b_to_b': sub.b_to_b or False,
                                'site': sub.site or False,
                                'b2b_company_name': sub.b2b_company_name or False,
                                'street': sub.street or False,
                                'street2': sub.street2 or False,
                                'city': sub.city or False,
                                'country_id': sub.country_id.id,
                                'state_id': sub.state_id.id or False,
                                'mobile': sub.mobile or False,
                                'zip': sub.zip or False,
                                'complete_address': sub.complete_address or False,
                            })
                            sub_list.append(sub_dict)
                        product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                           [[['name', '=', line.product_id.name]]],
                                                           {'fields': ['name', 'id']})

                        vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                                                               [[['license_plate', '=', line.vahicle.license_plate]]],
                                                                               {'fields': ['name', 'id']})
                        if vehicle_ser:
                            vehicle_ser = vehicle_ser[0]['id']
                        else:
                            vehicle_ser = False

                        vehicle_simply = models.execute_kw(db, uid, password, 'vehicle.simply', 'search_read',
                                                        [[['vehi_reg', '=', line.vahicle_char.vehi_reg]]],
                                                        {'fields': ['name', 'id']})
                        if vehicle_simply:
                            vehicle_simply = vehicle_simply[0]['id']
                        else:
                            vehicle_simply = False



                        product_main = (0, 0, {
                            'product_id': product_server[0]['id'],
                            'company_ids': line.company_ids.ids,
                            'branch_id': line.branch_id.id,
                            'product_uom': line.product_uom.id,
                            'tax_ids': line.tax_ids.ids,
                            'product_uom_qty': line.product_uom_qty,
                            'price_unit': line.price_unit,
                            'dippo_id': line.dippo_id.id,
                            'taluk': line.taluk.id,
                            'vahicle':vehicle_ser,
                            # 'vahicle_char':line.vahicle_char or False,
                            'vahicle_char':vehicle_simply,
                            'narration': line.narration,
                            'vahicle_expense':line.vahicle_expense,
                            'exp_inv_price': line.exp_inv_price,
                            'sub_customers': sub_list,
                        })
                        estimate_ids.append(product_main)

                    if not partner_passenger_id:

                        partner = models.execute_kw(db, uid, password, 'sale.estimate', 'create',
                                                      [{
                                                              # 'name':self.name,
                                                              'owner_status':self.owner_status,
                                                              'owner_approved_price':self.owner_approved_price,
                                                              'set_selling_reason':self.set_selling_reason,
                                                              'vat':self.vat,
                                                              # 'area':self.area.id ,
                                                              'estimate_type':self.estimate_type,
                                                              'ship_to':self.ship_to,
                                                              'remarks':self.remarks,
                                                              'user_id':user_id,
                                                              'c_date':self.c_date,
                                                              'direct_sale':self.direct_sale,
                                                              'type':self.type ,
                                                              'basic_synch_estimate':str(self.id),
                                                              'payment_type':self.payment_type,
                                                              # 'partner_id':self.partner_id.id,
                                                              'partner_id':partner_pass_id[0]['id'],
                                                              'estimate_ids':estimate_ids,
                                                          }]
                                                      )
                        print(partner,'partner')
                    else:
                        upd = models.execute_kw(db, uid, password, 'sale.estimate', 'write', [[partner_passenger_id[0]['id']],
                                                                                            {
                                                                                'owner_status':self.owner_status,
                                                                                  'owner_approved_price':self.owner_approved_price,
                                                                                  'set_selling_reason':self.set_selling_reason,
                                                                                  'vat':self.vat,
                                                                                  # 'area':self.area.id ,
                                                                                  'estimate_type':self.estimate_type,
                                                                                  'ship_to':self.ship_to,
                                                                                  'remarks':self.remarks,
                                                                                  'user_id':user_id,
                                                                                  'c_date':self.c_date,
                                                                                  'direct_sale':self.direct_sale,
                                                                                  'type':self.type ,
                                                                                  'basic_synch_estimate':str(self.id),
                                                                                  'payment_type':self.payment_type,
                                                                                  # 'partner_id':self.partner_id.id,
                                                                                  'partner_id':partner_pass_id[0]['id'],
                                                                                  'estimate_ids':estimate_ids,
                                                    }])
                    return
            # else:
            #     if synch:
            #         if self:
            #             url = synch.server
            #             db = synch.db
            #             username = synch.username
            #             password = synch.password
            #             common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            #             uid = common.authenticate(db, username, password, {})
            #             models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            #
            #             estimate_order = models.execute_kw(db, uid, password, 'estimate.orders', 'search_read',
            #                                                [[['basic_synch_order', '=', self.est_order_id.id]]],
            #                                                {'fields': ['name', 'id']})
            #             if estimate_order:
            #                 estimate_order = estimate_order[0]['id']
            #             else:
            #                 estimate_order =False
            #             estimate = models.execute_kw(db, uid, password, 'sale.estimate', 'search_read',
            #                                          [[['est_order_id', '=', estimate_order]]])
            #
            #             if estimate:
            #                 estimate_ids = []
            #                 sub_list = []
            #                 for line in self.estimate_ids:
            #
            #                     for sub in line.sub_customers:
            #                         partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
            #                                                             [[['basic_synch_partner', '=',
            #                                                                self.partner_id.id]]],
            #                                                             {'fields': ['name', 'id']})
            #                         if partner_pass_id:
            #                             partner_pass_id = partner_pass_id[0]['id']
            #                         else:
            #                             partner_pass_id = False
            #
            #                         partner_sub_id = models.execute_kw(db, uid, password, 'sub.partner', 'search_read',
            #                                                            [[['name', '=', sub.partner.name]]],
            #                                                            {'fields': ['name', 'id']})
            #                         if partner_sub_id:
            #                             partner_sub_id = partner_sub_id[0]['id']
            #                         else:
            #                             partner_sub_id = False
            #
            #                         sub_dict = (0, 0, {
            #                             'sub_partner': partner_pass_id,
            #                             'partner': partner_sub_id,
            #                             'tax_ids': sub.tax_ids.ids,
            #                             'quantity': sub.quantity,
            #                             'amount': sub.amount,
            #                             'excluded_value': sub.excluded_value,
            #                             'vat': sub.vat or False,
            #                             'b_to_b': sub.b_to_b or False,
            #                             'site': sub.site or False,
            #                             'b2b_company_name': sub.b2b_company_name or False,
            #                             'street': sub.street or False,
            #                             'street2': sub.street2 or False,
            #                             'city': sub.city or False,
            #                             'country_id': sub.country_id.id,
            #                             'state_id': sub.state_id.id or False,
            #                             'mobile': sub.mobile or False,
            #                             'zip': sub.zip or False,
            #                             'complete_address': sub.complete_address or False,
            #                         })
            #                         sub_list.append(sub_dict)
            #                     product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
            #                                                        [[['name', '=', line.product_id.name]]],
            #                                                        {'fields': ['name', 'id']})
            #
            #                     vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
            #                                                     [[['license_plate', '=', line.vahicle.license_plate]]],
            #                                                     {'fields': ['name', 'id']})
            #                     if vehicle_ser:
            #                         vehicle_ser = vehicle_ser[0]['id']
            #                     else:
            #                         vehicle_ser = False
            #
            #                     vehicle_simply = models.execute_kw(db, uid, password, 'vehicle.simply', 'search_read',
            #                                                        [[['vehi_reg', '=', line.vahicle_char.vehi_reg]]],
            #                                                        {'fields': ['name', 'id']})
            #                     if vehicle_simply:
            #                         vehicle_simply = vehicle_simply[0]['id']
            #                     else:
            #                         vehicle_simply = False
            #
            #                     product_main = (0, 0, {
            #                         'product_id': product_server[0]['id'],
            #                         'company_ids': line.company_ids.ids,
            #                         'branch_id': line.branch_id.id,
            #                         'product_uom': line.product_uom.id,
            #                         'tax_ids': line.tax_ids.ids,
            #                         'product_uom_qty': line.product_uom_qty,
            #                         'price_unit': line.price_unit,
            #                         'dippo_id': line.dippo_id.id,
            #                         'taluk': line.taluk.id,
            #                         'vahicle': vehicle_ser,
            #                         # 'vahicle_char':line.vahicle_char or False,
            #                         'vahicle_char': vehicle_simply,
            #                         'narration': line.narration,
            #                         'vahicle_expense': line.vahicle_expense,
            #                         'exp_inv_price': line.exp_inv_price,
            #                         'sub_customers': sub_list,
            #                     })
            #                     estimate_ids.append(product_main)
            #                 # estimate.estimate_ids=False
            #                 upd = models.execute_kw(db, uid, password, 'sale.estimate', 'write', [[estimate[0]['id']],
            #                                                                                       {
            #                                                                                           'estimate_ids': estimate_ids,
            #                                                                                       }])




class VehilcleLocation(models.Model):
    _inherit = 'vehicle.location'

    @api.constrains('name')
    def constraint_name(self):
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
            # area_id = models.execute_kw(db, uid, password, 'estimate.dippo', 'search_read',
            #                             [[['basic_synch_area', '=', self.id], ['name', '=', self.name]]],
            #                             {'fields': ['name', 'id', 'pin_code']})
            area_id = models.execute_kw(db, uid, password, 'vehicle.location', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'vehicle.location', 'create',
                                            [{
                                                'name': self.name,

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'vehicle.location', 'write', [[area_id[0]['id']],
                                                                                       {
                                                                                           'name': self.name,
                                                                                       }])
            return


class EstimateDippo(models.Model):
    _inherit = 'estimate.dippo'

    @api.constrains('name', 'pin_code')
    def constraint_pin_code(self):
        import xmlrpc.client
        synch = self.env['synch.configuration'].search([('activate', '=', True)])
        if synch:
            url = synch.server
            db = synch.db
            username = synch.username
            password = synch.password
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            # area_id = models.execute_kw(db, uid, password, 'estimate.dippo', 'search_read',
            #                             [[['basic_synch_area', '=', self.id], ['name', '=', self.name]]],
            #                             {'fields': ['name', 'id', 'pin_code']})
            area_id = models.execute_kw(db, uid, password, 'estimate.dippo', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})
            taluks = models.execute_kw(db, uid, password, 'vehicle.location', 'search_read',
                                        [[['name', '=', self.taluks.name]]],
                                        {'fields': ['name', 'id']})

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'estimate.dippo', 'create',
                                            [{
                                                'name': self.name,
                                                'amount': self.amount,
                                                'taluks': taluks[0]['id']

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'estimate.dippo', 'write', [[area_id[0]['id']],
                                                                                            {
                                                                                                'name': self.name,
                                                                                                'amount': self.amount,
                                                                                                'taluks': taluks[0]['id']
                                                                                            }])
            return

class DigitalSignCustomers(models.Model):

    _inherit = "digital.sign.form"

    @api.constrains('name', 'create_date','partner_id','place','amount','company_id','actual_amount','balance','balance_inword','digital_signature')
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
            area_id = models.execute_kw(db, uid, password, 'digital.sign.form', 'search_read',
                                        [[['id', '=', self.id]]],
                                        {'fields': ['name', 'id']})
            partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                [[['basic_synch_partner', '=', self.partner_id.id]]],
                                                {'fields': ['name', 'id']})
            if partner_pass_id:
                partner_pass_id = partner_pass_id[0]['id']
            else:
                partner_pass_id = False
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'digital.sign.form', 'create',
                                            [{
                                                'create_date': self.create_date,
                                                'partner_id': partner_pass_id,
                                                'place': self.place,
                                                'amount':self.amount,
                                                'company_id':self.company_id.id,
                                                'actual_amount':self.actual_amount,
                                                'balance':self.balance,
                                                'balance_inword':self.balance_inword,
                                                'digital_signature':self.digital_signature

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'digital.sign.form', 'write', [[area_id[0]['id']],
                                                                                            {
                                                                                                'create_date': self.create_date,
                                                                                                'partner_id': partner_pass_id,
                                                                                                'place': self.place,
                                                                                                'amount': self.amount,
                                                                                                'company_id': self.company_id.id,
                                                                                                'actual_amount': self.actual_amount,
                                                                                                'balance': self.balance,
                                                                                                'balance_inword': self.balance_inword,
                                                                                                'digital_signature': self.digital_signature
                                                                                            }])
            return

