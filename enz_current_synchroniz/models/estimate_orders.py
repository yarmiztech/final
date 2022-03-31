import requests

from odoo import http
from odoo.http import request
from datetime import datetime
from num2words import num2words
import urllib.parse as urlparse
from urllib.parse import parse_qs
from odoo import models,fields,api



class EstimateOrders(models.Model):
    _inherit = 'estimate.orders'


    def action_oder_confirm(self):
        # rec = super(SaleEstimate, self).action_approve()
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

            estimate = models.execute_kw(db, uid, password, 'estimate.orders', 'search_read',
                                                     [[['basic_synch_order', '=',self.id]]])

            upd = models.execute_kw(db, uid, password, 'estimate.orders', 'write', [[estimate[0]['id']],
                                                                                {
                                                                                    'basic_synch_order_button': True,
                                                                                }])
        return super(EstimateOrders, self).action_oder_confirm()
        # return True


        # res = super(SaleEstimate, self).action_approve()




    @api.constrains('name','partner_id','order_lines','user_id','estimate_order_shop')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
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

                # partner_passenger_id = models.execute_kw(db, uid, password, 'sale.estimate', 'search_read',
                #                                      [[['basic_synch_partner', '=', self.id],['name', '=', self.name]]],
                #                                      {'fields': ['name', 'id', 'mobile']})
                partner_passenger_id = models.execute_kw(db, uid, password, 'estimate.orders', 'search_read',
                                                     [[['basic_synch_order', '=', self.id]]],
                                                     {'fields': ['name', 'id']})

                partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                     [[['basic_synch_partner', '=', self.partner_id.id]]],
                                                     {'fields': ['name', 'id']})
                if partner_pass_id:
                    partner_pass_id = partner_pass_id[0]['id']
                else:
                    partner_pass_id =False
                user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                            [[['name', '=', self.user_id.name]]],
                                            {'fields': ['name', 'id']})

                if user_id:
                    user_id = user_id[0]['id']
                else:
                    user_id = False
                estimate_user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                            [[['name', '=', self.estimate_user_id.name]]],
                                            {'fields': ['name', 'id']})

                if estimate_user_id:
                    estimate_user_id = estimate_user_id[0]['id']
                else:
                    estimate_user_id = False
                area_wise = models.execute_kw(db, uid, password, 'area.wise', 'search_read',
                                            [[['name', '=', self.area.name]]],
                                            {'fields': ['name', 'id']})

                if area_wise:
                    area_wise = area_wise[0]['id']
                else:
                    area_wise = False
                exe_area_wise = models.execute_kw(db, uid, password, 'executive.area.wise', 'search_read',
                                            [[['name', '=', self.executive_areas.name]]],
                                            {'fields': ['name', 'id']})

                if exe_area_wise:
                    exe_area_wise = exe_area_wise[0]['id']
                else:
                    exe_area_wise = False

                estimate_ids = []
                for line in self.order_lines:
                    product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                       [[['name', '=', line.product_id.name]]],
                                                       {'fields': ['name', 'id']})
                    if product_server:
                        product_server = product_server[0]['id']
                    else:
                        product_server =False
                    product_uom = models.execute_kw(db, uid, password, 'uom.uom', 'search_read',
                                                       [[['name', '=', line.product_uom.name]]],
                                                       {'fields': ['name', 'id']})
                    if product_uom:
                        product_uom = product_uom[0]['id']
                    else:
                        product_uom = False


                    product_main = (0, 0, {
                        'product_id': product_server,
                        'product_uom':product_uom,
                        'char_price': line.char_price,
                        'price': line.price,
                        'char_quantity': line.char_quantity,
                        'quantity': line.quantity,
                    })
                    estimate_ids.append(product_main)

                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'estimate.orders', 'create',
                                                  [{
                                                          'total_amount':self.total_amount,
                                                          'credit_status':self.credit_status,
                                                          'estimate_order_shop':self.estimate_order_shop,
                                                          'c_date':self.c_date,
                                                          'area':area_wise ,
                                                         'basic_synch_order':str(self.id),
                                                          'inv_status':self.inv_status,
                                                          'deli_status':self.deli_status,
                                                          'executive_areas':exe_area_wise,
                                                          'estimate_user_id':estimate_user_id,
                                                          'user_id':user_id,
                                                          'another_area':self.another_area ,
                                                          # 'basic_synch_estimate':str(self.id),
                                                          'vat':self.vat,
                                                          'partner_id':partner_pass_id,
                                                          'order_lines':estimate_ids,
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'estimate.orders', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'total_amount': self.total_amount,
                                                                                            'credit_status': self.credit_status,
                                                                                            'estimate_order_shop': self.estimate_order_shop,
                                                                                            'c_date': self.c_date,
                                                                                            'area': area_wise,
                                                                                            'inv_status': self.inv_status,
                                                                                            'deli_status': self.deli_status,
                                                                                            'executive_areas': exe_area_wise,
                                                                                            'estimate_user_id': estimate_user_id,
                                                                                            'user_id': user_id,
                                                                                            'another_area': self.another_area,
                                                                                            # 'basic_synch_estimate':str(self.id),
                                                                                            'vat': self.vat,
                                                                                            'partner_id': partner_pass_id,
                                                }])
                return






