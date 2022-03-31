import requests

from odoo import http
from odoo.http import request
from datetime import datetime
from num2words import num2words
import urllib.parse as urlparse
from urllib.parse import parse_qs
from odoo import models, fields, api


class HrEmployeePrivate(models.Model):
    _inherit = 'hr.employee'

    @api.constrains('name', 'work_email', 'company_id', 'parent_id', 'address_id', 'resource_calender_id', 'user_id')
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
            area_id = models.execute_kw(db, uid, password, 'hr.employee', 'search_read',
                                        [[['basic_synch_hr_employee', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            company_id = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                           [[['name', '=', self.company_id.name]]],
                                           {'fields': ['name', 'id']})
            if company_id:
                company_id = company_id[0]['id']
            else:
                company_id = 1
            partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                           [[['basic_synch_partner', '=', self.address_id.id],
                                             ]],
                                           {'fields': ['name', 'id', 'mobile']})
            if partner_id:
                partner_id = partner_id[0]['id']
            else:
                partner_id = False
            user_id = models.execute_kw(db, uid, password, 'res.users', 'search_read',
                                        [[['name', '=', self.user_id.name]]],
                                        {'fields': ['name', 'id']})

            if user_id:
                user_id = user_id[0]['id']
            else:
                user_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'hr.employee', 'create',
                                            [{
                                                'name': self.name,
                                                'work_email': self.work_email,
                                                'mobile_phone': self.mobile_phone,
                                                'work_phone': self.work_phone,
                                                'company_id': company_id,
                                                'job_title': self.job_title,
                                                'address_id': partner_id,
                                                'user_id': user_id,
                                                'basic_synch_hr_employee': str(self.id),

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'hr.employee', 'write', [[area_id[0]['id']],
                                                                                    {
                                                                                        'name': self.name,
                                                                                        'work_email': self.work_email,
                                                                                        'company_id': company_id,
                                                                                        'address_id': partner_id,
                                                                                        'work_phone': self.work_phone,
                                                                                        'company_id': company_id,
                                                                                        'user_id': user_id
                                                                                    }])
            return


class FuelType(models.Model):
    _inherit = 'fuel.type'


class LoadingConfig(models.Model):
    _inherit = 'loading.config'

    @api.constrains('name', 'amount', 'branch_id')
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
            area_id = models.execute_kw(db, uid, password, 'loading.config', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id', 'amount']})

            if self.branch_id:

                branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                              [[
                                                  ['name', '=', self.branch_id.name]]],
                                              {'fields': ['name', 'id']})

                if branch_id:
                    branch_id = branch_id[0]['id']
                else:
                    branch_id = False
            else:
                branch_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'loading.config', 'create',
                                            [{
                                                'name': self.name,
                                                'amount': self.amount,
                                                'branch_id': branch_id

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'loading.config', 'write', [[area_id[0]['id']],
                                                                                       {
                                                                                           'name': self.name,
                                                                                           'amount': self.amount,
                                                                                           'branch_id': branch_id
                                                                                       }])
            return


class MamoolConfig(models.Model):
    _inherit = 'mamool.config'

    @api.constrains('name', 'amount', 'branch_id')
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
            area_id = models.execute_kw(db, uid, password, 'mamool.config', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id', 'amount']})

            if self.branch_id:

                branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                              [[
                                                  ['name', '=', self.branch_id.name]]],
                                              {'fields': ['name', 'id']})

                if branch_id:
                    branch_id = branch_id[0]['id']
                else:
                    branch_id = False
            else:
                branch_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'mamool.config', 'create',
                                            [{
                                                'name': self.name,
                                                'amount': self.amount,
                                                'branch_id': branch_id

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'mamool.config', 'write', [[area_id[0]['id']],
                                                                                      {
                                                                                          'name': self.name,
                                                                                          'amount': self.amount,
                                                                                          'branch_id': branch_id
                                                                                      }])
            return


class AdvanceConfig(models.Model):
    _inherit = 'advance.config'

    @api.constrains('name', 'amount')
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
            area_id = models.execute_kw(db, uid, password, 'advance.config', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id', 'amount']})
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'advance.config', 'create',
                                            [{
                                                'name': self.name,
                                                'amount': self.amount,

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'advance.config', 'write', [[area_id[0]['id']],
                                                                                       {
                                                                                           'name': self.name,
                                                                                           'amount': self.amount,
                                                                                       }])
            return


class PetrolPumb(models.Model):
    _inherit = 'petrol.pumb'

    @api.constrains('type', 'name', 'owner_id', 'partner_details', 'fuel_price', 'street', 'street2', 'city', 'state',
                    'zip', 'country', 'phone_no')
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
            area_id = models.execute_kw(db, uid, password, 'petrol.pumb', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})

            owner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                         [[['basic_synch_partner', '=', self.owner_id.id],
                                           ]],
                                         {'fields': ['name', 'id']})
            if owner_id:
                owner_id = owner_id[0]['id']
            else:
                owner_id = False
            partner_details = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                [[['basic_synch_partner', '=', self.partner_details.id],
                                                  ]],
                                                {'fields': ['name', 'id']})
            if partner_details:
                partner_details = partner_details[0]['id']
            else:
                partner_details = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'petrol.pumb', 'create',
                                            [{
                                                'name': self.name,
                                                'type': self.type,
                                                'owner_id': owner_id,
                                                'partner_details': partner_details,
                                                'fuel_price': self.fuel_price,
                                                'street': self.street,
                                                'street2': self.street2,
                                                'city': self.city,
                                                'state': self.state.id,
                                                'country': self.country.id,
                                                'phone_no': self.phone_no,

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'petrol.pumb', 'write', [[area_id[0]['id']],
                                                                                    {
                                                                                        'name': self.name,
                                                                                        'type': self.type,
                                                                                        'owner_id': owner_id,
                                                                                        'partner_details': partner_details,
                                                                                        'fuel_price': self.fuel_price,
                                                                                        'street': self.street,
                                                                                        'street2': self.street2,
                                                                                        'city': self.city,
                                                                                        'state': self.state.id,
                                                                                        'country': self.country.id,
                                                                                        'phone_no': self.phone_no,
                                                                                    }])

            return


class BranchCodeConfig(models.Model):
    _inherit = 'branch.code.config'

    def create_code(self):
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

            estimate = models.execute_kw(db, uid, password, 'branch.code.config', 'search_read',
                                         [[['basic_synch_branch_code', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'branch.code.config', 'write', [[estimate[0]['id']],
                                                                                       {
                                                                                           'basic_synch_branch_code_button': True,
                                                                                       }])
        return super(BranchCodeConfig, self).create_code()

    @api.constrains('branch_id', 'name', 'code', 'prefix', 'padding')
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
            area_id = models.execute_kw(db, uid, password, 'branch.code.config', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})

            if self.branch_id:

                branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                              [[
                                                  ['name', '=', self.branch_id.name]]],
                                              {'fields': ['name', 'id']})

                if branch_id:
                    branch_id = branch_id[0]['id']
                else:
                    branch_id = False
            else:
                branch_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'branch.code.config', 'create',
                                            [{
                                                'name': self.name,
                                                'branch_id': branch_id,
                                                'code': self.code,
                                                'prefix': self.prefix,
                                                'padding': self.padding,

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'branch.code.config', 'write', [[area_id[0]['id']],
                                                                                           {
                                                                                               'name': self.name,
                                                                                               'branch_id': branch_id,
                                                                                               'code': self.code,
                                                                                               'prefix': self.prefix,
                                                                                               'padding': self.padding,
                                                                                           }])

            return


class RouteKmSetUp(models.Model):
    _inherit = 'route.km.set.up'

    @api.constrains('location', 'km', 'customer_id', 'branch_id', 'main_branch_id', 'pick_up_street', 'pick_up_street2',
                    'pick_up_city', 'pick_up_state', 'pick_up_country')
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
            area_id = models.execute_kw(db, uid, password, 'route.km.set.up', 'search_read',
                                        [[['location', '=', self.location]]],
                                        {'fields': ['location', 'id']})

            partner_pass_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                [[['basic_synch_partner', '=', self.customer_id.id]]],
                                                {'fields': ['name', 'id']})
            if partner_pass_id:
                partner_pass_id = partner_pass_id[0]['id']
            else:
                partner_pass_id = False

            if self.branch_id:

                branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                              [[
                                                  ['name', '=', self.branch_id.name]]],
                                              {'fields': ['name', 'id']})

                if branch_id:
                    branch_id = branch_id[0]['id']
                else:
                    branch_id = False
            else:
                branch_id = False

            if self.main_branch_id:

                main_branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                                   [[
                                                       ['name', '=', self.main_branch_id.name]]],
                                                   {'fields': ['name', 'id']})

                if main_branch_id:
                    main_branch_id = main_branch_id[0]['id']
                else:
                    main_branch_id = False
            else:
                main_branch_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'route.km.set.up', 'create',
                                            [{
                                                'location': self.location,
                                                'km': self.km,
                                                'customer_id': partner_pass_id,
                                                # 'basic_synch_area':str(self.id),
                                                'branch_id': branch_id,
                                                'main_branch_id': main_branch_id,
                                                'pick_up_street': self.pick_up_street,
                                                'pick_up_street2': self.pick_up_street2,
                                                'pick_up_city': self.pick_up_city,
                                                'pick_up_state': self.pick_up_state.id,
                                                'pick_up_country': self.pick_up_country.id,
                                                'destination': self.destination,
                                                'approximate_price': self.approximate_price,
                                                'own_rate': self.own_rate,
                                                'drop_street': self.drop_street,
                                                'drop_street2': self.drop_street2,
                                                'drop_city': self.drop_city,
                                                'drop_state': self.drop_state.id,
                                                'drop_country': self.drop_country.id,

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'route.km.set.up', 'write', [[area_id[0]['id']],
                                                                                        {
                                                                                            'location': self.location,
                                                                                            'km': self.km,
                                                                                            'customer_id': partner_pass_id,
                                                                                            'basic_synch_area': str(
                                                                                                self.id),
                                                                                            'branch_id': branch_id,
                                                                                            'main_branch_id': main_branch_id,
                                                                                            'pick_up_street': self.pick_up_street,
                                                                                            'pick_up_street2': self.pick_up_street2,
                                                                                            'pick_up_city': self.pick_up_city,
                                                                                            'pick_up_state': self.pick_up_state.id,
                                                                                            'pick_up_country': self.pick_up_country.id,
                                                                                            'destination': self.destination,
                                                                                            'approximate_price': self.approximate_price,
                                                                                            'own_rate': self.own_rate,
                                                                                            'drop_street': self.drop_street,
                                                                                            'drop_street2': self.drop_street2,
                                                                                            'drop_city': self.drop_city,
                                                                                            'drop_state': self.drop_state.id,
                                                                                            'drop_country': self.drop_country.id,
                                                                                        }])

            return


class VehicleRequest(models.Model):
    _inherit = 'vehicle.request'

    @api.constrains('company_type', 'customer', 'request_date', 'route', 'pick_up_street''pick_up_street2',
                    'request_type', 'from_branch', 'req_branch', 'external_company', 'receiver', 'delivery_date',
                    'drop_street', 'vehicle_lines')
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
            area_id = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                        [[['basic_synch_v_req', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            customer = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                         [[['basic_synch_partner', '=', self.customer.id]]],
                                         {'fields': ['name', 'id']})
            if customer:
                customer = customer[0]['id']
            else:
                customer = False
            route = models.execute_kw(db, uid, password, 'route.km.set.up', 'search_read',
                                      [[['location', '=', self.route.location]]],
                                      {'fields': ['location', 'id']})
            if route:
                route = route[0]['id']
            else:
                route = False
            if self.from_branch:

                from_branch = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                                [[
                                                    ['name', '=', self.from_branch.name]]],
                                                {'fields': ['name', 'id']})

                if from_branch:
                    from_branch = from_branch[0]['id']
                else:
                    from_branch = False
            else:
                from_branch = False
            if self.req_branch:

                req_branch = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                               [[
                                                   ['name', '=', self.req_branch.name]]],
                                               {'fields': ['name', 'id']})

                if req_branch:
                    req_branch = req_branch[0]['id']
                else:
                    req_branch = False
            else:
                req_branch = False

            external_company = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                 [[['name', '=', self.external_company.name]]],
                                                 {'fields': ['name', 'id']})
            if external_company:
                external_company = external_company[0]['id']
            else:
                external_company = False

            vehicle_lines = []
            for line in self.vehicle_lines:
                product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                   [[['name', '=', line.product_id.name]]],
                                                   {'fields': ['name', 'id']})
                if product_server:
                    product_server = product_server[0]['id']
                else:
                    product_server = False
                unit_of_measure = models.execute_kw(db, uid, password, 'uom.uom', 'search_read',
                                                    [[['name', '=', line.unit_of_measure.name]]],
                                                    {'fields': ['name', 'id']})
                if unit_of_measure:
                    unit_of_measure = unit_of_measure[0]['id']
                else:
                    unit_of_measure = False

                # unit_of_measure
                product_main = (0, 0, {
                    'product_id': product_server,
                    'quantity': line.quantity,
                    'unit_of_measure': unit_of_measure,
                    'bags': line.bags,
                    'compute_qty_in_kg': line.compute_qty_in_kg,
                    'no_of_vehicles': line.no_of_vehicles,
                })
                vehicle_lines.append(product_main)

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'vehicle.request', 'create',
                                            [{
                                                'company_type': self.company_type,
                                                'customer': customer,
                                                'request_date': self.request_date,
                                                'route': route,
                                                'basic_synch_v_req': str(self.id),
                                                'approximate_price': self.approximate_price,
                                                'approximate_km': self.approximate_km,
                                                'pick_up_street': self.pick_up_street,
                                                # 'basic_synch_vehi_req':str(self.id),
                                                'pick_up_street2': self.pick_up_street2,
                                                'pick_up_city': self.pick_up_city,
                                                'pick_up_state': self.pick_up_state.id,
                                                'pick_up_zip': self.pick_up_zip,
                                                'pick_up_country': self.pick_up_country.id,
                                                'request_type': self.request_type,
                                                'from_branch': from_branch,
                                                'req_branch': req_branch,
                                                'external_company': external_company,
                                                'reciever': self.reciever,
                                                'delivery_date': self.delivery_date,
                                                'drop_street': self.drop_street,
                                                'drop_street2': self.drop_street2,
                                                'drop_city': self.drop_city,
                                                'drop_state': self.drop_state.id,
                                                'drop_zip': self.drop_zip,
                                                'drop_country': self.drop_country.id,
                                                'vehicle_lines': vehicle_lines,

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'vehicle.request', 'write', [[area_id[0]['id']],
                                                                                        {
                                                                                            'company_type': self.company_type,
                                                                                            'customer': customer,
                                                                                            'request_date': self.request_date,
                                                                                            'route': route,
                                                                                            'pick_up_street': self.pick_up_street,
                                                                                            'pick_up_street2': self.pick_up_street2,
                                                                                            'pick_up_city': self.pick_up_city,
                                                                                            'approximate_price': self.approximate_price,
                                                                                            'pick_up_state': self.pick_up_state.id,
                                                                                            'pick_up_zip': self.pick_up_zip,
                                                                                            'pick_up_country': self.pick_up_country.id,
                                                                                            'request_type': self.request_type,
                                                                                            'from_branch': from_branch,
                                                                                            'req_branch': req_branch,
                                                                                            'external_company': external_company,
                                                                                            'reciever': self.reciever,
                                                                                            'delivery_date': self.delivery_date,
                                                                                            'drop_street': self.drop_street,
                                                                                            'drop_street2': self.drop_street2,
                                                                                            'drop_city': self.drop_city,
                                                                                            'drop_state': self.drop_state.id,
                                                                                            'drop_zip': self.drop_zip,
                                                                                            'drop_country': self.drop_country.id,
                                                                                            'vehicle_lines': vehicle_lines,

                                                                                        }])
            return


class VehicleRequsetApproval(models.Model):
    _inherit = 'vehicle.requset.approval'

    def allocate_vehicle(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.name)])

            estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                         [[['basic_synch_v_req', '=', req.id]]])

            upd = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_alloc_vehi_button': True,
                                                                                                 'basic_synch_alloc_vehi_button_test': True,
                                                                                             }])
        return super(VehicleRequsetApproval, self).allocate_vehicle()


    def button_approve(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.name)])

            estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                         [[['basic_synch_v_req', '=', req.id]]])

            upd = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_v_req_approval_button': True,
                                                                                             }])
        return super(VehicleRequsetApproval, self).button_approve()

    def check_availability(self):
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

            req = self.env['vehicle.request'].search([('name', '=', self.name)])
            estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                         [[['basic_synch_v_req', '=', req.id]]])

            upd = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_v_req_appr_che_button': True,
                                                                                             }])
        return super(VehicleRequsetApproval, self).check_availability()

    def external_vehicle(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.name)])

            estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                         [[['basic_synch_v_req', '=', req.id]]])

            upd = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'basic_synch_v_req_appr_exter_button': True,
                                                                                             }])
        return super(VehicleRequsetApproval, self).external_vehicle()


    @api.constrains('company_type', 'customer', 'request_date', 'route', 'pick_up_street''pick_up_street2',
                    'request_type', 'from_branch', 'req_branch', 'external_company', 'receiver', 'delivery_date',
                    'drop_street', 'vehicle_lines', 'total_vehicle_capacity_needed', 'no_of_vehicle', 'vehicle_id',
                    'allocate_vehicle_lines', 'allocate_vehicle_lines.select',
                    'allocate_vehicle_lines.capacity', 'allocate_vehicle_lines.petrol_bunk',
                    'allocate_vehicle_lines.fuel_rate', 'allocate_vehicle_lines.fuel_qty',
                    'allocate_vehicle_lines.petrol_price', 'allocate_vehicle_lines.ind_no',
                    'allocate_vehicle_lines.advance_amount')
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
            area_id = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                        [[['basic_synch_v_req', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            customer = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                         [[['basic_synch_partner', '=', self.customer.id]]],
                                         {'fields': ['name', 'id']})
            if customer:
                customer = customer[0]['id']
            else:
                customer = False
            route = models.execute_kw(db, uid, password, 'route.km.set.up', 'search_read',
                                      [[['location', '=', self.route.location]]],
                                      {'fields': ['location', 'id']})
            if route:
                route = route[0]['id']
            else:
                route = False
            if self.from_branch:

                from_branch = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                                [[
                                                    ['name', '=', self.from_branch.name]]],
                                                {'fields': ['name', 'id']})

                if from_branch:
                    from_branch = from_branch[0]['id']
                else:
                    from_branch = False
            else:
                from_branch = False
            if self.req_branch:

                req_branch = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                               [[
                                                   ['name', '=', self.req_branch.name]]],
                                               {'fields': ['name', 'id']})

                if req_branch:
                    req_branch = req_branch[0]['id']
                else:
                    req_branch = False
            else:
                req_branch = False

            external_company = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                 [[['name', '=', self.external_company.name]]],
                                                 {'fields': ['name', 'id']})
            if external_company:
                external_company = external_company[0]['id']
            else:
                external_company = False

            vehicle_lines = []
            allocate_vehicle_lines = []
            for v_line in self.allocate_vehicle_lines:
                line_vehicle_id = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                                    [[['license_plate', '=', v_line.vehicle_id.license_plate]]],
                                                    {'fields': ['name', 'id']})
                if line_vehicle_id:
                    line_vehicle_id = line_vehicle_id[0]['id']
                else:
                    line_vehicle_id = False
                driver_code = models.execute_kw(db, uid, password, 'driver.code', 'search_read',
                                                [[['code', '=', v_line.driver.code]]],
                                                {'fields': ['driver', 'id']})
                if driver_code:
                    driver_code = driver_code[0]['id']
                else:
                    driver_code = False
                petrol_bunk = models.execute_kw(db, uid, password, 'petrol.pumb', 'search_read',
                                                [[['name', '=', v_line.petrol_bunk.name]]],
                                                {'fields': ['name', 'id']})
                if petrol_bunk:
                    petrol_bunk = petrol_bunk[0]['id']
                else:
                    petrol_bunk = False

                product_main = (0, 0, {
                    'vehicle_id': line_vehicle_id,
                    'owner': v_line.owner,
                    'driver': driver_code,
                    'phone_no': v_line.phone_no,
                    'capacity': v_line.capacity,
                    'external': v_line.external,
                    'select': v_line.select,
                    # 'currency_capacity': v_line.currency_capacity,
                    'freight': v_line.freight,
                    'petrol_bunk': petrol_bunk,
                    'fuel_rate': v_line.fuel_rate,
                    'fuel_qty': v_line.fuel_qty,
                    'petrol_price': v_line.fuel_qty,
                    'ind_no': v_line.ind_no,
                    'advance_amount': v_line.advance_amount,
                })
                allocate_vehicle_lines.append(product_main)

            for line in self.vehicle_lines:
                product_server = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                   [[['name', '=', line.product_id.name]]],
                                                   {'fields': ['name', 'id']})
                if product_server:
                    product_server = product_server[0]['id']
                else:
                    product_server = False
                unit_of_measure = models.execute_kw(db, uid, password, 'uom.uom', 'search_read',
                                                    [[['name', '=', line.unit_of_measure.name]]],
                                                    {'fields': ['name', 'id']})
                if unit_of_measure:
                    unit_of_measure = unit_of_measure[0]['id']
                else:
                    unit_of_measure = False

                # unit_of_measure
                product_main = (0, 0, {
                    'product_id': product_server,
                    'quantity': line.quantity,
                    'unit_of_measure': unit_of_measure,
                    'bags': line.bags,
                    'compute_qty_in_kg': line.compute_qty_in_kg,
                    'no_of_vehicles': line.no_of_vehicles,
                })
                vehicle_lines.append(product_main)
            vehicle_id = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                           [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                           {'fields': ['name', 'id']})
            if vehicle_id:
                vehicle_id = vehicle_id[0]['id']
            else:
                vehicle_id = False

            # if not area_id:
            #     partner = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'create',
            #                                 [{
            #                                     'company_type': self.company_type,
            #                                     'customer': customer,
            #                                     'request_date': self.request_date,
            #                                     'route': route,
            #                                     'basic_synch_v_req_approval':str(self.id),
            #                                     'approximate_price': self.approximate_price,
            #                                     'approximate_km': self.approximate_km,
            #                                     'pick_up_street': self.pick_up_street,
            #                                     'pick_up_street2': self.pick_up_street2,
            #                                     'pick_up_city': self.pick_up_city,
            #                                     'pick_up_state': self.pick_up_state.id,
            #                                     'pick_up_zip': self.pick_up_zip,
            #                                     'total_vehicle_capacity_needed':self.total_vehicle_capacity_needed,
            #                                     'no_of_vehicles':self.no_of_vehicles,
            #                                     'pick_up_country': self.pick_up_country.id,
            #                                     'request_type': self.request_type,
            #                                     'from_branch': from_branch,
            #                                     'req_branch': req_branch,
            #                                     'external_company': external_company,
            #                                     'reciever': self.reciever,
            #                                     'allocate_vehicle_lines':allocate_vehicle_lines,
            #                                     'vehicle_id':vehicle_id,
            #                                     'delivery_date': self.delivery_date,
            #                                     'drop_street': self.drop_street,
            #                                     'drop_street2': self.drop_street2,
            #                                     'drop_city': self.drop_city,
            #                                     'drop_state': self.drop_state.id,
            #                                     'drop_zip': self.drop_zip,
            #                                     'drop_country': self.drop_country.id,
            #                                     'vehicle_lines': vehicle_lines,
            #                                     # 'basic_synch_area':str(self.id)
            #
            #                                 }]
            #                                 )
            if area_id:
                upd = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'write', [[area_id[0]['id']],
                                                                                                 {
                                                                                                     'company_type': self.company_type,
                                                                                                     'customer': customer,
                                                                                                     'request_date': self.request_date,
                                                                                                     'route': route,
                                                                                                     # 'basic_synch_v_req_approval':str(self.id),
                                                                                                     'total_vehicle_capacity_needed': self.total_vehicle_capacity_needed,
                                                                                                     'no_of_vehicles': self.no_of_vehicles,
                                                                                                     'pick_up_street': self.pick_up_street,
                                                                                                     'pick_up_street2': self.pick_up_street2,
                                                                                                     'pick_up_city': self.pick_up_city,
                                                                                                     'approximate_price': self.approximate_price,
                                                                                                     'pick_up_state': self.pick_up_state.id,
                                                                                                     'pick_up_zip': self.pick_up_zip,
                                                                                                     'pick_up_country': self.pick_up_country.id,
                                                                                                     'request_type': self.request_type,
                                                                                                     'from_branch': from_branch,
                                                                                                     'req_branch': req_branch,
                                                                                                     'external_company': external_company,
                                                                                                     'reciever': self.reciever,
                                                                                                     'delivery_date': self.delivery_date,
                                                                                                     'drop_street': self.drop_street,
                                                                                                     'drop_street2': self.drop_street2,
                                                                                                     'drop_city': self.drop_city,
                                                                                                     'drop_state': self.drop_state.id,
                                                                                                     'drop_zip': self.drop_zip,
                                                                                                     'drop_country': self.drop_country.id,
                                                                                                     'vehicle_lines': vehicle_lines,

                                                                                                 }])
            return


