# -*- coding: utf-8 -*-
###################################################################################
#
#    Tirasys
#    Copyright (C) 2020-TODAY Tirasys (<https://www.tirasys.com>).
#    Author: Akram Alfusayal
#
###################################################################################

from . import models

#from odoo import api, SUPERUSER_ID, _, tools

def configure_name_parts(env):
    """Populate first/middle/last names for an already created persons"""

    #env = api.Environment(cr, SUPERUSER_ID, {})

    persons = env['res.partner'].search([('is_company', '=', False)])

    for person in persons:
        if not person.first_name:
            person.write({'name': person.name})
