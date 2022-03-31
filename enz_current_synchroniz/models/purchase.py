import requests

from odoo import http
from odoo.http import request
from datetime import datetime
from num2words import num2words
import urllib.parse as urlparse
from urllib.parse import parse_qs
from odoo import models,fields,api

#
#
# class VehicleRequest(models.Model):
#     _inherit = 'vehicle.request'




class PurchaseDippo(models.Model):
    _inherit = 'purchase.dippo'

    @api.constrains('name', 'amount', 'user_id', 'days', 'create_date')
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
            area_id = models.execute_kw(db, uid, password, 'purchase.dippo', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})
            user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                        [[['name', '=', self.user_id.name]]],
                                        {'fields': ['name', 'id']})

            if user_id:
                user_id = user_id[0]['id']
            else:
                user_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'purchase.dippo', 'create',
                                            [{
                                                'name': self.name,
                                                'amount': self.amount,
                                                'user_id': user_id,
                                                'create_date': self.create_date,
                                                # 'basic_synch_area': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'purchase.dippo', 'write', [[area_id[0]['id']],
                                                                                               {
                                                                                                   'name': self.name,
                                                                                                    'amount': self.amount,
                                                                                                    'user_id': user_id,
                                                                                                    'create_date': self.create_date,
                                                                                               }])
            return


