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

    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", tracking=True)
    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Doctor Gender")

    active = fields.Boolean(string="Active", default=True, tracking=True)

    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count')
    
    # 1. Compute Methods (First)
    @api.depends('age')
    def _compute_age_group(self):
        for record in self:
            # Simplified logic
            if record.age < 18:
                record.age_group = 'minor'
            else:
                record.age_group = 'major'
    
    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', record.id)])

        # """Compute the number of appointments per patient using a single grouped query."""
        # Appointment = self.env['hospital.appointment']
        # # Aggregate counts for all patients in the current recordset
        # data = Appointment.read_group(
        #     [('patient_id', 'in', self.ids)],
        #     ['patient_id'],
        #     ['patient_id'],
        # )
        # # Build a mapping from patient_id -> appointment count
        # counts_by_patient = {
        #     item['patient_id'][0]: item['patient_id_count']
        #     for item in data
        #     if item.get('patient_id')
        # }
        # for record in self:
        #     record.appointment_count = counts_by_patient.get(record.id, 0)
        
    # 2. Onchange Methods (After Compute Methods)
    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        """Update doctor gender automatically when doctor is selected in the UI."""
        for record in self:
            if record.doctor_id:
                record.doctor_gender = record.doctor_id.gender
            else:
                record.doctor_gender = False

    # 3. Constrains (Third)
    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age < 5:
                raise ValidationError(_("Age cannot be less than 5."))

    # 4. CRUD Methods (Last)
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(HospitalPatient, self).create(vals)

    
    def action_view_appointments(self):
        return {
            'name': _('Appointments'),  # Added translation wrapper
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
        }