class CompanySoPOTransfer(models.Model):
    _inherit = 'company.sopo.transfer'



    def send_other_location(self):
        # rec = super(SaleEstimate, self).action_approve()
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

            estimate = models.execute_kw(db, uid, password, 'company.sopo.transfer', 'search_read',
                                                     [[['basic_synch_sopo', '=',self.id]]])

            upd = models.execute_kw(db, uid, password, 'company.sopo.transfer', 'write', [[estimate[0]['id']],
                                                                                {
                                                                                    'basic_synch_sopo_button': True,
                                                                                }])
        return super(CompanySoPOTransfer, self).send_other_location()

    @api.constrains('name','from_company','to_company','inter_company_lines','vehicle_no')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'company.sopo.transfer', 'search_read',
                                            [[['name', '=', self.from_company.name]]],
                                            {'fields': ['name', 'id']})
                estimate_ids = []
                for line in self.inter_company_lines:
                    product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                       [[['name', '=', line.product_id.name]]],
                                                       {'fields': ['name', 'id']})
                    if product_server:
                        product_server = product_server[0]['id']
                    else:
                        product_server =False
                    product_uom = models.execute_kw(db, uid, password, 'uom.uom', 'search_read',
                                                       [[['name', '=', line.uom_id.name]]],
                                                       {'fields': ['name', 'id']})
                    if product_uom:
                        product_uom = product_uom[0]['id']
                    else:
                        product_uom = False

                    product_main = (0, 0, {
                        'product_id': product_server,
                        'uom_id':product_uom,
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit': line.price_unit,
                        'product_hsn_code': line.product_hsn_code,
                        'company_id': line.company_id.id,
                        'tax_id': line.tax_id.ids,
                        'sub_total': line.sub_total,
                    })
                    estimate_ids.append(product_main)

                from_company = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                       [[['name', '=', self.from_company.name]]],
                                                       {'fields': ['name', 'id']})
                if from_company:
                    from_company = from_company[0]['id']
                else:
                    from_company = False
                to_company = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                 [[['name', '=', self.to_company.name]]],
                                                 {'fields': ['name', 'id']})
                if to_company:
                    to_company = to_company[0]['id']
                else:
                    to_company = False

                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'company.sopo.transfer', 'create',
                                                  [{
                                                          'from_company':from_company,
                                                          'to_company':to_company,
                                                      'basic_synch_sopo':str(self.id),
                                                          # 'estimate_order_shop':self.estimate_order_shop,
                                                          'inter_company_lines':estimate_ids,
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'company.sopo.transfer', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'from_company':from_company,
                                                                                            'to_company': to_company,
                                                                                            'basic_synch_sopo': str(
                                                                                                self.id),
                                                                                            # 'estimate_order_shop':self.estimate_order_shop,
                                                                                            'inter_company_lines': estimate_ids,
                                                }])
                return




class Location(models.Model):
    _inherit = "stock.location"



    @api.constrains('name','location_id','usage','company_id','branch_id')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'stock.location', 'search_read',
                                            [[['name', '=', self.name]]],
                                            {'fields': ['name', 'id']})
                estimate_ids = []

                company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                       [[['name', '=', self.company_id.name]]],
                                                       {'fields': ['name', 'id']})
                if company_id:
                    company_id = company_id[0]['id']
                else:
                    company_id = False
                location_id = models.execute_kw(db, uid, password, 'stock.location', 'search_read',
                                                       [[['name', '=', self.location_id.name]]],
                                                       {'fields': ['name', 'id']})
                if location_id:
                    location_id = location_id[0]['id']
                else:
                    location_id = False

                branch_id = models.execute_kw(db, uid, password, 'stock.location', 'search_read',
                                                       [[['name', '=', self.branch_id.name]]],
                                                       {'fields': ['name', 'id']})
                if branch_id:
                    branch_id = branch_id[0]['id']
                else:
                    branch_id = False
                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'stock.location', 'create',
                                                  [{
                                                          'name':self.name,
                                                          'usage':self.usage,
                                                          'company_id':company_id,
                                                          'location_id':location_id,
                                                          'branch_id':branch_id,
                                                      # 'basic_synch_sopo':str(self.id),
                                                          # 'estimate_order_shop':self.estimate_order_shop,
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'stock.location', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'name': self.name,
                                                                                            'usage': self.usage,
                                                                                            'company_id': company_id,
                                                                                            'location_id': location_id,
                                                                                            'branch_id': branch_id,
                                                }])
                return




