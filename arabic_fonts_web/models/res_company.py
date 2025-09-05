# -*- coding: utf-8 -*-

from odoo import fields, models

class Company(models.Model):
    _inherit = "res.company"

    font = fields.Selection(selection_add=[('NotoNaskhArabic', 'Noto Arabic Naskh'),
                                           ('Arial', 'Arial'), ('Zain', 'Zain')])