class PurchasePaymentTerms(models.Model):
    _inherit = 'purchase.payment.terms'

    @api.constrains('name', 'value', 'percentage', 'days','reduced_amount')
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
            area_id = models.execute_kw(db, uid, password, 'purchase.payment.terms', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'purchase.payment.terms', 'create',
                                            [{
                                                'name': self.name,
                                                'days': self.days,
                                                'reduced_amount': self.reduced_amount,
                                                'value': self.value,
                                                'percentage': self.percentage,
                                                # 'basic_synch_area': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'purchase.payment.terms', 'write', [[area_id[0]['id']],
                                                                                                {
                                                                                                    'name': self.name,
                                                                                                    'days': self.days,
                                                                                                    'reduced_amount': self.reduced_amount,
                                                                                                    'value': self.value,
                                                                                                    'percentage': self.percentage,

                                                                                                }])
            return


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    @api.constrains('name', 'company_id','tax_ids','account_ids','auto_apply')
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
            area_id = models.execute_kw(db, uid, password, 'account.fiscal.position', 'search_read',
                                        [[['company_id', '=', self.company_id.id], ['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})

            lines = []
            for line in self.tax_ids:
                tax_src_id = models.execute_kw(db, uid, password, 'account.tax', 'search_read',
                                               [[['name', '=', line.tax_src_id.name],
                                                 ['company_id', '=', line.tax_src_id.company_id.id]]],
                                               {'fields': ['name', 'id']})

                if tax_src_id:
                    tax_src_id = tax_src_id[0]['id']
                else:
                    tax_src_id = False

                tax_dest_id = models.execute_kw(db, uid, password, 'account.tax', 'search_read',
                                               [[['name', '=', line.tax_dest_id.name],
                                                 ['company_id', '=', line.tax_dest_id.company_id.id]]],
                                               {'fields': ['name', 'id']})

                if tax_dest_id:
                    tax_dest_id = tax_dest_id[0]['id']
                else:
                    tax_dest_id = False


                sub_dict = (0, 0, {
                    'tax_src_id': tax_src_id,
                    'tax_dest_id': tax_dest_id,


                })
                lines.append(sub_dict)
            # user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
            #                             [[['name', '=', self.user_id.name]]],
            #                             {'fields': ['name', 'id']})
            #
            # if user_id:
            #     user_id = user_id[0]['id']
            # else:
            #     user_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'account.fiscal.position', 'create',
                                            [{
                                                'name': self.name,
                                                'company_id': self.company_id.id,
                                                'tax_ids':lines,
                                                'auto_apply':self.auto_apply,
                                                # 'basic_synch_area': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'account.fiscal.position', 'write', [[area_id[0]['id']],
                                                                                            {
                                                                                                'name': self.name,
                                                                                                'company_id': self.company_id.id,
                                                                                                'tax_ids':lines,
                                                                                                'auto_apply':self.auto_apply,

                                                                                            }])
            return


class PurchaseOrderCustom(models.Model):
    _inherit = 'purchase.order.custom'


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

                estimate = models.execute_kw(db, uid, password, 'purchase.order.custom', 'search_read',
                                             [[['basic_synch_purchase_req', '=', self.id]]])


                upd = models.execute_kw(db, uid, password, 'purchase.order.custom', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_purchase_req_button': True,
                                                                                             }])
            return super(PurchaseOrderCustom, self).action_oder_confirm()


    @api.constrains('name','partner_id','invoiced_number','invoiced_date','purchase_date','vehicle_no','fiscal_position_id','custom_lines')
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
            area_id = models.execute_kw(db, uid, password, 'purchase.order.custom', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})

            user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                        [[['name', '=', self.user_id.name]]],
                                        {'fields': ['name', 'id']})

            if user_id:
                user_id = user_id[0]['id']
            else:
                user_id = False

            partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                [[['basic_synch_partner', '=', self.partner_id.id]]],
                                                {'fields': ['name', 'id']})
            if partner_pass_id:
                partner_pass_id = partner_pass_id[0]['id']
            else:
                partner_pass_id = False

            lines = []
            estimate_ids = []
            company_ids = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                           [[['name', '=', self.company_id.name]]],
                                           {'fields': ['name', 'id']})
            if company_ids:
                company_ids = company_ids[0]['id']
            else:
                company_ids = 1

            for line in self.custom_lines:
                product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                   [[['name', '=', line.product_id.name]]],
                                                   {'fields': ['name', 'id']})
                if product_server:
                    product_server = product_server[0]['id']
                else:
                    product_server = False
                product_uom = models.execute_kw(db, uid, password, 'uom.uom', 'search_read',
                                                [[['name', '=', line.product_uom.name]]],
                                                {'fields': ['name', 'id']})
                if product_uom:
                    product_uom = product_uom[0]['id']
                else:
                    product_uom = False
                fiscal_position_id = models.execute_kw(db, uid, password, 'account.fiscal.position', 'search_read',
                                            [[['name', '=', self.fiscal_position_id.name]]],
                                            {'fields': ['name', 'id']})
                if fiscal_position_id:
                    fiscal_position_id = fiscal_position_id[0]['id']
                else:
                    fiscal_position_id = False


                purchase_payment_term = models.execute_kw(db, uid, password, 'purchase.payment.terms', 'search_read',
                                            [[['name', '=', self.purchase_payment_term.name]]],
                                            {'fields': ['name', 'id']})
                if purchase_payment_term:
                    purchase_payment_term = purchase_payment_term[0]['id']
                else:
                    purchase_payment_term = False




                if line.branch_id:

                    branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                                                         [[
                                                                           ['name', '=', line.branch_id.name]]],
                                                                         {'fields': ['name', 'id']})

                    if branch_id:
                       branch_id = branch_id[0]['id']
                    else:
                        branch_id = False
                else:
                    branch_id =False


                dippo = models.execute_kw(db, uid, password, 'purchase.dippo', 'search_read',
                                                                     [[
                                                                       ['name', '=', line.dippo.name]]],
                                                                     {'fields': ['name', 'id']})

                if dippo:
                   dippo = dippo[0]['id']
                else:
                    dippo = False
                company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                       [[['name', '=', line.company_id.name]]],
                                                       {'fields': ['name', 'id']})
                if company_id:
                    company_id = company_id[0]['id']
                else:
                    company_id = 1

                product_main = (0, 0, {
                    'product_id': product_server,
                    'product_uom': product_uom,
                    'company_id': company_id,
                    'branch_id': branch_id,
                    'dippo': dippo,
                    'freight_charge': line.freight_charge,
                    'product_qty': line.product_qty,
                    'including_price': line.including_price,
                })
                estimate_ids.append(product_main)
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'purchase.order.custom', 'create',
                                            [{
                                                'name': self.name,
                                                'company_id':company_ids,
                                                'partner_id':partner_pass_id,
                                                'user_id':user_id,
                                                'basic_synch_purchase_req':str(self.id),
                                                'custom_lines':estimate_ids,
                                                'invoiced_number':self.invoiced_number,
                                                'invoiced_date':self.invoiced_date,
                                                'purchase_date':self.purchase_date,
                                                'vehicle_no':self.vehicle_no,
                                                'fiscal_position_id':fiscal_position_id,
                                                'create_date':self.create_date,
                                                'reduced_amount':self.reduced_amount,
                                                'percentage':self.percentage,
                                                'purchase_payment_term':purchase_payment_term,

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'purchase.order.custom', 'write', [[area_id[0]['id']],
                                                                                            {
                                                                                                'name': self.name,
                                                'partner_id':partner_pass_id,
                                                'user_id':user_id,
                                                 'company_id': company_ids,
                                                'custom_lines':estimate_ids,
                                                'invoiced_number':self.invoiced_number,
                                                'invoiced_date':self.invoiced_date,
                                                'purchase_date':self.purchase_date,
                                                'vehicle_no':self.vehicle_no,
                                                'fiscal_position_id':fiscal_position_id,
                                                'create_date':self.create_date,
                                                'reduced_amount':self.reduced_amount,
                                                'percentage':self.percentage,
                                                'purchase_payment_term':purchase_payment_term,

                                                                                            }])
            return



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # @api.constrains('name', 'partner_id', 'invoiced_number', 'invoiced_date', 'purchase_date', 'vehicle_no',
    #                 'fiscal_position_id', 'order_line','month','l10n_in_gst_treatment','date_approve')
    # def constraint_pin_code(self):
    #     import xmlrpc.client
    #     synch = self.env['synch.configuration'].search([('activate', '=', True)])
    #     if synch:
    #         url = synch.server
    #         db = synch.db
    #         username = synch.username
    #         password = synch.password
    #         # password = "YEZPR#ADM@786"
    #         common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    #         uid = common.authenticate(db, username, password, {})
    #         models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    #         area_id = models.execute_kw(db, uid, password, 'purchase.order', 'search_read',
    #                                     [[['basic_synch_purchase_order', '=', self.id]]],
    #                                     {'fields': ['name', 'id']})
    #
    #         user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
    #                                     [[['name', '=', self.user_id.name]]],
    #                                     {'fields': ['name', 'id']})
    #
    #         if user_id:
    #             user_id = user_id[0]['id']
    #         else:
    #             user_id = False
    #
    #         partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
    #                                             [[['basic_synch_partner', '=', self.partner_id.id]]],
    #                                             {'fields': ['name', 'id']})
    #         if partner_pass_id:
    #             partner_pass_id = partner_pass_id[0]['id']
    #         else:
    #             partner_pass_id = False
    #
    #         lines = []
    #         estimate_ids = []
    #         company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
    #                                        [[['name', '=', self.company_id.name]]],
    #                                        {'fields': ['name', 'id']})
    #         if company_id:
    #             company_id = company_id[0]['id']
    #         else:
    #             company_id = 1
    #         fiscal_position_id = models.execute_kw(db, uid, password, 'account.fiscal.position', 'search_read',
    #                                                [[['name', '=', self.fiscal_position_id.name]]],
    #                                                {'fields': ['name', 'id']})
    #         if fiscal_position_id:
    #             fiscal_position_id = fiscal_position_id[0]['id']
    #         else:
    #             fiscal_position_id = False
    #         purchase_payment_term = models.execute_kw(db, uid, password, 'purchase.payment.terms', 'search_read',
    #                                                   [[['name', '=', self.purchase_payment_term.name]]],
    #                                                   {'fields': ['name', 'id']})
    #         if purchase_payment_term:
    #             purchase_payment_term = purchase_payment_term[0]['id']
    #         else:
    #             purchase_payment_term = False
    #         company_ids = models.execute_kw(db, uid, password, 'res.company', 'search_read',
    #                                        [[['name', '=', self.company_id.name]]],
    #                                        {'fields': ['name', 'id']})
    #         if company_ids:
    #             company_ids = company_ids[0]['id']
    #         else:
    #             company_ids = 1
    #
    #         for line in self.order_line:
    #             product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
    #                                                [[['name', '=', line.product_id.name]]],
    #                                                {'fields': ['name', 'id']})
    #             if product_server:
    #                 product_server = product_server[0]['id']
    #             else:
    #                 product_server = False
    #             product_uom = models.execute_kw(db, uid, password, 'uom.uom', 'search_read',
    #                                             [[['name', '=', line.product_uom.name]]],
    #                                             {'fields': ['name', 'id']})
    #             if product_uom:
    #                 product_uom = product_uom[0]['id']
    #             else:
    #                 product_uom = False
    #
    #
    #             # if line.branch_id:
    #             #
    #             #     branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
    #             #                                   [[
    #             #                                       ['name', '=', line.branch_id.name]]],
    #             #                                   {'fields': ['name', 'id']})
    #             #
    #             #     if branch_id:
    #             #         branch_id = branch_id[0]['id']
    #             #     else:
    #             #         branch_id = False
    #             # else:
    #             #     branch_id = False
    #
    #             dippo = models.execute_kw(db, uid, password, 'purchase.dippo', 'search_read',
    #                                       [[
    #                                           ['name', '=', line.dippo.name]]],
    #                                       {'fields': ['name', 'id']})
    #
    #             if dippo:
    #                 dippo = dippo[0]['id']
    #             else:
    #                 dippo = False
    #             company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
    #                                            [[['name', '=', line.company_id.name]]],
    #                                            {'fields': ['name', 'id']})
    #             if company_id:
    #                 company_id = company_id[0]['id']
    #             else:
    #                 company_id = 1
    #             to_company = models.execute_kw(db, uid, password, 'res.company', 'search_read',
    #                                            [[['name', '=', line.to_company.name]]],
    #                                            {'fields': ['name', 'id']})
    #             if to_company:
    #                 to_company = to_company[0]['id']
    #             else:
    #                 to_company = 1
    #
    #             product_main = (0, 0, {
    #                 'product_id': product_server,
    #                 'name': line.name,
    #                 'product_hsn_code': line.name,
    #                 'product_uom': product_uom,
    #                 'to_company': to_company,
    #                 'company_id': company_id,
    #                 # 'branch_id': branch_id,
    #                 'dippo': dippo,
    #                 'freight_charge': line.freight_charge,
    #                 'product_qty': line.product_qty,
    #                 'including_price': line.including_price,
    #                 'price_unit': line.price_unit,
    #                 # 'taxes_ids': line.taxes_ids.ids,
    #                 'price_subtotal': line.price_subtotal,
    #             })
    #             estimate_ids.append(product_main)
    #         if not area_id:
    #             partner = models.execute_kw(db, uid, password, 'purchase.order', 'create',
    #                                         [{
    #                                             'company_id': company_ids,
    #                                             'partner_id': partner_pass_id,
    #                                             'user_id': user_id,
    #                                             # 'company_id':company_id,
    #                                             'partner_ref': self.partner_ref,
    #                                             'month': self.month,
    #                                             'basic_synch_purchase_order': str(self.id),
    #                                             'order_line': estimate_ids,
    #                                             'invoiced_number': self.invoiced_number,
    #                                             'invoiced_date': self.invoiced_date,
    #                                             'purchase_date': self.purchase_date,
    #                                             'vehicle_no': self.vehicle_no,
    #                                             'fiscal_position_id': fiscal_position_id,
    #                                             'create_date': self.create_date,
    #                                             'reduced_amount': self.reduced_amount,
    #                                             'percentage': self.percentage,
    #                                             'purchase_payment_term': purchase_payment_term,
    #
    #                                         }]
    #                                         )
    #         else:
    #             upd = models.execute_kw(db, uid, password, 'purchase.order', 'write', [[area_id[0]['id']],
    #                                                                                           {
    #                                                                                               'name': self.name,
    #                                                                                               'company_id': company_ids,
    #                                                                                               'partner_id': partner_pass_id,
    #                                                                                               'user_id': user_id,
    #                                                                                               'order_line': estimate_ids,
    #                                                                                               # 'basic_synch_purchase_order': str(
    #                                                                                               #     self.id),
    #                                                                                               'invoiced_number': self.invoiced_number,
    #                                                                                               'invoiced_date': self.invoiced_date,
    #                                                                                               'purchase_date': self.purchase_date,
    #                                                                                               'vehicle_no': self.vehicle_no,
    #                                                                                               'fiscal_position_id': fiscal_position_id,
    #                                                                                               'create_date': self.create_date,
    #                                                                                               'reduced_amount': self.reduced_amount,
    #                                                                                               'percentage': self.percentage,
    #                                                                                               'purchase_payment_term': purchase_payment_term,
    #
    #                                                                                           }])
    #         return
    #


    # def action_create_invoice(self):
    #         # rec = super(SaleEstimate, self).action_approve()
    #         import xmlrpc.client
    #         synch = self.env['synch.configuration'].search([('activate', '=', True)])
    #         if synch:
    #             url = synch.server
    #             db = synch.db
    #             username = synch.username
    #             password = synch.password
    #             common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    #             uid = common.authenticate(db, username, password, {})
    #             models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    #
    #             estimate = models.execute_kw(db, uid, password, 'purchase.order', 'search_read',
    #                                          [[['basic_synch_purchase_order', '=', self.id]]])
    #
    #
    #             upd = models.execute_kw(db, uid, password, 'purchase.order', 'write', [[estimate[0]['id']],
    #                                                                                          {
    #                                                                                              'basic_synch_po_invoice_button': True,
    #                                                                                          }])
    #         return super(PurchaseOrder, self).action_create_invoice()



class PurchaseDiscounts(models.Model):
    _inherit = "purchase.discounts"



    def action_approve(self):
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

                estimate = models.execute_kw(db, uid, password, 'purchase.discounts', 'search_read',
                                             [[['basic_synch_po_discount', '=', self.id]]])


                upd = models.execute_kw(db, uid, password, 'purchase.discounts', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_po_discount_buttons': True,
                                                                                             }])
            return super(PurchaseDiscounts, self).action_approve()


    @api.constrains('month', 'partner_id', 'ref_no', 'lumpsum_disc', 'date', 'user_id',
                    'discount_type','purchased_lines')
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
            area_id = models.execute_kw(db, uid, password, 'purchase.discounts', 'search_read',
                                        [[['name', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                [[['basic_synch_partner', '=', self.partner_id.id]]],
                                                {'fields': ['name', 'id']})

            user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                        [[['name', '=', self.user_id.name]]],
                                        {'fields': ['name', 'id']})

            if user_id:
                user_id = user_id[0]['id']
            else:
                user_id = False

            if partner_pass_id:
                partner_pass_id = partner_pass_id[0]['id']
            else:
                partner_pass_id = False
            estimate_ids =[]
            for line in self.purchased_lines:
                product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                   [[['name', '=', line.product_id.name]]],
                                                   {'fields': ['name', 'id']})
                if product_server:
                    product_server = product_server[0]['id']
                else:
                    product_server = False


                partner_line_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                    [[['basic_synch_partner', '=', line.partner_id.id]]],
                                                    {'fields': ['name', 'id']})
                if partner_line_id:
                    partner_line_id = partner_line_id[0]['id']
                else:
                    partner_line_id = False
                invoice_id  = models.execute_kw(db, uid, password, 'account.move', 'search_read',
                                                    [[['basic_synch_account_move', '=', line.invoice_id.id]]],
                                                    {'fields': ['name', 'id']})
                if invoice_id:
                    invoice_id = invoice_id[0]['id']
                else:
                    invoice_id = False

                product_main = (0, 0, {
                    'month': line.month,
                    'date': line.date,
                    'partner_id': partner_line_id,
                    'invoice_id': invoice_id,
                    'product_id': product_server,
                    'no_of_bags': line.no_of_bags,
                    'qty': line.qty,
                    'price': line.price,
                    'total_amount': line.total_amount,
                    # 'branch_id': branch_id,

                })
                estimate_ids.append(product_main)
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'purchase.discounts', 'create',
                                            [{
                                                'partner_id': partner_pass_id,
                                                'ref_no': self.ref_no,
                                                'month': self.month,
                                                'lumpsum_disc': self.lumpsum_disc,
                                                'date': self.date,
                                                'user_id':user_id,
                                                'basic_synch_po_discount': str(self.id),
                                                'purchased_lines': estimate_ids,
                                                'avarage_cost': self.avarage_cost,
                                                'lumpsum_cost': self.lumpsum_cost,
                                                'discount_type': self.discount_type,
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'purchase.discounts', 'write', [[area_id[0]['id']],
                                                                                       {
                                                                                            'partner_id': partner_pass_id,
                                                                                            'ref_no': self.ref_no,
                                                                                            'month': self.month,
                                                                                            'lumpsum_disc': self.lumpsum_disc,
                                                                                            'date': self.date,
                                                                                            'user_id':user_id,
                                                                                            # 'basic_synch_purchase_order': str(self.id),
                                                                                            'purchased_lines': estimate_ids,
                                                                                            'avarage_cost': self.avarage_cost,
                                                                                            'lumpsum_cost': self.lumpsum_cost,
                                                                                            'discount_type': self.discount_type,

                                                                                       }])
            return



class BudgetReportFirst(models.Model):
    _inherit = "budget.report.first"


    # @api.constrains('date', 'product_id', 'vendor_id', 'avg_purchase_price',
    #                 'po_offer','set_selling_price','get_amount')
    # def constraint_pin_code(self):
    #     import xmlrpc.client
    #     synch = self.env['synch.configuration'].search([('activate', '=', True)])
    #     if synch:
    #         url = synch.server
    #         db = synch.db
    #         username = synch.username
    #         password = synch.password
    #         # password = "YEZPR#ADM@786"
    #         common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    #         uid = common.authenticate(db, username, password, {})
    #         models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    #         area_id = models.execute_kw(db, uid, password, 'budget.report.first', 'search_read',
    #                                     [[['basic_synch_bud_repo_first', '=', self.id]]],
    #                                     {'fields': [ 'id']})
    #
    #         partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
    #                                             [[['basic_synch_partner', '=', self.vendor_id.id]]],
    #                                             {'fields': ['name', 'id']})
    #
    #         if partner_pass_id:
    #             partner_pass_id = partner_pass_id[0]['id']
    #         else:
    #             partner_pass_id = False
    #
    #         if not area_id:
    #             product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
    #                                                [[['name', '=', self.id]]],
    #                                                {'fields': ['name', 'id']})
    #             if product_server:
    #                 product_server = product_server[0]['id']
    #             else:
    #                 product_server = False
    #             partner = models.execute_kw(db, uid, password, 'budget.report.first', 'create',
    #                                         [{
    #                                             'vendor_id': partner_pass_id,
    #                                             'product_id': product_server,
    #                                             'avg_purchase_price': self.avg_purchase_price,
    #                                             'po_offer': self.po_offer,
    #                                             'set_selling_price': self.set_selling_price,
    #                                             'get_amount': self.get_amount,
    #                                             'date': self.date,
    #                                             'basic_synch_bud_repo_first':str(self.id)
    #                                         }]
    #                                         )
    #         else:
    #             upd = models.execute_kw(db, uid, password, 'budget.report.first', 'write', [[area_id[0]['id']],
    #                                                                                    {
    #                                                                                         'avg_purchase_price': self.avg_purchase_price,
    #                                                                                         'po_offer': self.po_offer,
    #                                                                                         'set_selling_price': self.set_selling_price,
    #                                                                                         'get_amount': self.get_amount,
    #
    #                                                                                    }])
    #         return



class BudgetReport(models.Model):
    _inherit = "budget.report"


    @api.constrains('product_so_qty', 'avg_purchase_price', 'discount', 'po_offer',
                    'freight','set_selling_price','avg_sold_price')
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
            area_id = models.execute_kw(db, uid, password, 'budget.report', 'search_read',
                                        [[['basic_synch_bud_repo', '=', self.id]]],
                                        {'fields': ['id']})

            partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                [[['basic_synch_partner', '=', self.vendor_id.id]]],
                                                {'fields': ['name', 'id']})

            if partner_pass_id:
                partner_pass_id = partner_pass_id[0]['id']
            else:
                partner_pass_id = False
            product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                               [[['name', '=', self.product_id.name]]],
                                               {'fields': ['name', 'id']})
            if product_server:
                product_server = product_server[0]['id']
            else:
                product_server = False
            if not area_id:

                partner = models.execute_kw(db, uid, password, 'budget.report', 'create',
                                            [{
                                                'date': self.date,
                                                'vendor_id': partner_pass_id,
                                                'product_id': product_server,
                                                'product_so_qty': self.product_so_qty,
                                                'avg_purchase_price': self.avg_purchase_price,
                                                'discount': self.discount,
                                                'po_offer': self.po_offer,
                                                'freight': self.freight,
                                                'set_selling_price': self.set_selling_price,
                                                'avg_sold_price': self.avg_sold_price,
                                                'old_get_amount': self.old_get_amount,
                                                'get_amount': self.get_amount,
                                                'total': self.total,
                                                'paid_amount': self.paid_amount,
                                                'sale_get_pd': self.paid_amount,
                                                'balance': self.balance,
                                                'remaining_balance': self.remaining_balance,
                                                'state': self.state,
                                                'basic_synch_bud_repo':str(self.id)
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'budget.report', 'write', [[area_id[0]['id']],
                                                                                       {
                                                                                             'date': self.date,
                                                'vendor_id': partner_pass_id,
                                                'product_id': product_server,
                                                'product_so_qty': self.product_so_qty,
                                                'avg_purchase_price': self.avg_purchase_price,
                                                'discount': self.discount,
                                                'po_offer': self.po_offer,
                                                'freight': self.freight,
                                                'set_selling_price': self.set_selling_price,
                                                'avg_sold_price': self.avg_sold_price,
                                                'old_get_amount': self.old_get_amount,
                                                'get_amount': self.get_amount,
                                                'total': self.total,
                                                'paid_amount': self.paid_amount,
                                                'sale_get_pd': self.paid_amount,
                                                'balance': self.balance,
                                                'remaining_balance': self.remaining_balance,
                                                'state': self.state,
                                                'basic_synch_bud_repo':str(self.id)
                                                                                       }])
            return




class BudgetReportFilter(models.Model):
    _inherit = "budget.report.filter"


    def action_credit_note(self):
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

            estimate = models.execute_kw(db, uid, password, 'budget.report.filter', 'search_read',
                                         [[['basic_synch_bud_repo_filt', '=', self.id]]])


            upd = models.execute_kw(db, uid, password, 'budget.report.filter', 'write', [[estimate[0]['id']],
                                                                                          {
                                                                                              'basic_synch_bud_repo_filt_button': True,
                                                                                          }])
        return super(BudgetReportFilter, self).action_credit_note()

    @api.constrains('to_date','from_date','partner_id','area_lines','paid_amount')
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
                partner_passenger_id = models.execute_kw(db, uid, password, 'budget.report.filter', 'search_read',
                                                     [[['id', '=', self.id]]],
                                                     {'fields': ['name', 'id']})



                estimate_ids = []
                partner_pass_ids = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                    [[['basic_synch_partner', '=', self.partner_id.id]]],
                                                    {'fields': ['name', 'id']})
                if partner_pass_ids:
                    partner_pass_ids = partner_pass_ids[0]['id']
                else:
                    partner_pass_ids = False

                for line in self.area_lines:
                    product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                       [[['name', '=', line.product_id.name]]],
                                                       {'fields': ['name', 'id']})
                    if product_server:
                        product_server = product_server[0]['id']
                    else:
                        product_server =False

                    partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                        [[['basic_synch_partner', '=', line.partner_id.id]]],
                                                        {'fields': ['name', 'id']})
                    if partner_pass_id:
                        partner_pass_id = partner_pass_id[0]['id']
                    else:
                        partner_pass_id = False

                    product_main = (0, 0, {
                        'product_id': product_server,
                        'partner_id': partner_pass_id,
                        'amount': line.amount,
                        'p_amount': line.p_amount,
                    })
                    estimate_ids.append(product_main)

                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'budget.report.filter', 'create',
                                                  [{
                                                          'to_date':self.to_date,
                                                          'from_date':self.from_date,
                                                          'partner_id':partner_pass_ids,
                                                          'paid_amount':self.paid_amount,
                                                          'area_lines':estimate_ids,
                                                      'basic_synch_bud_repo_filt':str(self.id)
                                                  }]

                                                  )
                else:
                    upd = models.execute_kw(db, uid, password, 'budget.report.filter', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'to_date': self.to_date,
                                                                                            'from_date': self.from_date,
                                                                                            'partner_id': partner_pass_ids,
                                                                                            'paid_amount': self.paid_amount,
                                                                                            'area_lines': estimate_ids,
                                                }])
                return