class InterBranchTransfer(models.Model):
    _inherit = 'inter.branch.transfer'


    def send_other_location(self):
        # rec = super(SaleEstimate, self).action_approve()
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

            estimate = models.execute_kw(db, uid, password, 'inter.branch.transfer', 'search_read',
                                                     [[['basic_synch_transfer', '=',self.id]]])

            upd = models.execute_kw(db, uid, password, 'inter.branch.transfer', 'write', [[estimate[0]['id']],
                                                                                {
                                                                                    'basic_synch_transfer_button': True,
                                                                                }])
        return super(InterBranchTransfer, self).send_other_location()





    @api.constrains('company_id','partner_id','from_branch','location_id','to_branch','dest_location_id','inter_company_lines')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'inter.branch.transfer', 'search_read',
                                            [[['basic_synch_transfer', '=', self.id]]],
                                            {'fields': ['name', 'id']})
                estimate_ids = []
                for line in self.inter_company_lines:
                    product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                       [[['name', '=', line.product_id.name]]],
                                                       {'fields': ['name', 'id']})
                    if product_server:
                        product_server = product_server[0]['id']
                    else:
                        product_server =False
                    uom_id = models.execute_kw(db, uid, password, 'uom.uom', 'search_read',
                                                       [[['name', '=', line.uom_id.name]]],
                                                       {'fields': ['name', 'id']})
                    if uom_id:
                        uom_id = uom_id[0]['id']
                    else:
                        uom_id = False

                    product_main = (0, 0, {
                        'product_id': product_server,
                        'uom_id':uom_id,
                        'transfer_qty': line.transfer_qty,
                        'price_unit': line.price_unit,
                    })
                    estimate_ids.append(product_main)

                company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                       [[['name', '=', self.company_id.name]]],
                                                       {'fields': ['name', 'id']})
                if company_id:
                    company_id = company_id[0]['id']
                else:
                    company_id = False
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', self.partner_id.id],
                                                 ]],
                                               {'fields': ['name', 'id', 'mobile']})
                if partner_id:
                    partner_id = partner_id[0]['id']
                else:
                    partner_id = False
                from_branch = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                                       [[['name', '=', self.from_branch.name]]],
                                                       {'fields': ['name', 'id']})
                if from_branch:
                    from_branch = from_branch[0]['id']
                else:
                    from_branch = False
                to_branch = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                                       [[['name', '=', self.to_branch.name]]],
                                                       {'fields': ['name', 'id']})
                if to_branch:
                    to_branch = to_branch[0]['id']
                else:
                    to_branch = False
                location_id = models.execute_kw(db, uid, password, 'stock.location', 'search_read',
                                                       [[['name', '=', self.location_id.name]]],
                                                       {'fields': ['name', 'id']})
                if location_id:
                    location_id = location_id[0]['id']
                else:
                    location_id = False

                dest_location_id = models.execute_kw(db, uid, password, 'stock.location', 'search_read',
                                                       [[['name', '=', self.dest_location_id.name]]],
                                                       {'fields': ['name', 'id']})
                if dest_location_id:
                    dest_location_id = dest_location_id[0]['id']
                else:
                    dest_location_id = False

                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'inter.branch.transfer', 'create',
                                                  [{
                                                          'basic_synch_transfer':str(self.id),
                                                          'company_id':company_id,
                                                          'partner_id':partner_id,
                                                          'from_branch':from_branch,
                                                          'to_branch':to_branch,
                                                          'location_id':location_id,
                                                          'dest_location_id':dest_location_id,
                                                          'inter_company_lines':estimate_ids,
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'inter.branch.transfer', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'company_id': company_id,
                                                                                            'partner_id': partner_id,
                                                                                            'from_branch': from_branch,
                                                                                            'to_branch': to_branch,
                                                                                            'location_id': location_id,
                                                                                            'dest_location_id': dest_location_id,
                                                                                            'inter_company_lines': estimate_ids,
                                                }])
                return




class OpeningBalanceCustomers(models.Model):
    _inherit = "opening.balance.customers"
    def action_opening_bal_all(self):
        # rec = super(SaleEstimate, self).action_approve()
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

            estimate = models.execute_kw(db, uid, password, 'opening.balance.customers', 'search_read',
                                                     [[['basic_synch_opening', '=',self.id]]])

            upd = models.execute_kw(db, uid, password, 'opening.balance.customers', 'write', [[estimate[0]['id']],
                                                                                {
                                                                                    'basic_synch_opening_button': True,
                                                                                }])
        return super(OpeningBalanceCustomers, self).action_opening_bal_all()




    @api.constrains('start_date','type_of_partner','company_id','type_of_credit','op_lines')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'opening.balance.customers', 'search_read',
                                            [[['basic_synch_opening', '=', self.id]]],
                                            {'fields': ['name', 'id']})
                estimate_ids = []
                for line in self.op_lines:
                    partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                   [[['basic_synch_partner', '=', line.partner_id.id],
                                                     ]],
                                                   {'fields': ['name', 'id', 'mobile']})
                    if partner_id:
                        partner_id = partner_id[0]['id']
                    else:
                        partner_id = False

                    # area_wise = models.execute_kw(db, uid, password, 'area.wise', 'search_read',
                    #                               [[['name', '=', self.area.name]]],
                    #                               {'fields': ['name', 'id']})
                    #
                    # if area_wise:
                    #     area_wise = area_wise[0]['id']
                    # else:
                    #     area_wise = False

                    product_main = (0, 0, {
                        'partner_id': partner_id,
                        # 'area':area_wise,
                        'op_amount': line.op_amount,
                    })
                    estimate_ids.append(product_main)

                company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                       [[['name', '=', self.company_id.name]]],
                                                       {'fields': ['name', 'id']})
                if company_id:
                    company_id = company_id[0]['id']
                else:
                    company_id = False
                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'opening.balance.customers', 'create',
                                                  [{
                                                          'start_date':self.start_date,
                                                          'company_id':company_id,
                                                          'basic_synch_opening':str(self.id),
                                                          'type_of_partner':self.type_of_partner,
                                                          'type_of_credit':self.type_of_credit,
                                                          'op_lines':estimate_ids,
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'opening.balance.customers', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'start_date': self.start_date,
                                                                                            'company_id': company_id,
                                                                                            'basic_synch_opening': str(
                                                                                                self.id),
                                                                                            'type_of_partner': self.type_of_partner,
                                                                                            'type_of_credit': self.type_of_credit,
                                                                                            'op_lines': estimate_ids,
                                                                                        }])
                return




