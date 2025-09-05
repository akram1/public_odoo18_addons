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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TagMixin(models.AbstractModel):
    """ Mixin to be used to add tag support to any model
        by inheriting from it like:
            _inherit=["tag.mixin"]
    """
    _name = "tag.mixin"
    _description = "Tag Mixin"

    def _search_no_tags(self, operator, value):
        with_tags = self.search([('fld_tags', operator, value)])
        return [('id', 'not in', with_tags.mapped('id'))]

    def _search_tags(self, operator, value):
        return [('fld_tags', operator, value)]

    def _compute_search_tag(self):
        for rec in self:
            rec.search_tags = False
            rec.search_no_tags = False

    fld_tags = fields.Many2many('tag.tag', string="Tags",
                                domain=lambda self: [('model_id.model', '=', self._name),
                                                     ('cat_type', '=', 'tag')])
    # Search capabilities
    search_tags = fields.Many2one('tag.tag', string='Tag',
                                  compute='_compute_search_tag',
                                  search='_search_tags', store=False, readonly=True,
                                  domain=lambda self: [('model_id.model', '=', self._name)],
                                  help="Find all records that contain this tag")
    search_no_tags = fields.Many2one('tag.tag', string='No tag',
                                     compute='_compute_search_tag',
                                     search='_search_no_tags', store=False, readonly=True,
                                     domain=lambda self: [('model_id.model', '=', self._name)],
                                     help="Find all records that have no this tag")