class GeneratePass(models.Model):
    _inherit = 'generate.pass'

    def allote_pass_new(self):
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
            vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                            [[['basic_synch_v_req', '=', self.vehicle_req.id]]],
                                            {'fields': ['name', 'id']})
            if vehicle_req:
                vehicle_req = vehicle_req[0]['id']
            else:
                vehicle_req = False
            estimate = models.execute_kw(db, uid, password, 'generate.pass', 'search_read',
                                         [[['vehicle_req', '=', vehicle_req]]])

            upd = models.execute_kw(db, uid, password, 'generate.pass', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_generate_pass_button': True,
                                                                                  }])
        return super(GeneratePass, self).allote_pass_new()


class GenerateOutPassRequest(models.Model):
    _inherit = 'generate.out.pass.request'

    @api.constrains('order_lines_out_pass')
    def constraint_order_lines_out_pass(self):
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
            area_id = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                        [[['basic_synch_v_req', '=', self.id]]],
                                        {'fields': ['name', 'id']})
            vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                            [[['basic_synch_v_req', '=', self.vehicle_req.id]]],
                                            {'fields': ['name', 'id']})
            if vehicle_req:
                vehicle_req = vehicle_req[0]['id']
            else:
                vehicle_req = False

            estimate = models.execute_kw(db, uid, password, 'generate.out.pass.request', 'search_read',
                                         [[['vehicle_req', '=', vehicle_req]]])



            vehicle_lines = []
            for line in self.order_lines_out_pass:
                vehicle_id = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                               [[['license_plate', '=', line.vehicle_id.license_plate]]],
                                               {'fields': ['name', 'id']})
                if vehicle_id:
                    vehicle_id = vehicle_id[0]['id']
                else:
                    vehicle_id = False

                route_id = models.execute_kw(db, uid, password, 'route.km.set.up', 'search_read',
                                            [[['location', '=', line.route_id.location]]],
                                            {'fields': ['location', 'id']})
                if route_id:
                    route_id = route_id[0]['id']
                else:
                    route_id =False

                company_name = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                                    [[['name', '=', line.company_name.name]]],
                                                    {'fields': ['name', 'id']})
                if company_name:
                    company_name = company_name[0]['id']
                else:
                    company_name = False
                # main_branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                #                                    [[
                #                                        ['name', '=', line.main_branch_id.name]]],
                #                                    {'fields': ['name', 'id']})
                #
                # if main_branch_id:
                #     main_branch_id = main_branch_id[0]['id']
                # else:
                #     main_branch_id = False
                #
                # branch_id = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                #                                    [[
                #                                        ['name', '=', line.branch_id.name]]],
                #                                    {'fields': ['name', 'id']})
                #
                # if branch_id:
                #     branch_id = branch_id[0]['id']
                # else:
                #     branch_id = False
                material_description = models.execute_kw(db, uid, password, 'product.product', 'search_read',
                                                   [[['name', '=', line.material_description.name]]],
                                                   {'fields': ['name', 'id']})
                if material_description:
                    material_description = material_description[0]['id']
                else:
                    material_description = False

                product_main = (0, 0, {
                    'vehicle_id': vehicle_id,
                    'route_id': route_id,
                    'company_name': company_name,
                    'invoice_no': line.invoice_no,
                    'invoice_date': line.invoice_date,
                    'exact_time': line.exact_time,
                    # 'main_branch_id':main_branch_id,
                    'material_description':material_description,
                    'm_code':line.m_code.id,
                    'place_from': line.place_from,
                    'place_to': line.place_to,
                    'party_name': line.party_name,
                    'ton': line.ton,
                    'own_rate': line.own_rate,
                    'company_rate': line.company_rate,
                    'mamool': line.mamool,
                    'loading_charge': line.loading_charge,
                    # 'pick_up_street': line.pick_up_street,
                    # 'pick_up_street2': line.pick_up_street2,
                    # 'pick_up_city': line.pick_up_city,
                    # 'pick_up_state': line.pick_up_state.id,
                    # 'pick_up_zip': line.pick_up_zip,
                    # 'pick_up_country': line.pick_up_country.id,
                    # 'drop_street': line.drop_street,
                    # 'drop_street2': line.drop_street2,
                    # 'drop_city': line.drop_city,
                    # 'drop_state': line.drop_state.id,
                    # 'drop_zip': line.drop_zip,
                    # 'drop_country': line.drop_country.id,
                })
                vehicle_lines.append(product_main)

            if estimate:
                upd = models.execute_kw(db, uid, password, 'generate.out.pass.request', 'write', [[estimate[0]['id']],
                                                                                        {
                                                                                            'order_lines_out_pass': vehicle_lines,
                                                                                        }])
            return

    def allote_out_pass_new(self):
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
            vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                            [[['basic_synch_v_req', '=', self.vehicle_req.id]]],
                                            {'fields': ['name', 'id']})
            if vehicle_req:
                vehicle_req = vehicle_req[0]['id']
            else:
                vehicle_req = False

            estimate = models.execute_kw(db, uid, password, 'generate.out.pass.request', 'search_read',
                                         [[['vehicle_req', '=', vehicle_req]]])

            upd = models.execute_kw(db, uid, password, 'generate.out.pass.request', 'write', [[estimate[0]['id']],
                                                                                              {
                                                                                                  'basic_synch_out_pass_button': True,
                                                                                                  'basic_synch_out_pass_button_test': True,
                                                                                              }])
        return super(GenerateOutPassRequest, self).allote_out_pass_new()
    def update_datas(self):
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
            vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                            [[['basic_synch_v_req', '=', self.vehicle_req.id]]],
                                            {'fields': ['name', 'id']})
            if vehicle_req:
                vehicle_req = vehicle_req[0]['id']
            else:
                vehicle_req = False

            estimate = models.execute_kw(db, uid, password, 'generate.out.pass.request', 'search_read',
                                         [[['vehicle_req', '=', vehicle_req]]])

            upd = models.execute_kw(db, uid, password, 'generate.out.pass.request', 'write', [[estimate[0]['id']],
                                                                                              {
                                                                                                  'basic_synch_update_datas_button': True,
                                                                                              }])
        return super(GenerateOutPassRequest, self).update_datas()
    def post_entries(self):
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
            vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                            [[['basic_synch_v_req', '=', self.vehicle_req.id]]],
                                            {'fields': ['name', 'id']})
            if vehicle_req:
                vehicle_req = vehicle_req[0]['id']
            else:
                vehicle_req = False

            estimate = models.execute_kw(db, uid, password, 'generate.out.pass.request', 'search_read',
                                         [[['vehicle_req', '=', vehicle_req]]])

            upd = models.execute_kw(db, uid, password, 'generate.out.pass.request', 'write', [[estimate[0]['id']],
                                                                                              {
                                                                                                  'basic_synch_post_entries_button': True,
                                                                                              }])
        return super(GenerateOutPassRequest, self).post_entries()