class OpenAccountBalance(models.Model):
    _inherit = 'open.account.balance'



    def op_create(self):
            # rec = super(SaleEstimate, self).action_approve()
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

                estimate = models.execute_kw(db, uid, password, 'open.account.balance', 'search_read',
                                             [[['basic_synch_ac_balance', '=', self.id]]])

                upd = models.execute_kw(db, uid, password, 'open.account.balance', 'write', [[estimate[0]['id']],
                                                                                                  {
                                                                                                      'basic_synch_ac_balance_button': True,
                                                                                                  }])
            return super(OpenAccountBalance, self).op_create()

    @api.constrains('create_date','open_lines')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'open.account.balance', 'search_read',
                                            [[['basic_synch_ac_balance', '=', self.id]]],
                                            {'fields': ['name', 'id']})
                estimate_ids = []
                for line in self.open_lines:
                    journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                   [[['name', '=', line.journal_id.name],
                                                     ['company_id', '=', line.journal_id.company_id.id]]],
                                                   {'fields': ['name', 'id']})

                    if journal_id:
                        journal_id = journal_id[0]['id']
                    else:
                        journal_id = False

                    account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                   [[['name', '=', line.account_id.name],
                                                     ['company_id', '=', line.account_id.company_id.id]]],
                                                   {'fields': ['name', 'id']})

                    if account_id:
                        account_id = account_id[0]['id']
                    else:
                        account_id = False
                    product_main = (0, 0, {
                        'journal_id': journal_id,
                        'account_id': account_id,
                        'op_balance': line.op_balance,
                    })
                    estimate_ids.append(product_main)
                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'open.account.balance', 'create',
                                                  [{
                                                          'create_date':self.create_date,
                                                          'basic_synch_ac_balance':str(self.id),
                                                          'open_lines':estimate_ids,
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'open.account.balance', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                              'create_date':self.create_date,
                                                                                              # 'basic_synch_opening':str(self.id),
                                                                                                'open_lines':estimate_ids,
                                                                                        }])
                return




class SalesReturn(models.Model):
    _inherit = 'sales.return'


    def credit_note_validation(self):
            # rec = super(SaleEstimate, self).action_approve()
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

                estimate = models.execute_kw(db, uid, password, 'sales.return', 'search_read',
                                             [[['basic_synch_return', '=', self.id]]])

                upd = models.execute_kw(db, uid, password, 'sales.return', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_return_button': True,
                                                                                             }])
            return super(SalesReturn, self).credit_note_validation()

    @api.constrains('partner_id','invoice_id','create_date','sales_returns_lines')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'sales.return', 'search_read',
                                            [[['basic_synch_return', '=', self.id]]],
                                            {'fields': ['name', 'id']})
                estimate_ids = []
                for line in self.sales_returns_lines:
                    product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                       [[['name', '=', line.product_id.name]]],
                                                       {'fields': ['name', 'id']})
                    if product_server:
                        product_server = product_server[0]['id']
                    else:
                        product_server = False
                    product_main = (0, 0, {
                        'product_id': product_server,
                        'quantity': line.quantity,
                        'price_unit': line.price_unit,
                        'tax_ids': line.tax_ids.ids,
                        'sub_total': line.sub_total,
                    })
                    estimate_ids.append(product_main)

                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', self.partner_id.id],
                                                 ]],
                                               {'fields': ['name', 'id']})
                if partner_id:
                    partner_id = partner_id[0]['id']
                else:
                    partner_id = False

                invoice_id = models.execute_kw(db, uid, password, 'account.move', 'search_read',
                                               [[['name', '=', self.invoice_id.name],
                                                 ]],
                                               {'fields': ['name', 'id']})
                if invoice_id:
                    invoice_id = invoice_id[0]['id']
                else:
                    invoice_id = False



                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'sales.return', 'create',
                                                  [{
                                                          'create_date':self.create_date,
                                                          'partner_id':partner_id,
                                                          'invoice_id':invoice_id,
                                                            'basic_synch_return':str(self.id),
                                                          # 'basic_synch_ac_balance':str(self.id),
                                                          'sales_returns_lines':estimate_ids,
                                                      'reason':self.reason
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'sales.return', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'create_date': self.create_date,
                                                                                            'partner_id': partner_id,
                                                                                            'invoice_id': invoice_id,
                                                                                            'reason': self.reason,
                                                                                            # 'basic_synch_ac_balance':str(self.id),
                                                                                            'sales_returns_lines': estimate_ids,
                                                                                        }])
                return




