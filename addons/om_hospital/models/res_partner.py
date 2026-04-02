from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.model
    def create(self, vals):
        return super(ResPartner, self).create(vals)