class InternalPumbPayments(models.Model):
    _inherit = 'internal.pumb.payment'

    def approve(self):
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

            estimate = models.execute_kw(db, uid, password, 'internal.pumb.payment', 'search_read',
                                         [[['vehicle_req', '=', self.vehicle_req.id]]])

            upd = models.execute_kw(db, uid, password, 'internal.pumb.payment', 'write', [[estimate[0]['id']],
                                                                                          {
                                                                                              'basic_synch_internal_expense_button': True,
                                                                                          }])
        return super(InternalPumbPayments, self).approve()


class BranchExpenses(models.Model):
    _inherit = 'branch.expenses'

    def submit_expense(self):
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

            estimate = models.execute_kw(db, uid, password, 'branch.expenses', 'search_read',
                                         [[['basic_synch_branch_expenses', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'branch.expenses', 'write', [[estimate[0]['id']],
                                                                                    {
                                                                                        'basic_synch_branch_expenses_button': True,
                                                                                    }])
        return super(BranchExpenses, self).submit_expense()

    def approve_expense(self):
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

            estimate = models.execute_kw(db, uid, password, 'branch.expenses', 'search_read',
                                         [[['basic_synch_branch_expenses', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'branch.expenses', 'write', [[estimate[0]['id']],
                                                                                    {
                                                                                        'basic_synch_branch_app_expenses_button': True,
                                                                                    }])
        return super(BranchExpenses, self).approve_expense()

    @api.constrains('name', 'amount', 'branch_id', 'employee_id', 'date')
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
            area_id = models.execute_kw(db, uid, password, 'branch.expenses', 'search_read',
                                        [[['basic_synch_branch_expenses', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            branch_id = models.execute_kw(db, uid, password, 'branch.account', 'search_read',
                                          [[['account_name', '=', self.branch_id.account_name]]],
                                          {'fields': ['id']})
            if branch_id:
                branch_id = branch_id[0]['id']
            else:
                branch_id = False

            branch_id_ref = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                              [[['name', '=', self.branch_id_ref.name]]],
                                              {'fields': ['id']})
            if branch_id_ref:
                branch_id_ref = branch_id_ref[0]['id']
            else:
                branch_id_ref = False

            # employee_id=False
            # area_id = models.execute_kw(db, uid, password, 'hr.employee', 'search_read',
            #                             [[['basic_synch_hr_employee', '=', self.employee_id.id]]],
            #                             {'fields': ['name', 'id']})
            employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'search_read',
                                            [[['name', '=', self.employee_id.name]]],
                                            {'fields': ['id']})
            if employee_id:
                employee_id = employee_id[0]['id']
            else:
                employee_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'branch.expenses', 'create',
                                            [{
                                                'name': self.name,
                                                'amount': self.amount,
                                                'branch_id': branch_id,
                                                'branch_id_ref': branch_id_ref,
                                                'employee_id': employee_id,
                                                'date': self.date,
                                                'basic_synch_branch_expenses': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'branch.expenses', 'write', [[area_id[0]['id']],
                                                                                        {
                                                                                            'name': self.name,
                                                                                            'amount': self.amount,
                                                                                            'branch_id': branch_id,
                                                                                            'branch_id_ref': branch_id_ref,
                                                                                            'employee_id': employee_id,
                                                                                            'date': self.date,
                                                                                            # 'basic_synch_branch_expenses'
                                                                                        }])
            return


class ReciptForm(models.Model):
    _inherit = 'recipt.form'

    def take_loan(self):
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

            estimate = models.execute_kw(db, uid, password, 'recipt.form', 'search_read',
                                         [[['basic_synch_recipt_form', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'recipt.form', 'write', [[estimate[0]['id']],
                                                                                {
                                                                                    'basic_synch_recipt_form_button': True,
                                                                                }])
        return super(ReciptForm, self).take_loan()

    @api.constrains('partner_id', 'loan_amt', 'check_no', 'branch_id', 'partner_account_id', 'bank_account_id', 'date')
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
            area_id = models.execute_kw(db, uid, password, 'recipt.form', 'search_read',
                                        [[['basic_synch_recipt_form', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            branch_id = models.execute_kw(db, uid, password, 'branch.account', 'search_read',
                                          [[['name', '=', self.branch_id.name]]],
                                          {'fields': ['id']})
            if branch_id:
                branch_id = branch_id[0]['id']
            else:
                branch_id = False

            partner_id = models.execute_kw(db, uid, password, 'branch.loan.account', 'search_read',
                                           [[['name', '=', self.partner_id.name],
                                             ]],
                                           {'fields': ['name', 'id']})
            if partner_id:
                partner_id = partner_id[0]['id']
            else:
                partner_id = False
            partner_account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                   [[['name', '=', self.partner_account_id.name],
                                                     ['company_id', '=', self.partner_account_id.company_id.id],
                                                     ]],
                                                   {'fields': ['name', 'id', ]})
            if partner_account_id:
                partner_account_id = partner_account_id[0]['id']
            else:
                partner_account_id = False
            branch_account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                  [[['name', '=', self.branch_account_id.name],
                                                    ['company_id', '=', self.branch_account_id.company_id.id],
                                                    ]],
                                                  {'fields': ['name', 'id', ]})
            if branch_account_id:
                branch_account_id = branch_account_id[0]['id']
            else:
                branch_account_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'recipt.form', 'create',
                                            [{
                                                'loan_amt': self.loan_amt,
                                                'check_no': self.check_no,
                                                'partner_account_id': partner_account_id,
                                                'branch_account_id': branch_account_id,
                                                'branch_id': branch_id,
                                                'partner_id': partner_id,
                                                'date': self.date,
                                                'basic_synch_recipt_form': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'recipt.form', 'write', [[area_id[0]['id']],
                                                                                    {
                                                                                        'loan_amt': self.loan_amt,
                                                                                        'check_no': self.check_no,
                                                                                        'partner_account_id': partner_account_id,
                                                                                        'branch_account_id': branch_account_id,
                                                                                        'branch_id': branch_id,
                                                                                        'partner_id': partner_id,
                                                                                        'date': self.date,
                                                                                    }])
            return


class AdvanceInternalTransfer(models.Model):
    _inherit = 'advance.internal.transfer'

    def post_transfer(self):
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

            estimate = models.execute_kw(db, uid, password, 'advance.internal.transfer', 'search_read',
                                         [[['basic_synch_advance_inter', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'advance.internal.transfer', 'write', [[estimate[0]['id']],
                                                                                              {
                                                                                                  'basic_synch_advance_inter_button': True,
                                                                                              }])
        return super(AdvanceInternalTransfer, self).post_transfer()

    @api.constrains('name', 'branch_id', 'journal_id', 'amount', 'date')
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
            area_id = models.execute_kw(db, uid, password, 'advance.internal.transfer', 'search_read',
                                        [[['basic_synch_advance_inter', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            branch_id = models.execute_kw(db, uid, password, 'branch.account', 'search_read',
                                          [[['account_name', '=', self.branch_id.account_name]]],
                                          {'fields': ['id']})
            if branch_id:
                branch_id = branch_id[0]['id']
            else:
                branch_id = False
            journal_id = models.execute_kw(db, uid, password, 'advance.internal.transfer', 'search_read',
                                           [[['name', '=', self.journal_id.name],
                                             ['company_id', '=', self.journal_id.company_id.id]]],
                                           {'fields': ['id']})
            if journal_id:
                journal_id = journal_id[0]['id']
            else:
                journal_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'advance.internal.transfer', 'create',
                                            [{
                                                'name': self.name,
                                                'branch_id': branch_id,
                                                'journal_id': journal_id,
                                                'amount': self.amount,
                                                'date': self.date,
                                                'basic_synch_advance_inter': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'advance.internal.transfer', 'write', [[area_id[0]['id']],
                                                                                                  {
                                                                                                      'name': self.name,
                                                                                                      'branch_id': branch_id,
                                                                                                      'journal_id': journal_id,
                                                                                                      'amount': self.amount,
                                                                                                      'date': self.date,
                                                                                                      'basic_synch_advance_inter': str(
                                                                                                          self.id)
                                                                                                  }])
            return


class SecondAdvance(models.Model):
    _inherit = 'second.advance'

    def pay_advance(self):
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

            estimate = models.execute_kw(db, uid, password, 'second.advance', 'search_read',
                                         [[['basic_synch_second_advance', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'second.advance', 'write', [[estimate[0]['id']],
                                                                                   {
                                                                                       'basic_synch_second_advance_button': True,
                                                                                   }])
        return super(SecondAdvance, self).pay_advance()

    @api.constrains('name', 'amount', 'branch_id', 'vehicle_req', 'vehicle_id', 'driver', 'date')
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
            area_id = models.execute_kw(db, uid, password, 'second.advance', 'search_read',
                                        [[['basic_synch_second_advance', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            branch_id = models.execute_kw(db, uid, password, 'branch.account', 'search_read',
                                          [[['account_name', '=', self.branch_id.account_name]]],
                                          {'fields': ['id']})
            if branch_id:
                branch_id = branch_id[0]['id']
            else:
                branch_id = False

            branch_id_ref = models.execute_kw(db, uid, password, 'company.branches', 'search_read',
                                              [[['name', '=', self.branch_id_ref.name]]],
                                              {'fields': ['id']})
            if branch_id_ref:
                branch_id_ref = branch_id_ref[0]['id']
            else:
                branch_id_ref = False
            vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                            [[['basic_synch_v_req', '=', self.vehicle_req.id]]],
                                            {'fields': ['name', 'id']})
            if vehicle_req:
                vehicle_req = vehicle_req[0]['id']
            else:
                vehicle_req = False
            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            driver_code = models.execute_kw(db, uid, password, 'driver.code', 'search_read',
                                            [[['code', '=', self.driver.code]]],
                                            {'fields': ['driver', 'id']})
            if driver_code:
                driver_code = driver_code[0]['id']
            else:
                driver_code = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'second.advance', 'create',
                                            [{
                                                'name': self.name,
                                                'amount': self.amount,
                                                'branch_id': branch_id,
                                                'branch_id_ref': branch_id_ref,
                                                'vehicle_req': vehicle_req,
                                                'vehicle_id': vehicle_ser,
                                                'driver': driver_code,
                                                'date': self.date,
                                                'basic_synch_second_advance': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'second.advance', 'write', [[area_id[0]['id']],
                                                                                       {
                                                                                           'name': self.name,
                                                                                           'amount': self.amount,
                                                                                           'branch_id': branch_id,
                                                                                           'branch_id_ref': branch_id_ref,
                                                                                           'vehicle_req': vehicle_req,
                                                                                           'vehicle_id': vehicle_ser,
                                                                                           'driver': driver_code,
                                                                                           'date': self.date,
                                                                                           # 'basic_synch_branch_expenses'
                                                                                       }])
            return


class BranchLoan(models.Model):
    _inherit = 'branch.loan'

    syn_amount = fields.Float(string="syn Amount")
    syn_wizard = fields.Boolean(string="syn Amount")

    def take_loan(self):
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

            estimate = models.execute_kw(db, uid, password, 'branch.loan', 'search_read',
                                         [[['basic_synch_branch_loan', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'branch.loan', 'write', [[estimate[0]['id']],
                                                                                {
                                                                                    'basic_synch_branch_loan_button': True,
                                                                                }])
        return super(BranchLoan, self).take_loan()

    @api.constrains('partner_id', 'loan_amt', 'check_no', 'branch_id', 'partner_account_id', 'bank_account_id', 'date')
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
            area_id = models.execute_kw(db, uid, password, 'branch.loan', 'search_read',
                                        [[['basic_synch_branch_loan', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            branch_id = models.execute_kw(db, uid, password, 'branch.account', 'search_read',
                                          [[['name', '=', self.branch_id.name]]],
                                          {'fields': ['id']})
            if branch_id:
                branch_id = branch_id[0]['id']
            else:
                branch_id = False

            partner_id = models.execute_kw(db, uid, password, 'branch.loan.account', 'search_read',
                                           [[['name', '=', self.partner_id.name],
                                             ]],
                                           {'fields': ['name', 'id']})
            if partner_id:
                partner_id = partner_id[0]['id']
            else:
                partner_id = False
            partner_account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                   [[['name', '=', self.partner_account_id.name],
                                                     ['company_id', '=', self.partner_account_id.company_id.id],
                                                     ]],
                                                   {'fields': ['name', 'id', ]})
            if partner_account_id:
                partner_account_id = partner_account_id[0]['id']
            else:
                partner_account_id = False
            branch_account_id = models.execute_kw(db, uid, password, 'account.account', 'search_read',
                                                  [[['name', '=', self.branch_account_id.name],
                                                    ['company_id', '=', self.branch_account_id.company_id.id],
                                                    ]],
                                                  {'fields': ['name', 'id', ]})
            if branch_account_id:
                branch_account_id = branch_account_id[0]['id']
            else:
                branch_account_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'branch.loan', 'create',
                                            [{
                                                'loan_amt': self.loan_amt,
                                                'check_no': self.check_no,
                                                'partner_account_id': partner_account_id,
                                                'branch_account_id': branch_account_id,
                                                'branch_id': branch_id,
                                                'partner_id': partner_id,
                                                'paid_amt': self.paid_amt,
                                                'pending_amt': self.pending_amt,
                                                'date': self.date,
                                                'basic_synch_branch_loan': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'branch.loan', 'write', [[area_id[0]['id']],
                                                                                    {
                                                                                        'loan_amt': self.loan_amt,
                                                                                        'check_no': self.check_no,
                                                                                        'partner_account_id': partner_account_id,
                                                                                        'branch_account_id': branch_account_id,
                                                                                        'branch_id': branch_id,
                                                                                        'partner_id': partner_id,
                                                                                        'date': self.date,
                                                                                        'paid_amt': self.paid_amt,
                                                                                        'pending_amt': self.pending_amt,
                                                                                    }])
            return


class PayLoanWizard(models.Model):
    _inherit = 'pay.loan.wizard'

    def pay_amt(self):
        rec = super(PayLoanWizard, self).pay_amt()
        if self:
            self.loan_id.syn_amount = self.amount
            self.loan_id.syn_wizard = True
            self.loan_id.basic_synch_pay_loan_button = True

    # @api.constrains('date', 'amount','loan_id')
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
    #         area_id = models.execute_kw(db, uid, password, 'pay.loan.wizard', 'search_read',
    #                                     [[['loan_id', '=', self.loan_id.id]]],
    #                                     {'fields': ['name', 'id']})
    #
    #
    #         estimate = models.execute_kw(db, uid, password, 'branch.loan', 'search_read',
    #                                      [[['basic_synch_branch_loan', '=', self.loan_id.id]]])
    #
    #         if estimate:
    #             estimate = estimate[0]['id']
    #         else:
    #             estimate =False
    #         if not area_id:
    #             partner = models.execute_kw(db, uid, password, 'pay.loan.wizard', 'create',
    #                                         [{
    #                                             'loan_id': estimate,
    #                                             'date': self.date,
    #                                             'amount': self.amount,
    #                                             # 'basic_synch_branch_loan': str(self.id)
    #
    #                                         }]
    #                                         )
    #         else:
    #             upd = models.execute_kw(db, uid, password, 'pay.loan.wizard', 'write', [[area_id[0]['id']],
    #                                                                                         {
    #                                                                                             'loan_id': estimate,
    #                                                                                             'date': self.date,
    #                                                                                             'amount': self.amount,
    #                                                                                         }])
    #         return


class AdvanceApproval(models.Model):
    _inherit = 'advance.approval'

    def approve(self):
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

            estimate = models.execute_kw(db, uid, password, 'advance.approval', 'search_read',
                                         [[['basic_synch_advance_approval', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'advance.approval', 'write', [[estimate[0]['id']],
                                                                                     {
                                                                                         'basic_synch_advance_approval_button': True,
                                                                                     }])
        return super(AdvanceApproval, self).approve()

    def reject(self):
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

            estimate = models.execute_kw(db, uid, password, 'advance.approval', 'search_read',
                                         [[['basic_synch_advance_approval', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'advance.approval', 'write', [[estimate[0]['id']],
                                                                                     {
                                                                                         'basic_synch_advance_reject_button': True,
                                                                                     }])
        return super(AdvanceApproval, self).reject()

    @api.constrains('vehicle_req', 'vehicle_id', 'amount', 'branch_id', 'owner', 'driver_id', 'date', 'phone_no')
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
            area_id = models.execute_kw(db, uid, password, 'advance.approval', 'search_read',
                                        [[['basic_synch_advance_approval', '=', self.id]]],
                                        {'fields': ['name', 'id']})

            branch_id = models.execute_kw(db, uid, password, 'branch.account', 'search_read',
                                          [[['name', '=', self.branch_id.name]]],
                                          {'fields': ['id']})
            if branch_id:
                branch_id = branch_id[0]['id']
            else:
                branch_id = False
            vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                            [[['basic_synch_v_req', '=', self.vehicle_req.id]]],
                                            {'fields': ['name', 'id']})
            if vehicle_req:
                vehicle_req = vehicle_req[0]['id']
            else:
                vehicle_req = False
            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False

            driver_code = models.execute_kw(db, uid, password, 'driver.code', 'search_read',
                                            [[['code', '=', self.driver_id.code]]],
                                            {'fields': ['driver', 'id']})
            if driver_code:
                driver_code = driver_code[0]['id']
            else:
                driver_code = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'advance.approval', 'create',
                                            [{
                                                'vehicle_req': vehicle_req,
                                                'branch_id': branch_id,
                                                'vehicle_id': vehicle_ser,
                                                'amount': self.amount,
                                                'owner': self.owner,
                                                'date': self.date,
                                                'driver_id': driver_code,
                                                'phone_no': self.phone_no,
                                                'basic_synch_advance_approval': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'advance.approval', 'write', [[area_id[0]['id']],
                                                                                         {
                                                                                             'vehicle_req': vehicle_req,
                                                                                             'branch_id': branch_id,
                                                                                             'vehicle_id': vehicle_ser,
                                                                                             'amount': self.amount,
                                                                                             'owner': self.owner,
                                                                                             'date': self.date,
                                                                                             'driver_id': driver_code,
                                                                                             'phone_no': self.phone_no,

                                                                                             # 'basic_synch_branch_loan': str(self.id)
                                                                                         }])
            return


class FreightTemplate(models.Model):
    _inherit = "freight.template"

    def create_freightbill(self):
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

            estimate = models.execute_kw(db, uid, password, 'freight.template', 'search_read',
                                         [[['basic_synch_freight_tmp', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'freight.template', 'write', [[estimate[0]['id']],
                                                                                     {
                                                                                         'basic_synch_freight_tmp_button': True,
                                                                                     }])
        return super(FreightTemplate, self).create_freightbill()

    def approve_freightbill(self):
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

            estimate = models.execute_kw(db, uid, password, 'freight.template', 'search_read',
                                         [[['basic_synch_freight_tmp', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'freight.template', 'write', [[estimate[0]['id']],
                                                                                     {
                                                                                         'basic_synch_freight_approve_button': True,
                                                                                     }])
        return super(FreightTemplate, self).approve_freightbill()

    @api.constrains('name', 'partner_id', 'payment_date', 'submission_date', 'filter_by', 'partner_invoices',
                    'bank_name', 'account_number', 'tax_ids', 'deduction_lines')
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
            area_id = models.execute_kw(db, uid, password, 'freight.template', 'search_read',
                                        [[['basic_synch_freight_tmp', '=', self.id]]],
                                        {'fields': ['name', 'id']})
            estimate_ids = []
            deduction_lines = []
            for line in self.partner_invoices:
                vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                                [[['basic_synch_v_req', '=', line.vehicle_req.id]]],
                                                {'fields': ['name', 'id']})
                if vehicle_req:
                    vehicle_req = vehicle_req[0]['id']
                else:
                    vehicle_req = False
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

                product_main = (0, 0, {
                    'vehicle_req': vehicle_req,
                    'location': line.location,
                    'destination': line.destination,
                    'from_date': line.from_date,
                    'to_date': line.to_date,
                    'bill_no': line.bill_no,
                    'bill_date': line.bill_date,
                    'product_id': product_server,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': product_uom,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                })
                estimate_ids.append(product_main)
            for de_lines in self.deduction_lines:
                product_main = (0, 0, {
                    'description': de_lines.description,
                    'amount': de_lines.amount,
                })
                deduction_lines.append(product_main)
            partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                           [[['basic_synch_partner', '=', self.partner_id.id],
                                             ]],
                                           {'fields': ['name', 'id']})
            if partner_id:
                partner_id = partner_id[0]['id']
            else:
                partner_id = False
            company_name = models.execute_kw(db, uid, password, 'res.company', 'search_read',
                                             [[['name', '=', self.company_name.name]]],
                                             {'fields': ['name', 'id']})
            if company_name:
                company_name = company_name[0]['id']
            else:
                company_name = False

            tax_ids = models.execute_kw(db, uid, password, 'account.tax', 'search_read',
                                        [[['name', '=', self.tax_ids.name]]],
                                        {'fields': ['name', 'id']})
            if tax_ids:
                tax_ids = tax_ids[0]['id']
            else:
                tax_ids = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'freight.template', 'create',
                                            [{
                                                'name': self.name,
                                                'partner_id': partner_id,
                                                'company_name': company_name,
                                                'submission_date': self.submission_date,
                                                'payment_date': self.payment_date,
                                                'from_date': self.from_date,
                                                'to_date': self.to_date,
                                                'filter_by': self.filter_by,
                                                'partner_invoices': estimate_ids,
                                                'deduction_lines': deduction_lines,
                                                'bank_name': self.bank_name,
                                                'account_number': self.account_number,
                                                'tax_ids': tax_ids,
                                                'amount_untaxed': self.amount_untaxed,
                                                'amount_tax': self.amount_tax,
                                                'amount_total': self.amount_total,
                                                'deduction_total': self.deduction_total,
                                                'amount_complete_total': self.amount_complete_total,
                                                'basic_synch_freight_tmp': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'freight.template', 'write', [[area_id[0]['id']],
                                                                                         {
                                                                                             'name': self.name,
                                                                                             'partner_id': partner_id,
                                                                                             'company_name': company_name,
                                                                                             'submission_date': self.submission_date,
                                                                                             'payment_date': self.payment_date,
                                                                                             'from_date': self.from_date,
                                                                                             'to_date': self.to_date,
                                                                                             'filter_by': self.filter_by,
                                                                                             'partner_invoices': estimate_ids,
                                                                                             'deduction_lines': deduction_lines,
                                                                                             'bank_name': self.bank_name,
                                                                                             'account_number': self.account_number,
                                                                                             'tax_ids': tax_ids,
                                                                                             'amount_untaxed': self.amount_untaxed,
                                                                                             'amount_tax': self.amount_tax,
                                                                                             'amount_total': self.amount_total,
                                                                                             'deduction_total': self.deduction_total,
                                                                                             'amount_complete_total': self.amount_complete_total,

                                                                                             # 'basic_synch_branch_loan': str(self.id)
                                                                                         }])
            return


class FuelPaymentForm(models.Model):
    _inherit = 'fuel.payment.form'

    def generate_bill(self):
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

            estimate = models.execute_kw(db, uid, password, 'fuel.payment.form', 'search_read',
                                         [[['basic_synch_fuel_payment', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'fuel.payment.form', 'write', [[estimate[0]['id']],
                                                                                      {
                                                                                          'basic_synch_fuel_payment_button': True,
                                                                                      }])
        return super(FuelPaymentForm, self).generate_bill()

    def pay_bill(self):
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

            estimate = models.execute_kw(db, uid, password, 'fuel.payment.form', 'search_read',
                                         [[['basic_synch_fuel_payment', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'fuel.payment.form', 'write', [[estimate[0]['id']],
                                                                                      {
                                                                                          'basic_synch_fuel_pay_bill_button': True,
                                                                                      }])
        return super(FuelPaymentForm, self).pay_bill()

    def cancel_bill(self):
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

            estimate = models.execute_kw(db, uid, password, 'fuel.payment.form', 'search_read',
                                         [[['basic_synch_fuel_payment', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'fuel.payment.form', 'write', [[estimate[0]['id']],
                                                                                      {
                                                                                          'basic_synch_fuel_cancel_bill_button': True,
                                                                                      }])
        return super(FuelPaymentForm, self).cancel_bill()

    @api.constrains('date', 'from_date', 'to_date', 'filter_by', 'fuel_lines')
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
            area_id = models.execute_kw(db, uid, password, 'fuel.payment.form', 'search_read',
                                        [[['basic_synch_fuel_payment', '=', self.id]]],
                                        {'fields': ['name', 'id']})
            estimate_ids = []
            deduction_lines = []
            for line in self.fuel_lines:
                vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                                [[['license_plate', '=', line.vehicle_id.license_plate]]],
                                                {'fields': ['name', 'id']})
                if vehicle_ser:
                    vehicle_ser = vehicle_ser[0]['id']
                else:
                    vehicle_ser = False

                bunk_id = models.execute_kw(db, uid, password, 'petrol.pumb', 'search_read',
                                            [[['name', '=', line.bunk_id.name]]],
                                            {'fields': ['name', 'id']})
                if bunk_id:
                    bunk_id = bunk_id[0]['id']
                else:
                    bunk_id = False
                product_main = (0, 0, {
                    'vehicle_id': vehicle_ser,
                    'date': line.date,
                    'ind_no': line.ind_no,
                    'bunk_id': bunk_id,
                    'fuel_rate': line.fuel_rate,
                    'fuel_quantity': line.fuel_quantity,
                    'amount': line.amount,
                })
                estimate_ids.append(product_main)

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'fuel.payment.form', 'create',
                                            [{
                                                'date': self.date,
                                                'from_date': self.from_date,
                                                'to_date': self.to_date,
                                                'filter_by': self.filter_by,
                                                'fuel_lines': estimate_ids,
                                                'basic_synch_fuel_payment': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'fuel.payment.form', 'write', [[area_id[0]['id']],
                                                                                          {
                                                                                              'date': self.date,
                                                                                              'from_date': self.from_date,
                                                                                              'to_date': self.to_date,
                                                                                              'filter_by': self.filter_by,
                                                                                              'fuel_lines': estimate_ids,
                                                                                              'basic_synch_fuel_payment': str(
                                                                                                  self.id)
                                                                                              # 'basic_synch_branch_loan': str(self.id)
                                                                                          }])
            return


class RtgsPaymentForm(models.Model):
    _inherit = 'rtgs.payment.form'

    def approve_rtgs(self):
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

            estimate = models.execute_kw(db, uid, password, 'rtgs.payment.form', 'search_read',
                                         [[['basic_synch_rtgs_payment', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'rtgs.payment.form', 'write', [[estimate[0]['id']],
                                                                                      {
                                                                                          'basic_synch_rtgs_payment_app_button': True,
                                                                                      }])
        return super(RtgsPaymentForm, self).approve_rtgs()

    def paid_rtgs(self):
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

            estimate = models.execute_kw(db, uid, password, 'rtgs.payment.form', 'search_read',
                                         [[['basic_synch_rtgs_payment', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'rtgs.payment.form', 'write', [[estimate[0]['id']],
                                                                                      {
                                                                                          'basic_synch_rtgs_payment_paid_button': True,
                                                                                      }])
        return super(RtgsPaymentForm, self).paid_rtgs()

    def create_rtgs(self):
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

            estimate = models.execute_kw(db, uid, password, 'rtgs.payment.form', 'search_read',
                                         [[['basic_synch_rtgs_payment', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'rtgs.payment.form', 'write', [[estimate[0]['id']],
                                                                                      {
                                                                                          'basic_synch_rtgs_payment_button': True,
                                                                                      }])
        return super(RtgsPaymentForm, self).create_rtgs()

    @api.constrains('referance', 'form_date', 'to_date', 'rtgs_lines')
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
            area_id = models.execute_kw(db, uid, password, 'rtgs.payment.form', 'search_read',
                                        [[['basic_synch_rtgs_payment', '=', self.id]]],
                                        {'fields': ['name', 'id']})
            estimate_ids = []
            deduction_lines = []
            for line in self.rtgs_lines:
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                               [[['basic_synch_partner', '=', line.account_holder.id],
                                                 ]],
                                               {'fields': ['name', 'id', 'mobile']})
                if partner_id:
                    partner_id = partner_id[0]['id']
                else:
                    partner_id = False

                trip_id = models.execute_kw(db, uid, password, 'trip.sheet', 'search_read',
                                            [[['id', '=', line.trip_id.id]]],
                                            {'fields': ['name', 'id']})
                if trip_id:
                    trip_id = trip_id[0]['id']
                else:
                    trip_id = False
                vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                                [[['basic_synch_v_req', '=', line.vehicle_req.id]]],
                                                {'fields': ['name', 'id']})
                if vehicle_req:
                    vehicle_req = vehicle_req[0]['id']
                else:
                    vehicle_req = False
                product_main = (0, 0, {
                    'account_holder': partner_id,
                    'account_number': line.account_number,
                    'bank_name': line.bank_name,
                    'bank_branch': line.bank_branch,
                    'ifsc_code': line.ifsc_code,
                    'trip_id': trip_id,
                    'vehicle_req': vehicle_req,
                    'select': line.select,
                })
                estimate_ids.append(product_main)

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'rtgs.payment.form', 'create',
                                            [{
                                                'form_date': self.form_date,
                                                'to_date': self.to_date,
                                                'referance': self.referance,
                                                'rtgs_lines': estimate_ids,
                                                'basic_synch_rtgs_payment': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'rtgs.payment.form', 'write', [[area_id[0]['id']],
                                                                                          {
                                                                                              'form_date': self.form_date,
                                                                                              'to_date': self.to_date,
                                                                                              'referance': self.referance,
                                                                                              'rtgs_lines': estimate_ids,
                                                                                              'basic_synch_rtgs_payment': str(
                                                                                                  self.id)

                                                                                              # 'basic_synch_branch_loan': str(self.id)
                                                                                          }])
            return


class BettaForm(models.Model):
    _inherit = 'betta.form'

    def payment(self):
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

            estimate = models.execute_kw(db, uid, password, 'betta.form', 'search_read',
                                         [[['basic_synch_betta_form', '=', self.id]]])

            upd = models.execute_kw(db, uid, password, 'betta.form', 'write', [[estimate[0]['id']],
                                                                               {
                                                                                   'basic_synch_betta_form_button': True,
                                                                               }])
        return super(BettaForm, self).payment()

    @api.constrains('driver_code', 'paid_date', 'betta_lines')
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
            area_id = models.execute_kw(db, uid, password, 'betta.form', 'search_read',
                                        [[['basic_synch_betta_form', '=', self.id]]],
                                        {'fields': ['name', 'id']})
            estimate_ids = []
            driver_code = models.execute_kw(db, uid, password, 'driver.code', 'search_read',
                                            [[['code', '=', self.driver_code.code]]],
                                            {'fields': ['driver', 'id']})
            if driver_code:
                driver_code = driver_code[0]['id']
            else:
                driver_code = False
            for line in self.betta_lines:
                driver_code = models.execute_kw(db, uid, password, 'driver.code', 'search_read',
                                                [[['code', '=', line.driver_code.code]]],
                                                {'fields': ['driver', 'id']})
                if driver_code:
                    driver_code = driver_code[0]['id']
                else:
                    driver_code = False

                vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                                [[['basic_synch_v_req', '=', line.vehicle_req.id]]],
                                                {'fields': ['name', 'id']})
                if vehicle_req:
                    vehicle_req = vehicle_req[0]['id']
                else:
                    vehicle_req = False
                product_main = (0, 0, {
                    'driver_code': driver_code,
                    'vehicle_req': vehicle_req,
                    'select': line.select,
                    'balance_amt': line.balance_amt,
                })
                estimate_ids.append(product_main)

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'betta.form', 'create',
                                            [{
                                                'driver_code': driver_code,
                                                'paid_date': self.paid_date,
                                                'betta_lines': estimate_ids,
                                                'basic_synch_betta_form': str(self.id)

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'betta.form', 'write', [[area_id[0]['id']],
                                                                                   {
                                                                                       'driver_code': driver_code,
                                                                                       'paid_date': self.paid_date,
                                                                                       'betta_lines': estimate_ids,
                                                                                       # 'basic_synch_branch_loan': str(self.id)
                                                                                   }])
            return


class AllocatedVehicles(models.Model):
    _inherit = 'allocated.vehicle.lines'

    # @api.constrains('driver')
    # def constraints_driver(self):
    #     import xmlrpc.client
    #     synch = self.env['synch.configuration'].search([('activate', '=', True)])
    #     if synch:
    #         url = synch.server
    #         db = synch.db
    #         username = synch.username
    #         password = synch.password
    #         common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    #         uid = common.authenticate(db, username, password, {})
    #         models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    #         req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])
    #
    #         re_estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
    #                                         [[['basic_synch_v_req', '=', req.id]]])
    #         if re_estimate:
    #             re_estimate = re_estimate[0]['id']
    #         else:
    #             re_estimate = False
    #
    #         vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
    #                                         [[['license_plate', '=', self.vehicle_id.license_plate]]],
    #                                         {'fields': ['name', 'id']})
    #         if vehicle_ser:
    #             vehicle_ser = vehicle_ser[0]['id']
    #         else:
    #             vehicle_ser = False
    #         estimate = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'search_read',
    #                                      [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])
    #
    #         driver_code = models.execute_kw(db, uid, password, 'driver.code', 'search_read',
    #                                         [[['code', '=', self.driver.code]]],
    #                                         {'fields': ['driver', 'id']})
    #         if driver_code:
    #             driver_code = driver_code[0]['id']
    #         else:
    #             driver_code = False
    #
    #         upd = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'write', [[estimate[0]['id']],
    #                                                                                         {
    #                                                                                             'driver':driver_code,
    #                                                                                         }])

    @api.constrains('select')
    def constraints_select(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])

            re_estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                            [[['basic_synch_v_req', '=', req.id]]])
            if re_estimate:
                re_estimate = re_estimate[0]['id']
            else:
                re_estimate = False

            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            estimate = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'search_read',
                                         [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])

            if estimate:
                upd = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'write', [[estimate[0]['id']],
                                                                                                {
                                                                                                    'select': self.select,
                                                                                                }])

    @api.constrains('curreny_capacity')
    def constraints_curreny(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])

            re_estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                            [[['basic_synch_v_req', '=', req.id]]])
            if re_estimate:
                re_estimate = re_estimate[0]['id']
            else:
                re_estimate = False

            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            estimate = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'search_read',
                                         [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])

            if estimate:
                upd = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'write', [[estimate[0]['id']],
                                                                                                {
                                                                                                    'curreny_capacity': self.curreny_capacity,
                                                                                                }])

    @api.constrains('freight')
    def constraints_freight(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])

            re_estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                            [[['basic_synch_v_req', '=', req.id]]])
            if re_estimate:
                re_estimate = re_estimate[0]['id']
            else:
                re_estimate = False

            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id[0].license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            estimate = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'search_read',
                                         [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])

            if estimate:
                upd = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'write', [[estimate[0]['id']],
                                                                                                {
                                                                                                    'freight': self.freight,
                                                                                                }])

    @api.constrains('petrol_bunk')
    def constraints_petrol_bunk(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])

            re_estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                            [[['basic_synch_v_req', '=', req.id]]])
            if re_estimate:
                re_estimate = re_estimate[0]['id']
            else:
                re_estimate = False

            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            petrol_bunk = models.execute_kw(db, uid, password, 'petrol.pumb', 'search_read',
                                            [[['name', '=', self.petrol_bunk.name]]],
                                            {'fields': ['name', 'id']})
            if petrol_bunk:
                petrol_bunk = petrol_bunk[0]['id']
            else:
                petrol_bunk = False

            estimate = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'search_read',
                                         [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])

            if estimate:
                upd = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'write', [[estimate[0]['id']],
                                                                                                {
                                                                                                    'petrol_bunk': petrol_bunk,
                                                                                                }])

    @api.constrains('fuel_qty')
    def constraints_fuel_qty(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])

            re_estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                            [[['basic_synch_v_req', '=', req.id]]])
            if re_estimate:
                re_estimate = re_estimate[0]['id']
            else:
                re_estimate = False

            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            estimate = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'search_read',
                                         [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])

            if estimate:
                upd = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'write', [[estimate[0]['id']],
                                                                                                {
                                                                                                    'fuel_qty': self.fuel_qty,
                                                                                                }])

    @api.constrains('petrol_price')
    def constraints_petrol_price(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])

            re_estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                            [[['basic_synch_v_req', '=', req.id]]])
            if re_estimate:
                re_estimate = re_estimate[0]['id']
            else:
                re_estimate = False

            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            estimate = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'search_read',
                                         [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])

            if estimate:
                upd = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'write', [[estimate[0]['id']],
                                                                                                {
                                                                                                    'petrol_price': self.petrol_price,
                                                                                                }])

    @api.constrains('ind_no')
    def constraints_ind_no(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])

            re_estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                            [[['basic_synch_v_req', '=', req.id]]])
            if re_estimate:
                re_estimate = re_estimate[0]['id']
            else:
                re_estimate = False

            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            estimate = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'search_read',
                                         [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])

            if estimate:
                upd = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'write', [[estimate[0]['id']],
                                                                                                {
                                                                                                    'ind_no': self.ind_no,
                                                                                                }])

    @api.constrains('advance_amount')
    def constraints_advance_amount(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])

            re_estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                            [[['basic_synch_v_req', '=', req.id]]])
            if re_estimate:
                re_estimate = re_estimate[0]['id']
            else:
                re_estimate = False

            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            estimate = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'search_read',
                                         [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])

            if estimate:
                upd = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'write', [[estimate[0]['id']],
                                                                                                {
                                                                                                    'advance_amount': self.advance_amount,
                                                                                                }])

    @api.constrains('capacity')
    def constraints_capacity(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])

            re_estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                            [[['basic_synch_v_req', '=', req.id]]])
            if re_estimate:
                re_estimate = re_estimate[0]['id']
            else:
                re_estimate = False

            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id[0].license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            estimate = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'search_read',
                                         [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])

            if estimate:
                upd = models.execute_kw(db, uid, password, 'allocated.vehicle.lines', 'write', [[estimate[0]['id']],
                                                                                                {
                                                                                                    'capacity': self.capacity,
                                                                                                }])


class DetailsInvoiceFreight(models.Model):
    _inherit = 'details.invoice.freight'

    @api.constrains('petrol_bunk')
    def constraints_petrol_bunk(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])

            re_estimate = models.execute_kw(db, uid, password, 'details.invoice.freight', 'search_read',
                                            [[['basic_synch_v_req', '=', req.id]]])
            if re_estimate:
                re_estimate = re_estimate[0]['id']
            else:
                re_estimate = False

            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            petrol_bunk = models.execute_kw(db, uid, password, 'petrol.pumb', 'search_read',
                                            [[['name', '=', self.petrol_bunk.name]]],
                                            {'fields': ['name', 'id']})
            if petrol_bunk:
                petrol_bunk = petrol_bunk[0]['id']
            else:
                petrol_bunk = False

            estimate = models.execute_kw(db, uid, password, 'details.invoice.freight', 'search_read',
                                         [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])

            if estimate:
                upd = models.execute_kw(db, uid, password, 'details.invoice.freight', 'write', [[estimate[0]['id']],
                                                                                                {
                                                                                                    'petrol_bunk': petrol_bunk,
                                                                                                }])
    # @api.constrains('owner')
    # def constraints_owner(self):
    #     import xmlrpc.client
    #     synch = self.env['synch.configuration'].search([('activate', '=', True)])
    #     if synch:
    #         url = synch.server
    #         db = synch.db
    #         username = synch.username
    #         password = synch.password
    #         common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    #         uid = common.authenticate(db, username, password, {})
    #         models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    #         req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])
    #
    #         re_estimate = models.execute_kw(db, uid, password, 'details.invoice.freight', 'search_read',
    #                                         [[['basic_synch_v_req', '=', req.id]]])
    #         if re_estimate:
    #             re_estimate = re_estimate[0]['id']
    #         else:
    #             re_estimate = False
    #
    #         vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
    #                                         [[['license_plate', '=', self.vehicle_id.license_plate]]],
    #                                         {'fields': ['name', 'id']})
    #         if vehicle_ser:
    #             vehicle_ser = vehicle_ser[0]['id']
    #         else:
    #             vehicle_ser = False
    #
    #         estimate = models.execute_kw(db, uid, password, 'details.invoice.freight', 'search_read',
    #                                      [[['vehicle_id', '=', vehicle_ser], ['vehicle_req', '=', re_estimate]]])
    #
    #         if estimate:
    #             upd = models.execute_kw(db, uid, password, 'details.invoice.freight', 'write', [[estimate[0]['id']],
    #                                                                                             {
    #                                                                                                 'petrol_bunk': petrol_bunk,
    #                                                                                             }])


class OrderLinesOutPass(models.Model):
    _inherit = 'order.lines.out.pass'

    @api.constrains('vehicle_id')
    def constraints_vehicle_id(self):
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
            req = self.env['vehicle.request'].search([('name', '=', self.vehicle_req.name)])

            re_estimate = models.execute_kw(db, uid, password, 'vehicle.requset.approval', 'search_read',
                                            [[['basic_synch_v_req', '=', req.id]]])
            if re_estimate:
                re_estimate = re_estimate[0]['id']
            else:
                re_estimate = False

            vehicle_ser = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                            [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                            {'fields': ['name', 'id']})
            if vehicle_ser:
                vehicle_ser = vehicle_ser[0]['id']
            else:
                vehicle_ser = False
            estimate = models.execute_kw(db, uid, password, 'order.lines.out.pass', 'search_read',
                                         [[['vehicle_req', '=', re_estimate]]])

            if estimate:
                upd = models.execute_kw(db, uid, password, 'order.lines.out.pass', 'write', [[estimate[0]['id']],
                                                                                             {
                                                                                                 'vehicle_id': vehicle_ser
                                                                                             }])

class UpdateStatus(models.Model):
    _inherit = 'update.status'

    syn_update_amount = fields.Float(string="syn update Amount")
    syn_update_wizard = fields.Boolean(string="syn update Amount")
    vehicle_id_halt = fields.Many2one('fleet.vehicle')


    # def pay_amt(self):
    #     rec = super(UpdateStatus, self).pay_amt()
    #     if self:
    #         self.loan_id.syn_amount = self.amount
    #         self.loan_id.syn_wizard = True
    #         self.loan_id.basic_synch_pay_loan_button = True

    def change_current_status_all_reached(self):
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
            vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                            [[['basic_synch_v_req', '=', self.vehicle_req.id]]],
                                            {'fields': ['name', 'id']})
            if vehicle_req:
                vehicle_req = vehicle_req[0]['id']
            else:
                vehicle_req = False
            estimate = models.execute_kw(db, uid, password, 'update.status', 'search_read',
                                         [[['vehicle_req', '=', vehicle_req]]])

            upd = models.execute_kw(db, uid, password, 'update.status', 'write', [[estimate[0]['id']],
                                                                                  {
                                                                                      'basic_synch_update_status_button': True,
                                                                                  }])
        return super(UpdateStatus, self).change_current_status_all_reached()


class VehilcleHalt(models.TransientModel):
    _inherit = 'vehicle.halt'

    @api.constrains('vehicle_req','vehicle_id','location','reason')
    def constraints_vehicle_req(self):
        if self.vehicle_req:
            self.env['update.status'].search([('vehicle_req','=',self.vehicle_req)])
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
                vehicle_req = models.execute_kw(db, uid, password, 'vehicle.request', 'search_read',
                                                [[['basic_synch_v_req', '=', self.vehicle_req.id]]],
                                                {'fields': ['name', 'id']})
                if vehicle_req:
                    vehicle_req = vehicle_req[0]['id']
                else:
                    vehicle_req = False
                estimate = models.execute_kw(db, uid, password, 'update.status', 'search_read',
                                             [[['vehicle_req', '=', vehicle_req]]])


                vehicle_id_halt = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                                [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                                {'fields': ['name', 'id']})
                if vehicle_id_halt:
                    vehicle_id_halt = vehicle_id_halt[0]['id']
                else:
                    vehicle_id_halt = False

                upd = models.execute_kw(db, uid, password, 'update.status', 'write', [[estimate[0]['id']],
                                                                                      {
                                                                                          'basic_synch_update_sta_halt_button': True,
                                                                                          'vehicle_id_halt':vehicle_id_halt,
                                                                                          'location_halt':self.location,
                                                                                          'reason_halt':self.reason,
                                                                                          'vehicle_req':vehicle_req,
                                                                                      }])