class SalesInvoiceCancel(models.Model):
    _inherit = 'sales.invoice.cancel'


    def action_cancel_create(self):
            # rec = super(SaleEstimate, self).action_approve()
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

                estimate = models.execute_kw(db, uid, password, 'sales.invoice.cancel', 'search_read',
                                             [[['basic_synch_cancel', '=', self.id]]])

                upd = models.execute_kw(db, uid, password, 'sales.invoice.cancel', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_cancel_button': True,
                                                                                             }])
            return super(SalesInvoiceCancel, self).action_cancel_create()


    @api.constrains('partner_id','invoice_id','create_date','branch_id','vehicle','sales_return_lines','company_id','complete_address','vat')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'sales.invoice.cancel', 'search_read',
                                            [[['basic_synch_cancel', '=', self.id]]],
                                            {'fields': ['name', 'id']})
                estimate_ids = []
                for line in self.sales_return_lines:
                    product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                       [[['name', '=', line.product_id.name]]],
                                                       {'fields': ['name', 'id']})
                    if product_server:
                        product_server = product_server[0]['id']
                    else:
                        product_server = False
                    product_main = (0, 0, {
                        'product_id': product_server,
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit': line.price_unit,
                        'tax_ids': line.tax_ids.ids,
                        'sub_total': line.sub_total,
                    })
                    estimate_ids.append(product_main)

                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', self.partner_id.id],
                                                 ]],
                                               {'fields': ['name', 'id']})
                if partner_id:
                    partner_id = partner_id[0]['id']
                else:
                    partner_id = False

                invoice_id = models.execute_kw(db, uid, password, 'account.move', 'search_read',
                                               [[['name', '=', self.invoice_id.name],
                                                 ]],
                                               {'fields': ['name', 'id']})
                if invoice_id:
                    invoice_id = invoice_id[0]['id']
                else:
                    invoice_id = False
                branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                                       [[['name', '=', self.branch_id.name]]],
                                                       {'fields': ['name', 'id']})
                if branch_id:
                    branch_id = branch_id[0]['id']
                else:
                    branch_id = False


                user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                            [[['name', '=', self.user_id.name]]],
                                            {'fields': ['name', 'id']})

                if user_id:
                    user_id = user_id[0]['id']
                else:
                    user_id = False
                company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                       [[['name', '=', self.company_id.name]]],
                                                       {'fields': ['name', 'id']})
                if company_id:
                    company_id = company_id[0]['id']
                else:
                    company_id = False


                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'sales.invoice.cancel', 'create',
                                                  [{
                                                          'create_date':self.create_date,
                                                          'basic_synch_cancel':str(self.id),
                                                          'partner_id':partner_id,
                                                          'invoice_id':invoice_id,
                                                          'branch_id':branch_id,
                                                          'vehicle':self.vehicle,
                                                          'complete_address':self.complete_address,
                                                          'user_id':user_id,
                                                          'company_id':company_id,
                                                            # 'basic_synch_return':str(self.id),
                                                          # 'basic_synch_ac_balance':str(self.id),
                                                          'sales_return_lines':estimate_ids,
                                                      'vat':self.vat
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'sales.invoice.cancel', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'create_date': self.create_date,
                                                                                            'partner_id': partner_id,
                                                                                            'invoice_id': invoice_id,
                                                                                            'branch_id': branch_id,
                                                                                            'vehicle': self.vehicle,
                                                                                            'complete_address': self.complete_address,
                                                                                            'user_id': user_id,
                                                                                            'company_id': company_id,
                                                                                            # 'basic_synch_return':str(self.id),
                                                                                            # 'basic_synch_ac_balance':str(self.id),
                                                                                            'sales_return_lines': estimate_ids,
                                                                                            'vat': self.vat
                                                                                        }])
                return



class CreditLimitRecord(models.Model):
    _inherit = "credit.limit.record"


    @api.constrains('date','credit_limit_lines')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'credit.limit.record', 'search_read',
                                            [[['date', '=', self.date]]],
                                            {'fields': ['name', 'id']})
                estimate_ids = []
                for line in self.credit_limit_lines:
                    partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                   [[['basic_synch_partner', '=', line.partner_id.id],
                                                     ]],
                                                   {'fields': ['name', 'id']})
                    if partner_id:
                        partner_id = partner_id[0]['id']
                    else:
                        partner_id = False

                    product_main = (0, 0, {
                            'partner_id': partner_id,
                            'average_amount': line.average_amount,
                            'balance': line.balance,
                            'credit_limit_amount': line.credit_limit_amount,
                            'min_credit_amount': line.min_credit_amount,
                        })
                    estimate_ids.append(product_main)



                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'credit.limit.record', 'create',
                                                  [{
                                                          'date':self.date,
                                                          'credit_limit_lines':estimate_ids,
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'credit.limit.record', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'date': self.date,
                                                                                            'credit_limit_lines': estimate_ids,
                                                                                        }])
                return


