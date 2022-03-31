import requests

from odoo import http
from odoo.http import request
from datetime import datetime
from num2words import num2words
import urllib.parse as urlparse
from urllib.parse import parse_qs
from odoo import models,fields,api


class SalesExecutiveCollections(models.Model):
    _inherit = "executive.collection"


    @api.constrains('name','cashier_id','user_id','another_area','partner_invoices')
    def constraint_cashier_id_name(self):
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
            area_id = models.execute_kw(db, uid, password, 'executive.collection', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})
            cashier_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                        [[['name', '=', self.cashier_id.name]]],
                                        {'fields': ['name', 'id']})
            if cashier_id:
                cashier_id = cashier_id[0]['id']
            else:
                cashier_id = False
            user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                           [[['name', '=', self.user_id.name]]],
                                           {'fields': ['name', 'id']})

            if user_id:
                user_id = user_id[0]['id']
            else:
                user_id = False
            journal = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                        [[['name', '=', 'Cash'],['company_id','=',1]
                                          ]],
                                        {'fields': ['name', 'id']})
            collection_lines = []
            for line in self.partner_invoices:
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', line.partner_id.id],
                                                 ]],
                                               {'fields': ['name', 'id', 'mobile']})
                if partner_id:
                    partner_id = partner_id[0]['id']
                else:
                    partner_id = False
                sub_dict = (0, 0, {
                    'partner_id': partner_id,
                    'amount_total': line.amount_total,
                    'journal_id':journal[0]['id']
                })
                collection_lines.append(sub_dict)

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'executive.collection', 'create',
                                            [{
                                                'name': self.name,
                                                'cashier_id': cashier_id,
                                                'user_id': user_id,
                                                'basic_synch_collection':str(self.id),
                                                # 'company_id': self.company_id.id,
                                                'another_area': self.another_area or False,
                                                'partner_invoices':collection_lines
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'executive.collection', 'write', [[area_id[0]['id']],
                                                                                                  {
                                                                                                    'name': self.name,
                                                                                                    'cashier_id': cashier_id,
                                                                                                    'user_id': user_id,
                                                                                                    'company_id': self.company_id.id,
                                                                                                    'another_area': self.another_area or False,
                                                                                                    'partner_invoices':collection_lines
                                                                                                  }])
            return


    def action_exe_confirm(self):
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

            estimate = models.execute_kw(db, uid, password, 'executive.collection', 'search_read',
                                         [[['basic_synch_collection', '=', self.id]]])

            # xmlrpc.execute_kw(db, uid, password, 'sale.estimate', 'action_approve', [56])
            upd = models.execute_kw(db, uid, password, 'executive.collection', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_cash_colled': True,
                                                                                  }])
        return super(SalesExecutiveCollections, self).action_exe_confirm()
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
            estimate = models.execute_kw(db, uid, password, 'executive.collection', 'search_read',
                                         [[['basic_synch_collection', '=', self.id]]])
            journal = self.env['account.journal'].search([('name','=','Cash'),('company_id','=',1)])

            upd = models.execute_kw(db, uid, password, 'executive.collection', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_cash_confirm': True,
                                                                                  }])
        return super(SalesExecutiveCollections, self).action_confirm()
    def action_reverse(self):
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
            estimate = models.execute_kw(db, uid, password, 'executive.collection', 'search_read',
                                         [[['basic_synch_collection', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'executive.collection', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_cash_reversed': True,
                                                                                  }])
        return super(SalesExecutiveCollections, self).action_reverse()

class SalesExecutiveCheque(models.Model):
    _inherit = "executive.cheque.collection"



    def action_deposit(self):
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
            estimate = models.execute_kw(db, uid, password, 'executive.cheque.collection', 'search_read',
                                         [[['basic_synch_check_collection', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'executive.cheque.collection', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_check_colled': True,
                                                                                  }])
        return super(SalesExecutiveCheque, self).action_deposit()


    @api.constrains('name', 'cashier_id', 'user_id', 'another_area', 'partner_invoices','sub_partner_invoices','a_partner_invoices')
    def constraint_cashier_id_name(self):
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
            area_id = models.execute_kw(db, uid, password, 'executive.collection', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})
            cashier_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                           [[['name', '=', self.cashier_id.name]]],
                                           {'fields': ['name', 'id']})
            if cashier_id:
                cashier_id = cashier_id[0]['id']
            else:
                cashier_id = False
            user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                        [[['name', '=', self.user_id.name]]],
                                        {'fields': ['name', 'id']})

            if user_id:
                user_id = user_id[0]['id']
            else:
                user_id = False
            collection_lines = []
            sub_collection_lines = []
            ad_collection_lines = []
            for line in self.partner_invoices:
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', line.partner_id.id],
                                                 ]],
                                               {'fields': ['name', 'id', 'mobile']})
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
                    holder_name =False
                # journal = self.env['account.journal'].search([('name', '=', 'Cash'), ('company_id', '=', 1)])

                sub_dict = (0, 0, {
                    'partner_id': partner_id,
                    'check_no': line.check_no,
                    'check_type': line.check_type,
                    'check_manual_date': line.check_manual_date,
                    'check_date': line.check_date,
                    'bank_name': line.bank_name,
                    # 'holder_name': line.holder_name,
                    'holder_name': holder_name,
                    'debited_account': line.debited_account.id if line.debited_account else False,
                    'amount_total': line.amount_total
                })
                collection_lines.append(sub_dict)
            for sub_line in self.sub_partner_invoices:
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', sub_line.partner_id.id],
                                                 ]],
                                               {'fields': ['name', 'id', 'mobile']})
                if partner_id:
                    partner_id = partner_id[0]['id']
                else:
                    partner_id = False
                sub_partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', sub_line.sub_customer.id],
                                                 ]],
                                               {'fields': ['name', 'id', 'mobile']})
                if sub_partner_id:
                    sub_partner_id = sub_partner_id[0]['id']
                else:
                    sub_partner_id = False

                sub_dict = (0, 0, {
                    'partner_id': partner_id,
                    'sub_customer': sub_partner_id,
                })
                sub_collection_lines.append(sub_dict)
            for a_line in self.a_partner_invoices:
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', a_line.partner_id.id],
                                                 ]],
                                               {'fields': ['name', 'id', 'mobile']})
                if partner_id:
                    partner_id = partner_id[0]['id']
                else:
                    partner_id = False
                holder_name = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', a_line.holder_name.id],
                                                 ]],
                                               {'fields': ['name', 'id', 'mobile']})

                if holder_name:
                    holder_name = holder_name[0]['id']
                else:
                    holder_name =False
                # holder_name = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                #                                 [[['basic_synch_partner', '=', a_line.debited_account.id],
                #                                   ]],
                #                                 {'fields': ['name', 'id', 'mobile']})

                sub_dict = (0, 0, {
                     'partner_id': partner_id,
                    'check_no': a_line.check_no or False,
                    'check_type': a_line.check_type or False,
                    'check_manual_date': a_line.check_manual_date or False,
                    'date': a_line.date or False,
                    'bank_name': a_line.bank_name or False,
                    'holder_name': holder_name,
                    # 'debited_account': ,
                    # 'debited_account':a_line.debited_account.id if a_line.debited_account else False,
                    'amount_total': a_line.amount_total or False,
                    # 'status': a_line.status
                })
                ad_collection_lines.append(sub_dict)

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'executive.cheque.collection', 'create',
                                            [{
                                                'name': self.name,
                                                'cashier_id': cashier_id,
                                                'user_id': user_id,
                                                'basic_synch_check_collection':str(self.id),
                                                # 'company_id': self.company_id.id,
                                                'another_area': self.another_area or False,
                                                'partner_invoices': collection_lines,
                                                'sub_partner_invoices': sub_collection_lines,
                                                'a_partner_invoices': ad_collection_lines,

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'executive.cheque.collection', 'write', [[area_id[0]['id']],
                                                                                             {
                                                                                                 'name': self.name,
                                                                                                 'cashier_id': cashier_id,
                                                                                                 'user_id': user_id,
                                                                                                 # 'company_id': self.company_id.id,
                                                                                                 'another_area': self.another_area or False,
                                                                                                 'partner_invoices': collection_lines,
                                                                                                 'sub_partner_invoices': sub_collection_lines,
                                                                                                 'a_partner_invoices': ad_collection_lines,
                                                                                             }])
            return





class TodayCheques(models.Model):
    _inherit = "today.cheques"

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
            estimate = models.execute_kw(db, uid, password, 'today.cheques', 'search_read',
                                         [[['basic_synch_today_cheques', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'today.cheques', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_tocheques_button': True,
                                                                                  }])
        return super(TodayCheques, self).action_confirm()
    @api.constrains('name', 'from_date','to_date','sales_person','partner_id','check_count')
    def constraint_cashier_id_name(self):
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
            area_id = models.execute_kw(db, uid, password, 'today.cheques', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})

            collected_check = []
            for line in self.today_lines:
                ref_id = models.execute_kw(db, uid, password, 'executive.cheque.collection', 'search_read',
                                            [[['basic_synch_check_collection', '=', line.ref_id.id]]],
                                            {'fields': ['name', 'id']})
                if ref_id:
                    ref_id = ref_id[0]['id']
                else:
                    ref_id =False
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                         [[['basic_synch_partner', '=', line.partner_id.id],
                                                           ]],
                                                         {'fields': ['name', 'id', 'mobile']})
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
                    holder_name =False
                debited_account = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                [[['name', '=', line.debited_account.name],['company_id','=',line.debited_account.company_id.id]
                                                  ]],
                                                {'fields': ['name', 'id']})
                if debited_account:
                    debited_account = debited_account[0]['id']
                else:
                    debited_account = False
                sub_dict = (0, 0, {
                    'ref_id':ref_id,
                    'partner_id':partner_id,
                    'date':line.date,
                    'check_no':line.check_no,
                    'check_type':line.check_type,
                    'bank_name':line.bank_name,
                    'holder_name':holder_name,
                    'amount_total':line.amount_total,
                    'debit_mandory':line.debit_mandory,
                    'debited_account':debited_account,
                    'status':line.status,
                    'clearing_date':line.clearing_date,
                    'submitted_date':line.submitted_date,
                })
                collected_check.append(sub_dict)
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'today.cheques', 'create',
                                            [{
                                                'from_date': self.from_date,
                                                'to_date': self.to_date,
                                                'basic_synch_today_cheques': str(self.id),
                                                'today_lines': collected_check,

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'today.cheques', 'write', [[area_id[0]['id']],
                                                                                                    {
                                                                                                        'from_date': self.from_date,
                                                                                                        'to_date': self.to_date,
                                                                                                        'basic_synch_today_cheques': str(
                                                                                                            self.id),
                                                                                                        'today_lines': collected_check,

                                                                                                    }])
            return


