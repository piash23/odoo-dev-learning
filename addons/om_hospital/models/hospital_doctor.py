from odoo import models, fields, api


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"

    name = fields.Char(string="Doctor Name", required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')], string="Gender", required=True, tracking=True)
    related_user_id = fields.Many2one('res.users', string="Related User", tracking=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)
    