class SalesIncentives(models.Model):
    _inherit = "sales.person.incentives"

    def action_incentives(self):
            # rec = super(SaleEstimate, self).action_approve()
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

                estimate = models.execute_kw(db, uid, password, 'sales.person.incentives', 'search_read',
                                             [[['basic_synch_incentives', '=', self.id]]])

                upd = models.execute_kw(db, uid, password, 'sales.person.incentives', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_incentives_button': True,
                                                                                             }])
            return super(SalesIncentives, self).action_incentives()


    @api.constrains('name','company_id')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'sales.person.incentives', 'search_read',
                                            [[['basic_synch_incentives', '=', self.id]]],
                                            {'fields': ['name', 'id']})
                estimate_ids = []
                for line in self.incentive_lines:
                    product_main = (0, 0, {
                            'per_type': line.per_type,
                            'achievement_percentage': line.achievement_percentage,
                            'reward': line.reward,
                            'type': line.type,
                        })
                    estimate_ids.append(product_main)
                company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                       [[['name', '=', self.company_id.name]]],
                                                       {'fields': ['name', 'id']})
                if company_id:
                    company_id = company_id[0]['id']
                else:
                    company_id = False



                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'sales.person.incentives', 'create',
                                                  [{
                                                          'name':self.name,
                                                          'company_id':company_id,
                                                          'basic_synch_incentives':str(self.id),
                                                          'incentive_lines':estimate_ids,
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'sales.person.incentives', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'name': self.name,
                                                                                            'company_id': company_id,
                                                                                            'incentive_lines': estimate_ids,
                                                                                        }])
                return


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.constrains('name', 'company_id','type','default_account_id','suspense_account_id','profit_account_id',
                    'loss_account_id','code','bank_account_id','payment_debit_account_id','payment_credit_account_id')
    def constraint_partner(self):
        import xmlrpc.client
        synch = self.env['synch.configuration'].search([('activate', '=', True)])
        if synch:
            url = synch.server
            db = synch.db
            username = synch.username
            password = synch.password
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            print('uid=', uid)
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            partner_passenger_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                     [[['basic_synch_journal', '=', self.id]]],
                                                     {'fields': ['name', 'id']})
            estimate_ids = []
            company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                           [[['name', '=', self.company_id.name]]],
                                           {'fields': ['name', 'id']})
            if company_id:
                company_id = company_id[0]['id']
            else:
                company_id = False
            if self.l10n_in_gstin_partner_id:

                l10n_in_gstin_partner_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                               [[['basic_synch_partner', '=', self.l10n_in_gstin_partner_id.id],
                                                 ]],
                                               {'fields': ['name', 'id']})
                if l10n_in_gstin_partner_id:
                    l10n_in_gstin_partner_id = l10n_in_gstin_partner_id[0]['id']
                else:
                    l10n_in_gstin_partner_id = False

            else:
                l10n_in_gstin_partner_id = False
            default_account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                [[['name', '=', self.default_account_id.name],
                                                  ['company_id', '=', self.default_account_id.company_id.id]
                                                  ]],
                                                {'fields': ['name', 'id']})
            if default_account_id:
                default_account_id = default_account_id[0]['id']
            else:
                default_account_id = False
            suspense_account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                [[['name', '=', self.suspense_account_id.name],
                                                  ['company_id', '=', self.suspense_account_id.company_id.id]
                                                  ]],
                                                {'fields': ['name', 'id']})
            if suspense_account_id:
                suspense_account_id = suspense_account_id[0]['id']
            else:
                suspense_account_id = False
            profit_account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                [[['name', '=', self.profit_account_id.name],
                                                  ['company_id', '=', self.profit_account_id.company_id.id]
                                                  ]],
                                                {'fields': ['name', 'id']})
            if profit_account_id:
                profit_account_id = profit_account_id[0]['id']
            else:
                profit_account_id = False
            loss_account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                [[['name', '=', self.loss_account_id.name],
                                                  ['company_id', '=', self.loss_account_id.company_id.id]
                                                  ]],
                                                {'fields': ['name', 'id']})
            if loss_account_id:
                loss_account_id = loss_account_id[0]['id']
            else:
                loss_account_id = False
            payment_debit_account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                [[['name', '=', self.payment_debit_account_id.name],
                                                  ['company_id', '=', self.payment_debit_account_id.company_id.id]
                                                  ]],
                                                {'fields': ['name', 'id']})
            if payment_debit_account_id:
                payment_debit_account_id = payment_debit_account_id[0]['id']
            else:
                payment_debit_account_id = False
            payment_credit_account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                [[['name', '=', self.payment_credit_account_id.name],
                                                  ['company_id', '=', self.payment_credit_account_id.company_id.id]
                                                  ]],
                                                {'fields': ['name', 'id']})
            if payment_credit_account_id:
                payment_credit_account_id = payment_credit_account_id[0]['id']
            else:
                payment_credit_account_id = False

            if not partner_passenger_id:

                partner = models.execute_kw(db, uid, password, 'account.journal', 'create',
                                            [{
                                                'name': self.name,
                                                'company_id': company_id,
                                                'type': self.type,
                                                'l10n_in_gstin_partner_id': l10n_in_gstin_partner_id,
                                                'default_account_id': default_account_id,
                                                'suspense_account_id': suspense_account_id,
                                                'profit_account_id': profit_account_id,
                                                'loss_account_id': loss_account_id,
                                                'payment_debit_account_id': payment_debit_account_id,
                                                'payment_credit_account_id': payment_credit_account_id,
                                                'code': self.code,
                                                'basic_synch_journal': str(self.id),
                                                # 'incentive_lines': estimate_ids,
                                            }]
                                            )
                print(partner, 'partner')
            else:
                upd = models.execute_kw(db, uid, password, 'account.journal', 'write',
                                        [[partner_passenger_id[0]['id']],
                                         {
                                             'name': self.name,
                                             'company_id': company_id,
                                             'type': self.type,
                                             'l10n_in_gstin_partner_id': l10n_in_gstin_partner_id,
                                             'default_account_id': default_account_id,
                                             'suspense_account_id': suspense_account_id,
                                             'profit_account_id': profit_account_id,
                                             'loss_account_id': loss_account_id,
                                             'payment_debit_account_id': payment_debit_account_id,
                                             'payment_credit_account_id': payment_credit_account_id,
                                             'code': self.code,
                                             # 'basic_synch_incentives': str(self.id),
                                             # 'incentive_lines': estimate_ids,
                                         }])
            return




