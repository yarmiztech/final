import requests

from odoo import http
from odoo.http import request
from datetime import datetime
from num2words import num2words
import urllib.parse as urlparse
from urllib.parse import parse_qs
from odoo import models,fields,api



class ExecutiveAreaWise(models.Model):
    _inherit = 'executive.area.wise'

    # synch_area_id = fields.Char(string="Sync Area")

    @api.constrains('name','pin_code')
    def constraint_pin_code(self):
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
            area_id = models.execute_kw(db, uid, password, 'executive.area.wise', 'search_read',
                                                 [[['basic_synch_area', '=', self.id],['name', '=', self.name]]],
                                                 {'fields': ['name', 'id', 'pin_code']})
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'executive.area.wise', 'create',
                                              [{
                                                      'name':self.name,
                                                      'pin_code':self.pin_code,
                                                      'basic_synch_area':str(self.id)

                                                  }]
                                              )
            else:
                upd = models.execute_kw(db, uid, password, 'executive.area.wise', 'write', [[area_id[0]['id']],
                                                                                    {
                                                                                            'name': self.name,
                                                                                            'pin_code':self.pin_code,
                                            }])
            return




class PinInformation(models.Model):
    _inherit = "pin.information"

    @api.constrains('from_area', 'from_pin','to_area','to_pin','distance')
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
            area_id = models.execute_kw(db, uid, password, 'pin.information', 'search_read',
                                        [[['basic_synch_pin', '=', self.id]]],
                                        {'fields': ['id']})
            # area_id = models.execute_kw(db, uid, password, 'pin.information', 'search_read',
            #                             [[['from_area', '=', self.from_area.name]]],
            #                             {'fields': ['id']})
            from_area = models.execute_kw(db, uid, password, 'executive.area.wise', 'search_read',
                                         [[['name', '=', self.from_area.name]]],
                                         {'fields': [ 'id']})
            to_area = models.execute_kw(db, uid, password, 'executive.area.wise', 'search_read',
                                         [[['name', '=', self.to_area.name]]],
                                         {'fields': [ 'id']})



            if from_area:
                from_area = from_area[0]['id']
            else:
                from_area = False

            if to_area:
                to_area = to_area[0]['id']
            else:
                to_area = False


            if not area_id:
                partner = models.execute_kw(db, uid, password, 'pin.information', 'create',
                                            [{
                                                'from_area': from_area,
                                                'from_pin': self.from_pin,
                                                'to_area': to_area,
                                                'to_pin': self.to_pin,
                                                'distance': self.distance,
                                                'basic_synch_pin': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'pin.information', 'write', [[area_id[0]['id']],
                                                                                            {
                                                                                                'from_area': self.name,
                                                                                                'from_pin': self.from_pin,
                                                                                                'to_area': self.to_area,
                                                                                                'to_pin': self.to_pin,
                                                                                                'distance': self.distance,
                                                                                                'basic_synch_pin': str(self.id)
                                                                                            }])
            return




class TransportationDeatails(models.Model):
    _inherit = "transportation.details"

    @api.constrains('name', 'transportation_mode', 'email_id', 'transportation_date', 'transporter_id','mobile','street_one','street_two','state_id','country_id','city','zip')
    def constraint_transportation_mode(self):
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
            area_id = models.execute_kw(db, uid, password, 'transportation.details', 'search_read',
                                        [[['basic_synch_transporter', '=', self.id], ['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})
            # area_id = models.execute_kw(db, uid, password, 'transportation.details', 'search_read',
            #                             [[['name', '=', self.name]]],
            #                             {'fields': ['name', 'id']})
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'transportation.details', 'create',
                                            [{
                                                'name': self.name,
                                                'transportation_mode': self.transportation_mode,
                                                'basic_synch_transporter': str(self.id),
                                                'email_id':self.email_id,
                                                'transportation_date':self.transportation_date,
                                                'transporter_id':self.transporter_id,
                                                'mobile':self.mobile,
                                                'street_one':self.street_one,
                                                'street_two':self.street_two,
                                                'state_id':self.state_id.id,
                                                'country_id':self.country_id.id,
                                                'city':self.city,
                                                'zip':self.zip,
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'transportation.details', 'write', [[area_id[0]['id']],
                                                                                            {
                                                                                                'name': self.name,
                                                                                                'transportation_mode': self.transportation_mode,
                                                                                                'email_id': self.email_id,
                                                                                                'transportation_date': self.transportation_date,
                                                                                                'transporter_id': self.transporter_id,
                                                                                                'mobile': self.mobile,
                                                                                                'mobile': self.mobile,
                                                                                                'street_one': self.street_one,
                                                                                                'street_two': self.street_two,
                                                                                                'state_id': self.state_id.id,
                                                                                                'country_id': self.country_id.id,
                                                                                                'city': self.city,
                                                                                                'zip': self.zip,
                                                                                            }])
            return





class EwayConfiguration(models.Model):
    _inherit = "eway.configuration"

    # basic_synch_eway

    @api.constrains('company_id', 'asp_id', 'password', 'url', 'postman_token', 'gstin',
                    'user_name', 'ewb_password', 'sand_user_name', 'sand_password', 'access_token', 'access_date','access_exp_date',
                    'eway_url','eway_cancel_url','consolidate_url','eway_by_irn','irn_einvoice','irn_cancel_url'
                    )
    def constraint_eway_mode(self):
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
            area_id = models.execute_kw(db, uid, password, 'eway.configuration', 'search_read',
                                        [[['basic_synch_eway', '=', self.id], ['name', '=', self.name]]],
                                        {'fields': ['id']})
            # area_id = models.execute_kw(db, uid, password, 'eway.configuration', 'search_read',
            #                             [[['company_id', '=', self.company_id.id]]],
            #                             {'fields': ['id']})
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'eway.configuration', 'create',
                                            [{
                                                'company_id': self.company_id.id,
                                                'asp_id': self.asp_id,
                                                'basic_synch_eway': str(self.id),
                                                'password': self.password,
                                                'url': self.url,
                                                'postman_token': self.postman_token,
                                                'gstin': self.gstin,
                                                'user_name': self.user_name,
                                                'ewb_password': self.ewb_password,
                                                'sand_user_name': self.sand_user_name,
                                                'sand_password': self.sand_password,
                                                'access_token': self.access_token,
                                                'access_date': self.access_date,
                                                'access_exp_date': self.access_exp_date,
                                                'eway_url':self.eway_url,
                                                'eway_cancel_url':self.eway_cancel_url,
                                                'consolidate_url':self.consolidate_url,
                                                'eway_by_irn':self.eway_by_irn,
                                                'irn_einvoice':self.irn_einvoice,
                                                'irn_cancel_url':self.irn_cancel_url

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'eway.configuration', 'write', [[area_id[0]['id']],
                                                                                               {
                                                                                                    'company_id': self.company_id.id,
                                                'asp_id': self.asp_id,
                                                # 'basic_synch_transporter': str(self.id),
                                                'password': self.password,
                                                'url': self.url,
                                                'postman_token': self.postman_token,
                                                'gstin': self.gstin,
                                                'user_name': self.user_name,
                                                'ewb_password': self.ewb_password,
                                                'sand_user_name': self.sand_user_name,
                                                'sand_password': self.sand_password,
                                                'access_token': self.access_token,
                                                'access_date': self.access_date,
                                                'access_exp_date': self.access_exp_date,
                                                'eway_url':self.eway_url,
                                                'eway_cancel_url':self.eway_cancel_url,
                                                'consolidate_url':self.consolidate_url,
                                                'eway_by_irn':self.eway_by_irn,
                                                'irn_einvoice':self.irn_einvoice,
                                                'irn_cancel_url':self.irn_cancel_url
                                                                                                                                               }])
            return



class EInvoiceConfiguration(models.Model):
    _inherit = "einvoice.configuration"

    @api.constrains('company_id', 'asp_id', 'password', 'gstin',
                   'access_token', 'access_date',
                    'access_exp_date'
                    )
    def constraint_einvoice_mode(self):
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
            area_id = models.execute_kw(db, uid, password, 'einvoice.configuration', 'search_read',
                                        [[['basic_synch_einvoice', '=', self.id], ['name', '=', self.name]]],
                                        {'fields': ['id']})
            # area_id = models.execute_kw(db, uid, password, 'einvoice.configuration', 'search_read',
            #                             [[['company_id', '=', self.company_id.id]]],
            #                             {'fields': ['id']})
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'einvoice.configuration', 'create',
                                            [{
                                                'company_id': self.company_id.id,
                                                'asp_id': self.asp_id,
                                                'basic_synch_einvoice': str(self.id),
                                                'password': self.password,
                                                'gstin': self.gstin,
                                                'access_token': self.access_token,
                                                'access_date': self.access_date,
                                                'access_exp_date': self.access_exp_date,

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'einvoice.configuration', 'write', [[area_id[0]['id']],
                                                                                           {
                                                                                               'company_id': self.company_id.id,
                                                                                               'asp_id': self.asp_id,
                                                                                               # 'basic_synch_einvoice': str(self.id),
                                                                                               'password': self.password,
                                                                                               'gstin': self.gstin,
                                                                                               'access_token': self.access_token,
                                                                                               'access_date': self.access_date,
                                                                                               'access_exp_date': self.access_exp_date,
                                                                                           }])
            return

