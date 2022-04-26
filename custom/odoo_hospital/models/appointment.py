import pytz

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

    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        print('Test write function')
        return res

    # def action_notify(self):
    #     for rec in self:
    #         rec.doctor_id.user_id.notify_success(message='Appointment confirmed!')

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed',
                    'type': 'rainbow_man',
                }
            }

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: ('New'))

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, ondelete='cascade')
    patient_age = fields.Integer(string='Age', related='patient_id.patient_age')
    notes = fields.Text(string='Appointment Notes')
    amount = fields.Float(string='Paid Amount')
    ref = fields.Char(string='Reference', help='Reference from patient record')
    prescription = fields.Text(string='Prescription')
    pharmacy_history = fields.Text(string='Pharmacy History')
    appointment_date = fields.Date(string='Date')
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string='Appointment Lines')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    # doctor_gender = fields.Selection([
    #     ('male', 'Male'),
    #     ('fe_male', 'Female'),
    # ], default='male', string='Gender', related='doctor_id.gender')
    #
    # @api.onchange('doctor_id')
    # def set_doctor_gender(self):
    #     for rec in self:
    #         if rec.doctor_gender:
    #             rec.doctor_gender = rec.doctor_id.gender

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], string='Status', readonly=True, default='draft')

    def delete_lines(self):
        for rec in self:
            # user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            # date_today = pytz.utc.localize(rec.appointment_date().astimezone(user_tz))
            rec.appointment_lines = [(5, 0, 0)]

    partner_id = fields.Many2one('res.partner',string='Customer')
    order_id = fields.Many2one('sale.order', string='Sale Order')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}
    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        res['notes']= 'Write patients problem here.'
        print('Working!')
        return res
class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointmnet Lines'

    product_id = fields.Many2one('product.product', string='Medicine')
    sequence = fields.Integer(string="Sequence")
    product_qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')