class ResBank(models.Model):
    _inherit = "res.bank"



    @api.constrains('name','bic','phone','email','street','street2','city','state','zip','country')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'res.bank', 'search_read',
                                            [[['bic', '=', self.bic]]],
                                            {'fields': ['name', 'id']})
                estimate_ids = []

                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'res.bank', 'create',
                                                  [{
                                                          'name':self.name,
                                                          'bic':self.bic,
                                                          'phone':self.phone,
                                                          'email':self.email,
                                                          'street':self.street,
                                                          'street2':self.street2,
                                                          'city':self.city,
                                                          'state':self.state.id,
                                                          'zip':self.zip,
                                                          'country':self.country.id,
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'res.bank', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                             'name':self.name,
                                                          'bic':self.bic,
                                                          'phone':self.phone,
                                                          'email':self.email,
                                                          'street':self.street,
                                                          'street2':self.street2,
                                                          'city':self.city,
                                                          'state':self.state.id,
                                                          'zip':self.zip,
                                                          'country':self.country.id,
                                                                                        }])
                return




class SetupBarBankConfigWizard(models.TransientModel):
    _inherit = 'account.setup.bank.manual.config'


    @api.constrains('acc_number','bank_id','bank_bic','linked_journal_id')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'account.setup.bank.manual.config', 'search_read',
                                            [[['acc_number', '=', self.acc_number]]],
                                            {'fields': ['name', 'id']})
                estimate_ids = []
                if self.bank_id:
                    bank_id = models.execute_kw(db, uid, password, 'res.bank', 'search_read',
                                                             [[['name', '=', self.bank_id.name]]],
                                                             {'fields': ['name', 'id']})
                    if bank_id:
                        bank_id = bank_id[0]['id']
                    else:
                        bank_id =False
                else:
                    bank_id = False
                if self.linked_journal_id:
                    linked_journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                   [[['name', '=', self.linked_journal_id.name],
                                                     ['company_id', '=', self.linked_journal_id.company_id.id]]],
                                                   {'fields': ['name', 'id']})

                    if linked_journal_id:
                        linked_journal_id = linked_journal_id[0]['id']
                    else:
                        linked_journal_id = False
                else:
                    linked_journal_id = False
                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'account.setup.bank.manual.config', 'create',
                                                  [{
                                                          'acc_number':self.acc_number,
                                                          'bank_id':bank_id,
                                                          'bank_bic':self.bank_bic,
                                                          # 'basic_synch_incentives':str(self.id),
                                                          'linked_journal_id':linked_journal_id,
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'account.setup.bank.manual.config', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'acc_number': self.acc_number,
                                                                                            'bank_id': bank_id,
                                                                                            'bank_bic': self.bank_bic,
                                                                                            # 'basic_synch_incentives':str(self.id),
                                                                                            'linked_journal_id': linked_journal_id,
                                                                                        }])
                return



class PdcConfiguration(models.Model):
    _inherit = "pdc.configuration"


    @api.constrains('days')
    def constraint_days(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'pdc.configuration', 'search_read',
                                            [[['days', '=', self.days]]],
                                            {'fields': ['name', 'id']})

                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'pdc.configuration', 'create',
                                                  [{
                                                          'days':self.days,
                                                      }]
                                                  )
                return


class CreditLimitConfiguration(models.Model):
    _inherit = "credit.limit.configuration"


    @api.constrains('months','percentage','min_credit_amount')
    def constraint_days(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'credit.limit.configuration', 'search_read',
                                            [[['months', '=', self.months]]],
                                            {'fields': ['months', 'id']})

                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'credit.limit.configuration', 'create',
                                                  [{
                                                          'months':self.months,
                                                          'percentage':self.percentage,
                                                          'min_credit_amount':self.min_credit_amount,
                                                      }]
                                                  )
                return


class FreightDiscountConfig(models.Model):
    _inherit = 'freight.disc.config'


    @api.constrains('name')
    def constraint_days(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'freight.disc.config', 'search_read',
                                            [[['name', '=', self.name]]],
                                            {'fields': ['name', 'id']})

                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'freight.disc.config', 'create',
                                                  [{
                                                          'name':self.name,
                                                      }]
                                                  )
                return

