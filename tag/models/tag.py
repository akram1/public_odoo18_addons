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
from odoo.exceptions import UserError


CAT_TYPES = {'tag': 'fld_tags', 'type': 'fld_type', 'state': 'fld_state',
             'reason': 'fld_reason'}


class Tag(models.Model):
    _name = "tag.tag"
    _description = "Tags"
    _access_log = False
    _order = 'fld_cat, sequence, name'

    name = fields.Char('Name', index=True, required=True, translate=True)
    complete_name = fields.Char(
                'Complete Name', compute="_compute_complete_name",
                store=True, translate=True, index=True,
                help="Full name of tag including category name")
    description = fields.Text('Description', translate=True)
    code = fields.Char('Code')
    sequence = fields.Integer('Sequence', default=1)
    color = fields.Integer()
    value1 = fields.Char()
    value2 = fields.Char()
    value3 = fields.Char()
    image = fields.Image('Image')
    active = fields.Boolean(default=True, index=True)
    fld_cat = fields.Many2one('tag.category', string='Category', required=True,
                              ondelete='restrict', index=True)
    cat_type = fields.Selection(related='fld_cat.cat_type', store=True,
                                readonly=True)
    cat_code = fields.Char(related='fld_cat.code', string="Category Code",
                           store=True, readonly=True)
    model_id = fields.Many2one(related='fld_cat.model_id', string="Model",
                               store=True, readonly=True)
    parent_cat = fields.Many2one(related='fld_cat.parent_cat', store=True,
                                 readonly=True)
    model_name = fields.Char(related='fld_cat.model_id.model')
    category_name = fields.Char(related='fld_cat.name', string="Category Name",
                                readonly=True)
    req_category = fields.Many2one(
                    'tag.category', string='Required Category',
                    domain="[('model_id', '=', model_id.id),"
                           " ('id', '!=', fld_cat), ('cat_type', '=', 'tag')]",
                    help='This means you have to choose one tag of this '
                         'category if this tag is selected.'
                         '\nInstall Tag Pro to activate this feature.')
    tag_range = fields.Char(
                   'Tag Range', default="[]",
                   help='You can fine turn which tags of the required category'
                        ' are available for selection.'
                        '\nInstall Tag Pro to activate this feature.')
    no_delete = fields.Boolean(
                'No Delete?', default=False,
                help='This protects the record from being deleted '
                     'at given state regardless of record rules or security '
                     'groups. \nInstall Tag State to activate this feature.')
    no_write = fields.Boolean(
                'No Write?', default=False,
                help='This protects the record from being modified '
                     'at given state regardless of record rules or security '
                     'groups. \nInstall Tag State to activate this feature.')
    readonly_fields = fields.Char(
                'Readonly Fields', default="[]",
                help='You can set some fields of document as readonly once a '
                     'state is selected. \nInstall Tag State to activate '
                     'this feature.')
    required_fields = fields.Char(
                'Required Fields', default="[]",
                help='You can set some fields of document as required once a '
                     'state is selected.\nInstall Tag State to activate this '
                     'feature.')
    objects_count = fields.Integer("Objects", compute="_compute_objects_count",
                                   help="How many objects contains this tag")
    state_type = fields.Selection(
                [('new', 'User Request'), ('todo', 'Process State'),
                 ('hold', 'No Action State')], 'State Type',
                help='Type of work flow for tag state.\n  * User Request: '
                     'document is created by a user. States like: new/draft. '
                     '\n  * Process State: document is in the work flow being '
                     'processed by responsible users. States like: to approve,'
                     ' to review\n  * No Action State: document has no '
                     'actions. States like: expired/cancelled.\nInstall Tag '
                     'State Pro to activate this feature.')
    requester_type = fields.Selection(
                [('user', 'Internal Users'), ('portal', 'Portal Users'),
                 ('both', 'Both Groups')], 'Requester Type',
                help='Allowed user type to create document at State Type: User'
                     ' Request. Use this to initiate the document as a request'
                     ' to be processed in the state work flow.\n Install Tag '
                     'State Pro to activate this feature.')
    state_group = fields.Many2one(
                'res.groups', string='State Group',
                help='Allowed Group to control the follow of documents. This '
                     'group can approve/farward, return/backward or cancel '
                     'document state. \nInstall Tag State to activate this '
                     'feature.')
    duration = fields.Integer(
                'Minutes to Spend',
                help='Max minutes the action should take. This applies to '
                     'State Type: Process State\nInstall Tag State to activate'
                     'this feature.')
    refer_requester = fields.Boolean(
                'Refer Requester',
                help='Allow feedback from the requester. This applies to '
                     'State Type: Process State\nInstall Tag State to '
                     'activate this feature.')
    auto_process = fields.Selection(
                [('duration', 'Use time in Duration field'),
                 ('other', 'Use time of other field')], 'Auto Process',
                help='This state can be auto processed, and is moved to '
                     'another state.\nInstall Tag State Pro to activate '
                     'this feature.')
    other_field = fields.Many2one(
                'ir.model.fields', string='Other Field',
                domain="[('model_id', '=', model_id.id), "
                        "('ttype', 'in', ['date', 'datetime'])]",
                help='Choose a field of date or datetime to use it in Auto '
                     'Process.\nInstall Tag State Pro to activate this '
                     'feature.')
    move_to_state = fields.Many2one(
                'tag.tag', string='Move to State',
                domain="[('id', '!=', id), ('cat_type', '=', 'state'), "
                       "('model_id', '=', model_id.id)]",
                help='Choose the state to move to when doing auto process.'
                     '\nInstall Tag State Pro to activate this feature.')

    _sql_constraints = [
        ('name_uniq', 'unique(name, model_id, cat_type)',
         'Name must be uniqe per Model and Category Type.')]

    @api.constrains('code')
    def check_code(self):
        for tag in self:
            if not tag.code:
                continue
            if self.env['tag.tag'].search([('code', '=', tag.code),
                                           ('model_id', '=', tag.model_id.id),
                                           ('id', '!=', tag.id)], limit=1):
                raise UserError(_(
                    f"Code: {tag.code} of Tag: {tag.name} is already "
                     "used. It must be unique per Model."))

    @api.depends('name', 'category_name')
    def _compute_complete_name(self):
        for tag in self:
            if tag.category_name:
                tag.complete_name = f"{tag.category_name} / {tag.name}"
            else:
                tag.complete_name = f" / {tag.name}"

    def _compute_display_name(self):
        if self.env.context.get('_long_tag_name', False):
            for tag in self:
                tag.display_name = tag.complete_name
        elif self.env.context.get('_short_tag_name', False):
            for tag in self:
                tag.display_name = tag.name
        else:
            for tag in self:
                if tag.cat_type != 'tag':
                    tag.display_name = tag.name
                else:
                    tag.display_name = tag.complete_name

    def _compute_objects_count(self):
        for tag in self:
            field = CAT_TYPES[tag.cat_type]
            if field in self.env[tag.model_name]._fields:
                tag.objects_count = self.env[tag.model_name].\
                            sudo().search_count([(field, '=', tag.id)])
            else:
                tag.objects_count = 0

    @api.onchange('fld_cat')
    def onchange_action_state(self):
        domain = {}
        self.req_category = None
        self.tag_range = "[]"
        domain['req_category'] = []
        if self.fld_cat and self.cat_type == 'tag':
            domain['req_category'] = [('cat_type', '=', 'tag'),
                                      ('id', '!=', self.fld_cat.id),
                                      ('model_id', '=', self.model_id.id)]
        return {'domain': domain}

    def check_tag_code(self, tag, name, seq, model_name):
        if 'cat_type' in tag:
            if tag['cat_type'] == 'type':
                if not tag['code']:
                    raise UserError(_("Code is required for tag type Type. "
                                      "Please set unique code for Type "
                                      f": {name}."))
            elif tag['cat_type'] == 'state':
                if not tag['code']:
                    raise UserError(_("Code is required for tag type State. "
                                      "You can go to Tags app and set unique "
                                      f"code for State : {name}."))
                if not seq:
                    raise UserError(_("Sequence is required for tag type "
                                      "State. Please set sequence number for "
                                      f"State : {name}. Make sure to number"
                                      " all states in a logical sequence."))

                if self.env['tag.tag'].search([
                        ('model_name', '=',  model_name),
                        ('id', '!=', tag['id']),
                        ('sequence', '=', seq)], limit=1):
                    raise UserError(_("Sequence is duplicate of another state."
                                      " Please set sequence number for State "
                                      f": {name}. Make sure to number all "
                                      "states in a logical sequence."))

    def unlink(self):
        if self.objects_count > 0:
            raise UserError(_("You cannot delete this tag because it is "
                              "bieng used"))

    def write(self, vals):
        if 'complete_name' in vals or 'cat_code' in vals or 'model_id' \
            in vals or 'cat_type' in vals:
            return super().write(vals)
        recs = super().write(vals)
        if isinstance(recs, bool):
            return recs
        categories = []
        # update the help attribute of state_field type_field and stage_field
        # help attribute
        for rec in recs:
            self.check_tag_code(rec, rec.name, rec.sequence, rec.model_name)
            if 'description' in vals and rec.fld_cat.id not in categories \
               and rec.cat_type == 'state':
                categories.append(rec.fld_cat.id)
        for cat in categories:
            descriptions = recs.search([('fld_cat', '=', cat)],
                                       order="sequence").description
            category = self.env['tag.category'].browse(cat)
            category.description = "".join([f"- {r.description}\n"
                                            for r in descriptions])
            field = category.model_id.field_id.search(
                [('name', '=', 'state')], limit=1)
            if field:
                field.help = category.description
        return recs

    @api.model_create_multi
    def create(self, vals_list):
        categories = []
        for val in vals_list:
            model_id = self.env['tag.category'].browse(val['fld_cat']).model_id
            self.check_tag_code(val, val['name'], val.get('sequence', False), model_id.model)
            cat_type = self.env['tag.category'].browse(val['fld_cat']).cat_type
            if 'description' in val and val['fld_cat'] not in categories and \
                cat_type == 'state':
                categories.append(val['fld_cat'])
        recs = super().create(vals_list)
        #update the help attribute of state_field type_field and stage_field help attribute
        for cat in categories:
            descriptions = self.env['tag.tag'].search([('fld_cat', '=', cat)],
                                        order="sequence").mapped('description')
            if descriptions:
                category = self.env['tag.category'].browse(cat)
                category.description = "".join([f"- {r}\n" for r in descriptions if not r])
                field = category.model_id.field_id.search([('name', '=', 'state')], limit=1)
                if field:
                    field.help = category.description
        return recs

    def action_show_objects(self):
        return {
            'name': _(f"Objects related to tag {self.name}"),
            'view_mode': 'list,form',
            'res_model': self.model_id.model,
            'type': 'ir.actions.act_window',
            'domain': [(CAT_TYPES[self.cat_type], '=', self.id)],
        }

    def action_get_tag_range(self):
        pass

    def action_get_fields(self):
        pass


class TagSubCategory(models.Model):
    _name = 'tag.sub.category'
    _description = "Tag Sub Category"

    name = fields.Char('Name', required=True, translate=True, index=True)
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique.')
    ]


