from odoo import models, fields


class Product(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "tag.mixin"]

    model_name = fields.Char('Model Name', readonly=True)
