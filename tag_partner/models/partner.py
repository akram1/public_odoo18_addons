from odoo import models, fields, api, _


class Partner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "tag.mixin"]
    _order = "complete_name"

    category_id = fields.Many2many(string="Old Tags")
    model_name = fields.Char('Model Name')