class PurchaseDateDiscounts(models.Model):
    _inherit = "purchase.date.discounts"

    def action_approve(self):
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

                estimate = models.execute_kw(db, uid, password, 'purchase.date.discounts', 'search_read',
                                             [[['basic_synch_po_date_discount', '=', self.id]]])


                upd = models.execute_kw(db, uid, password, 'purchase.date.discounts', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_po_date_discount_button': True,
                                                                                             }])
            return super(PurchaseDateDiscounts, self).action_approve()

    @api.constrains('month', 'partner_id', 'ref_no', 'lumpsum_disc', 'date', 'user_id',
                    'discount_type','purchased_lines','discount','start_date','end_date')
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
            area_id = models.execute_kw(db, uid, password, 'purchase.date.discounts', 'search_read',
                                        [[['basic_synch_po_date_discount', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                [[['basic_synch_partner', '=', self.partner_id.id]]],
                                                {'fields': ['name', 'id']})

            user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                        [[['name', '=', self.user_id.name]]],
                                        {'fields': ['name', 'id']})

            if user_id:
                user_id = user_id[0]['id']
            else:
                user_id = False

            if partner_pass_id:
                partner_pass_id = partner_pass_id[0]['id']
            else:
                partner_pass_id = False
            estimate_ids =[]
            for line in self.purchased_date_lines:
                product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                   [[['name', '=', line.product_id.name]]],
                                                   {'fields': ['name', 'id']})
                if product_server:
                    product_server = product_server[0]['id']
                else:
                    product_server = False


                partner_line_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                    [[['basic_synch_partner', '=', line.partner_id.id]]],
                                                    {'fields': ['name', 'id']})
                if partner_line_id:
                    partner_line_id = partner_line_id[0]['id']
                else:
                    partner_line_id = False
                invoice_id  = models.execute_kw(db, uid, password, 'account.move', 'search_read',
                                                    [[['basic_synch_account_move', '=', line.invoice_id.id]]],
                                                    {'fields': ['name', 'id']})
                if invoice_id:
                    invoice_id = invoice_id[0]['id']
                else:
                    invoice_id = False

                product_main = (0, 0, {
                    'month': line.month,
                    'date': line.date,
                    'partner_id': partner_line_id,
                    'invoice_id': invoice_id,
                    'product_id': product_server,
                    'no_of_bags': line.no_of_bags,
                    'qty': line.qty,
                    'price': line.price,
                    'total_amount': line.total_amount,

                })
                estimate_ids.append(product_main)
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'purchase.date.discounts', 'create',
                                            [{
                                                'partner_id': partner_pass_id,
                                                'ref_no': self.ref_no,
                                                # 'month': self.month,
                                                'lumpsum_disc': self.lumpsum_disc,
                                                # 'date': self.date,
                                                'start_date': self.start_date,
                                                'end_date': self.end_date,
                                                'user_id':user_id,
                                                'basic_synch_po_date_discount': str(self.id),
                                                'purchased_date_lines': estimate_ids,
                                                'avarage_cost': self.avarage_cost,
                                                'lumpsum_cost': self.lumpsum_cost,
                                                'discount_type': self.discount_type,
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'purchase.date.discounts', 'write', [[area_id[0]['id']],
                                                                                       {
                                                                                           'partner_id': partner_pass_id,
                                                                                           'ref_no': self.ref_no,
                                                                                           # 'month': self.month,
                                                                                           'lumpsum_disc': self.lumpsum_disc,
                                                                                           # 'date': self.date,
                                                                                           'start_date': self.start_date,
                                                                                           'end_date': self.end_date,
                                                                                           'user_id': user_id,
                                                                                           'purchased_date_lines': estimate_ids,
                                                                                           'avarage_cost': self.avarage_cost,
                                                                                           'lumpsum_cost': self.lumpsum_cost,
                                                                                           'discount_type': self.discount_type,
                                                                                       }])
            return



class BillDiscounts(models.Model):
    _inherit = "bill.discounts"


    def action_approve(self):
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

                estimate = models.execute_kw(db, uid, password, 'bill.discounts', 'search_read',
                                             [[['basic_synch_bill_date_discount', '=', str(self.id)]]])


                upd = models.execute_kw(db, uid, password, 'bill.discounts', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_bill_date_discount_button': True,
                                                                                             }])
            return super(BillDiscounts, self).action_approve()

    @api.constrains('month', 'partner_id', 'ref_no', 'lumpsum_disc', 'date', 'user_id',
                    'discount_type','bill_lines','discount','start_date','end_date')
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
            area_id = models.execute_kw(db, uid, password, 'bill.discounts', 'search_read',
                                        [[['basic_synch_bill_date_discount', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                [[['basic_synch_partner', '=', self.partner_id.id]]],
                                                {'fields': ['name', 'id']})

            user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                        [[['name', '=', self.user_id.name]]],
                                        {'fields': ['name', 'id']})

            if user_id:
                user_id = user_id[0]['id']
            else:
                user_id = False

            if partner_pass_id:
                partner_pass_id = partner_pass_id[0]['id']
            else:
                partner_pass_id = False
            estimate_ids =[]
            for line in self.bill_lines:
                product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                   [[['name', '=', line.product_id.name]]],
                                                   {'fields': ['name', 'id']})
                if product_server:
                    product_server = product_server[0]['id']
                else:
                    product_server = False


                partner_line_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                    [[['basic_synch_partner', '=', line.partner_id.id]]],
                                                    {'fields': ['name', 'id']})
                if partner_line_id:
                    partner_line_id = partner_line_id[0]['id']
                else:
                    partner_line_id = False
                invoice_id  = models.execute_kw(db, uid, password, 'account.move', 'search_read',
                                                    [[['basic_synch_account_move', '=', line.invoice_id.id]]],
                                                    {'fields': ['name', 'id']})
                if invoice_id:
                    invoice_id = invoice_id[0]['id']
                else:
                    invoice_id = False

                product_main = (0, 0, {
                    'date': line.date,
                    'partner_id': partner_line_id,
                    'invoice_id': invoice_id,
                    'product_id': product_server,
                    'qty': line.qty,
                    'price': line.price,
                    'total_amount': line.total_amount,

                })
                estimate_ids.append(product_main)
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'bill.discounts', 'create',
                                            [{
                                                'partner_id': partner_pass_id,
                                                'ref_no': self.ref_no,
                                                # 'month': self.month,
                                                'lumpsum_disc': self.lumpsum_disc,
                                                # 'date': self.date,
                                                'start_date': self.start_date,
                                                'end_date': self.end_date,
                                                'user_id':user_id,
                                                'basic_synch_bill_date_discount': str(self.id),
                                                'bill_lines': estimate_ids,
                                                'avarage_cost': self.avarage_cost,
                                                'lumpsum_cost': self.lumpsum_cost,
                                                'discount_type': self.discount_type,
                                            }]
                                            )

            return



