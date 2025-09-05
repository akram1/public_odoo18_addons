# -*- coding: utf-8 -*-
###################################################################################
#
#    Tirasys
#    Copyright (C) 2021-TODAY Tirasys (<https://www.tirasys.com>).
#    Author: Akram Alfusayal
#
###################################################################################

from odoo import api, fields, models, _

first_part = ['عبد', 'أمة', 'امة', 'شجرة', 'فتح']
second_part = ['الهدى', 'الزهراء', 'الله', 'بالله', 'الدين', 'الرحمن']


def get_first_mid(name):
    if name is None:
        return [None, None]
    length = len(name)
    if length == 1:
        return [name[0], None]
    if name[0] in first_part or name[1] in second_part:
        first_name = " ".join(name[0:2])
        middle_name = " ".join(name[2:]) if length > 2 else None
    else:
        first_name = name[0]
        middle_name = " ".join(name[1:])
    return [first_name, middle_name]

def get_mid_last(name):
    if name is None:
        return [None, None]
    length = len(name)
    if length == 1:
        return [None, name[0]]
    if name[length - 1] in second_part or name[length - 2] in first_part:
        last_name = " ".join(name[length - 2:])
        middle_name = " ".join(name[0:length - 1]) if length > 2 else None
    else:
        last_name = name[length - 1]
        middle_name = " ".join(name[0:length - 1])
    return [middle_name, last_name]

def split_person_name(name):
    comma = ',' in name
    parts = name.split("," if comma else " ")
    if comma:
        last_name = parts[0]
        if len(parts) > 1:
            parts = get_first_mid(parts[1].split(" "))
            return [parts[0], parts[1], last_name]
        else:
            return [None, None, last_name]
    else:
        parts = get_first_mid(parts)
        first_name = parts[0]
        if parts[1] is not None:
            parts = get_mid_last(parts[1].split(" "))
            return [first_name, parts[0], parts[1]]
        else:
            return [first_name, None, None]


class Employee(models.Model):
    _inherit = 'hr.employee'

    first_name = fields.Char("First name")
    middle_name = fields.Char("Middle name")
    last_name = fields.Char("Last name")
    name_changed = fields.Boolean('Name Changed?', default=False)

    @api.onchange("first_name", "middle_name", "last_name")
    def _compute_full_name(self):
        if self.first_name or self.middle_name or self.last_name:
            self.name = " ".join((p for p in (self.first_name,
                                              self.middle_name,
                                              self.last_name) if p))
            self.name_changed = True

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if "name_changed" in values:
                first = values["first_name"] if "first_name" in values else None
                middle = values["middle_name"] if "middle_name" in values else None
                last = values["last_name"] if "first_name" in values else None
                values["name"] = "%s %s %s" %(first, middle, last)
            else:
                names = split_person_name(values.get("name"))
                values['first_name'] = names[0]
                values['middle_name'] = names[1]
                values['last_name'] = names[2]
        return super().create(vals_list)

    def write(self, values):
        if "name_changed" in values:
            first = values["first_name"] if "first_name" in values else self.first_name
            middle = values["middle_name"] if "middle_name" in values else self.middle_name
            last = values["last_name"] if "first_name" in values else self.last_name
            values["name"] = "%s %s %s" %(first, middle, last)
        elif "name" in values:
            names = split_person_name(values['name'])
            values["first_name"] = names[0]
            values["middle_name"] = names[1]
            values["last_name"] = names[2]
        return super().write(values)
