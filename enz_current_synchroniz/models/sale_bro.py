import requests

from odoo import http
from odoo.http import request
from datetime import datetime
from num2words import num2words
import urllib.parse as urlparse
from urllib.parse import parse_qs
from odoo import models,fields,api


class ResPartner(models.Model):
    _inherit = 'res.partner'


    local = fields.Boolean(defult=False)

    @api.constrains('name','vat','mobile','state_id','country_id','b_to_b','b_to_c','restriction','is_subc')
    def constraint_partner(self):
        if self.company_type != 'company':
            import xmlrpc.client

            # url = "https://minis.enzapps-gcc.com"
            # db = "minis"
            # username = "info@enzapps.com"
            # password = "YEZPR#ADM@786"

            # url = "https://serb.enzapps-gcc.com"
            # db = "serb"
            # username = "admin"
            # password = "YEZPR#ADM@786"
            synch = self.env['synch.configuration'].search([('activate','=',True)])
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
                partner_passenger_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                     [[['basic_synch_partner', '=', self.id],['name', '=', self.name]]],
                                                     {'fields': ['name', 'id', 'mobile']})

                partner_area_id = models.execute_kw(db, uid, password, 'area.wise', 'search_read',
                                                     [[['executive_area', '=', self.area.name]]],
                                                     {'fields': ['executive_area', 'id']})
                # executive_area_id = models.execute_kw(db, uid, password, 'executive.area.wise', 'search_read',
                #                                      [[['name', '=', self.exicutive_area.name]]],
                #                                      {'fields': ['id']})
                #
                if partner_area_id:
                    partner_area_id = partner_area_id[0]['id']
                else:
                    partner_area_id =False

                if self.is_subc:
                    is_subc = True
                else:
                    is_subc = False
                if not partner_passenger_id:
                    partner = models.execute_kw(db, uid, password, 'res.partner', 'create',
                                                  [{
                                                          'name':self.name,
                                                          'vat':self.vat,
                                                          'street':self.street,
                                                          'street2':self.street2,
                                                          'state_id':self.state_id.id,
                                                          'country_id':self.country_id.id ,
                                                          'mobile':self.mobile,
                                                          'phone':self.phone,
                                                          'basic_synch_partner':str(self.id),
                                                          'city':self.city,
                                                          'zip':self.zip,
                                                          'email':self.email,
                                                          'website':self.website,
                                                          'company_type':self.company_type,
                                                          # 'area': self.area.id,
                                                          # 'area': partner_area_id[0]['id'],
                                                          'area': partner_area_id,
                                                          'estimator':self.estimator,
                                                          'b2b_company_name':self.b2b_company_name or False,
                                                           'site':self.site or False,
                                                           'complete_address':self.complete_address or False,
                                                          'l10n_in_gst_treatment':self.l10n_in_gst_treatment,
                                                          'tcs': self.tcs or False,
                                                          'b_to_b': self.b_to_b or False,
                                                          'restriction': self.restriction or False,
                                                          'b_to_c': self.b_to_c or False,
                                                          'is_subc': is_subc or False,
                                                      # 'executive_area':
                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'res.partner', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                                'name': self.name,
                                                                                                'vat': self.vat,
                                                                                                'street': self.street,
                                                                                                'street2': self.street2,
                                                                                                'state_id': self.state_id.id,
                                                                                                'country_id': self.country_id.id,
                                                                                                'mobile': self.mobile,
                                                                                                'phone': self.phone,
                                                                                                'city': self.city,
                                                                                                'zip': self.zip,
                                                                                                'email': self.email,
                                                                                                'estimator': self.estimator,
                                                                                                'website': self.website,
                                                                                                'company_type': self.company_type,
                                                                                                # 'area': partner_area_id[0]['id'],
                                                                                                'area': partner_area_id,
                                                                                                'site':self.site,
                                                                                                'complete_address': self.complete_address or False,
                                                                                                'l10n_in_gst_treatment': self.l10n_in_gst_treatment or False,
                                                                                                'b2b_company_name': self.b2b_company_name or False,
                                                                                                'tcs': self.tcs or False,
                                                                                                  'b_to_b': self.b_to_b or False,
                                                                                                  'restriction': self.restriction or False,
                                                                                                  'b_to_c': self.b_to_c or False,
                                                                                                  'is_subc': is_subc or False,

                                                                                                # 'l10n_in_gst_treatment': self.l10n_in_gst_treatment or None,

                                                }])
                    print(upd,'upd')
                return


            # print(len(partner_passenger_id))
            # i = 0
            # for all in partner_passenger_id:
            #     # mou = requests.env['res.partner'].search([('reh_driver_id', '=', all['reh_driver_id'])])
                # mous = request.env['res.partner'].sudo().search([('id', '=', all['name'])])
                mous = self
                # for mou in mous:
                #     if mou.name != all['name']:
                #         print('dfhhd',all['name'])