class SpecialDiscounts(models.Model):
    _inherit = "special.discounts"

    def action_confirm(self):
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

                estimate = models.execute_kw(db, uid, password, 'special.discounts', 'search_read',
                                             [[['basic_synch_special_discount', '=', self.id]]])


                upd = models.execute_kw(db, uid, password, 'special.discounts', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_special_discount_button': True,
                                                                                             }])
            return super(SpecialDiscounts, self).action_confirm()





    @api.constrains('start_date','partner_id','special_lines','user_id')
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
                partner_passenger_id = models.execute_kw(db, uid, password, 'special.discounts', 'search_read',
                                                     [[['id', '=', self.id]]],
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


                estimate_ids = []
                for line in self.special_lines:
                    product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                       [[['name', '=', line.product_id.name]]],
                                                       {'fields': ['name', 'id']})
                    if product_server:
                        product_server = product_server[0]['id']
                    else:
                        product_server =False

                    partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                        [[['basic_synch_partner', '=', self.partner_id.id]]],
                                                        {'fields': ['name', 'id']})
                    if partner_pass_id:
                        partner_pass_id = partner_pass_id[0]['id']
                    else:
                        partner_pass_id = False


                    product_main = (0, 0, {
                        'product_id': product_server,
                        'partner_id':partner_pass_id,
                        'avarage_cost': line.avarage_cost,
                        'sell_price': line.sell_price,
                        'special_cost': line.special_cost,
                    })
                    estimate_ids.append(product_main)

                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'special.discounts', 'create',
                                                  [{
                                                         # 'basic_synch_order':str(self.id),
                                                          'start_date':self.start_date,
                                                          'user_id':user_id,
                                                          'partner_id':partner_pass_id,
                                                          'special_lines':estimate_ids,
                                                      'basic_synch_special_discount_button':str(self.id)
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'special.discounts', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'start_date': self.start_date,
                                                                                            'user_id': user_id,
                                                                                            'partner_id': partner_pass_id,
                                                                                            'special_lines': estimate_ids,
                                                }])
                return

