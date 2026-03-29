from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "appointment_seq"
    _order = "appointment_date desc"

    # Fields
    appointment_seq = fields.Char(string="Appointment Sequence", required=True, copy=False, readonly=True,
                                  default=lambda self: _('New'))  # Added translation wrapper
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True, tracking=True)
    patient_age = fields.Integer(related='patient_id.age', string="Patient Age", store=True, readonly=True)
    appointment_date = fields.Datetime(string="Appointment Date", required=True, tracking=True)
    doctor_name = fields.Char(string="Doctor Name", required=True, tracking=True)
    notes = fields.Text(string="Notes")

    # 1. Compute Methods (First)
    # (No compute methods needed for this model currently) 

    # 2. Constrains (Second)
    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        for record in self:
            if record.appointment_date < fields.Datetime.now():
                raise ValidationError(_("Appointment date cannot be in the past."))

    # 3. CRUD Methods (Last)
    @api.model
    def create(self, vals):
        if vals.get('appointment_seq', _('New')) == _('New'):
            vals['appointment_seq'] = self.env['ir.sequence'].next_by_code('hospital.appointment.code') or _('New')
        return super(HospitalAppointment, self).create(vals)