import requests

from odoo import http
from odoo.http import request
from datetime import datetime
from num2words import num2words
import urllib.parse as urlparse
from urllib.parse import parse_qs
from odoo import models,fields,api
class VehicleSimply(models.Model):
    _inherit = 'vehicle.simply'

    @api.constrains('name', 'fleet_model_brand', 'vehi_reg', 'company_id','type')
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
            area_id = models.execute_kw(db, uid, password, 'vehicle.simply', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})
            fleet_mode = models.execute_kw(db, uid, password, 'fleet.vehicle.model', 'search_read',
                                        [[['name', '=', self.fleet_mode.name]]],
                                        {'fields': ['name', 'id']})
            if fleet_mode:
                fleet_mode = fleet_mode[0]['id']
            else:
                fleet_mode =False

            fleet_mode_brand = models.execute_kw(db, uid, password, 'fleet.vehicle.model.brand', 'search_read',
                                           [[['name', '=', self.fleet_model_brand.name]]],
                                           {'fields': ['name', 'id']})


            if fleet_mode_brand:
                fleet_mode_brand = fleet_mode_brand[0]['id']
            else:
                fleet_mode_brand = False

            vehicle_id = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                                 [[['license_plate', '=', self.vehicle_id.license_plate]]],
                                                 {'fields': ['license_plate', 'id']})

            if vehicle_id:
                vehicle_id = vehicle_id[0]['id']
            else:
                vehicle_id = False

            if not area_id:
                partner = models.execute_kw(db, uid, password, 'vehicle.simply', 'create',
                                            [{
                                                'name': self.name,
                                                'vehi_reg': self.vehi_reg,
                                                'type': self.type,
                                                'fleet_model_brand': fleet_mode_brand,
                                                'fleet_mode': fleet_mode,
                                                'vehicle_id':vehicle_id,
                                                'company_id':self.company_id.id,

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'vehicle.simply', 'write', [[area_id[0]['id']],
                                                                                    {
                                                                                        'name': self.name,
                                                                                        'vehi_reg': self.vehi_reg,
                                                                                        'type': self.type,
                                                                                        'fleet_model_brand': fleet_mode_brand,
                                                                                        'fleet_mode': fleet_mode,
                                                                                        'vehicle_id': vehicle_id,
                                                                                        'company_id': self.company_id.id,

                                                                                    }])
            return


class PriceSetup(models.Model):
    _inherit = 'price.setup'



    @api.constrains('name','ton_internal','km_internal','company_id')
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
            area_id = models.execute_kw(db, uid, password, 'price.setup', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'price.setup', 'create',
                                            [{
                                                'name': self.name,
                                                'ton_internal': self.ton_internal,
                                                'km_internal': self.km_internal,
                                                'company_id': self.company_id.id,
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'price.setup', 'write', [[area_id[0]['id']],
                                                                                                  {
                                                                                                      'name': self.name,
                                                                                                      'ton_internal': self.ton_internal,
                                                                                                      'km_internal': self.km_internal,
                                                                                                      'company_id': self.company_id.id,                                                                                                  }])
            return


class FleetVehicleModelBrand(models.Model):
    _inherit = 'fleet.vehicle.model.brand'

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
            area_id = models.execute_kw(db, uid, password, 'fleet.vehicle.model.brand', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'fleet.vehicle.model.brand', 'create',
                                            [{
                                                'name': self.name,
                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'fleet.vehicle.model.brand', 'write', [[area_id[0]['id']],
                                                                                            {
                                                                                                'name': self.name,
                                                                                            }])
            return


class FleetVehicleModel(models.Model):
    _inherit = 'fleet.vehicle.model'

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
            area_id = models.execute_kw(db, uid, password, 'fleet.vehicle.model', 'search_read',
                                        [[['name', '=', self.name]]],
                                        {'fields': ['name', 'id']})
            brand_id = models.execute_kw(db, uid, password, 'fleet.vehicle.model.brand', 'search_read',
                                        [[['name', '=', self.brand_id.name]]],
                                        {'fields': ['name', 'id']})
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'fleet.vehicle.model', 'create',
                                            [{
                                                'name': self.name,
                                                'brand_id': brand_id[0]['id'],
                                                'vehicle_type':self.vehicle_type,


                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'fleet.vehicle.model', 'write', [[area_id[0]['id']],
                                                                                       {
                                                                                           'name': self.name,
                                                                                            'brand_id': brand_id[0]['id'],
                                                                                            'vehicle_type':self.vehicle_type,
                                                                                       }])
            return

class DriverCode(models.Model):
    _inherit = 'driver.code'

    @api.constrains('name', 'code','license_no','driver','phone_no','external')
    def constraint_code(self):
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
            area_id = models.execute_kw(db, uid, password, 'driver.code', 'search_read',
                                        [[['code', '=', self.code],['license_no', '=', self.license_no]]],
                                        {'fields': ['driver', 'id']})

            driver_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                     [[['basic_synch_partner', '=', self.driver.id]]],
                                                     {'fields': ['name', 'id']})
            if not area_id:
                partner = models.execute_kw(db, uid, password, 'driver.code', 'create',
                                            [{
                                                'code': self.code,
                                                'driver': driver_id[0]['id'] if driver_id else False,
                                                'license_no': self.license_no,
                                                'phone_no': self.phone_no,
                                                'external': self.external

                                            }]
                                            )
            else:
                upd = models.execute_kw(db, uid, password, 'driver.code', 'write', [[area_id[0]['id']],
                                                                                            {
                                                                                                 'code': self.code,
                                                                                                'driver': driver_id[0]['id'],
                                                                                                'license_no': self.license_no,
                                                                                                'phone_no': self.phone_no,
                                                                                                'external': self.external
                                                                                            }])
            return


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    def mark_vehicle(self):
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
                estimate = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                             [[['basic_synch_vehicle', '=', self.id]]])
                upd = models.execute_kw(db, uid, password, 'fleet.vehicle', 'write', [[estimate[0]['id']],
                                                                                      {
                                                                                          'basic_synch_vehicle_mark': True,
                                                                                      }])
            return super(FleetVehicle, self).mark_vehicle()


    @api.constrains('name','model_id','license_plate','company_type','vin_sn','driver','mobility_card','net_car_value'
                    'stearing_box'



                    )
    def constraint_partner(self):
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
                print('uid=', uid)
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

                partner_passenger_id = models.execute_kw(db, uid, password, 'fleet.vehicle', 'search_read',
                                                     [[['license_plate', '=', self.license_plate]]],
                                                     {'fields': ['license_plate', 'id', 'model_id']})
                v_model_id =  models.execute_kw(db, uid, password, 'fleet.vehicle.model', 'search_read',
                                        [[['name', '=', self.model_id.name]]],
                                        {'fields': ['name', 'id']})

                external = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                              [[['mtc_supplier', '=', True],
                                                ['name', '=', self.external_company.name]]],
                                              {'fields': ['name', 'id']})
                if external:
                    external = external[0]['id']
                else:
                    external =False

                driver_code = models.execute_kw(db, uid, password, 'driver.code', 'search_read',
                                            [[['code', '=', self.driver.code]]],
                                            {'fields': ['driver', 'id']})
                if driver_code:
                    driver_code = driver_code[0]['id']
                else:
                    driver_code = False
                future_driver_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                             [[['name', '=', self.future_driver_id.name]]],
                                             {'fields': ['name', 'id']})
                if future_driver_id:
                    future_driver_id = future_driver_id[0]['id']
                else:
                    future_driver_id = False
                account_holder = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                                                     [[['name', '=', self.account_holder.name]]],
                                                     {'fields': ['name', 'id']})
                if account_holder:
                    account_holder = account_holder[0]['id']
                else:
                    account_holder =False


                if not partner_passenger_id:
                    partner = models.execute_kw(db, uid, password, 'fleet.vehicle', 'create',
                                                  [{
                                                          'model_id':v_model_id[0]['id'],
                                                      'license_plate':self.license_plate,
                                                      'tag_ids':self.tag_ids.ids,
                                                      'company_type':self.company_type,
                                                      'external_company':external ,
                                                      'driver':driver_code,
                                                      'mobility_card':self.mobility_card or False,
                                                      'future_driver_id':future_driver_id,
                                                      'plan_to_change_car':self.plan_to_change_car or False,
                                                      'next_assignation_date':self.next_assignation_date,
                                                      'location':self.location or False,
                                                      'odometer':self.odometer or False,
                                                      'acquisition_date':self.acquisition_date,
                                                      'vin_sn':self.vin_sn or False,
                                                      'car_value':self.car_value or False,
                                                      'net_car_value':self.net_car_value or False,
                                                      'residual_value':self.residual_value,
                                                      'account_holder':account_holder  or False,
                                                      'account_number':self.account_number or False,
                                                      'bank_name':self.bank_name  or False,
                                                      'bank_branch':self.bank_branch  or False,
                                                      'ifsc_code':self.ifsc_code  or False,
                                                      'company_id':self.company_id.id,
                                                      'seats':self.seats or False,
                                                      'doors':self.doors or False,
                                                      'color':self.color or False,
                                                      'model_year':self.model_year or False,
                                                      'local':self.local or False,
                                                      'type':self.type.id if self.type else False,
                                                      'fuel_type':self.fuel_type.id if self.fuel_type else False,
                                                      'assigned_to':self.assigned_to or False,
                                                      'allocate':self.allocate or False,
                                                      'capacity':self.capacity or False,
                                                      'transmission':self.transmission or False,
                                                      'co2':self.co2 or False,
                                                      'horsepower':self.horsepower or False,
                                                      'horsepower_tax':self.horsepower_tax or False,
                                                      'power':self.power or False,
                                                      # 'basic_synch_vehicle':str(self.id),
                                                      'description':self.description or False,
                                                      'permit_id':self.permit_id.id if self.permit_id else False,
                                                      'insurance_last_renew':self.insurance_last_renew.id if self.insurance_last_renew else False,
                                                      'engine_oil_change':self.engine_oil_change.id if self.engine_oil_change else False,
                                                      'engine_oil_changed':self.engine_oil_changed or False,
                                                      'gear_box':self.gear_box or False,
                                                      'deferencial':self.deferencial or False,
                                                      'stearing_box':self.stearing_box or False,
                                                      # 'grease_change':self.grease_change or False,

                                                      }]
                                                  )
                    print(partner,'partner')
                else:
                    upd = models.execute_kw(db, uid, password, 'fleet.vehicle', 'write', [[partner_passenger_id[0]['id']],
                                                                                        {
                                                                                            'model_id': v_model_id[0][
                                                                                                'id'],
                                                                                            'license_plate': self.license_plate,
                                                                                            'tag_ids': self.tag_ids.ids,
                                                                                            'company_type': self.company_type,
                                                                                            'external_company': external,
                                                                                            'driver': driver_code,
                                                                                            'mobility_card': self.mobility_card or False,
                                                                                            'future_driver_id': future_driver_id,
                                                                                            'plan_to_change_car': self.plan_to_change_car or False,
                                                                                            'next_assignation_date': self.next_assignation_date,
                                                                                            'location': self.location or False,
                                                                                            'odometer': self.odometer or False,
                                                                                            'acquisition_date': self.acquisition_date,
                                                                                            'vin_sn': self.vin_sn or False,
                                                                                            'car_value': self.car_value or False,
                                                                                            'net_car_value': self.net_car_value or False,
                                                                                            'residual_value': self.residual_value,
                                                                                            'account_holder': account_holder or False,
                                                                                            'account_number': self.account_number or False,
                                                                                            'bank_name': self.bank_name or False,
                                                                                            'bank_branch': self.bank_branch or False,
                                                                                            'ifsc_code': self.ifsc_code or False,
                                                                                            'company_id': self.company_id.id,
                                                                                            'seats': self.seats or False,
                                                                                            'doors': self.doors or False,
                                                                                            'color': self.color or False,
                                                                                            'model_year': self.model_year or False,
                                                                                            'local': self.local or False,
                                                                                            'type': self.type.id if self.type else False,
                                                                                            'fuel_type': self.fuel_type.id if self.fuel_type else False,
                                                                                            'assigned_to': self.assigned_to or False,
                                                                                            'allocate': self.allocate or False,
                                                                                            'capacity': self.capacity or False,
                                                                                            'transmission': self.transmission or False,
                                                                                            'co2': self.co2 or False,
                                                                                            'horsepower': self.horsepower or False,
                                                                                            'horsepower_tax': self.horsepower_tax or False,
                                                                                            'power': self.power or False,
                                                                                            # 'basic_synch_vehicle': str(
                                                                                            #     self.id),
                                                                                            'description': self.description or False,
                                                                                            'permit_id': self.permit_id.id if self.permit_id else False,
                                                                                            'insurance_last_renew': self.insurance_last_renew.id if self.insurance_last_renew else False,
                                                                                            'engine_oil_change': self.engine_oil_change.id if self.engine_oil_change else False,
                                                                                            'engine_oil_changed': self.engine_oil_changed or False,
                                                                                            'gear_box': self.gear_box or False,
                                                                                            'deferencial': self.deferencial or False,
                                                                                            'stearing_box': self.stearing_box or False,
                                                                                            # 'grease_change':self.grease_change or False,

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