class BankFeesStatement(models.Model):
    _inherit = "bank.fee.statement"


    def action_credit_statement(self):
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

                estimate = models.execute_kw(db, uid, password, 'bank.fee.statement', 'search_read',
                                             [[['basic_synch_bank_fee', '=', self.id]]])

                upd = models.execute_kw(db, uid, password, 'bank.fee.statement', 'write', [[estimate[0]['id']],
                                                                                          {
                                                                                              'basic_synch_bank_fee_button': True,
                                                                                          }])
            return super(BankFeesStatement, self).action_credit_statement()

    @api.constrains('create_date','user_id','partner_id','journal_id','fee_amount','company_id','note')
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
                partner_passenger_id = models.execute_kw(db, uid, password, 'bank.fee.statement', 'search_read',
                                                     [[['id', '=', self.id]]],
                                                     {'fields': ['name', 'id']})

                user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                            [[['name', '=', self.user_id.name]]],
                                            {'fields': ['name', 'id']})

                if user_id:
                    user_id = user_id[0]['id']
                else:
                    user_id = False
                journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                               [[['name', '=', self.journal_id.name],
                                                 ['company_id', '=', self.journal_id.company_id.id]]],
                                               {'fields': ['name', 'id']})

                if journal_id:
                    journal_id = journal_id[0]['id']
                else:
                    journal_id = False
                company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                       [[['name', '=', self.company_id.name]]],
                                                       {'fields': ['name', 'id']})
                if company_id:
                    company_id = company_id[0]['id']
                else:
                    company_id = 1




                if not partner_passenger_id:

                    partner = models.execute_kw(db, uid, password, 'bank.fee.statement', 'create',
                                                  [{
                                                         # 'basic_synch_order':str(self.id),
                                                          'create_date':self.create_date,
                                                          'user_id':user_id,
                                                          # 'partner_id':partner_pass_id,
                                                          'journal_id':journal_id,
                                                          'company_id':company_id,
                                                          # 'special_lines':estimate_ids,
                                                      'basic_synch_bank_fee':str(self.id)
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'bank.fee.statement', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                             'create_date':self.create_date,
                                                                                              'user_id':user_id,
                                                                                              'partner_id':partner_pass_id,
                                                                                              'journal_id':journal_id,
                                                                                              'company_id':company_id,
                                                                                        }])
                return

