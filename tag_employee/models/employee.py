from odoo import models, fields, api


class Employee(models.Model):
    _name = "hr.employee"
    _inherit = ["hr.employee", "tag.mixin"]

    @api.model
    def getStateTag(self):
        states = self.env['tag.tag'].search([('model_id.model', '=',  self._name),
                                             ('cat_type', '=', 'state')])
        return [(state.code, state.name) for state in states]

    @api.model
    def getDefaultState(self):
         return self.env['tag.category'].search([('model_id.model', '=', self._name),
                                        ('cat_type', '=', 'state')]).default_tag.code or None
    category_ids = fields.Many2many(string="Old Tags")
    state = fields.Selection(selection='getStateTag', string='Status', tracking=True,
                             default=getDefaultState, required=True)

    employee_type = fields.Selection(selection_add=[('collaborator', 'Collaborator')],
                                     ondelete={'collaborator': 'cascade', 'employee': 'set default'})