# class ResUsers(models.Model):
#     _inherit = "res.users"
#
#
#
#
#     @api.constrains('name','login','password','company_id')
#     def constraint_users(self):
#         import xmlrpc.client
#         synch = self.env['synch.configuration'].search([('activate', '=', True)])
#         if synch:
#             url = synch.server
#             db = synch.db
#             username = synch.username
#             password = synch.password
#             # password = "YEZPR#ADM@786"
#
#             common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
#             uid = common.authenticate(db, username, password, {})
#             print('uid=', uid)
#             models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
#
#             print(models)
#
#             # partner_passenger_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
#             #                                          [[['basic_synch_users', '=', self.id],
#             #                                            ['name', '=', self.name]]],
#             #                                          {'fields': ['name', 'id', 'login']})
#
#             partner_passenger_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
#                                                      [[['login', '=', self.login]]],
#                                                      {'fields': ['name', 'id', 'login']})
#             # if self.branch_id:
#             #
#             #     branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
#             #                                                          [[['login', '=', self.login],
#             #                                                            ['name', '=', self.branch_id.name]]],
#             #                                                          {'fields': ['name', 'id']})
#             #     branch_id = branch_id[0]['id']
#             # else:
#             #     branch_id =False
#
#
#             if not partner_passenger_id:
#                 partner = models.execute_kw(db, uid, password, 'res.users', 'create',
#                                             [{
#                                                 'name': self.name,
#                                                 'login':self.login,
#                                                 'company_id':self.company_id.id,
#                                                 # 'password':self.password,
#                                                 # 'branch_id':branch_id
#                                             }]
#                                             )
#                 print(partner, 'partner')
#             else:
#                 upd = models.execute_kw(db, uid, password, 'res.users', 'write', [[partner_passenger_id[0]['id']],
#                                                                                     {
#                                                                                         'name': self.name,
#                                                                                         'login': self.login,
#                                                                                         'company_id': self.company_id.id,
#                                                                                         # 'password': self.password,
#                                                                                         # 'branch_id': branch_id
#                                                                                     }])
#             return





class CompanyBranches(models.Model):
    _inherit = "company.branches"

    @api.constrains('name', 'code', 'company_id', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id','company_registry','email','mobile','vat')
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

            partner_passenger_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                                     [[['basic_synch_branch', '=', self.id],
                                                       ['name', '=', self.name]]],
                                                     {'fields': ['name', 'id', 'mobile']})
            # partner_passenger_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
            #                                                      [[['name', '=', self.name]]],
            #                                                      {'fields': ['name', 'id', 'mobile']})

            if not partner_passenger_id:
                partner = models.execute_kw(db, uid, password, 'company.branches', 'create',
                                            [{
                                                'name': self.name,
                                                'code':self.code,
                                                'company_id':self.company_id.id,
                                                'street':self.street,
                                                'street2':self.street2,
                                                'city':self.city,
                                                'state_id':self.state_id.id,
                                                'zip':self.zip,
                                                'country_id':self.country_id.id,
                                                'website':self.website,
                                                'phone':self.phone,
                                                'mobile':self.mobile,
                                                'email':self.email,
                                                'vat':self.vat,
                                                'company_registry':self.company_registry,

                                            }]
                                            )
                print(partner, 'partner')
            else:
                upd = models.execute_kw(db, uid, password, 'company.branches', 'write', [[partner_passenger_id[0]['id']],
                                                                                    {
                                                                                        'name': self.name,
                                                'code':self.code,
                                                'company_id':self.company_id.id,
                                                'street':self.street,
                                                'street2':self.street2,
                                                'city':self.city,
                                                'state_id':self.state_id.id,
                                                'zip':self.zip,
                                                'country_id':self.country_id.id,
                                                'website':self.website,
                                                'phone':self.phone,
                                                'mobile':self.mobile,
                                                'email':self.email,
                                                'vat':self.vat,
                                                'company_registry':self.company_registry,
                                                                                    }])
                print(upd, 'upd')
            return

class ResCompany(models.Model):
    _inherit = "res.company"


    @api.constrains('name', 'code', 'parent_id', 'street', 'street2', 'city', 'state_id', 'zip', 'country_id','company_registry','email','phone','vat')
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

            # partner_passenger_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
            #                                          [[['basic_synch_branch', '=', self.id],
            #                                            ['name', '=', self.name]]],
            #                                          {'fields': ['name', 'id', 'mobile']})
            partner_passenger_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                                 [[['name', '=', self.name]]],
                                                                 {'fields': ['name', 'id', 'phone']})

            if not partner_passenger_id:
                partner = models.execute_kw(db, uid, password, 'res.company', 'create',
                                            [{
                                                'name': self.name,
                                                'code':self.code,
                                                'parent_id':self.parent_id.id,
                                                'street':self.street,
                                                'street2':self.street2,
                                                'city':self.city,
                                                'state_id':self.state_id.id,
                                                'zip':self.zip,
                                                'country_id':self.country_id.id,
                                                'website':self.website,
                                                'phone':self.phone,
                                                # 'mobile':self.mobile,
                                                'email':self.email,
                                                'vat':self.vat,
                                                'company_registry':self.company_registry,

                                            }]
                                            )
                print(partner, 'partner')
            else:
                upd = models.execute_kw(db, uid, password, 'res.company', 'write', [[partner_passenger_id[0]['id']],
                                                                                    {
                                                'name': self.name,
                                                'code':self.code,
                                                'parent_id':self.parent_id.id,
                                                'street':self.street,
                                                'street2':self.street2,
                                                'city':self.city,
                                                'state_id':self.state_id.id,
                                                'zip':self.zip,
                                                'country_id':self.country_id.id,
                                                'website':self.website,
                                                'phone':self.phone,
                                                # 'mobile':self.mobile,
                                                'email':self.email,
                                                'vat':self.vat,
                                                'company_registry':self.company_registry,
                                                                                    }])
                print(upd, 'upd')
            return



