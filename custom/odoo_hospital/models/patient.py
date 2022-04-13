from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartners(models.Model):
    _inherit = 'res.partner'

    # Override create function in odoo
    @api.model
    def create(self, vals):
        res = super(ResPartners, self).create(vals)
        # custom coding here
        return res


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    patient_name = fields.Char(string='Patient Name')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _rec_name = 'patient_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s %s' % (field.name_seq, field.patient_name)))
        return res

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError('The age must be greater then 5')

    def _get_default_notes(self):
        return 'This is a normal problem!'

    def open_patient_appointments(self):
        return {
            'name': ('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    @api.model
    def create(self, vals):
        if vals.get('name_seq', ('New')) == ('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or ('New')
        result = super(HospitalPatient, self).create(vals)
        return result

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            # if rec.patient_age:
            if rec.patient_age < 18:
                rec.age_group = 'minor'
            else:
                rec.age_group = 'major'

    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count

    def action_send_card(self):
        template_id = self.env.ref('odoo_hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    patient_name = fields.Char(string='Name', required=True, track_visibility='always')

    name_seq = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: ('New'))
    patient_age = fields.Integer(string='Age', required=True, track_visibility='always')
    patient_name_upper = fields.Char(compute='_compute_upper_name', inverse='_inverse_upper_name')
    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    @api.depends('patient_name')
    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name else False
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string='Gender')

    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
    ], string='Age Group', compute='set_age_group')

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    blood_group = fields.Char(string='Blood Group')
    notes = fields.Text(string='Notes', default=_get_default_notes)
    image = fields.Binary(string='Image')
    active = fields.Boolean('Active', default=True)
    appointment_count = fields.Integer(string='Appointment', compute="get_appointment_count")
    email_id = fields.Char(string='Email')
    contact_no = fields.Char(string="Contact No.")
    user_id = fields.Many2one('res.users', string='PRO')
    # Another way to define rec name
    # name = fields.Char('Default Name')
