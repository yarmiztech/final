import requests

from odoo import http
from odoo.http import request
from datetime import datetime
from num2words import num2words
import urllib.parse as urlparse
from urllib.parse import parse_qs
from odoo import models,fields,api


class FreightDiscountConfig(models.Model):
    _inherit = 'freight.disc.config'

    @api.constrains('name')
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
            area_id = models.execute_kw(db, uid, password, 'freight.disc.config', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'freight.disc.config', 'create',
                                            [{
                                                'name': self.name,
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'freight.disc.config', 'write', [[area_id[0]['id']],
                                                                                            {
                                                                                                'name': self.name,
                                                                                            }])
            return


class FreightDiscount(models.Model):
    _inherit = 'freight.disc'

    def action_post(self):
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
            estimate = models.execute_kw(db, uid, password, 'freight.disc', 'search_read',
                                         [[['basic_synch_freight', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'freight.disc', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_freight_button': True,
                                                                                  }])
        return super(FreightDiscount, self).action_post()
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
            estimate = models.execute_kw(db, uid, password, 'freight.disc', 'search_read',
                                         [[['basic_synch_freight', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'freight.disc', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_withdreverse_button': True,
                                                                                  }])
        return super(FreightDiscount, self).action_reverse()
    @api.constrains('name','creates_date','freight_lines')
    def constraint_withdraw_code(self):
        import xmlrpc.client
        synch = self.env['synch.configuration'].search([('activate','=',True)])
        if synch:
            url = synch.server
            db = synch.db
            username = synch.username
            password = synch.password
            # password = "YEZPR#ADM@786"
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            area_id = models.execute_kw(db, uid, password, 'freight.disc', 'search_read',
                                                 [[['basic_synch_freight', '=', self.id]]],
                                                 {'fields': ['name', 'id']})


            freight_lines = []
            for line in self.freight_lines:
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                         [[['basic_synch_partner', '=', line.partner_id.id]
                                                           ]],
                                                         {'fields': ['name', 'id', 'mobile']})
                if partner_id:
                    partner_id = partner_id[0]['id']
                else:
                    partner_id =False
                journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                               [[['name', '=', line.journal_id.name],
                                                 ['company_id', '=', line.journal_id.company_id.id]]],
                                               {'fields': ['name', 'id']})

                if journal_id:
                    journal_id = journal_id[0]['id']
                else:
                    journal_id = False

                freight = models.execute_kw(db, uid, password, 'freight.disc.config', 'search_read',
                                               [[['name', '=', line.freight.name],
                                                ]],
                                               {'fields': ['name', 'id']})
                if freight:
                    freight = freight[0]['id']
                else:
                    freight =False

                sub_dict = (0, 0, {
                    'partner_id': partner_id,
                    'journal_id': journal_id,
                    'freight': freight,
                    'amount': line.amount,
                    'reverse': line.reverse,

                })
                freight_lines.append(sub_dict)

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'freight.disc', 'create',
                                              [{
                                                  'creates_date': self.creates_date,
                                                  'basic_synch_freight':str(self.id),
                                                    'freight_lines':freight_lines,
                                                  }]
                                              )
            else:
                upd = models.execute_kw(db, uid, password, 'freight.disc', 'write', [[area_id[0]['id']],
                                                                                    {
                                                                                      'freight_lines':freight_lines,
                                            }])
            return



class PartyAdvanceLedger(models.Model):
    _inherit = "party.advance.ledger"


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
            estimate = models.execute_kw(db, uid, password, 'party.advance.ledger', 'search_read',
                                         [[['basic_synch_party_advance', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'party.advance.ledger', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_party_advance_button': True,
                                                                                  }])
        return super(PartyAdvanceLedger, self).action_confirm()


    @api.constrains('name', 'date', 'party_advance_lines')
    def constraint_party_advance_lines(self):
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
            area_id = models.execute_kw(db, uid, password, 'party.advance.ledger', 'search_read',
                                        [[['basic_synch_party_advance', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            freight_lines = []
            for line in self.party_advance_lines:
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', line.partner_id.id]
                                                 ]],
                                               {'fields': ['name', 'id', 'mobile']})
                if partner_id:
                    partner_id = partner_id[0]['id']
                else:
                    partner_id = False
                journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                               [[['name', '=', line.journal_id.name],
                                                 ['company_id', '=', line.journal_id.company_id.id]]],
                                               {'fields': ['name', 'id']})

                if journal_id:
                    journal_id = journal_id[0]['id']
                else:
                    journal_id = False
                sub_dict = (0, 0, {
                    'partner_id': partner_id,
                    'journal_id': journal_id,
                    'amount': line.amount,
                })
                freight_lines.append(sub_dict)

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'party.advance.ledger', 'create',
                                            [{
                                                'date': self.date,
                                                'basic_synch_party_advance': str(self.id),
                                                'party_advance_lines': freight_lines,
                                                'type_advance':self.type_advance                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'party.advance.ledger', 'write', [[area_id[0]['id']],
                                                                                     {
                                                                                         'date': self.date,
                                                                                        'basic_synch_party_advance': str(self.id),
                                                                                        'party_advance_lines': freight_lines,
                                                                                        'type_advance':self.type_advance
                                                                                     }])
            return




class CashierDirectCollection(models.Model):
    _inherit = "cashier.direct.collection"


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
            estimate = models.execute_kw(db, uid, password, 'cashier.direct.collection', 'search_read',
                                         [[['basic_synch_direct', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'cashier.direct.collection', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_direct_button': True,
                                                                                  }])
        return super(CashierDirectCollection, self).action_reverse()


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
            estimate = models.execute_kw(db, uid, password, 'cashier.direct.collection', 'search_read',
                                         [[['basic_synch_direct', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'cashier.direct.collection', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_direct_button': True,
                                                                                  }])
        return super(CashierDirectCollection, self).action_confirm()



    @api.constrains('name', 'cashier_id', 'payment_date')
    def constraint_party_advance_lines(self):
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
            area_id = models.execute_kw(db, uid, password, 'cashier.direct.collection', 'search_read',
                                        [[['basic_synch_direct', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            partner_invoices = []
            cashier_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                           [[['name', '=', self.cashier_id.name]]],
                                           {'fields': ['name', 'id']})
            if cashier_id:
                cashier_id = cashier_id[0]['id']
            else:
                cashier_id = False

            for line in self.partner_invoices:
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', line.partner_id.id]
                                                 ]],
                                               {'fields': ['name', 'id', 'mobile']})
                if partner_id:
                    partner_id = partner_id[0]['id']
                else:
                    partner_id = False
                journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                               [[['name', '=', line.journal_id.name],
                                                 ['company_id', '=', line.journal_id.company_id.id]]],
                                               {'fields': ['name', 'id']})

                if journal_id:
                    journal_id = journal_id[0]['id']
                else:
                    journal_id = False
                sub_dict = (0, 0, {
                    'partner_id': partner_id,
                    'reason': line.reason,
                    'journal_id': journal_id,
                    'amount_total': line.amount_total,
                })
                partner_invoices.append(sub_dict)





            if not area_id:

                partner = models.execute_kw(db, uid, password, 'cashier.direct.collection', 'create',
                                            [{
                                                'cashier_id': cashier_id,
                                                'basic_synch_direct': str(self.id),
                                                'partner_invoices': partner_invoices,
                                                'payment_date':self.payment_date                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'cashier.direct.collection', 'write', [[area_id[0]['id']],
                                                                                     {
                                                                                         'cashier_id': cashier_id,
                                                                                         'basic_synch_direct': str(
                                                                                             self.id),
                                                                                         'partner_invoices': partner_invoices,
                                                                                         'payment_date': self.payment_date
                                                                                     }])
            return




class RtgsNeftCollections(models.Model):
    _inherit = "neft.rtgs.collection"


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
            estimate = models.execute_kw(db, uid, password, 'neft.rtgs.collection', 'search_read',
                                         [[['basic_synch_neft', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'neft.rtgs.collection', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_neft_button': True,
                                                                                  }])
        return super(RtgsNeftCollections, self).action_confirm()


    @api.constrains('name', 'type', 'payment_date','accountant','sub_partner','address','journal_id','partner_type')
    def constraint_party_advance_lines(self):
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
            area_id = models.execute_kw(db, uid, password, 'neft.rtgs.collection', 'search_read',
                                        [[['basic_synch_neft', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            accountant = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                           [[['name', '=', self.accountant.name]]],
                                           {'fields': ['name', 'id']})
            if accountant:
                accountant = accountant[0]['id']
            else:
                accountant = False

            sub_partner = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                           [[['name', '=', self.sub_partner.name]]],
                                           {'fields': ['name', 'id']})
            if sub_partner:
                sub_partner = sub_partner[0]['id']
            else:
                sub_partner = False

            journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                           [[['name', '=', self.journal_id.name],
                                             ['company_id', '=', self.journal_id.company_id.id]]],
                                           {'fields': ['name', 'id']})

            if journal_id:
                journal_id = journal_id[0]['id']
            else:
                journal_id = False

            if not area_id:

                partner = models.execute_kw(db, uid, password, 'neft.rtgs.collection', 'create',
                                            [{
                                                'type': self.type,
                                                'basic_synch_neft': str(self.id),
                                                'payment_date': self.payment_date,
                                                'accountant':accountant,
                                                'sub_partner':sub_partner,
                                                'address':self.address,
                                                'journal_id':journal_id,
                                                'partner_type':self.partner_type,
                                                'bank_state':self.bank_state,
                                                'cleared_date':self.cleared_date,
                                                'amount_total':self.amount_total,
                                                'description':self.description,
                                                'amount_in_word':self.amount_in_word
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'neft.rtgs.collection', 'write', [[area_id[0]['id']],
                                                                                                  {
                                                                                                      'type': self.type,
                                                'basic_synch_neft': str(self.id),
                                                'payment_date': self.payment_date,
                                                'accountant':accountant,
                                                'sub_partner':sub_partner,
                                                'address':self.address,
                                                'journal_id':journal_id,
                                                'partner_type':self.partner_type,
                                                'bank_state':self.bank_state,
                                                'cleared_date':self.cleared_date,
                                                'amount_total':self.amount_total,
                                                'description':self.description,
                                                'amount_in_word':self.amount_in_word
                                                                                                  }])
            return


class ExpensesDiscount(models.Model):
    _inherit = 'expenses.disc'
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
            estimate = models.execute_kw(db, uid, password, 'expenses.disc', 'search_read',
                                         [[['basic_synch_expen', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'expenses.disc', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_direct_rev_button': True,
                                                                                  }])
        return super(ExpensesDiscount, self).action_reverse()


    def action_post(self):
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
            estimate = models.execute_kw(db, uid, password, 'expenses.disc', 'search_read',
                                         [[['basic_synch_expen', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'expenses.disc', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_expen_button': True,
                                                                                  }])
        return super(ExpensesDiscount, self).action_post()


    @api.constrains('name', 'creates_date', 'freight_lines')
    def constraint_withdraw_code(self):
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
            area_id = models.execute_kw(db, uid, password, 'expenses.disc', 'search_read',
                                        [[['basic_synch_expen', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            freight_lines = []
            for line in self.freight_lines:
                journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                               [[['name', '=', line.journal_id.name],
                                                 ['company_id', '=', line.journal_id.company_id.id]]],
                                               {'fields': ['name', 'id']})

                if journal_id:
                    journal_id = journal_id[0]['id']
                else:
                    journal_id = False
                sub_dict = (0, 0, {
                    'journal_id': journal_id,
                    'amount': line.amount,
                    'reason': line.reason,

                })
                freight_lines.append(sub_dict)

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'expenses.disc', 'create',
                                            [{
                                                'creates_date': self.creates_date,
                                                'basic_synch_expen': str(self.id),
                                                'freight_lines': freight_lines,
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'expenses.disc', 'write', [[area_id[0]['id']],
                                                                                     {
                                                                                         'creates_date': self.creates_date,
                                                                                         'basic_synch_expen': str(
                                                                                             self.id),
                                                                                         'freight_lines': freight_lines,                                                                                     }])
            return

