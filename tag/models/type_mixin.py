# -*- coding: utf-8 -*-

##############################################################################
#
#    Copyright (C) 2022-TODAY .
#    Author: Eng. Akram Alfusayal (<akram_ma@hotmail.com>)
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################
from odoo import fields, models

class TypeMixin(models.AbstractModel):
    _name = "tag.type.mixin"
    _description = "Type Mixin"

    def getDefaultType(self):
         return self.env['tag.category'].search([('model_id.model', '=', self._name),
                                            ('cat_type', '=', 'type')]).default_tag or None

    fld_type = fields.Many2one('tag.tag', string='Type', default=lambda self: self.getDefaultType,
                               ondelete="restricted",
                               domain=lambda self: "[('model_id.model', '=', '%s'), "
                                                 "('cat_type', '=', 'type')]" % self._name)

