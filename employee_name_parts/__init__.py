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
    """Populate first/middle/last names for an already created employees"""

    #env = api.Environment(cr, SUPERUSER_ID, {})

    employees= env['hr.employee'].search([])

    for employee in employees:
        if not employee.first_name:
            employee.write({'name':employee.name})

