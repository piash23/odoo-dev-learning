from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    patient_name = fields.Char(string="Patient Name")