from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "appointment_seq"
    _order = "appointment_date desc"


    def _get_default_notes(self):
        return _("No additional notes provided.")  # Added translation wrapper

    # Fields
    appointment_seq = fields.Char(string="Appointment Sequence", required=True, copy=False, readonly=True,
                                  default=lambda self: _('New'))  # Added translation wrapper
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True, tracking=True)
    patient_age = fields.Integer(related='patient_id.age', string="Patient Age", store=True, readonly=True)
    appointment_date = fields.Datetime(string="Appointment Date", required=True, tracking=True)
    doctor_name = fields.Char(string="Doctor Name", required=True, tracking=True)
    notes = fields.Text(string="Notes", default=_get_default_notes)  # Added default value for better UX
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    doctors_note = fields.Text(string="Doctor's Note", tracking=True)
    prescription = fields.Text(string="Prescription", tracking=True)

    # Compute Methods
    # (No compute methods needed for this model currently)

    # Python Constraints
    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        for record in self:
            if record.appointment_date < fields.Datetime.now():
                raise ValidationError(_("Appointment date cannot be in the past."))

    # CRUD Methods
    @api.model
    def create(self, vals):
        if vals.get('appointment_seq', _('New')) == _('New'):
            vals['appointment_seq'] = self.env['ir.sequence'].next_by_code('hospital.appointment.code') or _('New')
        return super(HospitalAppointment, self).create(vals)

    def action_confirm(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(_("Only appointments in draft state can be confirmed."))
            record.state = 'confirmed'
    
    def action_done(self):
        for record in self:
            if record.state != 'confirmed':
                raise ValidationError(_("Only confirmed appointments can be marked as done."))
            record.state = 'done'
    
    def action_cancel(self):
        for record in self:
            if record.state not in ['draft', 'confirmed']:
                raise ValidationError(_("Only appointments in draft or confirmed state can be cancelled."))
            record.state = 'cancelled'
    
    def action_reset_to_draft(self):
        for record in self:
            if record.state not in ['cancelled', 'done']:
                raise ValidationError(_("Only appointments in cancelled or done state can be reset to draft."))
            record.state = 'draft'