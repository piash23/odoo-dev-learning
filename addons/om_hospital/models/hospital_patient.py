from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = "name"  <-- Removed: Redundant because you have a field named 'name'

    # Fields
    name_seq = fields.Char(string="Sequence", required=True, copy=False, readonly=True, 
                           default=lambda self: _('New')) # Added translation wrapper
    name = fields.Char(string="Patient Name", required=True)
    age = fields.Integer(string="Age", tracking=True)
    note = fields.Text(string="Notes")
    
    # Use fields.Image for better performance/resizing
    image = fields.Image(string="Patient Image")
    
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender", default='male', tracking=True) # Added tracking here too (optional but good)

    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor')
    ], string="Age Group", compute='_compute_age_group', store=True)
    
    # 1. Compute Methods (First)
    @api.depends('age')
    def _compute_age_group(self):
        for record in self:
            # Simplified logic
            if record.age < 18:
                record.age_group = 'minor'
            else:
                record.age_group = 'major'

    # 2. Constrains (Second)
    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age < 5:
                raise ValidationError(_("Age cannot be less than 5."))

    # 3. CRUD Methods (Last)
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.code') or _('New')
        return super(HospitalPatient, self).create(vals)