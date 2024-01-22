from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"  # this is inheriting the sales order model into the om_hospital module

    # describe the fields used in the forms
    sale_description = fields.Char(string='Sale Description')
