# -*- coding: utf-8 -*-
###############################################################################
#
#    Tirasys
#    Copyright (C) 2017-TODAY Tirasys(<http://www.tirasys.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


from odoo import api, fields, models, _


class StateDistrictMixin(models.AbstractModel):
    _name = 'state.district.mixin'
    _description = "State District Mixin"

    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',
                                 default=lambda self: self.env.company.country_id)
    state_id = fields.Many2one('res.country.state', string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    city_id = fields.Many2one('res.city', string='City/Town', ondelete='restrict',
                               domain="[('state_id', '=?', state_id)]")
    district = fields.Many2one('res.district', string='District', ondelete='restrict',
                               domain="[('state_id', '=?', state_id)]")
    zone = fields.Many2one('res.zone', string='Zone', ondelete='restrict',
                               domain="[('district', '=?', district)]")

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.state_id.country_id and self.country_id != self.state_id.country_id:
            self.state_id = None
            self.district = None
            self.city_id = None
            self.zone = None

    @api.onchange('state_id')
    def _onchange_state(self):
        if not self.state_id:
            self.district = None
            self.city_id = None
            self.zone = None
        else:
            if self.district.state_id and self.state_id != self.district.state_id:
                self.district = None
                self.city_id = None
                self.zone = None
            self.country_id = self.state_id.country_id

    @api.onchange('district')
    def _onchange_district(self):
        if self.zone.district and self.district != self.zone.district:
            self.zone = None


class City(models.Model):
    _name = 'res.city'
    _description = "State City/Town"

    name = fields.Char('City', required=True, translate=True)
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one(related='state_id.country_id', store=True)
    _sql_constraints = [
        ('city_uniq', 'unique (name, state_id)',
            _('The city name must be unique within a state!'))]

    @api.depends('name', 'state_id.name')
    def _compute_display_name(self):
        if self.env.context.get('_short_city_name', False):
            return super()._compute_display_name()
        for record in self:
            record.display_name =  "{} ({})".format(record.name, record.state_id.name)


class DistrictZone(models.Model):
    _name = 'res.zone'
    _description = "District Zone"

    name = fields.Char('Zone Name', required=True, translate=True)
    district = fields.Many2one('res.district', string='District', required=True)
    state_id = fields.Many2one(related='district.state_id', store=True)
    country_id = fields.Many2one(related='district.country_id', store=True)

    _sql_constraints = [
        ('zone_uniq', 'unique (name, district)',
            _('The zone name must be unique within district!'))]


    @api.depends('name', 'district.name')
    def _compute_display_name(self):
        if self.env.context.get('_short_zone_name', False):
            return super()._compute_display_name()
        for record in self:
            record.display_name =  "{} ({})".format(record.name, record.district.name)


class StateDistrict(models.Model):
    _name = 'res.district'
    _description = "State District"

    name = fields.Char('District Name', required=True, translate=True)
    state_id = fields.Many2one('res.country.state', string='State', required=True)
    country_id = fields.Many2one(related='state_id.country_id', store=True)
    zones = fields.One2many('res.zone', 'district', 'Zones')
    zone_count = fields.Integer('Zone count', compute='_count_zone')

    _sql_constraints = [
        ('district_uniq', 'unique (name, state_id)',
            _('The district name must be unique within a state!'))]

    @api.depends('zones')
    def _count_zone(self):
        for district in self:
            if district.zones:
                district.zone_count = len(district.zones)
            else:
                district.zone_count = 0

    @api.depends('name', 'state_id.name')
    def _compute_display_name(self):
        if self.env.context.get('_short_district_name', False):
            return super()._compute_display_name()
        for record in self:
            record.display_name =  "{} ({})".format(record.name, record.state_id.name)


class CountryState(models.Model):
    _inherit = 'res.country.state'

    name = fields.Char(translate=True)
    districts = fields.One2many('res.district', 'state_id', 'Districts')
    cities = fields.One2many('res.city', 'state_id', 'Cities')
    zones = fields.One2many('res.zone', 'state_id', 'Zones')
    color = fields.Integer('Color')
    district_count = fields.Integer('District count', compute='_count_district')
    city_count = fields.Integer('City count', compute='_count_city')
    zone_count = fields.Integer('Zone count', compute='_count_zone')

    @api.depends('cities')
    def _count_city(self):
        for state in self:
            if state.cities:
                state.city_count = len(state.cities)
            else:
                state.city_count = 0

    @api.depends('districts')
    def _count_district(self):
        for state in self:
            if state.districts:
                state.district_count = len(state.districts)
            else:
                state.district_count = 0

    @api.depends('zones')
    def _count_zone(self):
        for state in self:
            if state.zones:
                state.zone_count = len(state.zones)
            else:
                state.zone_count = 0

    @api.depends('name', 'country_id.name')
    def _compute_display_name(self):
        if self.env.context.get('_long_state_name', False):
            for record in self:
                record.display_name =  "{} ({})".format(record.name, record.country_id.name)
        else:
            return super()._compute_display_name()


class Country(models.Model):
    _inherit = 'res.country'

    name = fields.Char(translate=True)
    districts = fields.One2many('res.district', 'country_id', 'Districts')
    zones = fields.One2many('res.zone', 'country_id', 'Zones')
    cities = fields.One2many('res.city', 'country_id', 'Cities')
    state_count = fields.Integer('State count', compute='_count_state')
    district_count = fields.Integer('District count', compute='_count_district')
    city_count = fields.Integer('City count', compute='_count_city')
    zone_count = fields.Integer('Zone count', compute='_count_zone')

    @api.depends('state_ids')
    def _count_state(self):
        for country in self:
            if country.state_ids:
                country.state_count = len(country.state_ids)
            else:
                country.state_count = 0

    @api.depends('cities')
    def _count_city(self):
        for country in self:
            if country.cities:
                country.city_count = len(country.cities)
            else:
                country.city_count = 0

    @api.depends('districts')
    def _count_district(self):
        for country in self:
            if country.districts:
                country.district_count = len(country.districts)
            else:
                country.district_count = 0

    @api.depends('zones')
    def _count_zone(self):
        for country in self:
            if country.zones:
                country.zone_count = len(state.zones)
            else:
                country.zone_count = 0


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'state.district.mixin']


