import requests

from odoo import http
from odoo.http import request
from datetime import datetime
from num2words import num2words
import urllib.parse as urlparse
from urllib.parse import parse_qs
from odoo import models,fields,api


class AmountWithdraw(models.Model):
    _inherit = "amount.withdraw"


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
            estimate = models.execute_kw(db, uid, password, 'amount.withdraw', 'search_read',
                                         [[['basic_synch_withdraw', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'amount.withdraw', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_withdraw_button': True,
                                                                                  }])
        return super(AmountWithdraw, self).action_confirm()
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
            estimate = models.execute_kw(db, uid, password, 'amount.withdraw', 'search_read',
                                         [[['basic_synch_withdraw', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'amount.withdraw', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_withdreverse_button': True,
                                                                                  }])
        return super(AmountWithdraw, self).action_reverse()
    @api.constrains('name','type_of_draw','to_journal_id','amount','reference','payment_date')
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
            area_id = models.execute_kw(db, uid, password, 'amount.withdraw', 'search_read',
                                                 [[['basic_synch_withdraw', '=', self.id]]],
                                                 {'fields': ['name', 'id']})

            to_journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                 [[['name', '=', self.to_journal_id.name],['company_id', '=', self.to_journal_id.company_id.id]]],
                                                 {'fields': ['name', 'id']})

            if to_journal_id:
                to_journal_id = to_journal_id[0]['id']
            else:
                to_journal_id =False
            journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                             [[['name', '=', self.journal_id.name],['company_id', '=', self.journal_id.company_id.id]]],
                                                             {'fields': ['name', 'id']})

            if journal_id:
                journal_id = journal_id[0]['id']
            else:
                journal_id =False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'amount.withdraw', 'create',
                                              [{
                                                      'basic_synch_withdraw':str(self.id),
                                                      'type_of_draw':self.type_of_draw,
                                                      'journal_id':journal_id,
                                                      'to_journal_id':to_journal_id,
                                                      'amount':self.amount,
                                                      'reference':self.reference,
                                                      'payment_date':self.payment_date,
                                                  }]
                                              )
            else:
                upd = models.execute_kw(db, uid, password, 'amount.withdraw', 'write', [[area_id[0]['id']],
                                                                                    {
                                                                                        'type_of_draw': self.type_of_draw,
                                                                                        'to_journal_id': to_journal_id,
                                                                                        'journal_id': journal_id,
                                                                                        'amount': self.amount,
                                                                                        'reference': self.reference,
                                                                                        'payment_date': self.payment_date,
                                            }])
            return

class CashToBank(models.Model):
    _inherit = 'cash.to.bank'

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
            estimate = models.execute_kw(db, uid, password, 'cash.to.bank', 'search_read',
                                         [[['basic_synch_to_bank', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'cash.to.bank', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_to_bank_button': True,
                                                                                  }])
        return super(CashToBank, self).action_confirm()
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
            estimate = models.execute_kw(db, uid, password, 'cash.to.bank', 'search_read',
                                         [[['basic_synch_to_bank', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'cash.to.bank', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_withdreverse_button': True,
                                                                                  }])
        return super(CashToBank, self).action_reverse()
    @api.constrains('name','journal_id','account_id','to_journal_id','amount','reference','payment_date')
    def constraint_journal_id(self):
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
            area_id = models.execute_kw(db, uid, password, 'cash.to.bank', 'search_read',
                                                 [[['basic_synch_to_bank', '=', self.id]]],
                                                 {'fields': ['name', 'id']})

            to_journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                 [[['name', '=', self.to_journal_id.name],['company_id', '=', self.to_journal_id.company_id.id]]],
                                                 {'fields': ['name', 'id']})

            if to_journal_id:
                to_journal_id = to_journal_id[0]['id']
            else:
                to_journal_id =False
            journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                             [[['name', '=', self.journal_id.name],['company_id', '=', self.journal_id.company_id.id]]],
                                                             {'fields': ['name', 'id']})

            if journal_id:
                journal_id = journal_id[0]['id']
            else:
                journal_id =False
            account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                           [[['name', '=', self.account_id.name],
                                             ['company_id', '=', self.account_id.company_id.id]]],
                                           {'fields': ['name', 'id']})
            if account_id:
                account_id = account_id[0]['id']
            else:
                account_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'cash.to.bank', 'create',
                                              [{
                                                      'basic_synch_to_bank':str(self.id),
                                                      'journal_id':journal_id,
                                                      'account_id':account_id,
                                                      'to_journal_id':to_journal_id,
                                                      'amount':self.amount,
                                                      'reference':self.reference,
                                                      'payment_date':self.payment_date,
                                                  }]
                                              )
            else:
                upd = models.execute_kw(db, uid, password, 'cash.to.bank', 'write', [[area_id[0]['id']],
                                                                                    {
                                                                                          'journal_id':journal_id,
                                                                                          'account_id':account_id,
                                                                                          'to_journal_id':to_journal_id,
                                                                                          'amount':self.amount,
                                                                                          'reference':self.reference,
                                                                                          'payment_date':self.payment_date,
                                            }])
            return





