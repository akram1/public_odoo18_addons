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

CATEGORIES = [('state', 'State'), ('type', 'Type'), ('tag', 'Tag'), ('reason', 'Reason')]

class TagCategory(models.Model):
    _name = 'tag.category'
    _description = "Tag Category"
    _access_log = False
    _order = 'model_id, sequence, name'

    name = fields.Char('Name', required=True, translate=True, index=True)
    complete_name = fields.Char('Complete Name', compute="_compute_complete_name",
                            store=True, translate=True, index=True,
                            help="Full name of tag (including category name)")
    description = fields.Text('Description', translate=True)
    code = fields.Char('Code', help="Can be used for special "
                       "tags which have programmable bechavior")
    color = fields.Integer()
    parent_cat = fields.Many2one('tag.sub.category', string="Parent Category", ondelete='restrict')
    sequence = fields.Integer('Sequence', default=1)
    cat_type = fields.Selection(CATEGORIES, 'Category Type', default='tag', required=True)
    active = fields.Boolean(index=True, default=True)
    fld_tags = fields.One2many("tag.tag", "fld_cat", "Tags")
    single_tag = fields.Boolean("Single Tag",
                                help="if set to True then only one tag from this category "
                                "may be present on a single object. "
                                "On attempt to add second tag from this category to object, "
                                "error will be raised. "
                                "Install Tag Pro to activate this feature.")
    default_tag = fields.Many2one('tag.tag', string='Default Tag',
                                  domain=lambda self: "[('fld_cat', '=',  id)]")
    required = fields.Boolean('Required Tag', help='This category requires to be tagged.'
                              'Install Tag Pro to activate this feature.')
    log_change = fields.Boolean('Log Changes?',
                                help="Log and track any changes made on this tag category. "
                                     "Install Tag Change Log to activate this feature.")
    model_id = fields.Many2one("ir.model", string="Model", ondelete='cascade', required=True,
                               help="Specify model for which this tag is available.")
    model_uname = fields.Char(related='model_id.model')
    model_name = fields.Char(related='model_id.name')
    tags_count = fields.Integer(compute="_compute_tags_count", store=True, readonly=True,
                                help="How many tags related to this category")
    _sql_constraints = [
        ('name_uniq', 'unique(name, model_id)', 'Category Name  must be unique per model'),
        ('code_uniq', 'unique(code)', 'Category code must be unique'),
    ]

    @api.depends('name', 'model_name')
    def _compute_complete_name(self):
        for category in self:
            if category.model_name:
                category.complete_name = f"{category.model_name} / {category.name}"
            else:
                category.complete_name = f" / {category.name}"

    def _compute_display_name(self):
        if self.env.context.get('_short_cat_name', False):
            for category in self:
                category.display_name = category.name
        else:
            for category in self:
                category.display_name = category.complete_name

    @api.depends('fld_tags')
    def _compute_tags_count(self):
        for rec in self:
            rec.tags_count = len(rec.fld_tags)
   
    def action_show_tags(self):
        return {
            'name': _('Tags related to category %s') % self.name,
            'view_mode': 'list,form',
            'res_model': 'tag.tag',
            'type': 'ir.actions.act_window',
            'context': {'default_fld_cat': self.id, '_short_tag_name': True},
            'domain': [('fld_cat', '=', self.id)],
        }

    @api.constrains('cat_type', 'model_id')
    def _check_redundancy(self):
        for rec in self:
            if rec.cat_type == 'state': 
                count = self.env['tag.category'].\
                    search_count([('cat_type', '=', 'state'), ('id', '!=', rec.id),
                           ('model_id', '=', rec.model_id.id)])
                if count > 0:
                    raise ValidationError(_(f"Category {rec.name} cannot have more than one "
                                             "of type 'State'. Only one is allowed."))
            elif rec.cat_type == 'reason': 
                count = self.env['tag.category']. \
                    search_count([('cat_type', '=', 'reason'), ('id', '!=', rec.id),
                                  ('model_id', '=', rec.model_id.id)])
                if count > 0:
                    raise ValidationError(_(f"Category {rec.name} cannot have more than one "
                                             "of type 'Reason'. Only one is allowed."))
            elif rec.cat_type == 'type':
                count = self.env['tag.category']. \
                    search_count([('cat_type', '=', 'type'), ('id', '!=', rec.id),
                                  ('model_id', '=', rec.model_id.id)])
                if count > 0:
                    raise ValidationError(_(f"Category {rec.name} cannot have more than one "
                                             "of type 'Type'. Only one is allowed."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'cat_type' in vals:
                if vals['cat_type'] == 'state':
                    vals['required'] = True
                    vals['single_tag'] = True
                    vals['log_change'] = True
                elif vals['cat_type'] in ['type', 'reason']:
                    vals['single_tag'] = True
        return super().create(vals_list)

    def write(self, vals):
        if 'cat_type' in vals:
            if vals['cat_type'] != self.cat_type:
                raise ValidationError(_("Cannot change Catagory Type after creation on "
                                        f"Category: {self.name}"))
        if 'model_id' in vals and vals['model_id'] != self.model_id.id:
            raise ValidationError(_("Cannot change Catagory Model after creation on "
                                    f"Category: {self.name}"))
        if self.cat_type == 'state':
            vals['required'] = True
            vals['single_tag'] = True
            vals['log_change'] = True
        elif self.cat_type in ['type', 'reason']:
            vals['single_tag'] = True
        return  super().write(vals)
