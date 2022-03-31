
from odoo import api, fields, models, _

from datetime import date
from datetime import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import calendar
import re
import json
from dateutil.relativedelta import relativedelta
import pgeocode
import qrcode
from PIL import Image
from random import choice
from string import digits



class EstimateOrders(models.Model):
    _inherit = 'estimate.orders'
    _order = 'id desc'

    def action_oder_confirm(self):
        res = super(EstimateOrders, self).action_oder_confirm()
        estimate = self.env['sale.estimate'].search([('est_order_id','=',self.id)])
        if estimate:
            estimate.c_date = self.c_date
        return res



class CashToBank(models.Model):
    _inherit = 'cash.to.bank'


    @api.onchange('journal_id')
    def onchange_journal_id(self):
        if self.journal_id:
            account = self.env['account.account'].search(
                [('name', '=', 'Cash'), ('company_id', '=', self.env.user.company_id.id)])
            self.account_id = account
            journals = self.env['account.journal'].search(
                [('type', '=', 'bank')])
            if journals:
                return {'domain': {'to_journal_id': [('id', 'in', journals.ids)]}}





    @api.onchange('to_journal_id')
    def onchange_to_journal_id(self):
        if self.to_journal_id:
            account = self.to_journal_id.payment_debit_account_id
            self.to_account_id = account


class ExpensesDiscounttLines(models.Model):
    _inherit = 'expense.disc.lines'

    def _get_default_journal_id(self):
        return self.env['account.journal'].search(
            [('type', '=', 'cash'),('company_id', '=', 1)])

    journal_id = fields.Many2one('account.journal', string='Journal', ondelete='cascade',default=_get_default_journal_id,
                                 help="This field is ignored in a bank statement reconciliation.")

class AmountWithdraw(models.Model):

    _inherit = "amount.withdraw"

    def _get_default_journal_id(self):
        # journals = self.env['account.journal']
        journals = self.env['account.journal'].search(
            [('type', '=', 'cash'), ('company_id', '=', 1)])
        journals+=self.env['account.journal'].search(
            [('type', '=', 'bank')])
        return {'domain': {'to_journal_id': [('id', 'in', journals.ids)]}}

    journal_company_id = fields.Many2one('res.company',string='Journal Company')
    to_journal_id = fields.Many2one('account.journal', string='Withdraw/Deposit', ondelete='cascade',

                                 help="This field is ignored in a bank statement reconciliation.")


    @api.onchange('type_of_draw')
    def onchange_journal_id(self):
        journals = self.env['account.journal'].search(
            [('type', '=', 'cash'), ('company_id', '=', 1)])
        journals += self.env['account.journal'].search(
            [('type', '=', 'bank')])
        return {'domain': {'to_journal_id': [('id', 'in', journals.ids)]}}



class SalesInvoiceCancel(models.Model):
    _inherit = 'sales.invoice.cancel'

    @api.onchange('company_id')
    def onchange_company_id_id(self):
        return {'domain': {'branch_id': [
            ('id', 'in', self.env['company.branches'].search([('company_id', '=', self.company_id.id)]).ids)]}}


    def action_cancel_create_all(self):
        print('dfgdfg')
        if self.invoice_id:
            self.invoice_id.sudo().write({'state': 'cancel'})
        ledger_invoices = self.env['partner.ledger.customer'].sudo().search(
            [('invoice_id', '=', self.invoice_id.id), ('company_id', '=', self.invoice_id.company_id.id)])
        if ledger_invoices:
            for each_ledger in ledger_invoices:
                each_ledger.unlink()
        self.write({'state':'cancel'})



class EstimateOrders(models.Model):
    _inherit = 'estimate.orders'

    @api.onchange('c_date')
    def _onchange_user_id(self):
        if self.c_date:
            journals = self.env['res.users'].search(
                [('company_id', '=', self.company_id.id)])
            if journals:
                return {'domain': {'user_id': [('id', 'in', journals.ids)]}}

    @api.onchange('partner_id')
    def _onchange_partner_ids(self):
        if self.partner_id:
            journals = self.env['res.users'].search(
                [('company_id', '=', self.company_id.id)])
            if journals:
                return {'domain': {'estimate_user_id': [('id', 'in', journals.ids)]}}



class SalesReturn(models.Model):
    _inherit = 'sales.return'
    def _compute_delivery_count(self):
        for each in self:
            each.delivery_challan_count =0

class SalesInvoiceCancel(models.Model):
    _inherit = 'sales.invoice.cancel'

    @api.depends('sales_return_lines')
    def _compute_tax_amount(self):
        for l in self:
            l.tax_amount = 0
            for line in l.sales_return_lines:
                if line.product_id:
                    actual = line.sub_total
                    for tax in line.tax_ids:
                        tax_value_system = actual * sum(tax.children_tax_ids.mapped('amount')) / 100
                        l.tax_amount += tax_value_system
