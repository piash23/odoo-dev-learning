from odoo import models, fields, api, _


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    _rec_name = "name" # by default, the record name is 'name' field, but we can specify it explicitly

    name_seq = fields.Char(string="Sequence", required=True, copy=False, readonly=True, default=lambda self: 'New')
    name = fields.Char(string="Patient Name", required=True)
    age = fields.Integer(string="Age", tracking=True)
    note = fields.Text(string="Notes")
    image = fields.Binary(string="Patient Image")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')], string="Gender", default='male')

    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor')],
        string="Age Group", compute='_compute_age_group', store=True)
    
    @api.depends('age')
    def _compute_age_group(self):
        for record in self:
            if record.age < 18:
                record.age_group = 'minor'
            else:
                record.age_group = 'major'

    @api.model
    def create(self, vals):
        if vals.get('name_seq', 'New') == 'New':
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.code') or 'New'
        return super(HospitalPatient, self).create(vals)
