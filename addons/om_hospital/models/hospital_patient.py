from odoo import models, fields


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    _rec_name = "name" # by default, the record name is 'name' field, but we can specify it explicitly
    
    name = fields.Char(string="Patient Name", required=True)
    age = fields.Integer(string="Age")
    note = fields.Text(string="Notes")
    image = fields.Binary(string="Patient Image")