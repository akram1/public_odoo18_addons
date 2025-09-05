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
from odoo import api, fields, models, _


class StateMixin(models.AbstractModel):
    _name = "tag.state.mixin"
    _description = "Tag State Mixin"

    @api.model
    def getStateTag(self):
        states = self.env['tag.tag'].search([('model_id.model', '=',  self._name),
                                             ('cat_type', '=', 'state')])
        return [(state.code, state.name) for state in states]

    @api.model
    def getDefaultState(self):
         return self.env['tag.category'].search([('model_id.model', '=', self._name),
                                        ('cat_type', '=', 'state')]).default_tag.code or None

    def getDefaultType(self):
         return self.env['tag.category'].search([('model_id.model', '=', self._name),
                                            ('cat_type', '=', 'type')]).default_tag or None

    state = fields.Selection(selection='getStateTag', string='Status', ondelete="restricted",
                             default=lambda self: self.getDefaultState(), required=True)
    fld_state = fields.Many2one('tag.tag', string='State Tag', readonly=False,
                 compute='_compute_state', store=True,
                 domain=lambda self: "[('model_id.model', '=', '%s'), "
                                     "('cat_type', '=', 'state')]" % self._name)
    fld_reason = fields.Many2one('tag.tag', string='Action Reason', ondelete="restricted",
                 domain=lambda self: "[('model_id.model', '=', '%s'), "
                                    "('cat_type', '=', 'reason')]" % self._name)
    fld_type = fields.Many2one('tag.tag', string='Type', default=lambda self: self.getDefaultType,
                               ondelete="restricted",
                               domain=lambda self: "[('model_id.model', '=', '%s'), "
                                                 "('cat_type', '=', 'type')]" % self._name)

    @api.depends('state', 'fld_type')
    def _compute_state(self):
        for rec in self:
            state = self.env['tag.tag'].search([('model_id.model', '=',  self._name),
                      ('code', '=', rec.state), ('cat_type', '=', 'state')], limit=1)
            if state:
                rec.fld_state = state
            else:
                rec.fld_state = False

