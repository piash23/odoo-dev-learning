from odoo import models, fields, api, _


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    _rec_name = "name" # by default, the record name is 'name' field, but we can specify it explicitly

    name_seq = fields.Char(string="Sequence", required=True, copy=False, readonly=True, default=lambda self: 'New')
    name = fields.Char(string="Patient Name", required=True)
    age = fields.Integer(string="Age")
    note = fields.Text(string="Notes")
    image = fields.Binary(string="Patient Image")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')], string="Gender", default='male')


    @api.model
    def create(self, vals):
        if vals.get('name_seq', 'New') == 'New':
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.code') or 'New'
        return super(HospitalPatient, self).create(vals)
