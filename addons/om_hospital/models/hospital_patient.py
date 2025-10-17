from odoo import models, fields


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    
    name = fields.Char(string="Patient Name", required=True)
    age = fields.Integer(string="Age")
    note = fields.Text(string="Notes")
    image = fields.Binary(string="Patient Image")