class InternalAmountTransfer(models.Model):
    _inherit = 'internal.amount.transfer'



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
            estimate = models.execute_kw(db, uid, password, 'internal.amount.transfer', 'search_read',
                                         [[['basic_synch_bank_transf', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'internal.amount.transfer', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_bank_transf_button': True,
                                                                                  }])
        return super(InternalAmountTransfer, self).action_post()

#################################################################################################
    @api.constrains('name', 'company_id','freight_lines')
    def constraint_journal_id(self):
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
            area_id = models.execute_kw(db, uid, password, 'internal.amount.transfer', 'search_read',
                                        [[['basic_synch_bank_transf', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            # to_journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
            #                                   [[['name', '=', self.to_journal_id.name],
            #                                     ['company_id', '=', self.to_journal_id.company_id.id]]],
            #                                   {'fields': ['name', 'id']})

            lines = []
            for line in self.freight_lines:
                journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                   [[['name', '=', line.journal_id.name],['company_id', '=', line.journal_id.company_id.id]]],
                                                   {'fields': ['name', 'id']})

                if journal_id:
                    journal_id = journal_id[0]['id']
                else:
                    journal_id =False
                from_acc_company = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                               [[['name', '=', line.from_acc_company.name],
                                                ]],
                                               {'fields': ['name', 'id']})
                if from_acc_company:
                    from_acc_company = from_acc_company[0]['id']
                else:
                    from_acc_company =False

                to_journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                               [[['name', '=', line.to_journal_id.name],
                                                 ['company_id', '=', line.to_journal_id.company_id.id]]],
                                                {'fields': ['name', 'id']})
                if to_journal_id:
                    to_journal_id = to_journal_id[0]['id']
                else:
                    to_journal_id =False

                to_acc_company = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                     [[['name', '=', line.to_acc_company.name]]],
                                                     {'fields': ['name', 'id']})
                if to_acc_company:
                    to_acc_company = to_acc_company[0]['id']
                else:
                    to_acc_company = False
                sub_dict = (0, 0, {
                    'journal_id': journal_id,
                    'from_acc_company': from_acc_company,
                    'to_journal_id': to_journal_id,
                    'to_acc_company':to_acc_company,
                    'amount': line.amount,

                })
                lines.append(sub_dict)

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'internal.amount.transfer', 'create',
                                            [{
                                                'basic_synch_bank_transf': str(self.id),
                                                'freight_lines': lines,
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'internal.amount.transfer', 'write', [[area_id[0]['id']],
                                                                                     {
                                                                                        'freight_lines': lines,
                                                                                     }])
            return




class FundTransferBTCompanies(models.Model):
    _inherit = "fund.transfer.companies"


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
            estimate = models.execute_kw(db, uid, password, 'fund.transfer.companies', 'search_read',
                                         [[['basic_synch_fund_transf', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'fund.transfer.companies', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_fund_t_ref_button': True,
                                                                                  }])
        return super(FundTransferBTCompanies, self).action_reverse()

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
            estimate = models.execute_kw(db, uid, password, 'fund.transfer.companies', 'search_read',
                                         [[['basic_synch_fund_transf', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'fund.transfer.companies', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_fund_transf_button': True,
                                                                                  }])
        return super(FundTransferBTCompanies, self).action_post()


    @api.constrains('name', 'create_date', 'fund_lines')
    def constraint_journal_id(self):
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
            area_id = models.execute_kw(db, uid, password, 'fund.transfer.companies', 'search_read',
                                        [[['basic_synch_fund_transf', '=', self.id]]],
                                        {'fields': ['name', 'id']})


            lines = []
            for line in self.fund_lines:
                journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                               [[['name', '=', line.journal_id.name],
                                                 ['company_id', '=', line.journal_id.company_id.id]]],
                                               {'fields': ['name', 'id']})

                if journal_id:
                    journal_id = journal_id[0]['id']
                else:
                    journal_id = False
                from_acc_company = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                     [[['name', '=', line.from_acc_company.name],
                                                       ]],
                                                     {'fields': ['name', 'id']})
                if from_acc_company:
                    from_acc_company = from_acc_company[0]['id']
                else:
                    from_acc_company = False

                to_journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search_read',
                                                  [[['name', '=', line.to_journal_id.name],
                                                    ['company_id', '=', line.to_journal_id.company_id.id]]],
                                                  {'fields': ['name', 'id']})
                if to_journal_id:
                    to_journal_id = to_journal_id[0]['id']
                else:
                    to_journal_id = False

                to_acc_company = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                   [[['name', '=', line.to_acc_company.name]]],
                                                   {'fields': ['name', 'id']})
                if to_acc_company:
                    to_acc_company = to_acc_company[0]['id']
                else:
                    to_acc_company = False
                account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                   [[['name', '=', line.account_id.name],['company_id', '=', line.account_id.company_id.id]]],
                                                   {'fields': ['name', 'id']})
                if account_id:
                    account_id = account_id[0]['id']
                else:
                    account_id =False
                to_account = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                                   [[['name', '=', line.to_account.name],['company_id', '=', line.to_account.company_id.id]]],
                                                                   {'fields': ['name', 'id']})
                if to_account:
                    to_account = to_account[0]['id']
                else:
                    to_account =False

                sub_dict = (0, 0, {
                    'journal_id': journal_id,
                    'from_acc_company': from_acc_company,
                    'to_journal_id': to_journal_id,
                    'to_acc_company': to_acc_company,
                    'account_id': account_id,
                    'to_account': to_account,
                    'amount': line.amount,

                })
                lines.append(sub_dict)

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'fund.transfer.companies', 'create',
                                            [{
                                                'basic_synch_fund_transf': str(self.id),
                                                'fund_lines': lines,
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'fund.transfer.companies', 'write', [[area_id[0]['id']],
                                                                                                 {
                                                                                                     'fund_lines': lines,
                                                                                                 }])
            return




class CashBookClosing(models.Model):
    _inherit = "cash.book.closing"


    def action_cash_book_close(self):
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
                estimate = models.execute_kw(db, uid, password, 'cash.book.closing', 'search_read',
                                             [[['basic_synch_closing', '=', self.id]]])

                upd = models.execute_kw(db, uid, password, 'cash.book.closing', 'write', [[estimate[0]['id']],
                                                                                                {
                                                                                                    'basic_synch_closing_button': True,
                                                                                                }])
            return super(CashBookClosing, self).action_cash_book_close()

    @api.constrains('date')
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
            area_id = models.execute_kw(db, uid, password, 'cash.book.closing', 'search_read',
                                        [[['basic_synch_closing', '=', self.id]]],
                                        {'fields': ['id']})

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'cash.book.closing', 'create',
                                            [{
                                                'basic_synch_closing': str(self.id),
                                                'date':self.date,
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'cash.book.closing', 'write', [[area_id[0]['id']],
                                                                                        {
                                                                                            'date': self.date,
                                                                                        }])
            return




class AccountAccount(models.Model):
    _inherit = "account.account"


    @api.constrains('code','name','user_type_id','reconcile','company_id','allowed_journal_ids')
    def constraint_user_type_id(self):
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
            # area_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
            #                                      [[['basic_synch_account', '=', self.id],['name', '=', self.name]]],
            #                                      {'fields': ['name', 'id', 'code']})
            #
            area_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                 [[['name', '=', self.name]]],
                                                 {'fields': ['name', 'id', 'code']})

            company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                 [[['name', '=', self.company_id.name]]],
                                                 {'fields': ['name', 'id']})
            if company_id:
                company_id = company_id[0]['id']
            else:
                company_id =1
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'account.account', 'create',
                                              [{
                                                      'name':self.name,
                                                      'code':self.code,
                                                      'user_type_id':self.user_type_id.id,
                                                      'reconcile':self.reconcile or False,
                                                      # 'company_id':company_id,
                                                      # 'allowed_journal_ids':self.allowed_journal_ids.id
                                                      # 'basic_synch_account':str(self.id)

                                                  }]
                                              )
            else:
                upd = models.execute_kw(db, uid, password, 'account.account', 'write', [[area_id[0]['id']],
                                                                                    {
                                                                                        'name': self.name,
                                                                                        'code': self.code,
                                                                                        'user_type_id': self.user_type_id,
                                                                                        'reconcile': self.reconcile,
                                                                                        # 'company_id': company_id,
                                                                                        # 'allowed_journal_ids':self.allowed_journal_ids.id
                                                                                        # 'basic_synch_account': str(
                                                                                        #     self.id)
                                                                                    }])
            return

