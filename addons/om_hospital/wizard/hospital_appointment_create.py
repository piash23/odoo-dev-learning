from odoo import models, fields, api, _


class HospitalAppointmentCreate(models.TransientModel):
    _name = "hospital.appointment.create"
    _description = "Hospital Appointment Create Wizard"

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_name = fields.Char(string="Doctor name", required=True)
    appointment_date = fields.Datetime(string="Appointment Date", required=True, default=fields.Datetime.now)

    def action_create_appointment(self):
        """Create an appointment record based on the wizard's data."""
        self.ensure_one()  # Ensure only one record is processed
        appointment_vals = {
            'patient_id': self.patient_id.id,
            'doctor_name': self.doctor_name,
            'appointment_date': self.appointment_date,
        }
        appointment = self.env['hospital.appointment'].create(appointment_vals)
        # Return an action to open the created appointment form view
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'form',
            'res_id': appointment.id,
            'target': 'current',
        }