class BounceCheques(models.Model):
    _inherit = "bounce.cheques"
    @api.constrains('payment_date','company_id','name','user_id','today_lines')
    def constraint_partner(self):
            import xmlrpc.client
            synch = self.env['synch.configuration'].search([('activate','=',True)])
            if synch:
                url = synch.server
                db = synch.db
                username = synch.username
                password = synch.password
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                uid = common.authenticate(db, username, password, {})
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                partner_passenger_id = models.execute_kw(db, uid, password, 'bounce.cheques', 'search_read',
                                            [[['basic_synch_bounce', '=', self.id]]],
                                            {'fields': ['name', 'id']})
                # partner_passenger_id = models.execute_kw(db, uid, password, 'bounce.cheques', 'search_read',
                #                             [[['name', '=', self.name]]],
                #                             {'fields': ['name', 'id']})

                estimate_ids = []
                user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                            [[['name', '=', self.user_id.name]]],
                                            {'fields': ['name', 'id']})

                if user_id:
                    user_id = user_id[0]['id']
                else:
                    user_id = False

                for line in self.today_lines:
                    partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                   [[['basic_synch_partner', '=', line.partner_id.id],
                                                     ]],
                                                   {'fields': ['name', 'id']})
                    if partner_id:
                        partner_id = partner_id[0]['id']
                    else:
                        partner_id = False
                    holder_name = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                    [[['basic_synch_partner', '=', line.holder_name.id],
                                                      ]],
                                                    {'fields': ['name', 'id', 'mobile']})
                    if holder_name:
                        holder_name = holder_name[0]['id']
                    else:
                        holder_name = False
                    debited_account = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                        [[['name', '=', line.debited_account.name],
                                                          ['company_id', '=', line.debited_account.company_id.id]
                                                          ]],
                                                        {'fields': ['name', 'id']})
                    if debited_account:
                        debited_account = debited_account[0]['id']
                    else:
                        debited_account = False

                    product_main = (0, 0, {
                            'partner_id': partner_id,
                            'date': line.date,
                            'check_no': line.check_no,
                            'check_type': line.check_type,
                            'bank_name': line.bank_name,
                            'holder_name': holder_name,
                            'debited_account': debited_account,
                            'amount_total': line.amount_total,
                            'status': line.status,
                            'reason': line.reason,
                            'bounce_date': line.bounce_date,
                            'new_date': line.new_date,
                        })
                    estimate_ids.append(product_main)
                # company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                #                                        [[['name', '=', self.company_id.name]]],
                #                                        {'fields': ['name', 'id']})
                # if company_id:
                #     company_id = company_id[0]['id']
                # else:
                #     company_id = 1



                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'bounce.cheques', 'create',
                                                  [{
                                                      'user_id': user_id,
                                                      'payment_date': self.payment_date,
                                                      'today_lines':estimate_ids,
                                                      'basic_synch_bounce':str(self.id)
                                                  }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'bounce.cheques', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'user_id': user_id,
                                                                                              'payment_date': self.payment_date,
                                                                                              'today_lines':estimate_ids,
                                                                                        }])
                return



class AreaOffers(models.Model):
    _inherit = "area.offers"

    @api.constrains('from_date', 'to_date','area','sales_person','product_id','discount','selling_price')
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

            partner_passenger_id = models.execute_kw(db, uid, password, 'area.offers', 'search_read',
                                        [[['basic_synch_offers', '=', self.id]]],
                                        {'fields': ['name', 'id', 'product_id']})

            area_id = models.execute_kw(db, uid, password, 'executive.area.wise', 'search_read',
                                        [[['basic_synch_area', '=', self.area.id]]],
                                        {'fields': ['name', 'id', 'pin_code']})
            sales_person = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                           [[['basic_synch_partner', '=', self.sales_person.id],
                                             ]],
                                           {'fields': ['name', 'id']})
            if sales_person:
                sales_person = sales_person[0]['id']
            else:
                sales_person = False
            if area_id:
                area_id = area_id[0]['id']
            else:
                area_id =False
            product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                               [[['name', '=', self.product_id.name]]],
                                               {'fields': ['name', 'id']})
            if product_server:
                product_server = product_server[0]['id']
            else:
                product_server = False

            if not partner_passenger_id:
                partner = models.execute_kw(db, uid, password, 'area.offers', 'create',
                                            [{
                                                'area': area_id,
                                                'from_date': self.from_date,
                                                'to_date': self.to_date,
                                                'sales_person':sales_person,
                                                'product_id':product_server,
                                                'discount':self.discount,
                                                'selling_price':self.selling_price,
                                                'basic_synch_offers':str(self.id)
                                                # 'basic_synch_area': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'area.offers', 'write', [[area_id[0]['id']],
                                                                                            {
                                                                                                'area': area_id,
                                                                                                'from_date': self.from_date,
                                                                                                'to_date': self.to_date,
                                                                                                'sales_person': sales_person,
                                                                                                'product_id': product_server,
                                                                                                'discount': self.discount,
                                                                                                'selling_price': self.selling_price
                                                                                            }])
            return


