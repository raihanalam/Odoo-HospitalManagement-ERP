from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'appointment_date asc'

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or ('New')
        result = super(HospitalAppointment, self).create(vals)
        return result
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: ('New'))

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    patient_age = fields.Integer(string='Age', related='patient_id.patient_age')
    notes = fields.Text(string='Appointment Notes')
    prescription = fields.Text(string='Prescription')
    pharmacy_history = fields.Text(string='Pharmacy History')
    appointment_date = fields.Date(string='Date')
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string='Appointment Lines')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], string='Status', readonly=True, default='draft')

class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointmnet Lines'

    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')